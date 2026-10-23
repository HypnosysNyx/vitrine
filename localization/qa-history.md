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
