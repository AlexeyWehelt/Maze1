import asyncio
from playwright.async_api import async_playwright
exec(open('mp_test3.py').read().split('info=')[0].split('srv=None')[1])
async def poll(pages, secs):
    for i in range(int(secs*4)):
        await pages[0].wait_for_timeout(250)
        for p in pages: await p.evaluate('1')
H="[__NET().host, __NET().hostKey, __D.filter(d=>!d.dead).length]"
POS="__D.map(d=>d.x.toFixed(2)+','+d.z.toFixed(2)).join(' ')"
async def moved(pg, pages):
    a=await pg.evaluate(POS); await poll(pages,3); return a!=await pg.evaluate(POS)
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx=await b.new_context(viewport={'width':320,'height':200}); errs=[]
    A=await newpage(ctx, errs); await login(A,'Аня','1234'); await poll([A],4)
    print('1 player: dinos', await A.evaluate(H))
    B=await newpage(ctx, errs); await login(B,'Борис','0007'); P=[A,B]; await poll(P,5)
    print('ticks A', await A.evaluate('__NET().tick'), 'stale on B', await B.evaluate('JSON.stringify(__NET().stale)')); await poll(P,2); print('ticks A', await A.evaluate('__NET().tick'), 'B tick', await B.evaluate('__NET().tick'))
    print('2 players: A', await A.evaluate(H), 'B', await B.evaluate(H), 'B sees motion', await moved(B,P))
    await A.evaluate("Object.defineProperty(document,'hidden',{get:()=>window.__hid,configurable:true}); window.__hid=true; document.dispatchEvent(new Event('visibilitychange'))")
    await poll([B],3)   # A's tab is 'in the background': it gets no frames
    print('A hidden: A', await A.evaluate(H), 'B', await B.evaluate(H), 'B sees motion', await moved(B,[B]))
    await A.evaluate("window.__hid=false; document.dispatchEvent(new Event('visibilitychange'))"); await poll(P,3)
    print('A back:   A', await A.evaluate(H), 'B', await B.evaluate(H), 'B sees motion', await moved(B,P))
    # A freezes without telling anyone (its world updates just stop)
    await A.evaluate("window.__sd=__NET().backend.setDinos; __NET().backend.setDinos=()=>{}"); await poll(P,8)
    print('A frozen: B', await B.evaluate(H), 'B sees motion', await moved(B,P))
    await A.evaluate("__NET().backend.setDinos=window.__sd"); await poll(P,3)
    print('A thawed: A', await A.evaluate(H), 'B', await B.evaluate(H), 'B sees motion', await moved(B,P))
    print('errors', errs); await b.close()
asyncio.run(main())
