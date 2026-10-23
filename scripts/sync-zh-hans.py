#!/usr/bin/env python3
"""Sync the zh-Hans JSON source of truth into the compiled Objective-C dictionary.

Usage:
    python3 scripts/sync-zh-hans.py            # regenerate SGL10n.m's table
    python3 scripts/sync-zh-hans.py --check    # fail if generated table is stale

The rest of SGL10n.m (language detection and Mod-only display helpers) is preserved.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "localization" / "zh-Hans.json"
TARGET = ROOT / "tweak" / "Sources" / "Core" / "SGL10n.m"
START = "        strings = @{\n"
END = "        };"


def make_table(translations: dict[str, str]) -> str:
    q = lambda s: "@" + json.dumps(s, ensure_ascii=False)
    return START + ",\n".join(
        "            " + q(key) + ": " + q(value)
        for key, value in sorted(translations.items())
    ) + "\n" + END


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    translations = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert isinstance(translations, dict) and len(translations) > 800
    assert all(isinstance(k, str) and isinstance(v, str) and k and v
               for k, v in translations.items())
    current = TARGET.read_text(encoding="utf-8")
    assert current.count(START) == 1 and END in current[current.index(START):], "Unexpected dictionary boundaries"
    a = current.index(START)
    b = current.index(END, a) + len(END)
    updated = current[:a] + make_table(translations) + current[b:]
    if args.check:
        if updated != current:
            raise SystemExit("Localization table and JSON are out of sync. Run scripts/sync-zh-hans.py.")
        print(f"PASS: JSON and compiled dictionary match ({len(translations)} entries)")
    else:
        TARGET.write_text(updated, encoding="utf-8", newline="\n")
        print(f"Generated {TARGET} ({len(translations)} entries)")


if __name__ == "__main__":
    main()
