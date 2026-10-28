import asyncio, math
from playwright.async_api import async_playwright
exec(open('mp_test3.py').read().split('info=')[0].split('srv=None')[1])
async def poll(pages, secs):
    for i in range(int(secs*4)):
        await pages[0].wait_for_timeout(250)
        for p in pages: await p.evaluate('1')
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx=await b.new_context(viewport={'width':1000,'height':640}); errs=[]
    A=await newpage(ctx, errs); await login(A,'Аня','1234'); await poll([A],3)
    ex=[]
    for k in range(6):
        ex.append(await A.evaluate("[+__x.EX.toFixed(2), +__x.EZ.toFixed(2), +Math.hypot(__x.EX-__x.SX,__x.EZ-__x.SZ).toFixed(1)]"))
        await A.keyboard.press('r'); await A.wait_for_timeout(150)
    print('exits (x, z, straight-line m from S):', ex, '| original', await A.evaluate("[+(__x.EX).toFixed(2)]"))
    print('marker at exit:', await A.evaluate("(()=>{let g=null; return 1})()"))
    # finish
    await A.evaluate("(()=>{const s=__st(); s.x=__x.EX; s.z=__x.EZ; s.t=75;})()"); await poll([A],1.5)
    print('won', await A.evaluate('__st().won'), '|', await A.evaluate('document.getElementById("winPts").textContent'), '| hud pts', await A.evaluate('document.getElementById("pts").textContent'))
    await A.click('#winShop'); await A.wait_for_timeout(1200)
    await A.screenshot(path='shop_shot.png')
    await A.click('text=Ковбойская шляпа'); await A.wait_for_timeout(300)
    print('try hat 180:', await A.evaluate('document.getElementById("shopMsg").textContent'))
    await A.click('text=Кепка'); await A.wait_for_timeout(300)
    await A.click('text=Голубые'); await A.wait_for_timeout(300)
    print('after buying cap+blue eyes:', await A.evaluate('document.getElementById("shopMsg").textContent'), await A.evaluate('document.getElementById("shopPts").textContent'))
    await A.wait_for_timeout(800); await A.screenshot(path='shop_shot2.png')
    print('stored:', await A.evaluate('JSON.stringify(JSON.parse(localStorage.getItem("sticker-maze-users"))["аня"])'))
    await A.click('#shopClose'); await A.click('#again'); await poll([A],1)
    B=await newpage(ctx, errs); await login(B,'Борис','0007'); await poll([A,B],5)
    print('B sees Аня wearing', await B.evaluate('__NET().players["аня"] && __NET().players["аня"].av.wear'), '| B knows A exit', await B.evaluate('[__NET().players["аня"].ex, __NET().players["аня"].ez]'), 'A exit', await A.evaluate('[__x.EX,__x.EZ]'))
    # B finishes and goes again: a dinosaur must appear at B's NEW exit (seen by A, the host)
    await B.evaluate("(()=>{const s=__st(); s.x=__x.EX; s.z=__x.EZ;})()"); await poll([A,B],2)
    await B.click('#again'); await poll([A,B],1.5)
    bex=await B.evaluate('[__x.EX,__x.EZ]')
    print('dino near B new exit (on A):', await A.evaluate('(e)=>__D.some(d=>!d.dead&&Math.hypot(d.x-e[0],d.z-e[1])<1)', bex))
    print('errors', errs); await b.close()
asyncio.run(main())
