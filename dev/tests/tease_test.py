import asyncio
from playwright.async_api import async_playwright
PLACE="""(()=>{const x=__x,s=__st(); s.x=x.SX; s.z=x.SZ; let best=null; for(const i of x.navCells){const d=Math.hypot(x.cellX(i)-s.x,x.cellZ(i)-s.z); if(!best||d<best[1]) best=[i,d];}
  const d=__D[0]; d.x=x.cellX(best[0]); d.z=x.cellZ(best[0]); d.a=Math.atan2(s.z-d.z,s.x-d.x); d.mode='calm'; d.tid=null; d.irk=0; d.calmSpd=0; d.calmT=3; window.__d0=d; return +best[1].toFixed(2);})()"""
STAT="(()=>{const d=__d0; return {mode:d.mode, irk:+d.irk.toFixed(1), inZone:__x.safe[__x.idxOf(d.x,d.z)], cut:!!__cut(), dist:+Math.hypot(d.x-__st().x,d.z-__st().z).toFixed(2), alive:__D.includes(d)}})()"
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx=await b.new_context(viewport={'width':320,'height':200}); errs=[]
    pg=await ctx.new_page(); await pg.add_init_script('window.__fast=1')
    await pg.route('**/three.min.js', lambda r: r.fulfill(path='three.min.js', content_type='application/javascript'))
    await pg.route('https://fonts.googleapis.com/**', lambda r: r.abort())
    await pg.route('http://maze.test/debug.html', lambda r: r.fulfill(path='debug.html', content_type='text/html'))
    pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.goto('http://maze.test/debug.html#local', wait_until='commit', timeout=120000); await pg.wait_for_function('window.__NET !== undefined', timeout=120000); await pg.wait_for_timeout(1500)
    await pg.fill('#pname','Тест'); await pg.fill('#pcode','1111'); await pg.click('#start')
    for i in range(60):
        await pg.wait_for_timeout(250)
        if await pg.evaluate("__D.length")>0: break
    print('dino placed at', await pg.evaluate(PLACE), 'm from S')
    # 1) standing still in the zone for 12 s
    for i in range(48): await pg.wait_for_timeout(250); await pg.evaluate("(()=>{const d=__d0,s=__st(); if(d.mode==='calm'){d.a=Math.atan2(s.z-d.z,s.x-d.x); d.calmSpd=0;} })()")
    print('standing still 12 s ->', await pg.evaluate(STAT))
    # 2) teasing: stepping back and forth inside the zone
    await pg.evaluate(PLACE); t0=None; log=[]
    for i in range(80):
        await pg.keyboard.down('w' if i%2==0 else 's'); await pg.wait_for_timeout(250); await pg.keyboard.up('w' if i%2==0 else 's')
        st=await pg.evaluate(STAT)
        if i%8==0 or st['mode']=='rage' or st['cut']: log.append((round(i*.25,1),st['mode'],st['irk'],st['cut']))
        if st['cut']: break
    print('teasing ->', log[:6], '...', log[-2:])
    print('player in zone when caught:', await pg.evaluate("__x.safe[__x.idxOf(__st().x,__st().z)]"))
    for i in range(26): await pg.wait_for_timeout(250); await pg.evaluate('1')
    seq=[]
    for i in range(24):
        await pg.wait_for_timeout(250); st=await pg.evaluate(STAT)
        if i%4==0: seq.append((st['mode'],st['inZone']))
    print('after the meal (mode, inZone) each second:', seq, 'errors', errs)
    await b.close()
asyncio.run(main())
