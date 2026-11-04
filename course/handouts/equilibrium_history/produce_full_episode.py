#!/usr/bin/env python3
"""Render an English two part episode with private reference conditioned narration.

Run in an environment with MLX Audio, NumPy, SoundFile and FFmpeg. Private
reference audio and resumable segment caches are supplied outside the repo.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

import numpy as np
import soundfile as sf
import mlx.core as mx
from mlx_audio.tts.utils import load_model
from mlx_audio.utils import load_audio
from num2words import num2words

RATE = 24000


def spoken_text(text):
    """Give the speech engine words for historical years and calendar dates."""
    months = "January February March April May June July August September October November December".split()
    pattern = r"\b(" + "|".join(months) + r") (\d{1,2})\b"
    text = re.sub(pattern, lambda m: m.group(1) + " " + num2words(int(m.group(2)), to="ordinal"), text)
    def year(match):
        value = int(match.group())
        century, remainder = divmod(value, 100)
        if century == 19:
            return "nineteen " + (num2words(remainder) if remainder >= 10 else "oh " + num2words(remainder))
        return "two thousand" + (" " + num2words(remainder) if remainder else "")
    text = re.sub(r"\b(?:19|20)\d{2}\b", year, text)
    return text.replace("-", " ")


def run(*args):
    return subprocess.run([str(x) for x in args], check=True, capture_output=True, text=True).stdout


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def chunks(text, maximum=115):
    """Keep sentences together and keep reference conditioned requests short."""
    sentences = []
    for paragraph in text.strip().split("\n\n"):
        sentences.extend(re.split(r"(?<=[.!?])\s+(?=[A-Z“])", paragraph.strip()))
    current = []
    for sentence in sentences:
        if current and len((" ".join(current + [sentence])).split()) > maximum:
            yield " ".join(current)
            current = []
        current.append(sentence)
    if current:
        yield " ".join(current)


def turns(section):
    text = section["text"]
    positioned = []
    for reading in section.get("readings", []):
        quote = reading["quote"]
        if text.count(quote) != 1:
            raise ValueError(f"Reading must occur once: {reading['id']}")
        positioned.append((text.index(quote), reading))
    cursor = 0
    for position, reading in sorted(positioned):
        before = text[cursor:position].strip().rstrip("“\"")
        for chunk in chunks(before):
            if chunk.strip():
                yield {"kind": "narrator", "text": chunk.strip()}
        yield {"kind": "reader", "text": reading["quote"], "voice": reading["cast_voice"],
               "speaker": reading["speaker"], "source": reading["source"], "reading_id": reading["id"]}
        cursor = position + len(reading["quote"])
        while cursor < len(text) and text[cursor] in "”\". \n":
            cursor += 1
    for chunk in chunks(text[cursor:]):
        if chunk.strip():
            yield {"kind": "narrator", "text": chunk.strip()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--narrator-model", type=Path, required=True)
    parser.add_argument("--cast-model", type=Path, required=True)
    parser.add_argument("--ref-audio", type=Path, required=True)
    parser.add_argument("--ref-text", type=Path, required=True)
    parser.add_argument("--part", type=int, choices=[1, 2])
    parser.add_argument("--assemble-only", action="store_true")
    parser.add_argument("--part2-narrator-voice", help="Optional clear English Kokoro narrator for Part Two")
    parser.add_argument("--master-gain-db", type=float, default=-0.7,
                        help="Final gain after normalization to retain encoded peak headroom")
    args = parser.parse_args()
    data = json.loads(args.script.read_text())
    assert data["language"] == "en"
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    ref_hash = hashlib.sha256(args.ref_audio.read_bytes()).hexdigest()
    ref_text = args.ref_text.read_text().strip()
    narrator = None
    actors = None
    reference = None
    plan = []
    for part in data["parts"]:
        if args.part and part["part"] != args.part:
            continue
        items = []
        for section in part["sections"]:
            section_turns = list(turns(section))
            for index, turn in enumerate(section_turns):
                spoken = spoken_text(turn["text"])
                preset = args.part2_narrator_voice if part["part"] == 2 and turn["kind"] == "narrator" else None
                settings = {"text": spoken, "kind": turn["kind"], "language": "english",
                            "voice": preset or turn.get("voice"), "engine_version": 1,
                            "reference": ref_hash if turn["kind"] == "narrator" and not preset else None,
                            "reference_text": ref_text if turn["kind"] == "narrator" and not preset else None,
                            "model": str(args.narrator_model if turn["kind"] == "narrator" and not preset else args.cast_model)}
                key = digest(settings)
                path = args.cache_dir / (key + ".wav")
                items.append({**turn, "spoken_text": spoken, "narrator_preset": preset,
                              "section": section["id"], "section_title": section["title"],
                              "path": str(path), "cache_key": key,
                              "pause": float(section.get("pause_after_seconds", 2.5))
                              if index == len(section_turns) - 1 else 0.65})
        plan.append({"part": part["part"], "title": part["title"],
                     "target_seconds": part.get("target_seconds", 900), "items": items})
    # This plan includes private cache paths and stays in the private cache.
    (args.cache_dir / "production_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2))
    jobs = [(part, item) for part in plan for item in part["items"]]
    total = len(jobs)

    def save(item, results):
        audio = np.concatenate([np.asarray(result.audio).reshape(-1) for result in results])
        assert results[0].sample_rate == RATE and np.isfinite(audio).all()
        duration = len(audio) / RATE
        if not 0.4 < duration < 100:
            raise RuntimeError(f"Unexpected segment duration {duration}: {item['section']}")
        path = Path(item["path"])
        temporary = path.with_suffix(".partial.wav")
        sf.write(temporary, audio, RATE)
        temporary.replace(path)
        return duration

    for position, (part, item) in enumerate(jobs):
        if Path(item["path"]).exists():
            print(f"Cached {position + 1}/{total}: {item['section']}", flush=True)
            continue
        if args.assemble_only:
            raise SystemExit(f"Missing cached audio for {item['section']}")
        print(f"Rendering {position + 1}/{total}: part {part['part']}, {item['section']}, {len(item['text'].split())} words", flush=True)
        began = time.monotonic()
        if item["kind"] == "narrator" and not item.get("narrator_preset"):
            if narrator is None:
                narrator = load_model(args.narrator_model)
                reference = load_audio(str(args.ref_audio), sample_rate=narrator.sample_rate)
            group = [item]
            if position + 1 < total:
                following = jobs[position + 1][1]
                if following["kind"] == "narrator" and not following.get("narrator_preset") and not Path(following["path"]).exists():
                    group.append(following)
            mx.random.seed(int(item["cache_key"][:7], 16))
            if len(group) == 2:
                results = list(narrator.batch_generate(texts=[job["spoken_text"] for job in group],
                    ref_audio=reference, ref_text=ref_text, lang_code="english", temperature=0.9,
                    max_tokens=1200, top_k=50, top_p=1.0, repetition_penalty=1.5, stream=False))
                by_index = {result.sequence_idx: result for result in results}
                for index, job in enumerate(group):
                    result = by_index[index]
                    cap = min(1200, max(75, len(narrator.tokenizer.encode(job["spoken_text"])) * 6))
                    if result.token_count >= cap:
                        print(f"Retrying possible batch cutoff: {job['section']}", flush=True)
                        single = list(narrator.generate(text=job["spoken_text"], ref_audio=reference,
                            ref_text=ref_text, lang_code="english", temperature=0.9, max_tokens=1200,
                            top_k=50, top_p=1.0, repetition_penalty=1.5, stream=False))
                    else:
                        single = [result]
                    duration = save(job, single)
                    print(f"Saved {duration:.1f} seconds: {job['section']}", flush=True)
            else:
                results = list(narrator.generate(text=item["spoken_text"], ref_audio=reference, ref_text=ref_text,
                    lang_code="english", temperature=0.9, max_tokens=1200,
                    top_k=50, top_p=1.0, repetition_penalty=1.5, stream=False))
                print(f"Saved {save(item, results):.1f} seconds", flush=True)
        else:
            if actors is None:
                actors = load_model(args.cast_model)
            voice = item.get("narrator_preset") or item["voice"]
            results = list(actors.generate(item["spoken_text"], voice=voice, speed=0.91,
                lang_code="b" if voice.startswith("b") else "a"))
            print(f"Saved {save(item, results):.1f} seconds", flush=True)
        print(f"Render took {time.monotonic() - began:.1f} seconds", flush=True)
    del narrator, actors
    mx.clear_cache()
    rendered_parts = []
    for part in plan:
        buffers = []
        timings = []
        elapsed = 0.0
        for item in part["items"]:
            audio, sample_rate = sf.read(item["path"])
            assert sample_rate == RATE
            duration = len(audio) / RATE
            timings.append({k: item[k] for k in ("kind", "text", "section", "section_title")}
                           | {"raw_start_seconds": elapsed, "raw_duration_seconds": duration,
                              "speaker": item.get("speaker", "Narrator")})
            buffers += [audio, np.zeros(round(RATE * item["pause"]))]
            elapsed += duration + item["pause"]
        raw = args.cache_dir / f"part{part['part']}_raw.wav"
        sf.write(raw, np.concatenate(buffers), RATE)
        target = part["target_seconds"]
        tempo = elapsed / target
        if not 0.78 <= tempo <= 1.16:
            raise RuntimeError(f"Part {part['part']} needs content/pacing revision: raw {elapsed:.1f}s for {target}s; tempo={tempo:.3f}")
        stem = f"ECON803_The_Price_of_Proof_Part_{part['part']}_English"
        normalized = args.cache_dir / (stem + ".wav")
        run("ffmpeg", "-y", "-v", "error", "-i", raw, "-af",
            f"atempo={tempo:.8f},loudnorm=I=-16:TP=-1.5:LRA=11,volume={args.master_gain_db}dB,apad,atrim=duration={target}",
            "-ar", RATE, "-ac", 1, normalized)
        mp3 = args.output_dir / (stem + ".mp3")
        run("ffmpeg", "-y", "-v", "error", "-i", normalized,
            "-metadata", f"title={part['title']}", "-metadata", "artist=ECON 803 · Victor Aguiar",
            "-metadata", "language=eng", "-codec:a", "libmp3lame", "-b:a", "96k", mp3)
        rendered_parts.append(normalized)
        for item in timings:
            item["start_seconds"] = round(item.pop("raw_start_seconds") / tempo, 3)
            item["duration_seconds"] = round(item.pop("raw_duration_seconds") / tempo, 3)
        manifest = {"part": part["part"], "title": part["title"], "language": "en", "file": mp3.name,
                    "target_seconds": target, "raw_seconds": elapsed, "tempo_factor": tempo,
                    "narrator_voice": args.part2_narrator_voice if part["part"] == 2 else "Victor synthetic narration",
                    "synthetic_narrator": True, "performed_document_readings": True,
                    "master_gain_db": args.master_gain_db,
                    "segments": timings, "sha256": hashlib.sha256(mp3.read_bytes()).hexdigest()}
        mp3.with_suffix(".json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        print(f"Part {part['part']} complete: {mp3}", flush=True)
    if len(rendered_parts) == 2:
        raw_all = args.cache_dir / "complete_episode.wav"
        audio = np.concatenate([sf.read(path)[0] for path in rendered_parts])
        sf.write(raw_all, audio, RATE)
        metadata = args.cache_dir / "chapters.ffmetadata"
        metadata.write_text(";FFMETADATA1\ntitle=The Price of Proof\nartist=ECON 803 · Victor Aguiar\nlanguage=eng\n"
                            "[CHAPTER]\nTIMEBASE=1/1000\nSTART=0\nEND=900000\ntitle=Part One: The Drama\n"
                            "[CHAPTER]\nTIMEBASE=1/1000\nSTART=900000\nEND=1800000\ntitle=Part Two: The Proof and the Invisible Hand\n")
        final = args.output_dir / "ECON803_The_Price_of_Proof_30_Minutes_English.mp3"
        run("ffmpeg", "-y", "-v", "error", "-i", raw_all, "-i", metadata,
            "-map_metadata", 1, "-map_chapters", 1, "-codec:a", "libmp3lame", "-b:a", "96k", final)
        run("ffmpeg", "-v", "error", "-i", final, "-f", "null", "-")
        info = json.loads(run("ffprobe", "-v", "error", "-show_format", "-show_chapters", "-of", "json", final))
        assert abs(float(info["format"]["duration"]) - 1800) < 0.15
        assert len(info["chapters"]) == 2
        manifest = {"file": final.name, "language": "en", "duration_seconds": float(info["format"]["duration"]),
                    "chapters": info["chapters"], "script_sha256": hashlib.sha256(args.script.read_bytes()).hexdigest(),
                    "sha256": hashlib.sha256(final.read_bytes()).hexdigest(), "synthetic_narration": True,
                    "part2_narrator_voice": args.part2_narrator_voice,
                    "master_gain_db": args.master_gain_db,
                    "performed_document_readings": True, "private_reference_included": False}
        final.with_suffix(".json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        print(f"COMPLETE: {final}", flush=True)


if __name__ == "__main__":
    main()
