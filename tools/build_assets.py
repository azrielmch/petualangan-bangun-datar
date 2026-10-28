from pathlib import Path
import json, html, zipfile

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'assets'
INK='#69402c'
colors={'persegi':'#43bdf0','lingkaran':'#f27d9e','segitiga':'#ffd15d','persegi-panjang':'#8dc943','segi-lima':'#b887e8'}
names={'persegi':'Persegi','lingkaran':'Lingkaran','segitiga':'Segitiga','persegi-panjang':'Persegi Panjang','segi-lima':'Segi Lima'}
manifest=[]

def svg(body, w=256,h=256):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs><linearGradient id="shine" x2="0" y2="1"><stop stop-color="#fff" stop-opacity=".32"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>{body}</svg>'

def save(group,name,body,w=256,h=256,**meta):
    p=A/group/f'{name}.svg';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(svg(body,w,h))
    manifest.append({'id':name,'path':str(p.relative_to(ROOT)),'type':group,'width':w,'height':h,**meta})

def shape(kind,fill,stroke=INK,sw=6):
    attr=f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"'
    return {'persegi':f'<rect x="48" y="48" width="160" height="160" rx="8" {attr}/>',
      'lingkaran':f'<circle cx="128" cy="128" r="82" {attr}/>',
      'segitiga':f'<path d="M128 37 221 207H35Z" {attr}/>',
      'persegi-panjang':f'<rect x="25" y="70" width="206" height="116" rx="7" {attr}/>',
      'segi-lima':f'<path d="m128 34 94 69-36 110H70L34 103Z" {attr}/>'}[kind]

def face(celebrate=False):
    eyes='<path d="M91 122q9-15 18 0m38 0q9-15 18 0" fill="none" stroke="#493125" stroke-width="7" stroke-linecap="round"/>' if celebrate else '<ellipse cx="100" cy="124" rx="7" ry="10" fill="#493125"/><ellipse cx="156" cy="124" rx="7" ry="10" fill="#493125"/><circle cx="102" cy="121" r="2" fill="white"/><circle cx="158" cy="121" r="2" fill="white"/>'
    return eyes+'<ellipse cx="83" cy="145" rx="12" ry="6" fill="#ee6e85" opacity=".55"/><ellipse cx="173" cy="145" rx="12" ry="6" fill="#ee6e85" opacity=".55"/><path d="M109 147q19 30 38 0Z" fill="#713b36" stroke="#493125" stroke-width="3"/><path d="M119 158q9-7 18 0" stroke="#ff9baf" stroke-width="6" fill="none"/>'

items={
 'persegi':['jendela','bingkai','ubin','serbet','catatan'],
 'lingkaran':['koin','piring','jam','kancing','biskuit-bulat'],
 'segitiga':['pizza','penggaris','bendera','roti','rambu'],
 'persegi-panjang':['pintu','buku','karpet','papan','tempat-pensil'],
 'segi-lima':['biskuit','bingkai-segilima','lencana','ubin-segilima','papan-segilima']}

for kind,c in colors.items():
    save('characters',kind,shape(kind,c)+face(),shape=kind,pose='normal')
    # Custom illustrated thumbs-up, not a Unicode or emoji glyph.
    thumb='<path d="M195 167q-7-13 0-21l9-13 1-23q1-12 10-8 9 4 5 29l13 1q13 2 9 15l-6 25q-2 10-13 10h-17Z" fill="#fff1cf" stroke="#69402c" stroke-width="5" stroke-linejoin="round"/>'
    save('characters',kind+'-great',shape(kind,c)+face(True)+thumb,shape=kind,pose='celebration')
    save('ui','shape-'+kind,shape(kind,c),shape=kind)
    # Puzzle master keeps its label in the same image so the label is cut with the illustration.
    card=f'<rect x="5" y="5" width="470" height="350" rx="25" fill="#fff4d8" stroke="{INK}" stroke-width="8"/><path d="M15 250q100-50 220 0t230 0v95H15Z" fill="#d1e9ad"/><circle cx="410" cy="57" r="24" fill="#ffda68"/><g transform="translate(111 6) scale(1.02)">{shape(kind,c)}{face()}</g><rect x="38" y="277" width="404" height="57" rx="18" fill="#fffaf0"/><text x="240" y="315" text-anchor="middle" font-family="Trebuchet MS,Arial,sans-serif" font-weight="bold" font-size="29" fill="{INK}">{names[kind].upper()}</text>'
    save('puzzles','master-'+kind,card,480,360,shape=kind,pieces=6)
    for name in items[kind]:
        base=shape(kind,c)
        detail=''
        if name=='jendela':
            base=shape(kind,'#9ce2f4');detail='<path d="M57 193 191 59" stroke="white" stroke-width="17" opacity=".45"/><rect x="48" y="48" width="160" height="160" rx="8" fill="none" stroke="#b8703e" stroke-width="13"/>'
        elif 'bingkai' in name:
            base=shape(kind,'#fff4cf', '#b9703e',15);detail='<path d="M128 159v-47m0 20q-33-32-35 0 17 19 35 0m0 9q30-28 34-1-17 17-34 1" fill="#90bb63" stroke="#65904b" stroke-width="3"/><circle cx="128" cy="96" r="16" fill="#ffca62"/>'
        elif name=='koin':
            base=shape(kind,'#ffd367');detail='<circle cx="128" cy="128" r="64" fill="none" stroke="#dda146" stroke-width="5"/><path d="m128 83 12 27 30 3-22 21 6 30-26-15-26 15 6-30-22-21 30-3Z" fill="#e8a940"/>'
        elif name=='piring':
            base=shape(kind,'#f8efcf');detail='<circle cx="128" cy="128" r="62" fill="#b4e4de" stroke="#5baca6" stroke-width="4"/>'
        elif name=='jam':
            base=shape(kind,'#fff9dc');detail='<circle cx="128" cy="128" r="73" fill="none" stroke="#49a4be" stroke-width="8"/><path d="M128 77v51l35 20M128 62v9m0 114v9M62 128h9m114 0h9" stroke="#69402c" stroke-width="6" stroke-linecap="round" fill="none"/><circle cx="128" cy="128" r="6" fill="#69402c"/>'
        elif name=='kancing':
            base=shape(kind,'#a98cdb');detail='<circle cx="128" cy="128" r="62" fill="none" stroke="#78569c" stroke-width="5"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="10" fill="#fff2d1" stroke="#69402c" stroke-width="3"/>' for x in [106,150] for y in [106,150])
        elif 'biskuit' in name:
            base=shape(kind,'#dda15b');detail=''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="#85502f"/>' for x,y in [(102,92),(149,98),(87,133),(129,130),(165,147),(112,172),(151,180)])
        elif name=='pizza':
            base=shape(kind,'#ffd15d');detail='<path d="M40 198h175" stroke="#c37b40" stroke-width="17" stroke-linecap="round"/><g fill="#e47555" stroke="#a64b35" stroke-width="3"><circle cx="126" cy="99" r="14"/><circle cx="96" cy="161" r="15"/><circle cx="159" cy="165" r="14"/></g>'
        elif name=='penggaris':
            base=shape(kind,'#ffd366');detail='<path d="m128 91 40 79H86Z" fill="#fff3d1" stroke="#b88535" stroke-width="5"/><path d="M60 191v-10m22 10v-10m22 10v-10m22 10v-10m22 10v-10m22 10v-10m22 10v-10" stroke="#8a6336" stroke-width="3"/>'
        elif name=='roti':
            base=shape(kind,'#d69652');detail='<path d="m128 59 78 138H50Z" fill="#fff0b8" stroke="#b76d37" stroke-width="4"/><path d="M59 181h138" stroke="#8fbe62" stroke-width="8"/>'
        elif name=='rambu':
            base=shape(kind,'#fff1c6');detail='<path d="m128 60 77 136H51Z" fill="#ffd15d" stroke="#df855a" stroke-width="10"/>'
        elif name=='pintu':
            # This asset is upright, with a rectangular silhouette.
            base='<rect x="66" y="22" width="124" height="212" rx="5" fill="#c98952" stroke="#69402c" stroke-width="6"/>';detail='<path d="M83 42h90v64H83Zm0 83h90v88H83Z" fill="#dca06a" stroke="#a7673a" stroke-width="4"/><circle cx="164" cy="120" r="7" fill="#ffda6c" stroke="#69402c" stroke-width="3"/>'
        elif name=='buku':
            base=shape(kind,'#4dadd4');detail='<path d="M49 73v110" stroke="#226e94" stroke-width="13"/><rect x="77" y="97" width="118" height="54" rx="4" fill="#fff4d7"/>'
        elif name in ['karpet','serbet']:
            detail=shape(kind,'none','#fff2cb',17)+shape(kind,'none',INK,5)+'<path d="m106 128 22-22 22 22-22 22Z" fill="#fff0c9"/>'
        elif name=='catatan':
            base=shape(kind,'#ffe1a0');detail='<path d="M77 94h102m-102 28h102m-102 28h70" stroke="#c5a16b" stroke-width="6" stroke-linecap="round"/>'
        elif name=='tempat-pensil':
            base=shape(kind,'#ec9a79');detail='<path d="M40 104h175" stroke="#fff0d1" stroke-width="7"/><rect x="184" y="93" width="18" height="24" rx="4" fill="#ffd16b" stroke="#69402c" stroke-width="3"/>'
        elif name=='papan':
            base=shape(kind,'#65a691','#b77b47',14);detail='<path d="M67 108h119m-119 28h88" stroke="#fff1ce" stroke-width="5" opacity=".7"/>'
        elif name=='lencana':
            base=shape(kind,'#ffca66');detail='<path d="m128 81 12 27 30 3-22 21 6 30-26-15-26 15 6-30-22-21 30-3Z" fill="#e9a343" stroke="#b97836" stroke-width="3"/>'
        elif name=='papan-segilima':
            base=shape(kind,'#a9d4b4','#b77b47',12)
        elif name=='bendera':
            base=shape(kind,'#ed927d');detail='<path d="m128 67 67 122H61Z" fill="none" stroke="#fff2cc" stroke-width="4"/>'
        else:
            detail=shape(kind,'none','#fff2d1',15)+shape(kind,'none',INK,5)
        save('objects',name,base+detail,shape=kind,label=name.replace('-',' '))

icons={
 'back':'<path d="m144 74-54 54 54 54M92 128h88"/>',
 'next':'<path d="m110 74 54 54-54 54M76 128h88"/>',
 'play':'<path d="m103 75 75 53-75 53Z" fill="#fff4d4"/>',
 'sound':'<path d="M68 105h27l35-29v104l-35-29H68Z" fill="#fff4d4"/><path d="M153 103q25 25 0 50m18-73q47 48 0 96"/>',
 'mute':'<path d="M58 105h27l35-29v104l-35-29H58Z" fill="#fff4d4"/><path d="m153 105 43 46m0-46-43 46"/>',
 'help':'<path d="M104 96q0-30 28-29 45 3 21 38l-23 20v15"/><circle cx="130" cy="168" r="5" fill="#fff4d4"/>',
 'home':'<path d="m65 120 63-52 63 52M83 109v77h90v-77m-58 77v-48h26v48"/>',
 'retry':'<path d="M83 94a61 61 0 1 1-5 61M81 63v39h40"/>',
 'lock':'<rect x="80" y="113" width="96" height="80" rx="13" fill="#fff4d4"/><path d="M97 112V86a31 31 0 0 1 62 0v26"/>',
 'check':'<path d="m72 130 38 37 77-83"/>',
 'close':'<path d="m84 84 88 88m0-88-88 88"/>'}
for name,body in icons.items():
    c='#78b85c' if name=='check' else '#e58a72' if name=='close' else '#52b7d1' if name=='help' else '#efb14d'
    save('ui','icon-'+name,f'<circle cx="128" cy="128" r="106" fill="{c}" stroke="{INK}" stroke-width="7"/><circle cx="128" cy="128" r="93" fill="none" stroke="#ffe9b7" stroke-width="4"/><g fill="none" stroke="#fff4d4" stroke-width="12" stroke-linecap="round" stroke-linejoin="round">{body}</g>')

star='M128 26 158 89 227 99 177 148 189 218 128 185 67 218 79 148 29 99 98 89Z'
for state in ['full','half','empty']:
    body=f'<path d="{star}" fill="#fffaf0" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    if state!='empty':
        body+=f'<defs><clipPath id="half"><rect width="{128 if state=="half" else 256}" height="256"/></clipPath></defs><path d="{star}" fill="#ffcf52" clip-path="url(#half)"/><path d="{star}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    save('ui','star-'+state,body)

for name,w,h in [('panel',640,400),('button',400,112),('title-board',700,160),('matching-slot',380,100)]:
    save('ui',name,f'<rect x="7" y="7" width="{w-14}" height="{h-14}" rx="26" fill="#b87845" stroke="{INK}" stroke-width="7"/><rect x="18" y="17" width="{w-36}" height="{h-37}" rx="20" fill="#ffeac1" stroke="#e2ab64" stroke-width="7"/>',w,h)

# An exact reusable six-piece jigsaw cutting template. Each shared edge uses the same curve in reverse.
# Full master is 480 x 360. Cell size is 160 x 180, knob radius about 18.
paths=[
 'M0 0H160V64C160 72 178 70 178 90S160 108 160 116V180H104C96 180 100 198 80 198S64 180 56 180H0Z',
 'M160 0H320V64C320 72 338 70 338 90S320 108 320 116V180H264C256 180 260 162 240 162S224 180 216 180H160V116C160 108 178 110 178 90S160 72 160 64Z',
 'M320 0H480V180H424C416 180 420 198 400 198S384 180 376 180H320V116C320 108 338 110 338 90S320 72 320 64Z',
 'M0 180H56C64 180 60 198 80 198S96 180 104 180H160V244C160 252 142 250 142 270S160 288 160 296V360H0Z',
 'M160 180H216C224 180 220 162 240 162S256 180 264 180H320V244C320 252 302 250 302 270S320 288 320 296V360H160V296C160 288 142 290 142 270S160 252 160 244Z',
 'M320 180H376C384 180 380 198 400 198S416 180 424 180H480V360H320V296C320 288 302 290 302 270S320 252 320 244Z']
(A/'puzzles'/'jigsaw-layout.json').write_text(json.dumps({'width':480,'height':360,'rows':2,'columns':3,'pieces':[{'id':i,'path':p,'targetX':(i%3)*160,'targetY':(i//3)*180} for i,p in enumerate(paths)]},indent=2))
save('puzzles','jigsaw-outline',''.join(f'<path d="{p}" fill="none" stroke="#69402c" stroke-width="2"/>' for p in paths),480,360)
for kind in colors:
    for i,p in enumerate(paths):
        # Standalone clipped SVG, embedded master content; no external dependency.
        master=(A/'puzzles'/f'master-{kind}.svg').read_text()
        inner=master[master.index('>')+1:master.rindex('</svg>')]
        save('puzzles',f'piece-{kind}-{i+1}',f'<defs><clipPath id="piece"><path d="{p}"/></clipPath></defs><g clip-path="url(#piece)">{inner}</g><path d="{p}" fill="none" stroke="#845d3f" stroke-width="2"/>',480,360,shape=kind,piece=i+1)

for label,title in [('great','GREAT!'),('completed','COMPLETED'),('correct','BENAR'),('wrong','COBA LAGI, YA!')]:
    fill='#82ba61' if label=='correct' else '#ed9a7f' if label=='wrong' else '#f5c461'
    save('ui','banner-'+label,f'<path d="m12 25 42 12V12h532v25l42-12-14 48 14 48-42-10v22H54v-22l-42 10 14-48Z" fill="{fill}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><text x="320" y="91" text-anchor="middle" font-family="Trebuchet MS,Arial,sans-serif" font-weight="bold" font-size="49" fill="#fff8df" stroke="{INK}" stroke-width="2" paint-order="stroke">{title}</text>',640,145)
save('ui','logo','<rect x="15" y="20" width="670" height="180" rx="45" fill="#c3894e" stroke="#69402c" stroke-width="8"/><rect x="28" y="32" width="644" height="155" rx="36" fill="#ffdf8a" stroke="#e8b565" stroke-width="5"/><text x="350" y="92" text-anchor="middle" font-family="Trebuchet MS,Arial,sans-serif" font-size="47" font-weight="bold" fill="#78502d">Petualangan</text><text x="350" y="155" text-anchor="middle" font-family="Trebuchet MS,Arial,sans-serif" font-size="55" font-weight="bold" fill="#318baf" stroke="#fff5d7" stroke-width="5" paint-order="stroke">Bangun Datar</text>',700,220)
for game in ['find','puzzle','match']:
    bg='<rect x="5" y="5" width="350" height="230" rx="24" fill="#fff0cf" stroke="#69402c" stroke-width="7"/>'
    if game=='find':
        art='<circle cx="173" cy="115" r="58" fill="#bde5dd" stroke="#b57b44" stroke-width="14"/><path d="m217 159 48 47" stroke="#69402c" stroke-width="24" stroke-linecap="round"/><path d="m217 159 48 47" stroke="#e4b45c" stroke-width="15" stroke-linecap="round"/>'+f'<g transform="translate(119 58) scale(.43)">{shape("persegi",colors["persegi"])}</g>'
    elif game=='puzzle':
        art='<path d="M67 46h79v24q-28-13-28 13t28 13v24h35q-13-28 13-28t13 28h29v77H67Z" fill="#b887e8" stroke="#69402c" stroke-width="6" stroke-linejoin="round"/><path d="M220 41h54v50h-20q12-24-10-24t-10 24h-14Z" fill="#ffd15d" stroke="#69402c" stroke-width="5"/>'
    else:
        art='<g fill="none" stroke="#78b85c" stroke-width="6"><path d="M104 65C170 65 170 177 252 177"/><path d="M104 177C170 177 170 65 252 65"/></g><path d="m76 39 27 48H49Z" fill="#ffd15d" stroke="#69402c" stroke-width="5"/><circle cx="76" cy="177" r="27" fill="#f27d9e" stroke="#69402c" stroke-width="5"/><circle cx="271" cy="65" r="27" fill="#f27d9e" stroke="#69402c" stroke-width="5"/><path d="m271 151 27 48h-54Z" fill="#ffd15d" stroke="#69402c" stroke-width="5"/>'
    save('ui','thumbnail-'+game,bg+art,360,240)
for state,fill in [('available','#f2c366'),('done','#89c36a'),('locked','#d6c7ad')]:
    save('ui','map-node-'+state,f'<circle cx="128" cy="128" r="100" fill="{fill}" stroke="{INK}" stroke-width="7"/><circle cx="128" cy="128" r="84" fill="none" stroke="#fff2d3" stroke-width="5"/>')
for p in sorted((A/'backgrounds').glob('*.png'))+sorted((A/'backgrounds').glob('*.webp')):
    manifest.append({'id':p.stem,'path':str(p.relative_to(ROOT)),'type':'backgrounds','width':1536,'height':1024})
(A/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
sections=[]
for group in ['backgrounds','characters','objects','puzzles','ui']:
    files=sorted((A/group).glob('*.svg'))+sorted((A/group).glob('*.png'))+sorted((A/group).glob('*.webp'))
    cards=''.join(f'<figure><img loading="lazy" src="{p.relative_to(ROOT)}" alt="{html.escape(p.stem)}"><figcaption>{html.escape(p.stem)}</figcaption></figure>' for p in files)
    sections.append(f'<section><h2>{group}</h2><div class="grid">{cards}</div></section>')
(ROOT/'asset-catalog.html').write_text('''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Katalog Aset — Petualangan Bangun Datar</title><style>body{margin:0;background:#f7efd9;color:#69402c;font:16px system-ui}header,main{max-width:1200px;margin:auto;padding:24px}header{border-bottom:3px solid #dfbd83}h1{margin:0 0 10px}h2{text-transform:capitalize}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px}figure{margin:0;background:#fffaf0;border:2px solid #dfbd83;border-radius:18px;overflow:hidden}img{display:block;width:100%;height:175px;object-fit:contain;background:repeating-conic-gradient(#f3ecd9 0% 25%,#fffaf0 0% 50%) 0/20px 20px}figcaption{padding:10px;font-size:13px;overflow-wrap:anywhere}</style><header><h1>Petualangan Bangun Datar</h1><p>Katalog aset produksi · kartun petualangan · tanpa emoji</p><p>Latar ilustrasi, karakter, 25 benda, kartu dan kepingan jigsaw, tombol, serta bintang.</p></header><main>'''+''.join(sections)+'</main></html>')
print(f'Created {len(manifest)} manifest entries and catalog')
