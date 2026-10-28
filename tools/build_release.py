"""Bundle the complete static game and its referenced assets."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
files=[ROOT/'manifest.webmanifest']+list((ROOT/'assets-3d').rglob('*'))+list((ROOT/'assets/backgrounds').glob('*.webp'))+list((ROOT/'content').rglob('*'))+list((ROOT/'docs').glob('*'))+list((ROOT/'tools').glob('*.py'))+list((ROOT/'tools').glob('*.js'))+list((ROOT/'style-options/puzzle').glob('*'))
files += [ROOT/p for p in ['README.md','index.html','results.html','asset-catalog.html','asset-catalog-3d.html','find.html','find-layout-preview.html','puzzle.html','matching.html','style-options/selected-style.json','style-options/school-02-soft-25d.png']]
with ZipFile(ROOT/'petualangan-bangun-datar-assets-3d.zip','w',ZIP_DEFLATED) as z:
 for p in files:
  if p.is_file():z.write(p,p.relative_to(ROOT))
print('Paket lengkap: beranda, tiga game, hasil akhir, aset, dokumentasi, dan sumber pembangun.')
