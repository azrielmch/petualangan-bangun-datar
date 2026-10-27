const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),config=JSON.parse(fs.readFileSync(path.join(root,'content/game-content.json'),'utf8'));
const {createRound}=require('../content/randomizer.js');
let seed=23579;const rng=()=>((seed=(Math.imul(seed,1664525)+1013904223)>>>0)/4294967296);
const sig=a=>[...a].sort().join('|');
assert.equal(config.themes.length,5);assert.equal(config.objects.length,40);assert.equal(config.puzzle.variants.length,25);
assert.deepEqual(config.puzzle.levels.map(l=>l.pieceCount),[4,4,6,6,8]);
assert.deepEqual(config.matching.levels.map(l=>[l.leftType,l.rightType]),[['shape','name'],['shape','object'],['object','name'],['shape','features'],['object','features']]);
for(const obj of config.objects)assert.ok(fs.existsSync(path.join(root,obj.asset)),obj.asset);
for(const theme of config.themes){assert.ok(fs.existsSync(path.join(root,theme.background)));for(const shape of config.shapes){const pool=theme.objectPools[shape.id];assert.ok(pool.length>=6);for(const id of pool)assert.equal(config.objects.find(o=>o.id===id).shape,shape.id);}}
for(const v of config.puzzle.variants)assert.ok(fs.existsSync(path.join(root,v.asset)));
for(const game of ['find','puzzle','matching']){
  assert.equal(config[game].levels.length,5);
  for(let level=1;level<=5;level++){
    let previous=null;const themes=new Set(),variants=new Set(),targetSets=new Set();
    for(let i=0;i<400;i++){
      const r=createRound(config,game,level,previous,rng);
      if(game==='find'){
        assert.equal(r.targetCount,3);assert.ok(r.targetIds.length>=3);assert.ok(r.distractorIds.length>=5);assert.equal(new Set(r.objects.map(o=>o.id)).size,r.objects.length);assert.ok(r.scene.asset);
        assert.ok(r.objects.filter(o=>o.isTarget).every(o=>o.shape===r.targetShape));assert.ok(r.objects.filter(o=>!o.isTarget).every(o=>o.shape!==r.targetShape));
        if(previous){assert.notEqual(r.sceneId,previous.sceneId);assert.notEqual(sig(r.targetIds),sig(previous.targetIds));}
        themes.add(r.themeId);targetSets.add(sig(r.targetIds));
      }else if(game==='puzzle'){
        assert.equal(r.pieceCount,[4,4,6,6,8][level-1]);assert.equal(r.layout.pieces.length,r.pieceCount);assert.equal(new Set(r.pieceOrder).size,r.pieceCount);assert.equal(r.variant.shape,r.shapeId);assert.equal(r.variant.theme,r.themeId);assert.equal(r.layout.shape,r.shapeId);
        if(previous){assert.notEqual(r.themeId,previous.themeId);assert.notEqual(r.shapeId,previous.shapeId);}
        themes.add(r.themeId);variants.add(r.variant.id);
      }else{
        assert.equal(r.left.length,5);assert.equal(r.right.length,5);assert.equal(r.pairs.length,5);
        for(const pair of r.pairs){const left=r.left.find(x=>x.id===pair.leftId),right=r.right.find(x=>x.id===pair.rightId);assert.equal(left.shapeId,right.shapeId);assert.equal(left.shapeId,pair.shapeId);if(previous)assert.notEqual(r.objectIds[pair.shapeId],previous.objectIds[pair.shapeId]);}
      }
      previous=r;
    }
    if(game==='puzzle')assert.equal(themes.size,5);
    if(game==='find'){assert.equal(themes.size,2);assert.equal(targetSets.size,2);}
    if(game==='puzzle')assert.equal(variants.size,25);
    console.log(game+' level '+level+': 400 sessions verified');
  }
}
assert.throws(()=>createRound(config,'find',6),/Level tidak tersedia/);
console.log('15 levels, 5 themes, 40 objects, 25 puzzle masters, and 6,000 random sessions verified');
