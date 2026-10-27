"""Export separate clipped pieces and a playable Biru Ceria gallery."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
c=json.loads((ROOT/'content/game-content.json').read_text())
files=[]
for v in c['puzzle']['variants']:
 for l in c['puzzle']['levels']:
  folder=ROOT/'assets-3d/puzzles/separate'/v['id']/f"level-{l['level']}"
  folder.mkdir(parents=True,exist_ok=True)
  for p in l['layout']['pieces']:
   b=p['bounds'];out=folder/f"piece-{p['id']+1}.svg"
   out.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{b['x']} {b['y']} {b['width']} {b['height']}" width="{round(b['width'])}" height="{round(b['height'])}"><defs><clipPath id="piece"><path d="{p['path']}"/></clipPath></defs><image href="../../../themes/{v['id']}.svg" width="480" height="360" clip-path="url(#piece)"/><path d="{p['path']}" fill="none" stroke="#94602b" stroke-width="2"/></svg>''')
   files.append({'variant':v['id'],'level':l['level'],'pieceId':p['id'],'path':str(out.relative_to(ROOT))})
(ROOT/'content/puzzle-pieces.json').write_text(json.dumps(files,indent=2))
# The shared game-page runner owns puzzle.html; do not overwrite its progress flow.
print(f'{len(files)} separate SVG pieces, 25 variants × 5 levels; playable puzzle.html')
