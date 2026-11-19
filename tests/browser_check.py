"""Actual Chromium browser smoke/layout tests for the Phase 4 interactive deck."""
from pathlib import Path
import json,datetime,sys,threading,functools
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
results=[]
server=ThreadingHTTPServer(("127.0.0.1",0),functools.partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f"http://127.0.0.1:{server.server_port}/deck.html"
def check(name,condition,extra=None):results.append({'test':name,'passed':bool(condition),'detail':extra or ''})
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width,height in [(1440,900),(390,844)]:
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
        page.set_content((ROOT/'deck.html').read_text(encoding='utf-8'),wait_until='load')
        check(f'initial slide {width}',page.locator('#heading').inner_text()=='先看懂衛星影像中的雲與陰影')
        check(f'no JS error {width}',len(errors)==0,str(errors))
        dims=page.evaluate('''() => ({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth})''')
        check(f'no horizontal overflow {width}',dims['scroll']<=dims['client'],str(dims))
        page.locator('#next').click();check(f'next button {width}',page.locator('#pageInfo').inner_text().startswith('02'))
        page.locator('#previous').click();check(f'previous button {width}',page.locator('#pageInfo').inner_text().startswith('01'))
        page.locator('#references').click();check(f'sources modal {width}',page.locator('#sourcesDialog').evaluate('(el)=>el.open'))
        check(f'doi link {width}',page.locator('#sourcesDialog a[href^="https://doi.org/"]').count()>0)
        page.locator('#closeDialog').click()
        # Click through all pages and check overflow in each viewport
        max_over=0
        for i in range(1,13):
            page.evaluate('(n)=>{document.getElementById("previous").disabled=false;}',i) if False else None
            if i>1: page.locator('#next').click()
            height_check=page.evaluate('''() => {const e=document.querySelector('.slide');return {scroll:e.scrollWidth, client:e.clientWidth}}''')
            max_over=max(max_over,height_check['scroll']-height_check['client'])
            check(f'slide {i:02d} heading {width}',bool(page.locator('#heading').inner_text()))
        check(f'12-slide horizontal layout {width}',max_over<=0,f'max={max_over}')
        check(f'last slide next disabled {width}',page.locator('#next').is_disabled())
        for i in range(2):page.locator('#previous').click()
        # go to page ten (from page 10) and switch demo modes
        check(f'slide ten reached {width}',page.locator('#pageInfo').inner_text().startswith('10'))
        page.locator('button[data-mode="multiclass"]').click()
        check(f'interactive mask {width}','四類遮罩示意' in page.locator('#scene').inner_text())
        page.screenshot(path=str(ROOT/'runs'/f'phase4_browser_{width}.png'),full_page=True)
        page.close()
    browser.close()
server.shutdown()
report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':all(x['passed'] for x in results),'tests':results}
(ROOT/'runs'/'phase4_browser_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('BROWSER:', 'PASS' if report['passed'] else 'FAIL',sum(x['passed'] for x in results),'/',len(results))
for x in results:
    if not x['passed']:print('FAILED',x)
sys.exit(not report['passed'])
