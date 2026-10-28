import asyncio
from playwright.async_api import async_playwright
src=open('mp_test3.py').read().split('info=')[0].split('srv=None')[1]
exec(src)
async def newroom(ctx, errs, room):
    pg=await ctx.new_page(); await pg.add_init_script('window.__fast=1; window.MAZE_ROOM=%r' % room)
    await pg.route('**/three.min.js', lambda r: r.fulfill(path='three.min.js', content_type='application/javascript'))
    await pg.route('https://fonts.googleapis.com/**', lambda r: r.abort())
    pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.route('http://maze.test/debug.html', lambda r: r.fulfill(path='debug.html', content_type='text/html'))
    await pg.goto('http://maze.test/debug.html#local', wait_until='commit', timeout=120000); await pg.wait_for_function('window.__NET !== undefined', timeout=120000); await pg.wait_for_timeout(1500)
    return pg
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx=await b.new_context(viewport={'width':320,'height':200}); errs=[]
    A=await newroom(ctx,errs,''); await login(A,'Аня','1234')
    B=await newroom(ctx,errs,'v2'); await login(B,'Борис','0007')
    C=await newroom(ctx,errs,'v2'); await login(C,'Вера','1111')
    for i in range(16):
        for pg in (A,B,C): await pg.evaluate('1')
        await A.wait_for_timeout(250)
    for n,pg in (('A main',A),('B v2',B),('C v2',C)): print(n,'sees', await pg.evaluate("Object.keys(__NET().players)"), 'host', await pg.evaluate("__NET().host"), 'dinos', await pg.evaluate("__D.filter(d=>!d.dead).length"))
    print('errors',errs); await b.close()
asyncio.run(main())
