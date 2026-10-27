"""Build themed asset variants and fifteen data-driven level definitions."""
from pathlib import Path
import base64,json,html

ROOT=Path(__file__).resolve().parents[1]
SHAPES={
 'persegi':('Persegi','4 sisi sama panjang\n4 sudut siku-siku'),
 'lingkaran':('Lingkaran','1 sisi lengkung\nTanpa sudut'),
 'segitiga':('Segitiga','3 sisi\n3 sudut'),
 'persegi-panjang':('Persegi Panjang','2 sisi panjang, 2 sisi pendek\n4 sudut siku-siku'),
 'segi-lima':('Segi Lima','5 sisi\n5 sudut')}
GROUPS={
 'persegi':['jendela','bingkai','ubin','serbet','catatan','peta-persegi','tatakan-persegi','kartu-benih-persegi'],
 'lingkaran':['koin','piring','jam','kancing','biskuit-bulat','irisan-jeruk','lencana-bunga-bulat','rebana'],
 'segitiga':['pizza','penggaris','bendera','roti','rambu','serbet-segitiga','penanda-taman-segitiga','tambalan-segitiga'],
 'persegi-panjang':['pintu','buku','karpet','papan','tempat-pensil','kartu-resep','bungkus-benih','alas-piknik'],
 'segi-lima':['biskuit','bingkai-segilima','lencana','ubin-segilima','papan-segilima','tatakan-segilima','tambalan-segilima','label-taman-segilima']}
THEMES=[
 {'id':'kamar','name':'Kamar Anak','background':'assets/backgrounds/child-room.png','accent':'#4bb8d2'},
 {'id':'belajar','name':'Ruang Belajar','background':'assets/backgrounds/workshop.png','accent':'#e3b24d'},
 {'id':'dapur','name':'Dapur Ceria','background':'assets-3d/backgrounds/kitchen.png','accent':'#ee9d78'},
 {'id':'taman','name':'Taman Bunga','background':'assets-3d/backgrounds/garden.png','accent':'#84b762'},
 {'id':'hutan','name':'Hutan Kastel','background':'assets/backgrounds/forest-castle.png','accent':'#9d8cd5'}]
POOLS={
 'kamar':[
  'jendela bingkai ubin serbet catatan tatakan-persegi',
  'jam kancing koin piring biskuit-bulat rebana',
  'penggaris bendera roti rambu serbet-segitiga tambalan-segitiga',
  'pintu buku karpet papan tempat-pensil alas-piknik',
  'biskuit bingkai-segilima lencana ubin-segilima papan-segilima tatakan-segilima tambalan-segilima'],
 'belajar':[
  'jendela bingkai ubin catatan peta-persegi tatakan-persegi',
  'jam koin kancing rebana lencana-bunga-bulat piring',
  'penggaris bendera penanda-taman-segitiga tambalan-segitiga rambu serbet-segitiga',
  'pintu buku papan tempat-pensil kartu-resep bungkus-benih',
  'bingkai-segilima lencana ubin-segilima papan-segilima label-taman-segilima tambalan-segilima tatakan-segilima'],
 'dapur':[
  'jendela ubin serbet tatakan-persegi catatan kartu-benih-persegi',
  'piring koin biskuit-bulat irisan-jeruk jam lencana-bunga-bulat',
  'pizza roti serbet-segitiga penanda-taman-segitiga bendera tambalan-segitiga',
  'pintu kartu-resep buku tempat-pensil bungkus-benih alas-piknik',
  'biskuit tatakan-segilima ubin-segilima label-taman-segilima lencana papan-segilima'],
 'taman':[
  'kartu-benih-persegi tatakan-persegi peta-persegi catatan ubin bingkai',
  'lencana-bunga-bulat irisan-jeruk piring koin biskuit-bulat kancing',
  'penanda-taman-segitiga bendera tambalan-segitiga rambu serbet-segitiga penggaris',
  'bungkus-benih alas-piknik kartu-resep papan buku tempat-pensil',
  'label-taman-segilima tatakan-segilima lencana ubin-segilima tambalan-segilima papan-segilima'],
 'hutan':[
  'peta-persegi serbet tatakan-persegi catatan kartu-benih-persegi ubin',
  'koin piring biskuit-bulat irisan-jeruk kancing lencana-bunga-bulat',
  'tambalan-segitiga bendera rambu serbet-segitiga roti penanda-taman-segitiga',
  'alas-piknik buku kartu-resep bungkus-benih tempat-pensil papan',
  'tambalan-segilima lencana tatakan-segilima biskuit label-taman-segilima ubin-segilima']}
LABELS={'biskuit':'Biskuit segi lima','roti':'Roti segitiga','rambu':'Rambu segitiga','papan':'Papan tulis','bendera':'Bendera segitiga','rebana':'Rebana','peta-persegi':'Peta persegi','tatakan-persegi':'Tatakan persegi','kartu-benih-persegi':'Kartu benih persegi','irisan-jeruk':'Irisan jeruk','lencana-bunga-bulat':'Lencana bunga bulat','penanda-taman-segitiga':'Penanda taman segitiga','tambalan-segitiga':'Tambalan segitiga','bungkus-benih':'Bungkus benih','biskuit-bulat':'Biskuit bulat'}
objects=[{'id':id,'shape':shape,'name':LABELS.get(id,id.replace('-',' ').capitalize()),'asset':f'assets-3d/objects/{id}.png'} for shape,ids in GROUPS.items() for id in ids]
for theme in THEMES:theme['objectPools']={s:POOLS[theme['id']][i].split() for i,s in enumerate(SHAPES)}
layouts=json.loads((ROOT/'assets-3d/puzzles/jigsaw-layout.json').read_text())['levels']
variants=[]
for theme in THEMES:
    background=ROOT/theme['background']
    if not background.exists():continue
    bg='data:image/png;base64,'+base64.b64encode(background.read_bytes()).decode()
    for shape,(label,_) in SHAPES.items():
        character=ROOT/'assets-3d/characters'/f'{shape}.png'
        char='data:image/png;base64,'+base64.b64encode(character.read_bytes()).decode()
        out=ROOT/'assets-3d/puzzles/themes'/f'{theme["id"]}-{shape}.svg'
        svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360"><defs><clipPath id="card"><rect x="4" y="4" width="472" height="352" rx="23"/></clipPath></defs><g clip-path="url(#card)"><image href="{bg}" width="480" height="360" preserveAspectRatio="xMidYMid slice"/><rect width="480" height="360" fill="#fff4da" opacity=".18"/><ellipse cx="240" cy="313" rx="139" ry="20" fill="#75441e" opacity=".2"/><image href="{char}" x="74" y="20" width="332" height="310"/></g><rect x="4" y="4" width="472" height="352" rx="23" fill="none" stroke="#bd8a4b" stroke-width="8"/></svg>'''
        out.write_text(svg)
        variants.append({'id':f'{theme["id"]}-{shape}','theme':theme['id'],'shape':shape,'asset':str(out.relative_to(ROOT))})
config={'version':1,'levelCountPerGame':5,'shapes':[{'id':s,'name':v[0],'features':v[1],'asset':f'assets-3d/ui/shape-{s}.svg'} for s,v in SHAPES.items()],'objects':objects,'themes':THEMES,
 'find':{'levels':[{'level':i+1,'targetShape':s,'targetCount':4,'availableTargetCount':5,'distractorCount':5,'themeIds':[t['id'] for t in THEMES]} for i,s in enumerate(SHAPES)]},
 'puzzle':{'levels':[{'level':l['level'],'pieceCount':l['pieceCount'],'layout':l,'themeIds':[t['id'] for t in THEMES],'shapeIds':list(SHAPES)} for l in layouts],'variants':variants},
 'matching':{'levels':[{'level':i+1,'leftType':a,'rightType':b,'pairCount':5,'name':label} for i,(a,b,label) in enumerate([
 ('shape','name','Bentuk bangun datar × nama bangun datar'),('shape','object','Bentuk bangun datar × benda'),('object','name','Benda × nama bangun datar'),('shape','features','Bangun datar × ciri-ciri'),('object','features','Benda × ciri-ciri')])]},
 'randomization':{'avoidImmediateThemeRepeat':True,'avoidImmediateTargetSetRepeat':True,'resumeKeepsCurrentRound':True,'replayCreatesNewRound':True},
 'completion':{'requiredLevels':15,'levelsPerGame':5,'scoreFormula':'max(0,100-10*ceil(errors/5))'}}
scene_file=ROOT/'content/find-scenes.json'
if scene_file.exists():
    config['find']['scenes']=json.loads(scene_file.read_text())
    for level in config['find']['levels']:
        level['sceneIds']=[s['id'] for s in config['find']['scenes'] if s['targetShape']==level['targetShape']]
        level['targetCount']=3
        level.pop('availableTargetCount',None)
        level.pop('distractorCount',None)
    config['find']['presentation']='integrated-illustration'
    config['find']['style']='cartoon-2.5d'
    config['find']['styleReference']='style-options/school-02-soft-25d.png'
(ROOT/'content/game-content.json').write_text(json.dumps(config,ensure_ascii=False,indent=2))
print(f'15 level definitions; {len(THEMES)} themes; {len(objects)} objects; {len(variants)} themed puzzle masters')
