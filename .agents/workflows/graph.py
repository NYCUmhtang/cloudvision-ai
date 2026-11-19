#!/usr/bin/env python3
"""Reproducible Wiki->evidence->outline graph, standard-library only.

Limitations: provenance/immutability checks are deterministic, NOT independent scientific review.
No AI API, external knowledge, HTML generation, or automatic source-ingestion occurs here.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
WF = ROOT/'.agents'/'workflows'
CARDS = ROOT/'cards'
RUNS = ROOT/'runs'
SOURCE_RE = re.compile(r'P0[1-5]')
WIKI_RE = re.compile(r'^wiki_id:\s*(W-M\d\d-\d\d\d)\s*$', re.M)
PAGE_RE = re.compile(r'^source_pages:\s*"([^"]+)"\s*$', re.M)
SRC_RE = re.compile(r'^source_ids:\s*\[([^]]+)\]', re.M)
SECTIONS = ('基礎說明','進階重點','文獻差異、適用條件及限制')


def utc():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def sha(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def dump(path, payload):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def parse_wiki(path):
    t=path.read_text(encoding='utf-8')
    wid=WIKI_RE.search(t); pg=PAGE_RE.search(t); sr=SRC_RE.search(t)
    if not (wid and pg and sr):
        raise ValueError('missing metadata: '+path.name)
    sources=[x.strip() for x in sr.group(1).split(',') if x.strip()]
    sections={}
    heads=list(re.finditer(r'^## (.+)$',t,re.M))
    for i,m in enumerate(heads):
        heading=m.group(1).strip()
        if heading=='來源追溯':continue
        end=heads[i+1].start() if i+1<len(heads) else len(t)
        content=t[m.end():end].strip()
        if content:sections[heading]=content
    if not sections:raise ValueError('no evidence section: '+path.name)
    title=re.search(r'^# (.+)$',t,re.M)
    return dict(wiki_id=wid.group(1),title=title.group(1) if title else wid.group(1),source_ids=sources,source_pages=pg.group(1),sections=sections,path=str(path.relative_to(ROOT)),sha256=sha(t))


def retrieve(slide, index, nodes):
    """Index-first deterministic retrieval limited to requested in-Wiki IDs.
    Score recorded for audit, never silently substitute an unrelated source.
    """
    assert '## 模組及條目' in index
    terms=set(re.findall(r'[A-Za-z0-9-]+|[\u4e00-\u9fff]{2,}',slide['query'].lower()))
    results=[]
    for wid in slide['wiki_ids']:
        if wid not in nodes: continue
        n=nodes[wid]
        body=(n['title']+' '+' '.join(n['sections'].values())).lower()
        score=sum(bool(term in body) for term in terms)
        results.append({'wiki_id':wid,'match_score':score,'title':n['title'],'source_ids':n['source_ids']})
    return results


def validate_coverage(slide,found):
    present={item['wiki_id'] for item in found}
    missing=[wid for wid in slide['wiki_ids'] if wid not in present]
    return {'passed':bool(found) and not missing,'missing_ids':missing,'retrieved':len(found)}


def make_card(slide,n,k):
    # Literal excerpts; the renderer MUST NOT invent additional research claims.
    sections=dict(n['sections'])
    return {
        'card_id':f"CARD-S{slide['number']:02d}-{k:02d}",
        'slide_number':slide['number'], 'slide_title':slide['title'],
        'teaching_objective':slide['objective'],
        'wiki_id':n['wiki_id'], 'wiki_title':n['title'], 'wiki_path':n['path'],
        'wiki_sha256':n['sha256'], 'source_ids':n['source_ids'],
        'source_pages':n['source_pages'],
        'evidence_sections':sections,
        'evidence_sha256':sha(json.dumps(sections,ensure_ascii=False,sort_keys=True)),
        'review_status':'automated_provenance_pass_only;human_scientific_review_pending'
    }


def check_card(card,n,sources_registry):
    problems=[]
    for field in ('wiki_id','wiki_path','source_ids','source_pages','evidence_sections','evidence_sha256'):
        if field not in card:problems.append('missing_field:'+field)
    if problems:return problems
    if card['wiki_id']!=n['wiki_id'] or card['wiki_path']!=n['path']:
        problems.append('incorrect_wiki_pointer')
    if card.get('wiki_sha256')!=n['sha256']:
        problems.append('wiki_content_hash_mismatch')
    if card['source_ids']!=n['source_ids'] or card['source_pages']!=n['source_pages']:
        problems.append('source_reference_mismatch')
    if card['evidence_sections']!=n['sections']:
        problems.append('evidence_not_literal_wiki_excerpt')
    if card['evidence_sha256']!=sha(json.dumps(card['evidence_sections'],ensure_ascii=False,sort_keys=True)):
        problems.append('evidence_hash_mismatch')
    for sid in n['source_ids']:
        if not re.search(r'^\| '+re.escape(sid)+r' \|.*\| ingested \|$',sources_registry,re.M):
            problems.append('source_missing_from_registry:'+sid)
    return problems


def build_outline(plan,cards):
    lines=['# CloudVision AI — Phase 3 教學大綱（證據卡草案）','','> 狀態：**待人工確認**。這不是簡報逐頁稿或 HTML。', '> 科學內容依 wiki/ 條目引用；機器檢查僅確認引用與原文一致。','']
    for slide in plan['slides']:
        c=[x for x in cards if x['slide_number']==slide['number']]
        lines += [f"## {slide['number']:02d}. {slide['title']}",f"- 教學目標：{slide['objective']}",f"- 查詢字串：{slide['query']}",f"- 對應 Wiki：{', '.join(x['wiki_id'] for x in c)}",f"- 證據卡：{', '.join(x['card_id'] for x in c)}",'- 審核狀態：待使用者確認','']
    lines += ['## 證據覆蓋規則','- 每頁至少一張證據卡，卡片必須逐字取自 Wiki 並含來源頁碼。','- 互動影像需待 Phase 4 素材授權及實際影像確認；此階段不生成示意影像或模型結果。']
    return '\n'.join(lines)+'\n'


def check_outline(plan,cards,outline):
    errors=[]
    if len(plan['slides']) not in range(8,16):errors.append('slides_outside_8_to_15')
    for s in plan['slides']:
        related=[c for c in cards if c['slide_number']==s['number']]
        if not related:errors.append(f"slide_{s['number']}_has_no_cards")
        if f"## {s['number']:02d}. {s['title']}" not in outline:errors.append('outline_missing_slide:'+str(s['number']))
        for c in related:
            if c['card_id'] not in outline:errors.append('outline_missing_card:'+c['card_id'])
    if '待人工確認' not in outline:errors.append('unapproved_outline_wrong_status')
    return errors


def run(args):
    RUNS.mkdir(exist_ok=True)
    plan=load(WF/'slide_plan.json')
    registry=(ROOT/'sources.md').read_text(encoding='utf-8')
    index=(ROOT/'wiki/index.md').read_text(encoding='utf-8')
    nodes={}
    for p in sorted((ROOT/'wiki').glob('W-M*.md')):
        n=parse_wiki(p);nodes[n['wiki_id']]=n
    log={'timestamp_utc':utc(),'run_type': 'coverage_failure_test' if args.inject_coverage_failure else ('fidelity_failure_test' if args.inject_card_failure else 'normal'),
         'graph_version':'1.0','nodes':[],'corrections':[],'source_count':len(set(s for n in nodes.values() for s in n['source_ids'])),
         'wiki_entry_count':len(nodes),'max_corrections_per_issue':3,'scope':'evidence_and_outline_only'}
    def event(node,status,details):log['nodes'].append({'node':node,'status':status,'details':details})
    event('wiki_query','PASS',{'index':'wiki/index.md','wiki_entries':len(nodes)})
    cards=[]; cover=[]; errors=[]; fallback=0; injected=False
    for slide in plan['slides']:
        if args.inject_coverage_failure and slide['number']==1:
            slide={**slide, 'wiki_ids':['W-M99-999']}
        results=retrieve(slide,index,nodes)
        gate=validate_coverage(slide,results)
        cover.append(dict(slide=slide['number'],query=slide['query'],results=results,**gate))
        if not gate['passed']:
            event('coverage_check','FAIL',{'slide':slide['number'],'missing':gate['missing_ids']})
            # Requery is permitted, but may not substitute unsupported documents.
            for attempt in range(1,4):
                fallback+=1
                results=retrieve(slide,index,nodes)
                event('requery', 'PASS' if validate_coverage(slide,results)['passed'] else 'FAIL',{'slide':slide['number'],'attempt':attempt})
                if validate_coverage(slide,results)['passed']:break
            if not validate_coverage(slide,results)['passed']:
                errors.append('INSUFFICIENT_WIKI_EVIDENCE: slide '+str(slide['number']))
                continue
        for i,result in enumerate(results,1):
            n=nodes[result['wiki_id']]
            card=make_card(slide,n,i)
            if args.inject_card_failure and not injected:
                card['source_pages']='unverified page 9999'
                injected=True
            issues=check_card(card,n,registry)
            attempts=0
            while issues and attempts<3:
                attempts+=1
                log['corrections'].append({'card_id':card['card_id'],'from':'fidelity_check','to':'evidence_cards','attempt':attempts,'issues':issues,'action':'regenerate_from_exact_wiki_entry'})
                card=make_card(slide,n,i)
                issues=check_card(card,n,registry)
            if issues:
                errors.append(card['card_id']+': '+str(issues))
                event('fidelity_check','FAIL',{'card_id':card['card_id'],'issues':issues,'corrections':attempts})
            else:
                cards.append(card)
                event('fidelity_check','PASS',{'card_id':card['card_id'],'corrections':attempts,'mode':'literal_excerpt_and_metadata'})
    event('coverage_check','PASS' if not any(not x['passed'] for x in cover) else 'FAIL',{'slides_checked':len(cover),'slides_covered':sum(x['passed'] for x in cover)})
    event('evidence_cards','PASS' if not errors else 'FAIL',{'cards_generated':len(cards)})
    # No partial publishing when a gate fails; preserve audit report.
    outline=build_outline(plan,cards)
    out_errors=check_outline(plan,cards,outline)
    errors+=out_errors
    event('outline_check','PASS' if not out_errors else 'FAIL',{'slides':len(plan['slides']),'issues':out_errors})
    log['summary']={'passed':not errors,'cards_generated':len(cards),'slides_covered':sum(c['passed'] for c in cover),'slides_total':len(plan['slides']), 'requery_attempts':fallback,'corrections':len(log['corrections']),'errors':errors,'human_review':'PENDING','html':'NOT_CREATED'}
    runid=args.run_id
    dump(RUNS/(runid+'_trace.json'),log)
    dump(RUNS/(runid+'_coverage.json'),cover)
    if not errors:
        for old in CARDS.glob('CARD-S*.json'):old.unlink()
        for card in cards:dump(CARDS/(card['card_id']+'.json'),card)
        (ROOT/'outline.md').write_text(outline,encoding='utf-8')
        event('human_outline_approval','PENDING',{'next_stage':'Phase 4 after approval'})
        dump(RUNS/(runid+'_trace.json'),log)
    print('GRAPH_RUN',runid)
    print('WIKI',len(nodes),'SOURCES',log['source_count'],'SLIDES',len(plan['slides']))
    print('COVERED',log['summary']['slides_covered'],'CARDS',len(cards),'CORRECTIONS',len(log['corrections']))
    print('RESULT:', 'PASS (automated provenance and outline)' if not errors else 'FAIL', '('+str(len(errors))+' issues)')
    print('HUMAN_REVIEW PENDING | HTML NOT CREATED')
    for er in errors: print('ERROR:',er)
    return 1 if errors else 0


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run-id',default='phase3_normal',help='fixed audit id')
    ap.add_argument('--inject-card-failure',action='store_true',help='test source-page mismatch and route to evidence regeneration')
    ap.add_argument('--inject-coverage-failure',action='store_true',help='test missing Wiki ID, three retries then stop safely')
    args=ap.parse_args()
    return run(args)
if __name__=='__main__':sys.exit(main())
