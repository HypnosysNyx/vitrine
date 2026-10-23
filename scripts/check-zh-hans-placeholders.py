#!/usr/bin/env python3
"""Validate printf placeholders in localization keys and translated formats.

Only actual %-specifiers count; normal percent signs in static notes are ignored.
"""
import json
import re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
cat=json.loads((root/"localization/zh-Hans.json").read_text(encoding="utf-8"))
pattern=re.compile(r'%(?:\d+\$)?[-+#0]*(?:\d+)?(?:\.\d+)?(?:hh|ll|[hlLzjt])?[diuoxXfFeEgGaAcCsSp@%]')
bad=[]
n=0
for k,v in cat.items():
  a=[x for x in pattern.findall(k) if x!='%%']
  b=[x for x in pattern.findall(v) if x!='%%']
  if a or b:
    n+=1
    if a!=b:bad.append((k,a,v,b))
print('Dynamic localization entries:',n)
for x in bad[:25]:print('MISMATCH',repr(x).encode('ascii','backslashreplace').decode()[:1200])
if bad:raise SystemExit('ERROR: %d format mismatches' % len(bad))
print('PASS: no placeholder differences across',len(cat),'entries')
