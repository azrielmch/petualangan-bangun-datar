"""Assemble generated PNG sprites and native UI into the v2 production package.
Raster images are copied unmodified; no raster image editing is performed.
"""
from pathlib import Path
import base64, html, json, re, struct, xml.etree.ElementTree as ET, zipfile, shutil
from jigsaw_layouts import all_layouts

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'assets-3d'
NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
def el(tag,attrs=None): return ET.Element('{'+NS+'}'+tag,attrs or {})
def mix(c,target,amount):
    a=[int(c[i:i+2],16) for i in (1,3,5)]
    return '#'+''.join(f'{round(x*(1-amount)+target*amount):02x}' for x in a)

def dimensional_svg(source,target):
    tree=ET.parse(source);root=tree.getroot()
    name=source.stem
    replacement=DEST/'ui'/(name+'.png')
    if name in ['banner-completed','banner-correct','banner-great','banner-wrong','logo'] and replacement.exists():
        w,h=struct.unpack('>II',replacement.read_bytes()[16:24])
        image=el('image',{'href':'data:image/png;base64,'+base64.b64encode(replacement.read_bytes()).decode(),'width':str(w),'height':str(h)})
        root=el('svg',{'viewBox':f'0 0 {w} {h}','width':str(w),'height':str(h)})
        root.append(image)
        target.write_text(ET.tostring(root,encoding='unicode'))
        return
    base=DEST/'ui'/('button-base.png' if name.startswith('icon-') or name.startswith('map-node-') else 'wood-panel.png')
    if base.exists() and (name.startswith('icon-') or name.startswith('map-node-') or name in ['panel','button','title-board','matching-slot','logo']):
        w=root.get('width');h=root.get('height')
        image=el('image',{'href':'data:image/png;base64,'+base64.b64encode(base.read_bytes()).decode(),'x':'0','y':'0','width':w,'height':h,'preserveAspectRatio':'none'})
        for child in list(root):
            if child.tag.split('}')[-1] in ['circle','rect']:root.remove(child)
        root.insert(0,image)
        if name=='map-node-done':
            root.append(el('path',{'d':'m72 130 38 37 77-83','fill':'none','stroke':'#fff4d4','stroke-width':'15','stroke-linecap':'round','stroke-linejoin':'round'}))
        elif name=='map-node-locked':
            root.append(el('rect',{'x':'87','y':'112','width':'82','height':'70','rx':'12','fill':'#fff4d4'}))
            root.append(el('path',{'d':'M102 113V91a26 26 0 0 1 52 0v22','fill':'none','stroke':'#fff4d4','stroke-width':'12'}))
    defs=el('defs')
    # This is an editable native UI material, preserving existing icon geometry.
    fil=el('filter',{'id':'volume','x':'-25%','y':'-25%','width':'160%','height':'170%','color-interpolation-filters':'sRGB'})
    fil.append(el('feGaussianBlur',{'in':'SourceAlpha','stdDeviation':'1.5','result':'soft'}))
    light=el('feSpecularLighting',{'in':'soft','surfaceScale':'4','specularConstant':'.45','specularExponent':'16','lighting-color':'#fff4d4','result':'light'})
    light.append(el('feDistantLight',{'azimuth':'225','elevation':'48'}));fil.append(light)
    fil.append(el('feComposite',{'in':'light','in2':'SourceAlpha','operator':'in','result':'shine'}))
    fil.append(el('feComposite',{'in':'SourceGraphic','in2':'shine','operator':'arithmetic','k1':'0','k2':'1','k3':'.65','k4':'0','result':'raised'}))
    fil.append(el('feDropShadow',{'in':'raised','dx':'0','dy':'3','stdDeviation':'2','flood-color':'#6b3b1f','flood-opacity':'.25'}))
    defs.append(fil)
    gradients={}
    for item in root.iter():
        if item.tag.split('}')[-1]=='text':
            item.set('fill','#69402c')
            item.set('stroke','none')
            continue
        fill=item.get('fill','')
        if re.fullmatch(r'#[0-9a-fA-F]{6}',fill):
            if fill not in gradients:
                gid='material'+str(len(gradients));gradients[fill]=gid
                grad=el('radialGradient',{'id':gid,'cx':'28%','cy':'18%','r':'94%'})
                for off,c in [('0%',mix(fill,255,.46)),('45%',fill),('100%',mix(fill,40,.32))]:
                    grad.append(el('stop',{'offset':off,'stop-color':c}))
                defs.append(grad)
            item.set('fill','url(#'+gradients[fill]+')')
        if item.get('stroke')=='#69402c':
            item.set('stroke','#9c693e')
            item.set('stroke-width',str(min(float(item.get('stroke-width','3')),2.5)))
    content=el('g',{'filter':'url(#volume)'})
    for child in list(root):
        root.remove(child)
        if child.tag.endswith('defs'):defs.extend(list(child))
        elif child.tag.endswith('image'):root.append(child)
        else:content.append(child)
    root.append(defs);root.append(content)
    target.write_text(ET.tostring(root,encoding='unicode'))

for source in (ROOT/'assets/ui').glob('*.svg'):
    dimensional_svg(source,DEST/'ui'/source.name)

labels={'segitiga':'SEGITIGA','persegi':'PERSEGI','lingkaran':'LINGKARAN','persegi-panjang':'PERSEGI PANJANG','segi-lima':'SEGI LIMA'}
layouts=all_layouts()
(DEST/'puzzles').mkdir(parents=True,exist_ok=True)
(DEST/'puzzles/jigsaw-layout.json').write_text(json.dumps({'levels':layouts},indent=2))
for shape,label in labels.items():
    layout=next(x for x in layouts if x['shape']==shape)
    for old in (DEST/'puzzles').glob('piece-*.svg'):
        match=re.fullmatch('piece-'+re.escape(shape)+r'-(\d+)',old.stem)
        if match and int(match[1])>layout['pieceCount']:
            archive=ROOT/'assets-archive'/'puzzle-revisions'
            archive.mkdir(parents=True,exist_ok=True)
            target=archive/old.name
            version=2
            while target.exists():
                target=archive/(old.stem+f'-v{version}.svg');version+=1
            shutil.move(str(old),str(target))
    (DEST/'puzzles'/f'layout-{shape}.json').write_text(json.dumps(layout,indent=2))
    p=DEST/'characters'/f'{shape}.png'
    if not p.exists():continue
    uri='data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
    content=f'''<defs><linearGradient id="card" x2=".2" y2="1"><stop stop-color="#fff9e4"/><stop offset="1" stop-color="#e6c48b"/></linearGradient><linearGradient id="grass" x2="0" y2="1"><stop stop-color="#d2e9ac"/><stop offset="1" stop-color="#83b96c"/></linearGradient></defs><rect x="4" y="4" width="472" height="352" rx="23" fill="url(#card)" stroke="#bd8a4b" stroke-width="8"/><path d="M9 247q110-43 230 0t232 0v101H9Z" fill="url(#grass)"/><circle cx="420" cy="55" r="22" fill="#ffdb76"/><image href="{uri}" x="100" y="13" width="280" height="253"/><rect x="25" y="280" width="430" height="58" rx="19" fill="#fff6de" stroke="#d2a369" stroke-width="2"/><text x="240" y="318" text-anchor="middle" font-family="Trebuchet MS,Arial,sans-serif" font-weight="bold" font-size="29" fill="#69402c">{label}</text>'''
    head='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360">'
    (DEST/'puzzles'/f'master-{shape}.svg').write_text(head+content+'</svg>')
    outlines=''.join(f'<path d="{p["path"]}" fill="none" stroke="#805b36" stroke-width="2.2"/>' for p in layout['pieces'])
    (DEST/'puzzles'/f'assembled-{shape}.svg').write_text(head+content+outlines+'</svg>')
    for piece in layout['pieces']:
        path=piece['path']
        # SVG clipping only, generated raster file is unchanged.
        body=f'<defs><clipPath id="piece"><path d="{path}"/></clipPath></defs><g clip-path="url(#piece)">{content}</g><path d="{path}" fill="none" stroke="#8e613b" stroke-width="1.5"/>'
        (DEST/'puzzles'/f'piece-{shape}-{piece["id"]+1}.svg').write_text(head+body+'</svg>')

manifest=[]
previous={item['id']:item for item in json.loads((ROOT/'assets/manifest.json').read_text())}
content_file=ROOT/'content/game-content.json'
game_content=json.loads(content_file.read_text()) if content_file.exists() else {}
for obj in game_content.get('objects',[]):previous[obj['id']]={**previous.get(obj['id'],{}),'shape':obj['shape'],'label':obj['name']}
for path in sorted(DEST.rglob('*')):
    if path.suffix not in ['.png','.svg']:continue
    if path.suffix=='.svg' and path.with_suffix('.png').exists():continue
    if path.suffix=='.png':w,h=struct.unpack('>II',path.read_bytes()[16:24])
    else:
        r=ET.parse(path).getroot();w=int(r.get('width'));h=int(r.get('height'))
    item=dict(previous.get(path.stem,{}))
    item.update({'id':path.stem,'path':str(path.relative_to(ROOT)),'type':path.parent.name,'width':w,'height':h,'style':'soft-3d'})
    if path.parent.name=='puzzles':
        puzzle=next((x for x in layouts if path.stem.endswith('-'+x['shape']) or re.fullmatch('piece-'+re.escape(x['shape'])+r'-\d+',path.stem)),None)
        if puzzle:item.update({'level':puzzle['level'],'shape':puzzle['shape'],'pieces':puzzle['pieceCount']})
    elif path.parent.name=='themes':
        variant=next((v for v in game_content.get('puzzle',{}).get('variants',[]) if v['id']==path.stem),None)
        item['type']='puzzle-variants'
        if variant:item.update({'theme':variant['theme'],'shape':variant['shape']})
    elif path.parent.name in ['find-scenes','find-scenes-25d']:
        scene=next((s for s in game_content.get('find',{}).get('scenes',[]) if s['id']==path.stem),None)
        item['type']='find-scenes'
        if scene:item.update({'shape':scene['targetShape'],'theme':scene['themeId'],'name':scene['name'],'style':scene.get('style','soft-3d'),'targetCount':sum(o['shape']==scene['targetShape'] for o in scene['hotspots'])})
    manifest.append(item)
for path in sorted((ROOT/'assets/backgrounds').glob('*.png')):
    w,h=struct.unpack('>II',path.read_bytes()[16:24]);manifest.append({'id':path.stem,'path':str(path.relative_to(ROOT)),'type':'backgrounds','width':w,'height':h})
(DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))

def card(item):
    title=(item.get('name',item['id'])+' · '+str(item['targetCount'])+' benda benar') if item['type']=='find-scenes' else item['id']
    return f'<figure><img loading="lazy" src="{item["path"]}" alt="{html.escape(title)}"><figcaption>{html.escape(title)}</figcaption></figure>'
sections=[]
for group,title in [('find-scenes','Gambar Utuh Temukan Benda'),('characters','Karakter 3D'),('objects','Benda 3D'),('puzzles','Puzzle'),('ui','Antarmuka'),('backgrounds','Latar')]:
    selected=[x for x in manifest if x['type']==group]
    if group=='puzzles':selected.sort(key=lambda x:(x.get('level',99),0 if x['id'].startswith('assembled-') else 1 if x['id'].startswith('master-') else 2,x['id']))
    featured_ids=['logo','banner-completed','banner-great','banner-correct','banner-wrong']
    featured=[next((x for x in selected if x['id']==key and x['path'].endswith('.png')),None) for key in featured_ids] if group=='ui' else []
    featured=[x for x in featured if x]
    intro=('<p>Logo dan banner 3D bertekstur kayu dengan huruf timbul.</p><div class="featured">'+''.join(card(x) for x in featured)+'</div>') if featured else ''
    if group=='puzzles':
        featured=[next(x for x in selected if x['id']=='assembled-'+level['shape']) for level in layouts]
        intro='<p><a href="puzzle.html">Mainkan puzzle Biru Ceria — kepingan terpisah dan papan tanpa panduan</a></p><p>Level 1 dan 2: 4 keping. Level 3 dan 4: 6 keping. Level 5: 8 keping.</p><div class="puzzle-levels">'+''.join(f'<figure><img loading="lazy" src="{x["path"]}" alt="Level {x["level"]}, {x["pieces"]} keping"><figcaption>Level {x["level"]} · {labels[x["shape"]].title()} · {x["pieces"]} keping</figcaption></figure>' for x in featured)+'</div><h3>Gambar utuh dan kepingan tiap level</h3>'
    sections.append(f'<section id="{group}"><h2>{title}</h2>'+intro+'<div class="grid">'+''.join(card(x) for x in selected if x not in featured)+'</div></section>')
room='assets/backgrounds/child-room.png'
placements=[('jendela',30,13,16),('bingkai',55,21,12),('jam',46,8,10),('buku',31,66,13),('pizza',59,71,12),('biskuit',47,76,9)]
sprites=''.join(f'<img class="placed" src="assets-3d/objects/{name}.png" alt="{name}" style="left:{x}%;top:{y}%;width:{w}%">' for name,x,y,w in placements if (DEST/'objects'/f'{name}.png').exists())
if game_content.get('find',{}).get('scenes'):
    room=game_content['find']['scenes'][0]['asset']
    sprites=''
char=''.join(f'<img src="assets-3d/characters/{s}.png" alt="{s}">' for s in labels if (DEST/'characters'/f'{s}.png').exists())
page='''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Aset 3D — Petualangan Bangun Datar</title><style>*{box-sizing:border-box}body{margin:0;background:#f7efd9;color:#69402c;font:16px system-ui}header,main{max-width:1240px;margin:auto;padding:24px}header{border-bottom:2px solid #dfbd83}h1{margin:0 0 10px}nav{display:flex;gap:18px;flex-wrap:wrap}a{color:#85602c}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px}figure{margin:0;background:#fffaf0;border:2px solid #dfbd83;border-radius:18px;overflow:hidden;box-shadow:0 4px 14px #69402c12}figure img{display:block;width:100%;height:180px;object-fit:contain;background:repeating-conic-gradient(#f3ecd9 0% 25%,#fffaf0 0% 50%) 0/20px 20px}figcaption{padding:10px;font-size:13px;overflow-wrap:anywhere}.scene{position:relative;aspect-ratio:3/2;border-radius:24px;overflow:hidden;box-shadow:0 10px 24px #69402c30}.scene>img.bg{width:100%;height:100%;object-fit:cover}.placed{position:absolute;filter:drop-shadow(0 5px 4px #593b282a)}.cast{background:linear-gradient(#fff6df,#ecd0a0);border:2px solid #d9b778;border-radius:24px;display:flex;align-items:center;padding:15px;margin-top:24px}.cast img{width:20%;min-width:0}section{scroll-margin-top:16px}p{line-height:1.6}.pill{display:inline-block;padding:5px 12px;border-radius:20px;background:#e9d4a7;font-size:13px}h2{margin-top:40px}</style><header><span class="pill">Versi 2 · Kartun 3D lembut</span><h1>Petualangan Bangun Datar</h1><p>Volume lembut, tekstur hangat, cahaya dari kiri atas, dan latar transparan. Tanpa emoji.</p><nav><a href="#composition">Dalam ruangan</a><a href="#characters">Karakter</a><a href="#objects">Benda</a><a href="#puzzles">Puzzle</a><a href="#ui">Antarmuka</a></nav></header><main><section id="composition"><h2>Pratinjau menyatu dengan latar</h2><p>Contoh penempatan aset untuk memeriksa kesesuaian gaya. Ini belum layar permainan interaktif.</p><div class="scene"><img class="bg" src="'''+room+'" alt="Latar kamar">'+sprites+'</div><div class="cast">'+char+'</div></section>'+''.join(sections)+'</main></html>'
page=page.replace('</style>','.featured,.puzzle-levels{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin-bottom:24px}.featured figure:first-child{grid-column:1/-1}.featured img,.puzzle-levels img{height:220px}.featured figure:first-child img{height:280px}@media(max-width:650px){.featured,.puzzle-levels{grid-template-columns:1fr}.featured img{height:200px}}'+'</style>')
if game_content:
    panel=(ROOT/'content/preview-panel.html').read_text()
    if game_content.get('find',{}).get('style')=='cartoon-2.5d':
        page=page.replace('Versi 2 · Kartun 3D lembut','Temukan Benda · Kartun 2.5D')
        page=page.replace('Contoh penempatan aset untuk memeriksa kesesuaian gaya. Ini belum layar permainan interaktif.','Contoh ilustrasi utuh dengan benda yang berada alami di dalam ruangan.')
    page=page.replace('<nav>','<nav><a href="index.html">Beranda</a><a href="results.html">Hasil Akhir</a><a href="find.html">Main Temukan Benda</a><a href="matching.html">Main Mencocokkan</a><a href="puzzle.html">Main Puzzle</a><a href="#random-levels">Isi 15 level</a><a href="#find-scenes">Gambar Temukan Benda</a>',1)
    page=page.replace('<main>','<main>'+panel,1)
    page=page.replace('<title>','<link rel="stylesheet" href="content/preview.css"><link rel="stylesheet" href="content/level-celebration.css"><link rel="stylesheet" href="content/find-game.css"><link rel="stylesheet" href="content/find-frame.css"><link rel="stylesheet" href="content/puzzle-game.css"><link rel="stylesheet" href="content/matching-game.css"><title>',1)
    page=page.replace('</html>','<script src="content/game-progress.js" defer></script><script src="content/level-celebration.js" defer></script><script src="content/randomizer.js" defer></script><script src="content/find-game.js" defer></script><script src="content/find-frame-game.js" defer></script><script src="content/puzzle-game.js" defer></script><script src="content/matching-game.js" defer></script><script src="content/preview.js" defer></script></html>')
page=re.sub(r'(src|href)="(content/[^"?]+\.(?:js|css))"',r'\1="\2?v=local-frame-3"',page)
page=re.sub(r'src="(assets-3d/[^\"]+)"',r'src="\1?v=clean-25d-1"',page)
(ROOT/'asset-catalog.html').write_text(page)
(ROOT/'asset-catalog-3d.html').write_text(page)
print(f'3D catalog: {len(manifest)} assets')
