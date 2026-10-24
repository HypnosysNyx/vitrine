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
assert contains("Redesigned/Lyrics/SGRKaraokeView.m", "message:([shownError isEqualToString:error] ? [self localizedTranslationError:error] : shownError)")
assert contains("Redesigned/Lyrics/SGRKaraokeView.m", "[NSString stringWithFormat:SGT(format), translated]")
assert contains("Shared/LyricsTranslation/OnDeviceTranslation.swift", 'Apple Intelligence could not translate the song (')
assert contains("Redesigned/Lyrics/SGRKaraokeView.m", "NSString *translated = SGT(reason);")
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

# Follow-up: Vitrine-owned target language picker must use Chinese locale when the
# Mod uses zh-Hans, keeping every language tag and saved index exactly unchanged.
lang_src = (SRC / "Shared/LyricsSources/LyricsSources.m").read_text(encoding="utf-8")
tag_anchor = "NSArray<NSString *> *SGLyricsTranslationLanguages(void) {"
assert tag_anchor in lang_src, "Language tag source moved; review persisted setting indices"
tag_start = lang_src.index(tag_anchor)
tag_end = lang_src.index("];", tag_start)
lang_tags = re.findall(r'@"([^"]*)"', lang_src[tag_start:tag_end])
expected_tags = ["", "ar", "zh-Hans", "zh-Hant", "cs", "da", "nl", "en",
                 "fi", "fr", "de", "el", "he", "hi", "hu", "id", "it", "ja",
                 "ko", "nb", "pl", "pt", "ro", "ru", "sk", "es", "sv", "th",
                 "tr", "uk", "vi"]
assert lang_tags == expected_tags, ("Language IDs must remain stable", lang_tags)
assert 'BOOL chinese = SGUseSimplifiedChinese();' in lang_src
assert 'chinese ? @"zh-Hans" : @"en"' in lang_src
assert '[display localizedStringForLocaleIdentifier:tag]' in lang_src
assert '[tag isEqualToString:@"zh-Hans"]' in lang_src and '[names addObject:@"简体中文"]' in lang_src
assert '[tag isEqualToString:@"zh-Hant"]' in lang_src and '[names addObject:@"繁体中文"]' in lang_src
assert contains("Core/SGL10n.h", "FOUNDATION_EXPORT BOOL SGUseSimplifiedChinese(void);")
assert contains("Settings/SGModPage.m", "SGFillCell(cell, SGT(_choices[index])")
assert contains("Settings/SGModPage.m", "SGSetInt(_key, path.row)")
assert contains("Shared/Lyrics/LyricsSettings.m", "SGLyricsTranslationLanguageNames(), 0")

# The iOS 27 guardrail screenshot must never show a raw English NSError to users.
assert TRANSLATIONS["The model's safety guardrails were triggered."] == "触发了模型的安全保护机制"
error_ui = (SRC / "Redesigned/Lyrics/SGRKaraokeView.m").read_text(encoding="utf-8")
assert "if (!error.length || !SGUseSimplifiedChinese()) return error;" in error_ui
assert "NSString *translated = SGT(reason);" in error_ui
assert "if (![translated isEqualToString:reason])" in error_ui
assert 'SGLog(@"lyrics: untranslated translation failure: %@", error)' in error_ui
assert 'return SGT(@"The translation could not be completed. Please try again.");' in error_ui
assert 'message:([shownError isEqualToString:error] ? [self localizedTranslationError:error] : shownError)' in error_ui
assert TRANSLATIONS["Apple Intelligence could not translate the song. Please try again."] != "Apple Intelligence could not translate the song. Please try again."
assert "detail.contains(\"safety guardrails\")" in (SRC / "Shared/LyricsTranslation/OnDeviceTranslation.swift").read_text(encoding="utf-8")
guardrail_shown = TRANSLATIONS["Apple Intelligence could not translate the song (%@)."].replace(
    "%@", TRANSLATIONS["The model's safety guardrails were triggered."])
assert guardrail_shown == "Apple 智能无法翻译这首歌曲（触发了模型的安全保护机制）。", guardrail_shown

# Screenshot 2026-10-24: beta.14's What's New sheet showed its title, categories,
# changelog bullets and Continue in English despite all earlier static checks
# passing. Track the actual runtime renderer and GENERATED changelog keys.
whatsnew = (SRC / "App/Onboarding/WhatsNew.m").read_text(encoding="utf-8")
assert "label(SGT(@\"What's New in Vitrine\")," in whatsnew
assert 'stringWithFormat:SGT(@"Version %s"), SG_VERSION' in whatsnew
assert 'SGOnboardingButton(SGT(@"Continue"))' in whatsnew
assert 'NSString *localized = SGT(change.text);' in whatsnew
assert 'UILabel *heading = label(SGT(kind),' in whatsnew
assert contains("App/About/UpdatePage.m", "row.title = SGT(change.text);")
assert contains("App/About/UpdatePage.m", "release.version, SGT(kind),")
assert contains("App/About/UpdateNotice.m", "SGT(changes[i].text)")
for static_key in ("What's New in Vitrine", "Version %s", "Continue", "Features", "Fixes"):
    assert TRANSLATIONS.get(static_key) and TRANSLATIONS[static_key] != static_key, static_key

# Compare against the exact English notes compiled into SGWhatsNewNotes.h by
# scripts/whats-new.sh; neither the CHANGELOG file itself nor commit URLs are changed.
current_version = (ROOT / "version.txt").read_text(encoding="utf-8").strip()
changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
section_match = re.search(r"(?ms)^## \[" + re.escape(current_version) +
                          r"\][^\n]*\n(.*?)(?=^## \[|\Z)", changelog)
assert section_match, ("Missing current release notes", current_version)
release_notes = []
for raw in section_match.group(1).splitlines():
    line = raw.strip()
    if not line.startswith(("* ", "- ")):
        continue
    line = re.sub(r"\s*\(\[[0-9a-f]{6,}\]\([^)]+\)\)\s*$", "", line[2:])
    line = re.sub(r"\[([^\]]*)\]\([^)]+\)", r"\1", line).replace("**", "").strip()
    if line:
        release_notes.append(line)
assert release_notes, ("Release sheet would be empty", current_version)
missing_notes = [line for line in release_notes
                 if line not in TRANSLATIONS or TRANSLATIONS[line] == line]
assert not missing_notes, ("Unlocalized What's New notes", current_version, missing_notes)
assert TRANSLATIONS["AI DJ player in the redesign (#36)"] == "重新设计版新增 AI DJ 播放器（#36）"
assert TRANSLATIONS["Automatic in Lyrics Source, and a switch to prefer word-by-word timing"].startswith("歌词来源新增")
assert TRANSLATIONS["AutoMix blends songs with Spotify's own Automix and crossfade (#41)"].endswith("（#41）")
print(f"PASS: What's New render path and all {len(release_notes)} current release notes translated")


# User screenshot 2026-10-24: karaoke translation menu has Chinese actions
# but renders the Mod-owned "Translated by" heading in English. Root cause:
# the UIMenu title and adjacent UIAction/date labels bypassed SGT entirely.
lyrics_menu = (SRC / "Redesigned/Lyrics/SGRKaraokeView.m").read_text(encoding="utf-8")
assert 'menuWithTitle:SGT(@"Translated by")' in lyrics_menu
assert 'actionWithTitle:SGT(@"Delete This Translation")' in lyrics_menu
assert ': SGT(@"Date unknown");' in lyrics_menu
assert 'actionWithTitle:SGT(_saved.name)' in lyrics_menu
assert '[SGT(@"Translate with ") stringByAppendingString:SGAITranslatorName()]' in lyrics_menu
assert '[SGT(@"Sends the lyrics to ") stringByAppendingString:SGAITranslatorRecipient()]' in lyrics_menu
assert TRANSLATIONS['Translated by'] == '翻译来源'
assert TRANSLATIONS['Delete This Translation'] == '删除此翻译'
assert TRANSLATIONS['Date unknown'] == '日期未知'
assert 'return SGT(@"Translate on iPhone")' in (SRC / "Shared/LyricsTranslation/LyricsTranslation.m").read_text(encoding="utf-8")

# Run-time text may be generated by an interpolator, OS errors or a status
# provider, rather than appearing verbatim in any English literal scan.
sing_src = (SRC / "Shared/Sing/Sing.x").read_text(encoding="utf-8")
assert 'stringWithFormat:SGT(@"Downloading %.0f%%")' in sing_src
assert 'stringWithFormat:SGT(@"Loading the voice model, %.0f s")' in sing_src
assert 'if (sg_stopped ?: sg_refused) return SGT(sg_stopped ?: sg_refused);' in sing_src
assert 'if (SGSingLoaderError()) return [SGT(error) stringByAppendingString:SGT(' in sing_src
assert 'static NSString *runsOnNote(void)' in sing_src
assert 'case SGSingFastReady: return SGT(@"Karaoke runs on the Neural Engine.")' in sing_src
assert TRANSLATIONS['Downloading %.0f%%'] == '正在下载 %.0f%%'
assert TRANSLATIONS['Loading the voice model, %.0f s'] == '正在加载人声模型，已用 %.0f 秒'
loader_src = (SRC / "Shared/Sing/SGSingLoader.m").read_text(encoding="utf-8")
assert 'stringWithFormat:SGT(@"The voice model did not load: %@")' in loader_src
assert 'SGUseSimplifiedChinese() ? SGT(@"Core ML could not load the voice model; diagnostic details are in the logs.")' in loader_src
assert 'stringWithFormat:SGT(@"%.2f GB left to the process")' in loader_src
# The runtime still logs original NSError descriptions for diagnostics and
# none of the underlying model-download, voice-model or audio work is changed.
assert 'SGLog(@"sing: load ' in loader_src
assert 'SGLyricsTranslationLanguages(void)' in (SRC / "Shared/LyricsSources/LyricsSources.m").read_text(encoding="utf-8")
assert 'setObject:_families[(NSUInteger)path.row]' in (SRC / "Shared/Fonts/FontImport.m").read_text(encoding="utf-8") or 'SGZHFontDisplayName(title)' in (SRC / "Shared/Fonts/FontImport.m").read_text(encoding="utf-8")
print("PASS: 2026-10-24 Translated by screenshot, renderer checks and dynamic Karaoke templates")

# Screenshot 2026-10-24: the redesigned player's three top quick actions
# appeared in English although their translations were already in zh-Hans.
# Keep matching the native Spotify row by the ORIGINAL English key / row ID.
quick_source = (SRC / "Redesigned/ContextMenu/ContextMenu.x").read_text(encoding="utf-8")
quick_trio = (
    ("Share", "分享", "square.and.arrow.up", "share", "9"),
    ("Add to Playlist", "添加到播放列表", "text.badge.plus", "add to playlist", "19"),
    ("Add to Queue", "加入播放队列", "text.line.last.and.arrowtriangle.forward", "add to queue", "11"),
)
for english, chinese, symbol, native_title, native_id in quick_trio:
    assert TRANSLATIONS.get(english) == chinese, ("Quick menu translation missing", english)
    source_item = f'@[@"{english}", @"{symbol}", @"{native_title}", @"{native_id}"]'
    assert source_item in quick_source, ("Spotify quick action identity changed", english)
quick_renderer = quick_source.split("- (UIMenu *)quickRow {", 1)[1].split("- (void)refreshQuickRow {", 1)[0]
assert "[UIAction actionWithTitle:SGT(item[0])" in quick_renderer, "Quick action text bypasses SGT"
assert "NSString *quick = item[2];" in quick_renderer, "Quick match key should remain original"
assert "[weakSelf fireQuick:quick];" in quick_renderer, "Quick native handler should not change"
assert "SGT(item[2])" not in quick_renderer, "Do not translate native matcher"
print("PASS: player menu three quick actions localized; native keys / handlers preserved")


# beta.15 regression: the redesigned player's Lyrics Source submenu became a
# live updating popover. The former row renderer was removed by upstream; new
# header/row/placeholder/action text must be localized at their NEW sinks.
player_menu = (SRC / "Redesigned/Player/PlayerMenu.m").read_text(encoding="utf-8")
assert 'title.text = SGT(@"Lyrics Source");' in player_menu
assert 'automatic.title = SGT(@"Automatic");' in player_menu
assert 'automatic.subtitle = current ? SGT(@"As the order chooses") : SGT(SGLyricsCreditFor(_track));' in player_menu
assert 'row.title = SGT(SGLyricsProviderFor(key).name);' in player_menu
assert 'row.subtitle = offer ? timingText(offer.karaokeLines) : SGT(@"Asking…");' in player_menu
assert 'none.title = SGT(@"No Source Has Lyrics");' in player_menu
assert 'actionWithTitle:SGT(@"Lyrics Source") image:symbol(@"quote.bubble")' in player_menu
assert 'open.subtitle = SGT(SGLyricsCreditFor(track));' in player_menu
assert 'if (row.key) SGLyricsChooseSource(_track, row.key);' in player_menu
assert 'else SGLyricsChooseAutomatic(_track);' in player_menu
assert 'SGLyricsOffersDidChangeNotification' in player_menu
assert TRANSLATIONS["Asking…"] == "正在查询…"
translator = (SRC / "Shared/LyricsTranslation/LyricsTranslation.m").read_text(encoding="utf-8")
assert "SGOnDeviceTranslatorRows(void)" in translator
for k in ("Apple's Translate in the lyrics' translate menu",
          "Apple Intelligence in the lyrics' translate menu",
          "Auto mix", "Auto mix in the context menu"):
    assert k in TRANSLATIONS and TRANSLATIONS[k] != k, k
assert "SGOnDeviceTranslatorRows()" in (SRC / "App/Pages.m").read_text(encoding="utf-8")
assert (ROOT / "version.txt").read_text(encoding="utf-8").strip() == "1.0.0-beta.15"
assert len(release_notes) == 7, ("beta.15 release notes unexpectedly changed", release_notes)
print("PASS: beta.15 7 release notes and new live lyrics source panel UI localized")

print(f"PASS: {checked} screenshot strings resolve exactly; 31 localized language choices, guardrail-error fallback, duplicate-case protection, dynamic templates, and raw IDs checked")
