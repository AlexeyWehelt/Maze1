import asyncio, json, sys
from playwright.async_api import async_playwright
JS = """
(async (N, minutes, hunt) => {
  const x=__x, st=__st(); st.x=x.SX; st.z=x.SZ;
  __spawn(N); const hist=new Map(), ev=[]; let offT=0, wallT=0, tot=0, caught=0;
  for (let s=0; s<minutes*60; s++) {
    if (hunt && s%6===0) { // drop the player right in front of a random dinosaur, then let it run away / get caught
      const d=__D[Math.floor(Math.random()*__D.length)]; let c=x.nearestNav(x.idxOf(d.x+Math.cos(d.a)*1.5, d.z+Math.sin(d.a)*1.5)); st.x=x.cellX(c); st.z=x.cellZ(c); }
    if (hunt && s%6===3) { const c=x.navCells[Math.floor(Math.random()*x.navCells.length)]; st.x=x.cellX(c); st.z=x.cellZ(c); }
    for (let k=0;k<20;k++){ if(hunt){ __mv(true); for(const d of __D) if(Math.hypot(d.x-st.x,d.z-st.z)<.45){ const c=x.navCells[Math.floor(Math.random()*x.navCells.length)]; st.x=x.cellX(c); st.z=x.cellZ(c); } } __step(1,.05); if(__cut()){ caught++; return {err:'cut', s}; } }
    for (const d of __D) { tot++; const i=x.idxOf(d.x,d.z); if(!x.nav[i]) offT++; if(__bits[i]) wallT++;
      let h=hist.get(d.id); if(!h){h=[];hist.set(d.id,h);} h.push([d.x,d.z]); if(h.length>25) h.shift();
      let pl=0; for(let q=1;q<h.length;q++) pl+=Math.hypot(h[q][0]-h[q-1][0],h[q][1]-h[q-1][1]); if(h.length===25 && pl<.3 && !d.dead) { ev.push({s,id:d.id,mode:d.mode,x:+d.x.toFixed(2),z:+d.z.toFixed(2),nav:x.nav[i],wall:__bits[i],safe:x.safe[i],spd:+d.spd.toFixed(2),calmSpd:+d.calmSpd.toFixed(2),stuck:+(d.stuck||0).toFixed(1),busy:d.busy}); h.length=0; } }
    if (s%10===0) await new Promise(r=>setTimeout(r,0));
  }
  return {offShare:+(offT/tot).toFixed(4), wallShare:+(wallT/tot).toFixed(4), stuckEvents:ev.length, sample:ev.slice(0,12)};
})
"""
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
    r=await pg.evaluate(f"({JS})({sys.argv[1]},{sys.argv[2]},{sys.argv[3]})")
    print(json.dumps(r,ensure_ascii=False)[:2500]); print('errors',errs[:3])
    await b.close()
asyncio.run(main())
