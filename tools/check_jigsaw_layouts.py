from collections import Counter,defaultdict
from pathlib import Path
import json,re,xml.etree.ElementTree as ET
from jigsaw_layouts import all_layouts

root=Path(__file__).resolve().parents[1]
layouts=all_layouts()
assert [x['pieceCount'] for x in layouts]==[4,4,6,6,8]
for layout in layouts:
    assert len(layout['pieces'])==layout['pieceCount']
    cells=Counter(tuple(c) for p in layout['pieces'] for c in p['cells'])
    expected={(x,y) for y in range(2) for x in range(layout['columns'])}
    assert set(cells)==expected and all(n==1 for n in cells.values()),'Gap or overlap'
    shared=defaultdict(list)
    for p in layout['pieces']:
        assert p['path'].startswith('M') and p['path'].endswith('Z')
        for e in p['sharedEdges']:shared[tuple(map(tuple,e['edge']))].append(e['direction'])
        f=root/'assets-3d/puzzles'/f'piece-{layout["shape"]}-{p["id"]+1}.svg'
        ET.parse(f)
    assert all(sorted(d)==[-1,1] for d in shared.values()),'Unmatched connector'
    files=[p for p in (root/'assets-3d/puzzles').glob('piece-*.svg') if re.fullmatch('piece-'+re.escape(layout['shape'])+r'-\d+',p.stem)]
    assert len(files)==layout['pieceCount'],'Unexpected leftover pieces'
    assert sum(1 for _ in shared)>=layout['pieceCount']-1
    print(f'Level {layout["level"]}: {layout["pieceCount"]} pieces; full coverage; complementary connectors')
index=json.loads((root/'assets-3d/puzzles/jigsaw-layout.json').read_text())
assert index['levels']==layouts
assert len(list((root/'assets-3d/puzzles').glob('piece-*.svg')))==28
manifest=json.loads((root/'assets-3d/manifest.json').read_text())
for layout in layouts:
    for item in manifest:
        if item['type']=='puzzles' and item.get('shape')==layout['shape']:
            assert item['pieces']==layout['pieceCount'] and item['level']==layout['level']
print('28 piece assets and all level metadata verified')
