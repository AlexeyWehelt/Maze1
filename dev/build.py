import re,sys,os
# Usage (from anywhere):  python3 dev/build.py dev/main.tpl.html deploy      -> index.html
#                         python3 dev/build.py dev/v2.tpl.html deploy-v2     -> v2/index.html
#                         python3 dev/build.py <tpl>                          -> only the test files in dev/out/
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE); OUT=os.path.join(HERE,'out'); os.makedirs(OUT,exist_ok=True)
src=sys.argv[1]; target=sys.argv[2] if len(sys.argv)>2 else ''; deploy=target in ('deploy','deploy-v2')
s=open(src).read()
d=open(os.path.join(HERE,'maze5.json')).read(); out=s.replace('__DATA__',d)
open(os.path.join(OUT,'sticker-maze.html'),'w').write(out)
open(os.path.join(OUT,'gcheck.js'),'w').write(re.findall(r'<script>(.*?)</script>',out,re.S)[0])
s2=out.replace('  spawnAll();\n','  spawnAll(); window.__D=dinos; window.__st=()=>st; window.__NET=()=>NET; window.__cut=()=>cut; window.__pitch=v=>{pitch=v}; window.__x={nav,navCells,safe,field,idxOf,nearestNav,W,H,SX,SZ,EX,EZ,cellX,cellZ,atHome,terr,buildTerritories,squeeze,lineOfSight}; Object.defineProperty(window.__x,"EX",{get:()=>EX}); Object.defineProperty(window.__x,"EZ",{get:()=>EZ}); window.__ev=s=>eval(s); window.__newExit=()=>{ if(typeof newExit==="function") newExit(); }; window.__spawn=n=>spawnAll(n); window.__mv=v=>{localMoving=v}; window.__upd=(n,dt)=>{for(let i=0;i<n;i++) update(dt)}; window.__keys=keys; window.__lb=()=>landBob; window.__B=()=>typeof bon!=="undefined"?{bon,finds,cam:camera}:null; window.__bits=bits; window.__collH=collH; window.__step=(n,dt)=>{for(let i=0;i<n;i++) worldUpdate(dt)}; window.__add=()=>{const i=nearestNav(idxOf(EX,EZ)); pickWander(addDino("d"+(dinoSeq++),cellX(i),cellZ(i)));};\n',1)
assert '__pitch' in s2
s2=s2.replace("    renderer.render(scene, camera);","    if (!window.__fast || (window.__shot && (window.__shot=0, true))) renderer.render(scene, camera);")
open(os.path.join(OUT,'debug.html'),'w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body>'+s2+'</body></html>')
if deploy:
    full='<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">\n'+out[:out.index('</style>')+8]+'\n'
    rest=out[out.index('</style>')+8:]
    le=rest.index('\n',rest.index('<link'))
    full+=rest[:le]+'\n<script src="firebase-config.js"></script>\n</head>\n<body>'+rest[le:]+'\n</body>\n</html>\n'
    if target=='deploy': open(os.path.join(ROOT,'index.html'),'w').write(full)
if target=='deploy-v2':
    import os
    os.makedirs(os.path.join(ROOT,'v2'), exist_ok=True)
    v2=full.replace('<script src="firebase-config.js"></script>','<script src="../firebase-config.js"></script>\n<script>window.MAZE_ROOM = "v2";</script>',1).replace('<title>Лабиринт со стикера</title>','<title>Лабиринт со стикера · вариант 2</title>',1)
    assert 'MAZE_ROOM' in v2 and 'вариант 2' in v2
    open(os.path.join(ROOT,'v2','index.html'),'w').write(v2)
