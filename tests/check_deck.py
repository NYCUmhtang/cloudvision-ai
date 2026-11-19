#!/usr/bin/env python3
"""Validate Phase 4 source mappings, drafts and local deck structure (not independent peer review)."""
from pathlib import Path
import json,re,sys
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Scan(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.scripts=[];self.open_scripts=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.add(d['id'])
        if tag=='script':self.scripts.append(d)

def validate():
    errors=[];f=ROOT/'deck.html'
    if not f.exists():return ['deck.html missing']
    text=f.read_text(encoding='utf-8');parser=Scan();parser.feed(text)
    for i in ['previous','next','references','sourcesDialog','demoTabs' if False else 'mainSlide','pageInfo','progressValue','deck-data']:
        if i not in parser.ids:errors.append('missing_element:'+i)
    match=re.search(r'<script id="deck-data" type="application/json">(.*?)</script>',text,re.S)
    if not match:return errors+['embedded json missing']
    try:data=json.loads(match.group(1))
    except Exception as e:return errors+['embedded json parse error:'+str(e)]
    if not 8<=len(data['slides'])<=15: errors.append('invalid slide count')
    index=(ROOT/'wiki/index.md').read_text(encoding='utf-8')
    cards=list((ROOT/'cards').glob('CARD-S*.json'))
    if len(cards)!=26:errors.append('expected 26 original evidence cards')
    if len(data['sources'])!=5: errors.append('expected five registered sources')
    for s in data['slides']:
        n=s['number'];draft=ROOT/'drafts'/f'slide_{n:02d}.md'
        if not draft.exists():errors.append(f'missing_draft:{n}');continue
        contents=draft.read_text(encoding='utf-8')
        if s['headline'] not in contents:errors.append(f'draft_headline_mismatch:{n}')
        if s['lead'] not in contents:errors.append(f'draft_lead_mismatch:{n}')
        if any(b not in contents for b in s['bullets']):errors.append(f'draft_bullets_mismatch:{n}')
        if len(s['cards'])!=len(s['wiki_ids']) or not s['cards']:errors.append(f'coverage_error:{n}')
        for card in s['cards']:
            wid=card['wiki_id'];src=card['source_ids']
            if wid not in index:errors.append('wiki_missing_index:'+wid)
            if not (ROOT/card['wiki_path']).exists():errors.append('wiki_path_missing:'+wid)
            for sid in src:
                if sid not in data['sources']:errors.append('source_url_missing:'+sid)
            if card['card_id'] not in contents:errors.append('draft_card_missing:'+card['card_id'])
    for feature in ['classificationSvg','ArrowRight','ArrowLeft','showModal()','aria-pressed','CloudS2Mask','人工繪製']:
        if feature not in text:errors.append('missing_feature:'+feature)
    return errors
if __name__=='__main__':
    problems=validate();print('RESULT:', 'PASS' if not problems else 'FAIL',f'({len(problems)} issues)')
    for p in problems:print(' -',p)
    sys.exit(bool(problems))
