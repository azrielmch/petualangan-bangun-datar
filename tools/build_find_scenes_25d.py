"""Reviewed regions for the selected clean 2.5D illustrations."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]

def B(id,label,shape,left,top,right,bottom,polygon=None):
    r={'cx':(left+right)/2,'cy':(top+bottom)/2,'rx':(right-left)/2,'ry':(bottom-top)/2}
    if polygon:r['polygon']=polygon
    elif shape in ['persegi','persegi-panjang']:r['polygon']=[[left,top],[right,top],[right,bottom],[left,bottom]]
    return {'id':id,'label':label,'shape':shape,'region':r}

def S(id,name,theme,shape,objects):
    file=ROOT/'assets-3d/find-scenes-25d'/f'{id}.webp'
    with Image.open(file) as im:w,h=im.size
    return {'id':id,'name':name,'themeId':theme,'themeName':{'kamar':'Kamar Anak','belajar':'Sekolah','dapur':'Dapur Ceria','taman':'Taman Sekolah','ruang':'Ruang Keluarga'}[theme],'targetShape':shape,'asset':str(file.relative_to(ROOT)),'width':w,'height':h,'style':'cartoon-2.5d','revision':hashlib.sha256(file.read_bytes()).hexdigest()[:12],'hotspots':objects,'targetCount':sum(o['shape']==shape for o in objects)}

scenes=[
 S('persegi-kamar','Kamar Baca 2.5D','kamar','persegi',[
  B('jendela','Jendela','persegi',4.5,4.4,29,39.9),
  B('bingkai','Bingkai biru','persegi',42.4,7.7,61.9,36.4),
  B('bantal','Bantal kuning','persegi',29.3,42.4,41.7,58.7),
  B('jam','Jam dinding','lingkaran',79.9,4.7,95.3,27.7),
  B('bendera','Bendera merah','segitiga',66.2,27.8,79.2,46.0),
  B('bingkai-bunga','Bingkai bunga','segi-lima',1.2,41.1,11.5,55.3),
  B('buku','Buku hijau','persegi-panjang',41.7,79.3,64.2,90.2),
  B('tatakan','Tatakan cangkir','lingkaran',69.4,82.1,80.8,90.5)]),
 S('persegi-kelas','Kelas Sekolah 2.5D','belajar','persegi',[
  B('jendela','Jendela','persegi',3.7,5.1,28.4,41.4),
  B('papan','Papan tulis','persegi',35.8,8.3,64.6,48),
  B('papan-gabus','Papan gabus','persegi',8.5,42.5,20.2,60.1),
  B('jam','Jam dinding','lingkaran',74.4,7.1,90.1,30.7),
  B('penggaris','Penggaris','segitiga',51.8,56.9,63.9,68.9),
  B('buku','Buku biru','persegi-panjang',63.2,59.6,81.2,67.5),
  B('bingkai-bunga','Bingkai bunga','segi-lima',86.8,34.7,97.5,49.6),
  B('penghapus','Penghapus','persegi-panjang',18.8,64.8,26.8,70.8)]),
 S('lingkaran-dapur','Dapur Sarapan 2.5D','dapur','lingkaran',[
  B('jam','Jam dinding','lingkaran',19.8,4.3,36.4,29.4),
  B('piring','Piring hias','lingkaran',70.8,4.8,86.8,29),
  B('tatakan','Tatakan bunga','lingkaran',46,31.8,55.8,46.7),
  B('ubin','Ubin hijau','persegi',45.8,5.8,60.2,27.2),
  B('buku','Buku resep','persegi-panjang',25.3,39.6,41.3,46.5),
  B('serbet','Serbet merah','segitiga',77,61.6,91,73.8),
  B('papan','Papan hijau','segi-lima',65.1,29.6,76.7,46.8),
  B('bantal','Bantal merah','persegi',20.8,58.7,40.8,85.3)]),
 S('lingkaran-ruang','Ruang Keluarga 2.5D','ruang','lingkaran',[
  B('cermin','Cermin','lingkaran',15.7,2.3,35.4,31),
  B('jam','Jam dinding','lingkaran',74.4,7.1,90,30.7),
  B('bantal-bulat','Bantal kuning','lingkaran',13.9,38.2,28,57.9),
  B('bantal-merah','Bantal merah','persegi',77,34.8,92,55.3),
  B('bendera','Bendera merah','segitiga',43.3,6.6,64.8,27.1),
  B('bingkai-bunga','Bingkai bunga','segi-lima',49.6,59.5,61.5,76.4),
  B('buku','Buku biru','persegi-panjang',75.4,79.8,96.6,91.5),
  B('remot','Remot','persegi-panjang',31.1,70.7,45.7,78.1)]),
 S('segitiga-taman','Halaman Sekolah 2.5D','taman','segitiga',[
  B('bendera','Bendera kuning','segitiga',28.1,15.8,40.3,31),
  B('papan','Papan tanaman','segitiga',51.4,14.7,68.4,36.2),
  B('penggaris','Penggaris','segitiga',76.6,34.2,92.2,54.3),
  B('jam','Jam taman','lingkaran',7.5,14.1,22.5,36.2),
  B('bantal','Bantal merah','persegi',30.8,39.8,43.4,57.5),
  B('bingkai','Bingkai kayu','segi-lima',81.1,16.3,93.5,33),
  B('buku','Buku berkebun','persegi-panjang',71.4,69.2,93.5,79.7),
  B('piring','Piring','lingkaran',52.8,56.8,67.7,79.1)]),
 S('segitiga-kelas','Ruang Belajar Sekolah 2.5D','belajar','segitiga',[
  B('bendera','Bendera merah','segitiga',6.5,5.2,22.8,22.1),
  B('rambu','Rambu kuning','segitiga',79.1,6.5,97,30.5),
  B('penggaris','Penggaris','segitiga',43.4,46.5,59.8,66.8),
  B('jendela','Jendela','persegi',27.8,4.7,53,40.5),
  B('jam','Jam dinding','lingkaran',56.9,7.3,74,33.2),
  B('bingkai','Bingkai bunga','segi-lima',5.4,24.9,18.9,43.5),
  B('buku','Buku biru','persegi-panjang',60.5,57.4,79.1,67),
  B('tempat-pensil','Tempat pensil','other',26.6,44.4,35,65.6)]),
 S('persegi-panjang-kamar','Kamar Tidur 2.5D','kamar','persegi-panjang',[
  B('pintu','Pintu','persegi-panjang',74.1,1.4,95.7,67.8),
  B('buku','Buku di meja','persegi-panjang',51.3,40.7,65.2,47.2),
  B('remot','Remot','persegi-panjang',26.4,84.3,46.1,92.8),
  B('bantal-putih','Bantal putih','persegi-panjang',4.3,41.3,27.1,53.5),
  B('jendela','Jendela','persegi',6,3.9,26,32.6),
  B('jam','Jam dinding','lingkaran',51.5,6.4,65,26.6),
  B('bingkai','Bingkai bunga','segi-lima',33.1,14.4,43.1,28.3),
  B('penggaris','Penggaris','segitiga',71.7,79.7,87.6,94.3),
  B('bantal','Bantal merah','persegi',8.9,39.7,21.2,55.6)]),
 S('persegi-panjang-dapur','Dapur Hangat 2.5D','dapur','persegi-panjang',[
  B('lukisan','Lukisan daun','persegi-panjang',3.8,8.5,40.8,27.4),
  B('buku','Buku resep','persegi-panjang',7,43.4,27.2,50.5),
  B('alas','Alas makan','persegi-panjang',55.5,70.1,93.8,80.8),
  B('jam','Jam dinding','lingkaran',72.8,5.6,90.1,31.5),
  B('ubin','Ubin biru','persegi',47.2,9.8,62.3,31),
  B('serbet','Serbet merah','segitiga',13.4,64.3,35.7,80.5),
  B('tatakan','Tatakan kuning','segi-lima',65.2,34.1,77.3,50.2),
  B('piring','Piring','lingkaran',37.8,46.8,55.5,73.1)]),
 S('segi-lima-taman','Taman Sekolah 2.5D','taman','segi-lima',[
  B('papan','Papan kayu','segi-lima',49.9,10,65.3,32.5),
  B('benih','Kartu benih','segi-lima',4.1,27.7,16.2,45.3),
  B('biskuit','Biskuit','segi-lima',70.8,58.1,86.1,81),
  B('jam','Jam taman','lingkaran',74.8,14.4,90.5,38),
  B('bantal','Bantal merah','persegi',16.7,26.3,30.8,45.4),
  B('penanda','Penanda tanaman','segitiga',36.5,27.4,41.9,36.6),
  B('buku','Buku berkebun','persegi-panjang',23,68.6,49,81.2),
  B('tatakan','Tatakan biru','lingkaran',51.4,68.4,65,80.5)]),
 S('segi-lima-ruang','Ruang Santai 2.5D','ruang','segi-lima',[
  B('cermin','Cermin','segi-lima',6.6,18.2,21.5,38.4),
  B('bingkai','Bingkai bunga','segi-lima',43,48.7,56.3,69.6),
  B('bantal-pink','Bantal merah muda','segi-lima',9.4,61.8,29.1,88),
  B('jam','Jam dinding','lingkaran',40.1,1.6,56.6,26.4),
  B('bantal-kuning','Bantal kuning','persegi',77.9,31.6,91.3,50.6),
  B('penggaris','Penggaris','segitiga',81.2,73.3,95.8,91.5),
  B('buku','Buku biru','persegi-panjang',55.8,63.5,73.8,73.1),
  B('piring','Piring hias','lingkaran',22.9,40.8,33.4,56.4)])]

assert len(scenes)==10
for scene in scenes:assert scene['targetCount']>=3
(ROOT/'content/find-scenes.json').write_text(json.dumps(scenes,ensure_ascii=False,indent=2))
print(f'{len(scenes)} clean 2.5D illustrations; {sum(len(s["hotspots"]) for s in scenes)} reviewed object regions')
