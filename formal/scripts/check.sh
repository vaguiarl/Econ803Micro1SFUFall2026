#!/usr/bin/env bash
set -euo pipefail

formal_dir="$(cd "$(dirname "$0")/.." && pwd)"
repo_dir="$(cd "$formal_dir/.." && pwd)"

printf 'Lean toolchain: '
(cd "$formal_dir" && lake env lean --version)

printf 'Checking pinned dependency manifest...\n'
python3 - "$formal_dir/lake-manifest.json" <<'PY'
import json
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as handle:
    manifest = json.load(handle)

packages = {entry["name"]: entry for entry in manifest["packages"]}
expected = "d874dab846e28928f2a75b2359a0c2a8766a7b93"
actual = packages.get("wgarp", {}).get("rev")
if actual != expected:
    raise SystemExit(f"WGARP revision mismatch: expected {expected}, got {actual}")
print(f"WGARP revision: {actual}")
print(f"Mathlib revision: {packages['mathlib']['rev']}")
PY

printf 'Rejecting unchecked declarations in textbook Lean sources...\n'
if rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b' \
    "$formal_dir" --glob '*.lean'; then
  printf 'Unchecked Lean declaration found.\n' >&2
  exit 1
fi

audit_tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/econ803-formal-audit.XXXXXX")"
trap 'rm -rf "$audit_tmp_dir"' EXIT
coverage_check="$audit_tmp_dir/CoverageDeclarations.lean"
audit_output="$audit_tmp_dir/axioms.txt"

printf 'Validating coverage schema and audit membership...\n'
python3 - "$formal_dir/coverage.json" \
    "$formal_dir/Econ803/TrustAudit.lean" "$coverage_check" <<'PY'
import json
import re
import sys

coverage_path, audit_path, lean_check_path = sys.argv[1:]
with open(coverage_path, encoding="utf-8") as handle:
    data = json.load(handle)
with open(audit_path, encoding="utf-8") as handle:
    audit_source = handle.read()

ids = [row["id"] for row in data["targets"]]
if len(ids) != len(set(ids)):
    raise SystemExit("duplicate coverage id")

allowed_statuses = {
    "verified-local", "verified-imported", "verified-core",
    "future-target", "cited-only"
}
verified = []
for row in data["targets"]:
    status = row["status"]
    if status not in allowed_statuses:
        raise SystemExit(f"bad status for {row['id']}: {status}")
    raw = row.get("declaration")
    if status.startswith("verified") and not raw:
        raise SystemExit(f"verified row lacks declaration: {row['id']}")
    if status.startswith("verified"):
        for declaration in (part.strip() for part in raw.split(";")):
            if not declaration:
                raise SystemExit(f"empty declaration in {row['id']}")
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_'.]*", declaration):
                raise SystemExit(
                    f"unsafe declaration syntax in {row['id']}: {declaration}")
            verified.append((row["id"], declaration))

audit_declarations = set(re.findall(
    r"^\s*#print\s+axioms\s+([A-Za-z_][A-Za-z0-9_'.]*)\s*$",
    audit_source,
    flags=re.MULTILINE,
))
missing_audit = [
    f"{row_id}: {declaration}"
    for row_id, declaration in verified
    if declaration not in audit_declarations
]
if missing_audit:
    raise SystemExit(
        "verified declarations missing from TrustAudit:\n  " +
        "\n  ".join(missing_audit)
    )

unique_verified = list(dict.fromkeys(declaration for _, declaration in verified))
with open(lean_check_path, "w", encoding="utf-8") as handle:
    handle.write("import Econ803\n\n")
    for declaration in unique_verified:
        handle.write(f"#check {declaration}\n")

print(f"coverage rows: {len(ids)}")
print(f"verified declarations: {len(unique_verified)}")
PY

printf 'Building the textbook library and pinned WGARP dependency...\n'
(cd "$formal_dir" && lake build)

printf 'Typechecking every verified coverage declaration...\n'
(cd "$formal_dir" && lake env lean "$coverage_check") >/dev/null

printf 'Compiling retained standalone checks...\n'
for source in BookNarrativeLogic.lean ChoiceTheory.lean OrderTheory.lean; do
  (cd "$formal_dir" && lake env lean "$source")
done

printf 'Running kernel axiom audit...\n'
(cd "$formal_dir" && lake env lean Econ803/TrustAudit.lean) 2>&1 | tee "$audit_output"

printf 'Checking the explicit kernel-axiom whitelist...\n'
python3 - "$formal_dir/coverage.json" \
    "$formal_dir/Econ803/TrustAudit.lean" "$audit_output" <<'PY'
import json
import re
import sys

coverage_path, audit_path, output_path = sys.argv[1:]
with open(coverage_path, encoding="utf-8") as handle:
    data = json.load(handle)
with open(audit_path, encoding="utf-8") as handle:
    audit_source = handle.read()
with open(output_path, encoding="utf-8") as handle:
    output = handle.read()

coverage_declarations = set()
for row in data["targets"]:
    if row["status"].startswith("verified"):
        coverage_declarations.update(
            part.strip() for part in row["declaration"].split(";") if part.strip()
        )

audit_declarations = set(re.findall(
    r"^\s*#print\s+axioms\s+([A-Za-z_][A-Za-z0-9_'.]*)\s*$",
    audit_source,
    flags=re.MULTILINE,
))

no_axioms = set(re.findall(
    r"'([^']+)' does not depend on any axioms", output
))
dependency_matches = re.findall(
    r"'([^']+)' depends on axioms:\s*\[(.*?)\]", output, flags=re.DOTALL
)
dependencies = {
    declaration: {
        axiom.strip()
        for axiom in raw.replace("\n", " ").split(",")
        if axiom.strip()
    }
    for declaration, raw in dependency_matches
}
reported = no_axioms | set(dependencies)

missing_reports = sorted(audit_declarations - reported)
if missing_reports:
    raise SystemExit(
        "TrustAudit declarations missing axiom reports: " +
        ", ".join(missing_reports)
    )

missing_verified = sorted(coverage_declarations - reported)
if missing_verified:
    raise SystemExit(
        "verified coverage declarations missing axiom reports: " +
        ", ".join(missing_verified)
    )

permitted_axioms = {"propext", "Classical.choice", "Quot.sound"}
violations = []
for declaration, axioms in sorted(dependencies.items()):
    forbidden = axioms - permitted_axioms
    if forbidden:
        violations.append(f"{declaration}: {', '.join(sorted(forbidden))}")
if violations:
    raise SystemExit(
        "non-whitelisted kernel axioms:\n  " + "\n  ".join(violations)
    )

print("permitted axioms: " + ", ".join(sorted(permitted_axioms)))
print(f"audited declarations: {len(reported)}")
PY

printf 'PASS: Lean builds; coverage declarations exist and are audited; axioms are whitelisted.\n'
