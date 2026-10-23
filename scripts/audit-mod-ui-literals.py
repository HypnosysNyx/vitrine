#!/usr/bin/env python3
"""Find likely untranslated user-facing literals across Vitrine-owned UI.

This is a heuristic, not a visual substitute. It intentionally leaves legal
copyright / attribution notices under App/About/Licenses.m unchanged.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tweak" / "Sources"
CATALOG = json.loads((ROOT / "localization" / "zh-Hans.json").read_text(encoding="utf-8"))
LITERALS = re.compile(r'@"(?:\\.|[^"\\])*"(?:\s*@?"(?:\\.|[^"\\])*")*')
PIECES = re.compile(r'"(?:\\.|[^"\\])*"')
UI_CONTEXT = re.compile(r'(SG\w*Row|SGNote|SGNotedSection|SGSectionFooter|'
                        r'SGSectionHeader|SGSection|SGFillCell|alertControllerWithTitle|'
                        r'message:|\.text\s*=|\.title\s*=|accessibilityLabel\s*=)')
# These are licenses that must retain their legally required notices verbatim.
LEGAL_NOTICES = {"App/About/Licenses.m"}
# Exact non-UI exceptions only: the trademarked picker catalog name and log diagnostics.
NON_UI_LITERAL_EXCEPTIONS = {
    ("Shared/Navigation/AddTabSheet.m", "Spotify Encore"),
    ("Redesigned/Navbar/Navbar.x", "row in %@ %@, icon %@ label %@, stack %@ axis %ld dist %ld align %ld spacing %.1f autolayout %d"),
    ("Native/Navbar/Navbar.x", "row in %@ %@, icon %@ label %@, stack %@ axis %ld dist %ld align %ld spacing %.1f autolayout %d"),
}
found = []
files_checked = 0

for path in SRC.rglob("*"):
    if path.suffix not in {".m", ".x", ".mm"} or path.name == "SGL10n.m":
        continue
    rel = path.relative_to(SRC).as_posix()
    if rel in LEGAL_NOTICES or path.name == "SGFlagList.m":
        continue
    files_checked += 1
    code = path.read_text(encoding="utf-8", errors="replace")
    for match in LITERALS.finditer(code):
        try:
            value = "".join(json.loads(piece) for piece in PIECES.findall(match.group()))
        except ValueError:
            continue
        if (rel, value) in NON_UI_LITERAL_EXCEPTIONS:
            continue
        if value in CATALOG or len(value) < 12 or " " not in value:
            continue
        if value.startswith(("spotifyglass.", "ios-", "https://", "http://", "#", "<", "/", "com.", "@")):
            continue
        before = code[max(0, match.start() - 200):match.start()]
        if not UI_CONTEXT.search(before):
            continue
        if re.search(r'NSLog|SGLog|functionWith|imageNamed|field\.text|placeholder=', before[-90:]):
            continue
        line = code.count("\n", 0, match.start()) + 1
        found.append((rel, line, value))

if found:
    print(f"FAIL: {len(found)} possible untranslated Mod UI literals")
    for rel, line, value in found:
        print(f"  {rel}:{line}: {value[:160]!r}")
    raise SystemExit(1)
print(f"PASS: {files_checked} Mod source files scanned; no unlisted likely UI strings")
