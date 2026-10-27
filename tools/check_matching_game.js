const assert=require('node:assert/strict'),c=require('../content/game-content.json'),R=require('../content/randomizer.js'),G=require('../content/matching-game.js');
const modes=[['shape','name'],['shape','object'],['object','name'],['shape','features'],['object','features']];
for(let level=1;level<=5;level++)for(let run=0;run<50;run++){
 const r=R.createRound(c,'matching',level),s=G.createState();assert.equal(r.left.length,5);assert.equal(r.right.length,5);assert.equal(r.leftType,modes[level-1][0]);assert.equal(r.rightType,modes[level-1][1]);
 const l=r.left[0],wrong=r.right.find(x=>x.shapeId!==l.shapeId),correct=r.right.find(x=>x.shapeId===l.shapeId);
 assert.equal(G.answer(r,s,l.id,wrong.id),'wrong');assert.equal(s.mistakes,1);assert.equal(s.matched.length,0);
 assert.equal(G.answer(r,s,l.id,correct.id),'correct');assert.equal(s.wrong,null);assert.equal(G.answer(r,s,l.id,correct.id),'ignored');
 for(const x of r.left.slice(1))assert.equal(G.answer(r,s,x.id,r.right.find(y=>y.shapeId===x.shapeId).id),'correct');
 assert(s.complete);assert.equal(s.matched.length,5);assert.equal(G.answer(r,s,l.id,wrong.id),'ignored');
 const next=R.createRound(c,'matching',level,r);for(const sh of c.shapes)assert.notEqual(next.objectIds[sh.id],r.objectIds[sh.id]);
}
console.log('250 matching rounds: five modes, five pairs, wrong retry, correct connection, locked pairs, completion and fresh objects verified.');
