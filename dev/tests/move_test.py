import asyncio
from playwright.async_api import async_playwright
exec(open('mp_test3.py').read().split('info=')[0].split('srv=None')[1])
FIND="""([lo,hi])=>{const x=__x,W=x.W; for(let i=W*5;i<W*(x.H-5);i++){ const h=__collH[i]; if(!(h>lo&&h<=hi)) continue;
  // a straight free approach of 0.5 m from the west, cells there empty
  let ok=true; for(let k=1;k<=5;k++){ const j=i-k; if(__collH[j]!==0||__bits[j]){ok=false;break;} for(const o of [-W,W]) if(__bits[j+o]){ok=false;break;} if(!ok)break; } if(!ok) continue;
  const s=__st(); s.x=x.cellX(i-5); s.z=x.cellZ(i); s.a=0; s.y=0; s.vy=0; window.__pk=i; window.__trace=[]; return +h.toFixed(3); } return null; }"""
SAMPLE="(()=>{const s=__st(); __trace.push([+s.x.toFixed(3),+s.y.toFixed(3),+s.vy.toFixed(2),s.ground]); return 1})()"
async def run(A,lo,hi):
    h=await A.evaluate(FIND,[lo,hi]); await A.keyboard.down('w')
    for i in range(30): await A.evaluate('__upd(1,.03)'); await A.evaluate(SAMPLE)
    await A.keyboard.up('w'); tr=await A.evaluate('__trace')
    print(f'prop h={h}: max vy', max(t[2] for t in tr), 'max y', max(t[1] for t in tr), 'x from', tr[0][0], 'to', tr[-1][0], 'prop at x', await A.evaluate('__x.cellX(__pk)'))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx=await b.new_context(viewport={'width':320,'height':200}); errs=[]
    A=await newpage(ctx, errs); await login(A,'Аня','1234')
    for i in range(40):
        await A.wait_for_timeout(250)
        if await A.evaluate('__st().running'): break
    print('running', await A.evaluate('__st().running'))
    await A.evaluate("(()=>{const s=__st(),x=__x; s.x=x.SX; s.z=x.SZ; for(const d of __D){const i=x.navCells[x.navCells.length-50]; d.x=x.cellX(i); d.z=x.cellZ(i);}})()")
    a0=await A.evaluate("[__st().x,__st().z,__st().a]")
    t0=await A.evaluate('__st().t'); await A.wait_for_timeout(1000); await A.evaluate('1'); print('t advance', await A.evaluate('__st().t')-t0, await A.evaluate('[__st().x,__st().z,__st().a,__x.SX,__x.SZ]')); print('active', await A.evaluate('document.activeElement.tagName')); await A.evaluate('document.activeElement.blur()')
    for key in ['w','d','ArrowLeft']:
        a0=await A.evaluate("[__st().x,__st().z,__st().a]"); await A.keyboard.down(key)
        await A.evaluate('__upd(10,.03)')
        await A.keyboard.up(key); a1=await A.evaluate("[__st().x,__st().z,__st().a]")
        import math
        dx,dz=a1[0]-a0[0],a1[1]-a0[1]; fwd=dx*math.cos(a0[2])+dz*math.sin(a0[2]); side=-dx*math.sin(a0[2])+dz*math.cos(a0[2])
        print(key,'forward',round(fwd,3),'side',round(side,3),'turned',round(a1[2]-a0[2],3))
    await run(A,.06,.1); await run(A,.18,.22)
    print('errors',errs); await b.close()
asyncio.run(main())
