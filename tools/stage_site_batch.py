from pathlib import Path
import json,sys,shutil
root=Path(__file__).resolve().parents[1]
p=json.loads((root/'sites/upload-batches.json').read_text());idx=int(sys.argv[1]);source=Path(p['source']);destination=Path(p['destination'])
for ref in p['batches'][idx]:
 out=destination/ref;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/ref,out)
print(f'Tahap {idx+1}/{len(p["batches"])} siap.')
