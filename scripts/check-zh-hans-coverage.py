#!/usr/bin/env python3
"""Screenshot-based localization regression checks for Vitrine-owned UI.

This does not establish visual correctness; it catches missing exact translations,
untranslated custom render paths and accidental changes to raw selection identifiers.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tweak" / "Sources"
TRANSLATIONS = json.loads((ROOT / "localization" / "zh-Hans.json").read_text(encoding="utf-8"))
# Exact literal keys seen in screenshots from follow-up batches 1-3, plus repeat failures.
CASES = {
    "Redesigned/Home/HomeSettings.m": [
        "Top picks, the tinted shortcut pills",
        "A shelf Home does not show today",
    ],
    "Redesigned/Home/HomeTopPicks.x": ["Home's first shelf above"],
    "Redesigned/Player/PlayerSettings.m": ["Brightness above 100%"],
    "Redesigned/NowPlayingBar/NowPlayingBarSettings.m": [
        "Kept on the bar between the tabs", "On the full now playing bar",
    ],
    "Redesigned/Navbar/NavbarSettings.m": ["Drag a tab to move it", "Off, the bar shows"],
    "Redesigned/Album/AlbumSettings.m": [
        "At the top of an album", "The artist under a track",
        "Any other section Spotify sends", "Sections are told apart",
    ],
    "Shared/Sing/SGSpatialPreview.m": [
        "Motion & Fitness is off", "Following your head. Turn it",
        "Following your head. Turn Spatial", "Preview. With AirPods",
    ],
    "Shared/Sing/SingSettings.m": ["The singer's voice keeps its place"],
    "Shared/HeadGestures/HeadGesturesSettings.m": [
        "Nod twice or shake your head to control the music",
        "They work while Spotify plays through headphones",
    ],
    "Shared/Haptics/SGVibrationsPreview.m": [
        "Tap to feel Controls", "Tap to feel Music Haptics",
        "In the Background is played", "Turn on Controls or Music",
    ],
    "Shared/Flags/FlagPages.m": ["One minute option", "Options sheet is always on"],
    "Shared/AudioEffects/AudioEffectsPage.m": [
        "Crossfeed is ", " by Boris Mikhaylov. Liveprog", ", from Cockos' WDL.",
    ],
    "Shared/AudioEffects/AudioEffectsPresetsPage.m": [
        "Corrections that make your headphones", "With this on, the correction",
    ],
    "Shared/ListeningStats/ListeningStatsPage.m": [
        "In Spotify's account privacy settings",
    ],
    "Shared/LiveActivity/LiveActivitySettings.m": [
        "Colors: Spotify puts the cover",
        "How long the sound fades before a sleep timer",
    ],
}
STRINGS = re.compile(r'@"(?:\\.|[^"\\])*"(?:\s*@?"(?:\\.|[^"\\])*")*')
PIECES = re.compile(r'"(?:\\.|[^"\\])*"')


def extract_strings(file: Path) -> list[str]:
    content = file.read_text(encoding="utf-8")
    found = []
    for m in STRINGS.finditer(content):
        try:
            found.append("".join(json.loads(x) for x in PIECES.findall(m.group())))
        except ValueError:
            continue  # non-JSON Objective-C escapes not used by screenshots
    return found


checked = 0
for rel, prefixes in CASES.items():
    strings = extract_strings(SRC / rel)
    for prefix in prefixes:
        candidates = [text for text in strings if text.startswith(prefix)]
        assert len(candidates) == 1, (rel, prefix, len(candidates))
        key = candidates[0]
        assert key in TRANSLATIONS, ("Untranslated screenshot string", rel, key)
        assert TRANSLATIONS[key] != key, ("No-op translation", rel, key)
        checked += 1

def contains(path: str, needle: str) -> bool:
    return needle in (SRC / path).read_text(encoding="utf-8")

# Exact matching is necessary, but insufficient: verify the custom renderers translate.
assert contains("Settings/SGModPage.m", "row.subtitle = SGT(subtitle);")
assert contains("Settings/SGPageStyle.m", "label.text = SGT(text);")
assert contains("Shared/Sing/SGSpatialPreview.m", "text = SGT(text);")
assert contains("Shared/Haptics/SGVibrationsPreview.m", "SGT(captionFor(_feature))")
assert contains("Shared/AudioEffects/AudioEffectsPage.m", "initWithString:SGT(@\"Crossfeed is \")")
assert contains("Shared/AudioEffects/AudioEffectsPage.m", "initWithString:SGT(part[0])")
assert contains("Redesigned/Lyrics/SGRKaraokeView.m", "shownError = [NSString stringWithFormat:SGT(@\"Apple Intelligence left ")
# Mod-owned picker display; raw system font names/Spotify Encore selectors remain unchanged.
assert contains("Shared/Fonts/FontImport.m", "SGZHFontDisplayName(title)")
assert contains("Shared/Fonts/FontImport.m", "setObject:_families[(NSUInteger)path.row] forKey:SGKeyAppFontFamily")
assert contains("Shared/Navigation/AddTabSheet.m", "SGZHIconDisplayName(name, symbols)")
assert contains("Shared/Navigation/AddTabSheet.m", "_draft.icon = _sections[(NSUInteger)path.section][(NSUInteger)path.row]")
assert contains("Shared/AudioEffects/AudioEffectsPresetsPage.m", "SGZHAutoEqCatalogDisplayName(headphone.name)")
assert contains("Shared/AudioEffects/AudioEffectsPresetsPage.m", "SGFillCell(cell, output[@\"name\"]")
assert contains("Shared/AudioEffects/AudioEffectsPresetsPage.m", "SGAutoEqOutputName()")
assert contains("Shared/AudioEffects/AudioEffectsPresetsPage.m", "_applying = headphone.path")
assert contains("Shared/AudioEffects/AudioEffectsPresetsPage.m", "NSString *original = _builtIn[(NSUInteger)path.row]")
assert contains("Shared/AudioEffects/AudioEffectsPresetsPage.m", "SGDSPLoadBuiltInPreset(path.row)")
print(f"PASS: {checked} screenshot strings resolve exactly; custom rendering and raw selectors/IDs checked")
