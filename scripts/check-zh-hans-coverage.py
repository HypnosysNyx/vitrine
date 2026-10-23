#!/usr/bin/env python3
"""Screenshot-based localization regression checks for Vitrine-owned UI.

This does not establish visual correctness; it catches missing exact translations,
untranslated custom render paths and accidental changes to raw selection identifiers.
"""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tweak" / "Sources"
TRANSLATIONS = json.loads((ROOT / "localization" / "zh-Hans.json").read_text(encoding="utf-8"))
# Exact literal keys seen in screenshots from follow-up batches 1-3, plus repeat failures.
CASES = {
    # Follow-up 4: dynamic Karaoke model alert, spatial voice note/value, and generated translation errors.
    "Shared/Sing/Sing.x": [
        "Karaoke needs its voice model, which is downloaded from Mod Settings",
        "Karaoke needs iOS 18, the first its voice model runs on",
    ],
    "Shared/Sing/SingSettings.m": [
        "After %.0f s",
        "How far ahead the voice sings, and how much of the room you hear",
        "The singer's voice keeps its place",
        "%@ · %@ of %@",
        "%@%@%@ from Hugging Face.",
        "The last try failed: %@\n\n",
        "The new voice model runs on the Neural Engine",
        "\n\nKaraoke is tested on the iPhone 15 Pro. On iPhones older than the iPhone 12 it may not keep up, even with the light model.",
        "\n\nKaraoke is tested on the iPhone 15 Pro. On iPhones older than the iPhone 12 it may not keep up; the light model has a better chance.",
        "The download waits for Wi-Fi. Over cellular",
        "What has come in is kept",
        "The voice model coming in stops",
        "Remove the other model?",
        "%@ is not in use. Removing it frees",
    ],
    "Redesigned/Lyrics/SGRSingButton.m": [
        "Karaoke turns the vocals down with a voice model",
        "\n\nThe last try failed: %@",
    ],
    "Redesigned/Lyrics/SGRKaraokeView.m": [
        "Apple Intelligence could not translate the song (%@).",
        "Apple's Translate could not translate the song (%@).",
    ],
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
# A former bug silently overwrote earlier screenshot checks by repeating a dict key.
# Inspect this Python source's own literal so duplicate CASES groups always fail CI.
case_nodes = [
    node.value for node in ast.parse(Path(__file__).read_text(encoding="utf-8")).body
    if isinstance(node, ast.Assign)
    and any(isinstance(target, ast.Name) and target.id == "CASES" for target in node.targets)
]
assert len(case_nodes) == 1 and isinstance(case_nodes[0], ast.Dict), "CASES must be one literal dictionary"
case_keys = [key.value for key in case_nodes[0].keys if isinstance(key, ast.Constant)]
assert len(case_keys) == len(set(case_keys)), "Duplicate screenshot regression group: previous checks would be lost"

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

# Follow-up 4: test real render entrypoints, not just dictionary presence.
assert contains("Shared/Sing/Sing.x", 'stringWithFormat:SGT(@"Karaoke needs its voice model')
assert contains("Shared/Sing/SGSingCard.m", "NSString *words = SGT(SGSingStatusText());")
assert contains("Shared/Sing/SGSingCard.m", 'alertControllerWithTitle:SGT(@"Karaoke") message:SGT(detail)')
assert contains("Shared/Sing/SGSingCard.m", 'actionWithTitle:SGT(SGSingCurrentState()')
assert contains("Shared/Sing/SingSettings.m", 'stringWithFormat:SGT(@"After %.0f s")')
assert contains("Redesigned/Lyrics/SGRSingButton.m", 'message:SGT(message)')
assert contains("Redesigned/Lyrics/SGRKaraokeView.m", "message:[self localizedTranslationError:shownError]")
assert contains("Redesigned/Lyrics/SGRKaraokeView.m", "[NSString stringWithFormat:SGT(format), translation]")
assert contains("Shared/LyricsTranslation/OnDeviceTranslation.swift", 'Apple Intelligence could not translate the song (')
assert contains("Redesigned/Lyrics/SGRKaraokeView.m", "NSString *translation = SGT(reason);")
example = TRANSLATIONS["Apple Intelligence could not translate the song (%@)."].replace(
    "%@", TRANSLATIONS["The model refused to answer."])
assert example == "Apple 智能无法翻译这首歌曲（模型拒绝提供译文）。", example
assert TRANSLATIONS["After %.0f s"] == "%.0f 秒后"
assert "恢复正前方" in TRANSLATIONS[next(k for k in TRANSLATIONS if k.startswith("How far ahead the voice sings"))]

# Latest Karaoke model-download screenshot: each dynamic template must be localized
# BEFORE NSString's format inserts the varying model size or error explanation.
sing_settings = (SRC / "Shared/Sing/SingSettings.m").read_text(encoding="utf-8")
assert 'stringWithFormat:SGT(@"%@%@%@ from Hugging Face.' in sing_settings
assert 'stringWithFormat:SGT(@"The last try failed: %@\\n\\n")' in sing_settings
assert 'update ? SGT(@"The new voice model runs on the Neural Engine' in sing_settings
assert '? SGT(@"\\n\\nKaraoke is tested on the iPhone 15 Pro.' in sing_settings
assert 'stringWithFormat:SGT(@"The download waits for Wi-Fi.' in sing_settings
assert 'stringWithFormat:SGT(@"%@ is not in use. Removing it frees %@' in sing_settings
assert 'stringWithFormat:SGT(@"%@ · %@ of %@")' in sing_settings
assert 'SGSingDownloadModel()' in sing_settings and 'SGSingDeleteOtherModel()' in sing_settings
# Every substantial English source string in this Mod page must have a catalog
# entry, regardless of whether it is currently visible in a particular screenshot.
uncatalogued = [
    value for value in extract_strings(SRC / "Shared/Sing/SingSettings.m")
    if len(value) >= 12 and " " in value and value not in TRANSLATIONS
]
assert not uncatalogued, ("Untranslated Karaoke Mod page strings", uncatalogued)

print(f"PASS: {checked} screenshot strings resolve exactly; duplicate-case protection, Karaoke model dynamic templates, custom rendering, and raw IDs checked")
