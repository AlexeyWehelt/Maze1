import asyncio, math
from playwright.async_api import async_playwright
exec(open('mp_test3.py').read().split('info=')[0].split('srv=None')[1])
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx=await b.new_context(viewport={'width':900,'height':500}); errs=[]
    A=await newpage(ctx, errs); await login(A,'Аня','1234')
    for i in range(40):
        await A.wait_for_timeout(250)
        if await A.evaluate('__st().running && __B().finds.length>0 && __D.length>0'): break
    a0=await A.evaluate('__st().a'); print('state', await A.evaluate('[__D.length, __NET().host, __NET().on, __NET().hostKey]'))
    print('finds on map', await A.evaluate('__B().finds.map(f=>f.type).join("")'))
    # walk onto a slipper find
    r=await A.evaluate("""(()=>{const B=__B(), f=B.finds.find(f=>f.type===0), s=__st(); s.x=f.x-.3; s.z=f.z; s.a=0; for(const d of __D){const i=__x.navCells[__x.navCells.length-50]; d.x=__x.cellX(i); d.z=__x.cellZ(i);} return 1})()""")
    await A.keyboard.down('w'); await A.evaluate('__upd(12,.03)'); await A.keyboard.up('w')
    print('after walking onto slippers: charge', await A.evaluate('__B().bon.c'), 'finds', await A.evaluate('__B().finds.length'), 'toast', await A.evaluate('document.getElementById("toast").textContent'))
    # select 1, hold Ctrl 2 s
    print('visible at start/after pickup', await A.evaluate('[...document.querySelectorAll(".bon")].map(e=>!e.hidden)'), 'sel', await A.evaluate('__B().bon.sel')); await A.keyboard.press('Digit2'); print('sel after pressing 2 (no energy)', await A.evaluate('__B().bon.sel')); await A.keyboard.down('Control'); await A.evaluate('__upd(10,.03)'); print('Ctrl does nothing now:', await A.evaluate('__B().bon.c')); await A.keyboard.up('Control'); await A.keyboard.down('Shift'); await A.evaluate('__upd(67,.03)')
    print('holding Shift: on', await A.evaluate('__B().bon.on'), 'charge', await A.evaluate('__B().bon.c'), 'hud', await A.evaluate('document.querySelector(".bon.on em")?.textContent'))
    await A.keyboard.up('Shift'); await A.evaluate('__upd(30,.03)')
    await A.evaluate("__B().bon.c[0]=.2"); await A.keyboard.down('Shift'); await A.evaluate('__upd(20,.03)'); print('ran out while held: visible', await A.evaluate('[...document.querySelectorAll(".bon")].map(e=>!e.hidden)')); await A.keyboard.up('Shift')
    print('released: on', await A.evaluate('__B().bon.on'), 'charge', await A.evaluate('__B().bon.c'))
    # energy: speed check
    await A.evaluate("__B().bon.c[1]=10"); await A.keyboard.press('Digit2')
    async def run(hold):
        x0=await A.evaluate("(()=>{const s=__st(); s.x=__x.SX; s.z=__x.SZ; s.a=%r; return [s.x,s.z]})()" % a0)
        if hold: await A.keyboard.down('Shift')
        await A.keyboard.down('w'); await A.evaluate('__upd(10,.03)'); await A.keyboard.up('w')
        if hold: await A.keyboard.up('Shift')
        x1=await A.evaluate("[__st().x,__st().z]"); return math.hypot(x1[0]-x0[0],x1[1]-x0[1])
    a=await run(False); bb=await run(True); print('distance in 0.3 s: normal', round(a,3), 'energy', round(bb,3), 'ratio', round(bb/a,3))
    print('state', await A.evaluate('[__D.length, __NET().host, __NET().on, __NET().hostKey, document.hidden]'))
    # hearing: dinosaur 2.5 m behind a moving player
    HEAR="""(q)=>{const x=__x,s=__st(); let best=null; for(const i of x.navCells){ if(Math.hypot(x.cellX(i)-x.SX,x.cellZ(i)-x.SZ)<6) continue; for(const j of x.navCells){} best=i; break;}
      // find a straight corridor: player at cell i, dino 2.5 m along a free line
      for(const i of x.navCells){ const px=x.cellX(i), pz=x.cellZ(i); if(Math.hypot(px-x.SX,pz-x.SZ)<6) continue; for(let k=0;k<8;k++){ const a=k*Math.PI/4, dx=px+Math.cos(a)*2.5, dz=pz+Math.sin(a)*2.5; const j=x.idxOf(dx,dz); if(x.nav[j] && x.lineOfSight(px,pz,dx,dz)){
        s.x=px; s.z=pz; const d=__D[0]; d.x=dx; d.z=dz; d.a=a; d.mode='calm'; d.tid=null; d.calmSpd=0; d.calmT=1e9; d.hearT=0; d.irk=0; d.target=-1; for(const o of __D) if(o!==d){const c=x.navCells[x.navCells.length-50]; o.x=x.cellX(c); o.z=x.cellZ(c);}
        __B().bon.on=q?0:-1; const d0=Math.hypot(d.x-s.x,d.z-s.z); for(let t=0;t<80;t++){ __mv(true); __step(1,.05);} const tg=d.target; return [d.mode, tg<0?'no new goal':'goal '+Math.hypot(x.cellX(tg)-s.x,x.cellZ(tg)-s.z).toFixed(2)+' m from player']; } } } }"""
    print('steps heard (no slippers): ->', await A.evaluate(HEAR, False))
    print('in slippers:                ->', await A.evaluate(HEAR, True))
    await A.evaluate("__B().bon.on=-1; __B().bon.c=[20,10]; __B().bon.sel=0; (()=>{const s=__st(),f=__B().finds[0]; s.x=f.x-.6; s.z=f.z; s.a=0;})()")
    await A.evaluate('__upd(1,.03)'); await A.keyboard.down('Shift'); await A.evaluate('__upd(2,.03)'); await A.evaluate('window.__shot=1'); await A.wait_for_timeout(600); await A.evaluate('1'); await A.wait_for_timeout(300)
    await A.screenshot(path='bonus_shot.png'); await A.keyboard.up('Shift')
    print('dinos', await A.evaluate('__D.length')); print('errors', errs); await b.close()
asyncio.run(main())
