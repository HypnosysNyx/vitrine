# Vitrine zh-Hans: regression and root-cause history

Purpose: Every screenshot regression must identify a root cause, fix the visible render path, and add a permanent check. Keep this record usable as source material for a future reusable Mod-localization Skill.

## Rules for all rounds

- Scope is **Vitrine-owned interfaces**, including third-party names or descriptions **shown inside Mod selectors** (use English plus Chinese description where needed). Do not alter native Spotify/iOS screens, Apple-owned UI, original IDs, font family names, hardware device names, AutoEq paths or saved selectors.
- First review previous screenshots and open issues, then inspect new screenshots. The acceptance criterion is the **rendered UI**, not the number of dictionary entries.
- For every missed literal, inspect its actual path from producer to renderer, including dynamically formatted strings, Swift-originated error text, composed status labels, and attributed text.
- Add coverage assertions for the **exact string key and its call site**. Tests cannot claim on-device verification.
- Keep `i18n/zh-hans` isolated from `main`; verify CI compile before making a new IPA and run a separate on-device acceptance pass.

## Feedback batch 4 — 2026-10-23

| Screenshot | Observed missing Chinese | Root cause | Code correction | Permanent check |
|---|---|---|---|---|
| IMG_1820 | Karaoke title, model-download message, and OK button; card status | The card's alert bypassed `SGT`; missing-model text was formatted before lookup; the status had `ⓘ` appended before translation | Translate title/actions in `SGSingCard.m`, localize format templates in `Sing.x` before substitution, and translate the base status before decorating it | `scripts/check-zh-hans-coverage.py`: exact model key and alert/status display call sites |
| IMG_1821 | `After 5 s` and Spatial voice settings footer | Dynamic slider formatter had no translation lookup, and entire footer was absent from catalog | Format with `SGT(@"After %.0f s")` and add exact full footer to catalog | Exact source-key checks for slider and footer; placeholder verification |
| IMG_1822 | Apple Intelligence: `The model refused to answer.` in a Vitrine alert | Previous patch only handled one partial-translation template, but other Swift-generated error forms still reached the alert without localization | Localize known Swift error wrappers and reasons at the Mod alert boundary; preserve unknown OS reasons as explicitly labelled original diagnostics | Exact error wrapper/known reason keys and `localizedTranslationError` call-path check |

**Pre-install status:** static checks and CI compilation are separate from on-device verification. Do not label any batch 'fully fixed on device' before installing the matching SHA build and confirming the same pages.

**Recurrence prevention:** This batch checks previous exact screenshot assertions as well as new call paths. A future occurrence of the same issue should become a failing check rather than another untracked screenshot.

## Follow-up: voice-model download confirmation — 2026-10-23

- **Observed:** Vitrine Karaoke's “下载人声模型？” alert had localized title and buttons, but its body still read “210.4 MB from Hugging Face. It waits for Wi-Fi ...”.
- **Root cause:** `Shared/Sing/SingSettings.m` composed a localized-looking alert from **untranslated fragments**. It passed a `stringWithFormat:` result with a concrete model size to `SGT(message)`, which cannot match the catalog's placeholder-based keys.
- **Fix:** Translate the main format **before insertion** and likewise translate optional download failure text, model update notice, device compatibility footnotes, cellular data prompt, partially downloaded progress, and removal confirmation. Do not touch model download choices, network behavior, device IDs, or the source brand “Hugging Face”.
- **Regression prevention:** The screenshot-coverage test now checks these exact template keys **and** their `SGT` call sites, and ensures no substantial untranslated English literal remains in the Mod Karaoke settings source.
- **Additional testing failure discovered:** The Python `CASES` dictionary had **two** `Shared/Sing/SingSettings.m` entries. The later one silently overwrote the earlier one, so the previously reported pass count excluded some tests. They are now merged, and the test uses Python's AST to fail when a duplicate `CASES` group is introduced.
- **Acceptance:** Only static assertions and successful macOS compilation are evidence of source correctness; re-test on a phone using the build from the exact new commit to verify rendered text.


## Follow-up: iOS 27 guardrail error and target-language list — 2026-10-23

| UI / feedback | Root cause | Fix | Permanent acceptance |
|---|---|---|---|
| Vitrine player: Apple Intelligence translation error displays “The model's safety guardrails were triggered.” after a Chinese prefix | The Mod's error wrapper translated the known prefix, but deliberately appended unfamiliar OS NSError descriptions as raw English; the Swift error enum also does not identify all iOS 27 bridge forms | In the **Vitrine alert only**, recognize the precise safety guardrail reason in the catalog. For unrecognized OS messages display a generic Chinese explanation and retain the original in diagnostic logs, rather than showing raw English. Swift classifies recognizable guardrail descriptions into the existing safe failure case; translation/safety policy is unchanged | Guardrail screenshot exact key and text; assert all known wrapper/fallback paths are Chinese, partial-translation counts stay specific, and non-Chinese UI still uses original errors |
| Vitrine > Lyrics > Translation language lists Arabic, Chinese, etc. in English | \`SGLyricsTranslationLanguageNames()\` always constructed English labels from the fixed \`NSLocale("en")\`, bypassing the rest of the Mod's localization | When the existing Mod language detector selects Simplified Chinese, use \`NSLocale("zh-Hans")\` for language **display names** and explicitly show \`简体中文\` / \`繁体中文\`; keep 31 original BCP-47 language tags, their order, selection index, translation requests and non-Chinese display logic unchanged | Assert all 31 raw tags and their order are unchanged; inspect the actual Vitrine picker display method and index persistence. Final visual verification needs the IPA of the matching commit |

**Avoid repeating:** Dynamic text, locale-derived labels and OS-provided errors are not necessarily literal strings in source files. Pure literal scans and dictionaries cannot prove they are localized; inspect each **producer-to-renderer** path and require a targeted render-path assertion. Never conflate static QA/CI success with on-device acceptance.

## Upstream beta.14 synchronization — 2026-10-24

- **Upstream source:** My-Name-Is-Jeff/vitrine at `f5473f76958b22232f6034443b4af84107729dbb` (beta.14 plus its latest commit on 2026-10-23).
- **Previously localized source:** HypnosysNyx/vitrine `i18n/zh-hans` at `98aca931d12a604f9fab5742dab5a4ddc662d7b5`.
- **Merge:** Seven file-level textual conflicts reviewed and resolved; retained upstream behavior for its revised AI translator, saved translations, lyrics settings, redesigned navbar and karaoke translation menu while preserving localized UI calls.
- **Translation updates:** Catalog increased from 1,058 to 1,074 entries. Localized new Keychain clearing confirmations, split-tab accessibility labels, word-level timing option, API key/model prompts and AI translation settings. Regenerated `Core/SGL10n.m`.
- **Verified locally:** `sync-zh-hans.py --check`, `check-zh-hans-coverage.py` (52 screenshot cases), `check-zh-hans-placeholders.py`, `audit-mod-ui-literals.py` (297 files), `check-layers.sh`, and `git diff --check`.
- **macOS compilation:** PR head `95e44c5` passed [macOS workflow run 39991312030](https://github.com/HypnosysNyx/vitrine/actions/runs/39991312030): localization checks, Xcode setup, appearance/settings harnesses and tweak compile/link all succeeded. PR #1 was merged at `c217a3f` on 2026-10-24. This step did **not** generate an IPA.
- **Still not verified:** Installation of a build from the merged code on a real iPhone or screenshot-based visual acceptance. Do not present this as a device-tested IPA release.


## Screenshot: beta.14 What's New sheet entirely English — 2026-10-24

- **Observed on iPhone:** The first-run sheet displayed “What's New in Vitrine”, “Version 1.0.0-beta.14”, “Features”, all release descriptions (e.g. AI DJ, Automatic lyric source, AutoMix) and “Continue” in English despite Simplified Chinese locale.
- **Root cause:** `App/Onboarding/WhatsNew.m` formatted fixed labels without `SGT` and passed `SGUpdateChangesIn(SGWhatsNewNotes)` strings directly from the generated `CHANGELOG.md` header to the UI, bypassing the translation dictionary. `scripts/audit-mod-ui-literals.py` missed the dynamically sourced text, and screenshot QA did not assert this renderer.
- **Fix:** Translate UI literals and the original changelog text at the display boundary before optional first-character capitalization, while keeping the source markdown, links, kinds and update-seen preference keys unchanged. Added Chinese entries for all 64 release-note lines in beta.14 and used the same translated presentation in Mod's update page and notice.
- **Permanent regression:** `scripts/check-zh-hans-coverage.py` now asserts the What's New title, version format, category heading, Continue button, row renderer, and parsing of the exact current-version notes from `CHANGELOG.md`; missing translations for newly released notes must fail CI, rather than silently shipping English.
- **Not yet verified:** matching-SHA IPA build and device screenshot; source/tests alone do not establish visual acceptance. Reinstalling a corrected build with the same version does not automatically reopen a sheet already marked seen.
