import asyncio, os, subprocess, time
from playwright.async_api import async_playwright
srv=None
async def newpage(ctx, errs):
    pg=await ctx.new_page()
    await pg.add_init_script('window.__fast=1')
    await pg.route('**/three.min.js', lambda r: r.fulfill(path='three.min.js', content_type='application/javascript'))
    await pg.route('https://fonts.googleapis.com/**', lambda r: r.abort())
    pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.route('http://maze.test/debug.html', lambda r: r.fulfill(path='debug.html', content_type='text/html'))
    await pg.goto('http://maze.test/debug.html#local', wait_until='commit', timeout=120000); await pg.wait_for_function('window.__NET !== undefined', timeout=120000); await pg.wait_for_timeout(1500)
    return pg
async def login(pg, name, code):
    await pg.fill('#pname', name); await pg.fill('#pcode', code); await pg.click('#start'); await pg.wait_for_timeout(1500)
    return await pg.evaluate("document.getElementById('loginMsg').textContent + '|' + document.getElementById('intro').hidden")
info="(()=>{const n=__NET(); return {on:n.on, host:n.host, me:n.me, others:Object.keys(n.players), dinos:__D.map(d=>d.id+':'+d.mode+(d.dead?':dead':'')), online:document.getElementById('online').textContent}})()"
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx=await b.new_context(viewport={'width':320,'height':200}); errs=[]
    A=await newpage(ctx, errs); await login(A,'Аня','1234'); await A.wait_for_timeout(4000)
    print('1 player dinos', await A.evaluate("__D.filter(d=>!d.dead).length"))
    B=await newpage(ctx, errs); await login(B,'Борис','0007'); await A.wait_for_timeout(5000)
    print('2 players dinos', await A.evaluate("__D.filter(d=>!d.dead).length"), 'B sees', await B.evaluate("__D.length"))
    pos="__D.map(d=>d.id+':'+(Math.hypot(d.x-__x.EX,d.z-__x.EZ)<2.5?'E':'-')).join(' ')"
    # keep dinosaurs away from E first
    print('before', await A.evaluate(pos))
    # B (not the host) reaches the exit, then goes again
    await B.evaluate("(()=>{const s=__st(); s.x=__x.EX; s.z=__x.EZ;})()"); await B.wait_for_timeout(2500)
    print('B won', await B.evaluate("__st().won"), 'A sees B state', await A.evaluate("Object.values(__NET().players)[0].s"), 'top', await B.evaluate("document.getElementById('top').textContent"))
    far=await A.evaluate("(()=>{for(const d of __D){ if(Math.hypot(d.x-__x.EX,d.z-__x.EZ)<3){ const i=__x.navCells[5000]; d.x=__x.cellX(i); d.z=__x.cellZ(i);} } return 1})()")
    await A.wait_for_timeout(800); print('moved away', await A.evaluate(pos))
    await B.click('#again'); await A.wait_for_timeout(1200)
    print('after B again', await A.evaluate(pos), '| B sees', await B.evaluate(pos), '| count', await A.evaluate("__D.filter(d=>!d.dead).length"))
    await A.wait_for_timeout(15000); print('15 s later', await A.evaluate(pos), 'homes', await A.evaluate("__D.map(d=>d.home).join(',')"))
    print('errors', errs)
    await b.close()
asyncio.run(main())
