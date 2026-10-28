import asyncio,sys
from playwright.async_api import async_playwright
MODE=sys.argv[1]   # escape | bait | baitpin | still
PLACE="""(()=>{const x=__x,s=__st(); s.x=x.SX; s.z=x.SZ; let best=null; for(const i of x.navCells){const dd=Math.hypot(x.cellX(i)-s.x,x.cellZ(i)-s.z); if(dd>2.8&&dd<3.3&&x.lineOfSight(s.x,s.z,x.cellX(i),x.cellZ(i))){ best=[i,dd]; break; } }
  const d=__D[0]; d.x=x.cellX(best[0]); d.z=x.cellZ(best[0]); s.a=Math.atan2(d.z-s.z,d.x-s.x); window.__a0=s.a; d.a=s.a+Math.PI; d.mode='calm'; d.tid=null; d.irk=0; d.calmSpd=0; d.calmT=3; window.__d0=d; window.__p0=[d.x,d.z]; for(const o of __D) if(o!==d){ const i=x.navCells[x.navCells.length-50]; o.x=x.cellX(i); o.z=x.cellZ(i); } return +best[1].toFixed(2);})()"""
STAT="(()=>{const d=__d0,s=__st(); return {m:d.mode, irk:+d.irk.toFixed(1), al:+d.alertT.toFixed(1), want:+d.baited, lost:+(d.lost||0).toFixed(1), safe:__x.safe[__x.idxOf(s.x,s.z)], cut:!!__cut(), dP:+Math.hypot(d.x-s.x,d.z-s.z).toFixed(2), dS:+Math.hypot(d.x-__x.SX,d.z-__x.SZ).toFixed(2)}})()"
PIN="(()=>{const d=__d0,s=__st(); if(d.mode==='calm'){d.x=__p0[0]; d.z=__p0[1]; d.a=Math.atan2(s.z-d.z,s.x-d.x); d.calmSpd=0; d.spd=0; d.calmT=1e9;} })()"
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
    print('dino', await pg.evaluate(PLACE), 'm from S')
    pin = MODE=='baitpin'
    async def tick(n):
        st=None
        for i in range(n):
            await pg.wait_for_timeout(250)
            if pin: await pg.evaluate(PIN)
            st=await pg.evaluate(STAT)
            if st['cut']: break
        return st
    async def out(force_chase=False):
        # face the dinosaur and walk out until it has noticed (alert) or 1.6 s passed
        await pg.evaluate("(()=>{const d=__d0,s=__st(); s.a=Math.atan2(d.z-s.z,d.x-s.x); if(d.mode==='calm') d.a=s.a+Math.PI;})()")
        await pg.keyboard.down('w'); st=None
        for i in range(8):
            st=await tick(1)
            if st['safe']==0 and st['m']!='calm' and i>=3: break
        if force_chase: await pg.evaluate("if(__d0.mode==='alert')__d0.alertT=2"); st=await tick(1)
        await pg.keyboard.up('w'); return st
    async def home():
        # run back to S
        await pg.evaluate("(()=>{const s=__st(); s.a=Math.atan2(__x.SZ-s.z,__x.SX-s.x)})()")
        await pg.keyboard.down('w'); st=None
        for i in range(10):
            st=await tick(1)
            if Math_h(await pg.evaluate("Math.hypot(__st().x-__x.SX,__st().z-__x.SZ)"))<.35: break
        await pg.keyboard.up('w'); return await pg.evaluate(STAT)
    def Math_h(v): return v
    if MODE=='escape':
        print(' out ', await out(True)); print(' home', await home())
        for k in range(15): print(f'  +{2*k+2}s', await tick(8))
    elif MODE=='still':
        for k in range(8): print(f'  +{2*k+2}s', await tick(8))
    else:
        for n in range(9):
            a=await out(n%2==1); h=await home(); print(f' {n+1}: out', a, '\n    home', h)
            if h['cut']: break
            r=await tick(6); print('    rest', r)
            if r['cut']: break
    print('player safe:', await pg.evaluate("__x.safe[__x.idxOf(__st().x,__st().z)]"), 'errors', errs)
    await b.close()
asyncio.run(main())
