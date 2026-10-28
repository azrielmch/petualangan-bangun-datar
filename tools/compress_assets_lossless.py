"""Lossless PNG compression, including PNG payloads embedded in SVG.

Keeps PNG dimensions, sample format, palette, transparency and every non-IDAT
chunk. Only accepts smaller output after verifying identical decoded samples.
SVG markup outside embedded PNG base64 payloads remains byte-for-byte intact.
"""
from pathlib import Path
import base64,hashlib,io,json,re,struct,time,zlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SIGNATURE=b'\x89PNG\r\n\x1a\n'
PNG_DATA=re.compile(rb'(data:image/png;base64,)([A-Za-z0-9+/=]+)')
cache={}

def chunks(data):
    assert data.startswith(SIGNATURE)
    pos=8;result=[]
    while pos<len(data):
        size=struct.unpack('>I',data[pos:pos+4])[0]
        kind=data[pos+4:pos+8];body=data[pos+8:pos+8+size]
        raw=data[pos:pos+12+size]
        assert len(raw)==size+12
        result.append((kind,body,raw));pos+=size+12
    return result

def chunk(kind,body):
    return struct.pack('>I',len(body))+kind+body+struct.pack('>I',zlib.crc32(kind+body)&0xffffffff)

def pixels(data):
    with Image.open(io.BytesIO(data)) as im:
        im.load();return im.mode,im.size,im.tobytes()

def optimize_png(data):
    key=hashlib.sha256(data).hexdigest()
    if key in cache:return cache[key]
    old=chunks(data)
    if any(k==b'acTL' for k,_,_ in old):cache[key]=data;return data
    packed=b''.join(b for k,b,_ in old if k==b'IDAT')
    candidates=[packed,zlib.compress(zlib.decompress(packed),9)]
    with Image.open(io.BytesIO(data)) as image:
        image.load();stream=io.BytesIO();image.save(stream,format='PNG',optimize=True,compress_level=9)
    proposed=chunks(stream.getvalue())
    # The encoded sample interpretation must match the original exactly.
    for kind in [b'IHDR',b'PLTE',b'tRNS']:
        if [b for k,b,_ in old if k==kind]!=[b for k,b,_ in proposed if k==kind]:break
    else:candidates.append(b''.join(b for k,b,_ in proposed if k==b'IDAT'))
    best=min(candidates,key=len)
    result=bytearray(SIGNATURE);inserted=False
    for k,b,raw in old:
        if k==b'IDAT':
            if not inserted:result.extend(chunk(k,best));inserted=True
        else:result.extend(raw)
    result=bytes(result)
    if len(result)>=len(data):result=data
    assert pixels(data)==pixels(result),'Pixel mismatch'
    assert [(k,b) for k,b,_ in old if k!=b'IDAT']==[(k,b) for k,b,_ in chunks(result) if k!=b'IDAT'],'Metadata mismatch'
    cache[key]=result;return result

def run():
    directory=ROOT/'assets-3d';files=sorted(p for p in directory.rglob('*') if p.is_file() and p.suffix.lower() in ['.png','.svg'])
    before=sum(p.stat().st_size for p in directory.rglob('*') if p.is_file())
    rows=[];started=time.monotonic()
    for index,path in enumerate(files,1):
        source=path.read_bytes();embedded=0
        if path.suffix.lower()=='.png':result=optimize_png(source)
        else:
            def replace(match):
                nonlocal embedded
                embedded+=1
                raw=base64.b64decode(match[2],validate=True)
                return match[1]+base64.b64encode(optimize_png(raw))
            result=PNG_DATA.sub(replace,source)
            assert PNG_DATA.sub(b'PNG_PAYLOAD',source)==PNG_DATA.sub(b'PNG_PAYLOAD',result),'SVG markup changed'
        if len(result)<len(source):
            temporary=path.with_name(path.name+'.lossless-tmp');temporary.write_bytes(result);temporary.replace(path)
            rows.append({'path':str(path.relative_to(ROOT)),'before_bytes':len(source),'after_bytes':len(result),'embedded_pngs':embedded})
        if index%20==0 or index==len(files):
            saved=sum(r['before_bytes']-r['after_bytes'] for r in rows)
            print(f'{index}/{len(files)} files checked; {saved/1024/1024:.1f} MiB saved; {len(cache)} unique PNGs verified',flush=True)
    after=sum(p.stat().st_size for p in directory.rglob('*') if p.is_file())
    report={'method':'lossless PNG IDAT optimization; all non-IDAT metadata and SVG markup retained','before_bytes':before,'after_bytes':after,'saved_bytes':before-after,'saved_percent':round((before-after)/before*100,2),'unique_pngs_verified':len(cache),'files_checked':len(files),'files_changed':len(rows),'elapsed_seconds':round(time.monotonic()-started,1),'files':rows}
    output=ROOT/'docs/ASSET-3D-COMPRESSION.json';output.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='files'}),flush=True)
if __name__=='__main__':run()
