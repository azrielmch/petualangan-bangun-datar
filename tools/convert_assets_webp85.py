"""Convert game raster assets and SVG-embedded PNGs to WebP quality 85.
Preserve dimensions, alpha samples and vector markup. Back up originals outside
this repository before removing superseded PNG files. Does not publish changes.
"""
from pathlib import Path
from PIL import Image
import base64,hashlib,io,json,re,shutil,time
ROOT=Path(__file__).resolve().parents[1]
BACKUP=ROOT.parent.parent/'arsip-lokal/sebelum-webp85'
PATTERN=re.compile(rb'data:image/png;base64,([A-Za-z0-9+/=]+)')
cache={};checks=[]
def backup(path):
 out=BACKUP/path.relative_to(ROOT);out.parent.mkdir(parents=True,exist_ok=True)
 if out.exists():assert out.read_bytes()==path.read_bytes(),f'Backup collision: {out}'
 else:shutil.copy2(path,out)
def webp(data):
 key=hashlib.sha256(data).hexdigest()
 if key in cache:return cache[key]
 with Image.open(io.BytesIO(data)) as im:
  im.load();rgba=im.convert('RGBA');stream=io.BytesIO()
  opts={'format':'WEBP','quality':85,'method':4,'lossless':False,'exact':True,'alpha_quality':100}
  for tag in ['icc_profile','exif','xmp']:
   if im.info.get(tag):opts[tag]=im.info[tag]
  im.save(stream,**opts);result=stream.getvalue()
  with Image.open(io.BytesIO(result)) as decoded:
   assert decoded.size==im.size
   assert decoded.convert('RGBA').getchannel('A').tobytes()==rgba.getchannel('A').tobytes(),'Alpha changed'
  checks.append({'source_sha256':key,'width':im.width,'height':im.height,'before_bytes':len(data),'after_bytes':len(result)})
 cache[key]=result;return result
def run():
 before=sum(p.stat().st_size for p in (ROOT/'assets-3d').rglob('*') if p.is_file());mapping={};changed=[]
 pngs=sorted((ROOT/'assets-3d').rglob('*.png'))+sorted((ROOT/'assets/backgrounds').glob('*.png'))
 for i,p in enumerate(pngs,1):
  data=p.read_bytes();encoded=webp(data);dest=p.with_suffix('.webp');backup(p);dest.write_bytes(encoded);assert dest.is_file();p.unlink();mapping[str(p.relative_to(ROOT))]=str(dest.relative_to(ROOT));changed.append(str(dest.relative_to(ROOT)))
  if i%15==0:print(f'PNG: {i}/{len(pngs)}',flush=True)
 svgs=sorted((ROOT/'assets-3d').rglob('*.svg'))
 for i,p in enumerate(svgs,1):
  data=p.read_bytes();encoded=PATTERN.sub(lambda m:b'data:image/webp;base64,'+base64.b64encode(webp(base64.b64decode(m[1],validate=True))),data)
  if encoded!=data:
   assert PATTERN.sub(b'PAYLOAD',data)==re.sub(rb'data:image/webp;base64,[A-Za-z0-9+/=]+',b'PAYLOAD',encoded)
   backup(p);p.write_bytes(encoded);changed.append(str(p.relative_to(ROOT)))
  if i%200==0:print(f'SVG: {i}/{len(svgs)}',flush=True)
 # Update literal asset references in source, configuration and preview pages.
 for p in ROOT.rglob('*'):
  if not p.is_file() or any(x in p.parts for x in ['.git','output','__pycache__']):continue
  if p.suffix not in ['.html','.js','.css','.json','.py','.md','.svg','.webmanifest']:continue
  if p.name in ['ASSET-3D-COMPRESSION.json','convert_assets_webp85.py']:continue
  text=p.read_text();new=text
  for src,dest in mapping.items():new=new.replace(src,dest)
  if new!=text:p.write_text(new)
 after=sum(p.stat().st_size for p in (ROOT/'assets-3d').rglob('*') if p.is_file())
 report={'quality':85,'dimensions_preserved':True,'alpha_preserved':True,'before_assets3d_bytes':before,'after_assets3d_bytes':after,'saved_percent':round((before-after)/before*100,2),'png_files_converted':len(pngs),'unique_images_verified':len(checks),'backup':str(BACKUP),'mapping':mapping,'files_changed':changed,'image_checks':checks}
 (ROOT/'docs/ASSET-WEBP85.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps({k:v for k,v in report.items() if k not in ['mapping','files_changed','image_checks']}),flush=True)
if __name__=='__main__':run()
