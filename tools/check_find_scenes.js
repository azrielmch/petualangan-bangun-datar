const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),config=JSON.parse(fs.readFileSync(path.join(root,'content/game-content.json'),'utf8'));
const {createRound}=require('../content/randomizer.js'),{createState,answer}=require('../content/find-game.js');
assert.equal(config.find.scenes.length,10);
const classroom=config.find.scenes.find(s=>s.id==='persegi-kelas');
assert.ok(classroom.hotspots.some(o=>o.id==='papan-gabus'&&o.shape==='persegi'));
assert.ok(classroom.hotspots.some(o=>o.id==='penghapus'&&o.shape==='persegi-panjang'));
assert.ok(!classroom.hotspots.some(o=>o.id==='bantal'||o.id==='piring'));
const schoolroom=config.find.scenes.find(s=>s.id==='segitiga-kelas');
assert.ok(schoolroom.hotspots.some(o=>o.id==='tempat-pensil'));
assert.ok(!schoolroom.hotspots.some(o=>o.id==='rebana'));
for(const level of config.find.levels)assert.equal(level.sceneIds.length,2);
let total=0;
for(const scene of config.find.scenes){
  const data=fs.readFileSync(path.join(root,scene.asset));assert.equal(data.readUInt32BE(16),scene.width);assert.equal(data.readUInt32BE(20),scene.height);
  assert.ok(scene.hotspots.filter(o=>o.shape===scene.targetShape).length>=3);
  assert.ok(scene.hotspots.filter(o=>o.shape!==scene.targetShape).length>=5);
  assert.equal(new Set(scene.hotspots.map(o=>o.id)).size,scene.hotspots.length);
  for(const o of scene.hotspots){const r=o.region;assert.ok(r.rx>0&&r.ry>0);assert.ok(r.cx-r.rx>=0&&r.cx+r.rx<=100&&r.cy-r.ry>=0&&r.cy+r.ry<=100,o.id);if(r.polygon)for(const [x,y] of r.polygon)assert.ok(x>=0&&x<=100&&y>=0&&y<=100);
    const ratio=r.rx*scene.width/(r.ry*scene.height);
    if(o.shape==='persegi')assert.ok(ratio>=.83&&ratio<=1.2,'Square visual bounds: '+scene.id+':'+o.id+' '+ratio);
    if(o.shape==='persegi-panjang')assert.ok(Math.max(ratio,1/ratio)>=1.8,'Rectangle too close to square: '+scene.id+':'+o.id);
  }
  const level=config.find.levels.find(l=>l.targetShape===scene.targetShape),alternate=level.sceneIds.find(id=>id!==scene.id);
  const round=createRound(config,'find',level.level,{sceneId:alternate},()=>0);assert.equal(round.sceneId,scene.id);
  const state=createState(round),wrong=round.distractorIds[0],first=round.targetIds[0];
  assert.equal(answer(round,state,undefined).kind,'background');assert.equal(state.mistakes,0);
  assert.equal(answer(round,state,wrong).kind,'wrong');assert.equal(state.mistakes,1);assert.deepEqual(state.wrongIds,[wrong]);
  assert.equal(answer(round,state,wrong).kind,'wrong');assert.equal(state.mistakes,2);assert.equal(state.wrongIds.length,1);
  assert.equal(answer(round,state,first).kind,'correct');assert.equal(state.foundIds.length,1);
  assert.equal(answer(round,state,first).kind,'already-found');assert.equal(state.foundIds.length,1);assert.equal(state.mistakes,2);
  for(const id of round.targetIds.slice(1,round.targetCount))answer(round,state,id);
  assert.ok(state.complete);assert.equal(state.foundIds.length,3);
  answer(round,state,wrong);assert.equal(state.mistakes,2);
  const next=createRound(config,'find',level.level,round,()=>0);assert.notEqual(next.sceneId,round.sceneId);assert.equal(createState(next).foundIds.length,0);
  total+=scene.hotspots.length;
}
console.log('10 integrated scenes, '+total+' object regions, 3+ targets per image, 5+ distractors, green/red answer state, no double counting, completion and replay verified');
console.log('Reviewed square regions remain near 1:1; rectangle regions have a visibly elongated aspect ratio of at least 1.8:1');
