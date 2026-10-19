"""Isolated public-release guard tests; all repository data are synthetic."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


GUARD = Path(__file__).resolve().parents[1] / "check_public_assessments.py"
RELEASE_DIR = "course/released_assessments"
ARTIFACT = f"{RELEASE_DIR}/midterm1/solutions.md"
MANIFEST = f"{RELEASE_DIR}/PUBLIC_RELEASES.json"


class PublicAssessmentGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="public-assessment-guard-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-q")

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.repo), *args], check=True, capture_output=True
        )

    def write(self, path, data):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def release(self):
        content = b"Synthetic released solution.\n"
        self.write(ARTIFACT, content)
        manifest = {"releases": [{
            "assessment": "Midterm 1, October 16, 2026",
            "released_on": "2026-10-18",
            "files": [{"path": ARTIFACT, "sha256": hashlib.sha256(content).hexdigest()}],
        }]}
        self.write(MANIFEST, json.dumps(manifest).encode())
        self.git("add", "--", ARTIFACT, MANIFEST)
        return manifest

    def run_guard(self, *args, succeeds=True, contains=None):
        result = subprocess.run(
            [sys.executable, str(GUARD), "--repo", str(self.repo), *args],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0 if succeeds else 3, result.stdout + result.stderr)
        if contains:
            self.assertIn(contains, result.stdout + result.stderr)

    def test_exact_release_passes_in_worktree_and_index(self):
        self.release()
        self.run_guard()
        self.run_guard("--staged")

    def test_unlisted_tracked_release_rejected(self):
        self.release()
        path = f"{RELEASE_DIR}/extra.md"
        self.write(path, b"Not authorized.\n")
        self.git("add", "--", path)
        self.run_guard(succeeds=False, contains="Unlisted tracked release artifact")
        self.run_guard("--staged", succeeds=False, contains="Unlisted tracked release artifact")

    def test_stale_hash_and_index_worktree_separation(self):
        self.release()
        self.write(ARTIFACT, b"Changed after authorization.\n")
        self.run_guard(succeeds=False, contains="SHA-256 mismatch")
        self.run_guard("--staged")
        self.git("add", "--", ARTIFACT)
        self.run_guard("--staged", succeeds=False, contains="SHA-256 mismatch")

    def test_legacy_restricted_patterns_remain_blocked(self):
        for path in ("course/Midterm_secret.pdf", "old/exam1.lyx", "problemsets/topic/answers.md"):
            with self.subTest(path=path):
                self.write(path, b"Synthetic restricted artifact.\n")
                self.git("add", "--", path)
                self.run_guard("--staged", succeeds=False, contains=path)
                self.git("rm", "--cached", "--", path)

    def test_untracked_manifest_cannot_authorize(self):
        self.release()
        self.git("rm", "--cached", "--", MANIFEST)
        self.run_guard(succeeds=False, contains="require a tracked PUBLIC_RELEASES.json")

    def test_path_traversal_and_unsupported_extension_rejected(self):
        for invalid in (f"{RELEASE_DIR}/../secret.md", f"{RELEASE_DIR}/script.py"):
            with self.subTest(path=invalid):
                manifest = self.release()
                manifest["releases"][0]["files"][0]["path"] = invalid
                self.write(MANIFEST, json.dumps(manifest).encode())
                self.run_guard(succeeds=False, contains="Invalid public release artifact path")

    def test_release_symlink_rejected_even_with_matching_hash(self):
        self.release()
        target = self.repo / ARTIFACT
        target.unlink()
        link_target = self.repo / "ordinary.md"
        link_target.write_text("Synthetic released solution.\n")
        target.symlink_to(link_target)
        self.run_guard(succeeds=False, contains="must not use a symlink")
        self.git("add", "--", ARTIFACT)
        self.run_guard("--staged", succeeds=False, contains="tracked regular file")


if __name__ == "__main__":
    unittest.main()
