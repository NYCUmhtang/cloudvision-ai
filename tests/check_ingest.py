"""Static Wiki ingest lint. Verifies presence/links/source IDs/file hashes; not semantic fidelity."""
from pathlib import Path
import re,hashlib,sys
R=Path(__file__).resolve().parents[1]
def main():
 errors=[]; registry=(R/'sources.md').read_text(encoding='utf8');idx=(R/'wiki/index.md').read_text(encoding='utf8')
 sids=('P01','P02','P03','P04','P05');files=list((R/'wiki').glob('W-*.md'));ids=[]
 for sid in sids:
  if not re.search(r'^\| '+sid+r' \|.*\| ingested \|$',registry,re.M):errors.append('source not ingested: '+sid)
  pdfs=list((R/'raw').glob(sid+'_*.pdf'))
  if len(pdfs)!=1:errors.append('wrong pdf count: '+sid);continue
  digest=hashlib.sha256(pdfs[0].read_bytes()).hexdigest()
  if digest not in registry:errors.append('SHA256 missing/mismatch '+sid)
  print('SOURCE',sid,'PDF hash', 'PASS' if digest in registry else 'FAIL')
 for path in files:
  c=path.read_text(encoding='utf8');m=re.search(r'^wiki_id: (W-[A-Z0-9-]+)$',c,re.M)
  if not m:errors.append('missing ID '+path.name);continue
  wid=m.group(1);ids.append(wid)
  if path.name!=wid+'.md':errors.append('filename mismatch '+wid)
  if f'({path.name})' not in idx:errors.append('not indexed '+wid)
  sm=re.search(r'^source_ids: \[(.*?)\]$',c,re.M)
  if not sm:errors.append('missing source IDs '+wid);continue
  for sid in (x.strip() for x in sm.group(1).split(',')):
   if sid not in sids:errors.append('unknown source '+sid+' in '+wid)
   if not re.search(r'\b'+sid+r'\b',c):errors.append('unreferenced source '+sid+' in '+wid)
  if not re.search(r'PDF pp?\.',c):errors.append('missing PDF page evidence '+wid)
 if len(ids)!=len(set(ids)):errors.append('duplicate IDs')
 if len(files)<15:errors.append('too few wiki entries')
 print('WIKI_ENTRIES',len(files),'UNIQUE_IDS',len(set(ids)))
 print('RESULT:', 'PASS' if not errors else 'FAIL',f'({len(errors)} issues)')
 for e in errors:print('ERROR:',e)
 return int(bool(errors))
if __name__=='__main__':sys.exit(main())
