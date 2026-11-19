"""Check generated Phase 3 cards against current Wiki, registry, and outline."""
from pathlib import Path
import importlib.util, json, sys
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('graph', R/'.agents/workflows/graph.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def main():
    errors=[]; plan=g.load(R/'.agents/workflows/slide_plan.json')
    registry=(R/'sources.md').read_text(encoding='utf-8')
    cards=[g.load(p) for p in sorted((R/'cards').glob('CARD-S*.json'))]
    nodes={g.parse_wiki(p)['wiki_id']:g.parse_wiki(p) for p in (R/'wiki').glob('W-M*.md')}
    for card in cards:
        wid=card.get('wiki_id')
        if wid not in nodes:errors.append('unknown wiki: '+str(wid));continue
        errors += [card.get('card_id','?')+': '+x for x in g.check_card(card,nodes[wid],registry)]
    if not (R/'outline.md').exists(): errors.append('missing outline')
    else:errors+=g.check_outline(plan,cards,(R/'outline.md').read_text(encoding='utf-8'))
    if len(cards)<19:errors.append('too few evidence cards')
    print('CARDS',len(cards),'SLIDES',len(plan['slides']))
    print('RESULT:', 'PASS' if not errors else 'FAIL',f'({len(errors)} issues)')
    for e in errors: print('ERROR:',e)
    return int(bool(errors))
if __name__=='__main__':sys.exit(main())
