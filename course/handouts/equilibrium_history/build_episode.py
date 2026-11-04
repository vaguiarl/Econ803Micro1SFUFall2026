#!/usr/bin/env python3
"""Build an accessible transcript and local synthetic narration without an API."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
STEM = "ECON803_The_Race_to_Prove_the_Invisible_Hand"


def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript-only", action="store_true")
    parser.add_argument("--script", type=Path, default=ROOT / "episode.json")
    parser.add_argument("--transcript-output", type=Path)
    options = parser.parse_args()
    script = options.script.resolve()
    if script != ROOT / "episode.json" and options.transcript_output is None:
        parser.error("An alternate script needs --transcript-output to preserve the released transcript")
    data = json.loads(script.read_text())
    transcript = [f"# {data['title']}", f"\n{data['subtitle']}\n", data["course"],
                  "\nSynthetic narration. Original teaching script; historical sources are linked by section.\n"]
    if data.get("spoken_language"):
        transcript += ["Language: " + data["spoken_language"] + ".\n"]
    if data.get("status"):
        transcript += [f"Status: {data['status']}.\n"]
    if data.get("audio_status"):
        transcript += [f"Audio: {data['audio_status']}.\n"]
    if data.get("performance_note"):
        transcript += [data["performance_note"] + "\n"]
    for section in data["sections"]:
        transcript += [f"## {section['title']}\n", section["text"], ""]
        for reading in section.get("readings", []):
            transcript += [f"Performed document reading: {reading['speaker']}, {reading['document']}.\n"]
        if section["sources"]:
            links = [f"[{data['sources'][key]['label']}]({data['sources'][key]['url']})"
                     for key in section["sources"]]
            transcript += ["Sources: " + "; ".join(links) + ".\n"]
    transcript += ["## Source notes\n"]
    for source in data["sources"].values():
        transcript += [f"[{source['label']}]({source['url']}). {source['note']}\n"]
    transcript_output = options.transcript_output or ROOT / "TRANSCRIPT.md"
    transcript_output.write_text("\n".join(transcript))
    if options.transcript_only:
        return
    if not data.get("voice") or not data.get("rate"):
        raise SystemExit("This script has no approved narration voice. The transcript is ready; review the private voice preview before rendering audio.")
    for executable in ("say", "ffmpeg", "ffprobe"):
        if not shutil.which(executable):
            raise SystemExit(f"Missing executable: {executable}")
    chapters = []
    with tempfile.TemporaryDirectory(prefix="econ803_equilibrium_") as temp:
        work = Path(temp)
        for index, section in enumerate(data["sections"]):
            text = work / f"part_{index:02d}.txt"
            text.write_text(section["title"] + ".\n\n" + section["text"])
            audio = work / f"part_{index:02d}.aiff"
            print(f"Narrating {index + 1}/{len(data['sections'])}: {section['title']}", flush=True)
            run("say", "-v", data["voice"], "-r", str(data["rate"]), "-f", str(text), "-o", str(audio))
            duration = float(run("ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "default=nw=1:nk=1", str(audio)).strip())
            chapters.append({"title": section["title"], "duration_seconds": duration})
        listing = work / "concat.txt"
        listing.write_text("\n".join(f"file '{work / f'part_{i:02d}.aiff'}'" for i in range(len(chapters))))
        metadata = [";FFMETADATA1", f"title={data['title']}: {data['subtitle']}",
                    "artist=ECON 803 teaching materials", "album=Victor Aguiar · Fall 2026",
                    f"comment=Synthetic narration using macOS {data['voice']}; script and sources accompany the audio."]
        elapsed = 0
        for chapter in chapters:
            chapter["start_seconds"] = round(elapsed, 3)
            end = elapsed + chapter["duration_seconds"]
            metadata += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={round(elapsed * 1000)}",
                         f"END={round(end * 1000)}", f"title={chapter['title']}"]
            elapsed = end
        meta = work / "metadata.txt"
        meta.write_text("\n".join(metadata) + "\n")
        output = ROOT / f"{STEM}.mp3"
        run("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listing),
            "-i", str(meta), "-map_metadata", "1", "-map_chapters", "1", "-af",
            "loudnorm=I=-16:TP=-1.5:LRA=11", "-ac", "1", "-ar", "44100", "-codec:a", "libmp3lame",
            "-b:a", "96k", str(output))
    verified = json.loads(run("ffprobe", "-v", "error", "-show_format", "-show_streams", "-show_chapters", "-of", "json", str(output)))
    assert len(verified["chapters"]) == len(chapters)
    assert verified["streams"][0]["codec_name"] == "mp3"
    assert abs(float(verified["format"]["duration"]) - elapsed) < 1
    # Decode the complete file to check the encoded audio, not just its header.
    run("ffmpeg", "-v", "error", "-i", str(output), "-f", "null", "-")
    manifest = {"file": output.name, "duration_seconds": float(verified["format"]["duration"]),
                "bytes": output.stat().st_size, "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
                "voice": data["voice"], "rate": data["rate"], "synthetic_narration": True,
                "chapters": chapters}
    (ROOT / "audio_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({key: manifest[key] for key in ("file", "duration_seconds", "bytes")}))


if __name__ == "__main__":
    main()
