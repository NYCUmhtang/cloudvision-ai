#!/usr/bin/env python3
"""Phase 5 deployment readiness: file parity, source traceability and package hygiene."""
from pathlib import Path
import json, hashlib, re, sys
root=Path(__file__).resolve().parents[1]
issues=[]
def check(cond, msg):
    if not cond: issues.append(msg)
html=(root/'index.html').read_bytes(); deck=(root/'deck.html').read_bytes()
check(html==deck, 'index.html and deck.html differ')
check(b'<html' in html.lower(), 'missing html tag')
d=json.loads((root/'assets/slide_content.json').read_text(encoding='utf-8'))
check(len(d['slides'])==12, 'expected 12 slides')
check(len(list((root/'cards').glob('CARD-S*.json')))==26, 'expected 26 evidence cards')
for s in d['slides']:
    check(bool(s.get('cards')), f"slide {s['number']} has no evidence card")
    for w in s['wiki_ids']:
        check((root/'wiki'/f'{w}.md').exists(),f'unknown wiki ID {w}')
for sid in ('P01','P02','P03','P04','P05'):
    check(sid in d['sources'],f'missing source {sid}')
check((root/'SUBMISSION.md').is_file(),'missing submission instructions')
check((root/'DEPLOY_GITHUB_PAGES.md').is_file(),'missing deployment guide')
print(f'Phase5 slides={len(d["slides"])} cards={len(list((root/"cards").glob("CARD-S*.json")))} sources={len(d["sources"])}')
print(f'RESULT: {"PASS" if not issues else "FAIL"} ({len(issues)} issues)')
for issue in issues:print('ISSUE:',issue)
sys.exit(bool(issues))
