import asyncio
from playwright.async_api import async_playwright
exec(open('mp_test3.py').read().split('info=')[0].split('srv=None')[1])
JS="""(()=>{const x=__x, W=x.W, out=[]; const st=__st(); st.x=x.SX; st.z=x.SZ;
  // candidate bad spots: wall cells and free-but-not-walkable cells next to walkable ones, spread over the map
  const wall=[], pocket=[]; for(let i=W;i<W*(x.H-1);i++){ if(x.safe[i]) continue; const nb=[i-1,i+1,i-W,i+W]; if(__bits[i] && nb.some(n=>!__bits[n])) wall.push(i); else if(!__bits[i] && !x.nav[i]) pocket.push(i); }
  const pick=a=>a[Math.floor(Math.random()*a.length)];
  let ok=0, bad=[]; const T=40;
  for(let t=0;t<T;t++){ const d=__D[t%__D.length], c= t%2? pick(wall): pick(pocket); d.x=x.cellX(c); d.z=x.cellZ(c); d.mode='calm'; d.tid=null; d.offT=0;
    let secs=-1; for(let k=0;k<200;k++){ __step(1,.05); if(x.nav[x.idxOf(d.x,d.z)]){ secs=k*.05; break; } }
    if(secs>=0){ ok++; out.push(secs);} else bad.push([t%2?'wall':'pocket',c]); }
  out.sort((a,b)=>a-b); return {walls:wall.length, pockets:pocket.length, freed:ok+'/'+T, median:out[out.length>>1], max:out[out.length-1], bad};})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx=await b.new_context(viewport={'width':320,'height':200}); errs=[]
    A=await newpage(ctx, errs); await login(A,'Аня','1234')
    for i in range(30):
        await A.wait_for_timeout(250)
        if await A.evaluate('__D.length')>0: break
    print(await A.evaluate(JS)); print('errors',errs); await b.close()
asyncio.run(main())
