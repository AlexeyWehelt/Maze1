import asyncio,sys
from playwright.async_api import async_playwright
exec(open('mp_test3.py').read().split('info=')[0].split('srv=None')[1])
JS="""(dt)=>{const s=__st(); let mx=0, ys=new Set(); for(let i=0;i<90;i++){ __upd(1,dt); mx=Math.max(mx,__lb()); ys.add(s.y.toFixed(4)); } return [+mx.toFixed(4), [...ys].slice(0,4)]; }"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx=await b.new_context(viewport={'width':320,'height':200}); errs=[]
    A=await newpage(ctx, errs); await login(A,'Аня','1234')
    for i in range(40):
        await A.wait_for_timeout(250)
        if await A.evaluate('__st().running'): break
    for dt in [.016,.033,.05]: print('ground dt',dt, await A.evaluate(JS,dt))
    # stand on a low prop
    await A.evaluate("(()=>{for(let i=0;i<__collH.length;i++){const h=__collH[i]; if(h>.07&&h<.1&&__collH[i+1]>.07&&__collH[i-1]>.07&&__collH[i+__x.W]>.07&&__collH[i-__x.W]>.07){const s=__st(); s.x=__x.cellX(i); s.z=__x.cellZ(i); s.y=h; s.vy=0; return h;}}})()")
    for dt in [.016,.033,.05]: print('on prop dt',dt, await A.evaluate(JS,dt))
    print('errors',errs); await b.close()
asyncio.run(main())
