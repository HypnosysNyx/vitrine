#!/usr/bin/env python3
"""Audit direct Vitrine UI string sinks missed by the older row-oriented scan.

Unlike a string-literal inventory, this source-aware guardrail examines places
where a label is handed directly to UIKit (menus, actions, fields, VoiceOver).
Catalog presence alone is not enough; the call site must localize the value.
Dynamic producer -> renderer paths are covered by check-zh-hans-coverage.py.

Don't translate Spotify native UI, app IDs, SF Symbol identifiers, API strings,
custom/persisted values or required third-party legal notices.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tweak" / "Sources"
CATALOG = json.loads((ROOT / "localization/zh-Hans.json").read_text(encoding="utf-8"))
# Anchored in direct mod-owned UIKit display sinks, *not* log output, stored
# values or Spotify's own views. Original English literals here bypass SGT.
DIRECT_UI = re.compile(
    r'(?:\[UIMenu\s+menuWithTitle:|\[UIAction\s+actionWithTitle:|'
    r'\[UIAlertAction\s+actionWithTitle:|'
    r'\[UIAlertController\s+alertControllerWithTitle:|SGOnboardingButton\(|'
    r'(?:\.text|\.title|\.subtitle|\.accessibilityLabel|\.accessibilityValue|'
    r'\.accessibilityHint|\.placeholder)\s*=\s*)'
    r'\s*@"((?:\\.|[^"\\])*)"', re.S
)
SGT_EXACT = re.compile(r'SGT\(\s*((?:@"(?:\\.|[^"\\])*"\s*)+)\)')
SEGMENT = re.compile(r'@("(?:\\.|[^"\\])*")')
# Only technical raw values, not user-facing English language.
EXCEPTIONS = {
    ("Shared/AudioEffects/AudioEffectsLibraryPage.m", "GraphicEQ"),  # file format identifier
    ("Shared/LyricsSources/SpicyLyrics.m", "sl_pk_..."),  # API-key placeholder example
    ("Shared/Navigation/AddTabSheet.m", "spotify:playlist:…"),  # URI example
}

ui_errors = []
lookup_errors = []
checked = 0
for file in sorted(SRC.rglob("*")):
    if file.suffix not in {".m", ".mm", ".x"} or file.name == "SGL10n.m":
        continue
    checked += 1
    text = file.read_text(encoding="utf-8")
    rel = file.relative_to(SRC).as_posix()
    for match in DIRECT_UI.finditer(text):
        name = match.group(1)
        if not re.search(r"[A-Za-z]", name) or (rel, name) in EXCEPTIONS:
            continue
        ui_errors.append((rel, text.count("\n", 0, match.start()) + 1, name))
    for match in SGT_EXACT.finditer(text):
        try:
            key = "".join(json.loads(p) for p in SEGMENT.findall(match.group(1)))
        except json.JSONDecodeError:
            continue
        if key not in CATALOG:
            lookup_errors.append((rel, text.count("\n", 0, match.start()) + 1, key))

for kind, errors in (("Direct UIKit literal bypasses localization", ui_errors),
                     ("SGT lookup key is absent from catalog", lookup_errors)):
    for rel, line, value in errors:
        print(f"FAIL: {kind}: {rel}:{line}: {value!r}")
if ui_errors or lookup_errors:
    raise SystemExit(1)
print(f"PASS: {checked} source files, no direct Mod UI literals or missing exact SGT keys")
