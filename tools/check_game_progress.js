const assert=require('node:assert/strict');
const saved=new Map();global.localStorage={getItem:k=>saved.get(k)||null,setItem:(k,v)=>saved.set(k,v)};
let P=require('../content/game-progress.js');assert.equal(P.settings().teacherMode,false);
for(const game of Object.keys(P.GAMES)){
 assert.equal(P.summary(game).score,null);P.record(game,5,0);assert.equal(P.summary(game).complete,false);assert.equal(P.summary(game).nextLevel,1);
 P.record(game,1,2);P.record(game,1,99);assert.equal(P.summary(game).mistakes,2);
 for(const n of [2,3,4])P.record(game,n,1);
 const s=P.summary(game);assert(s.complete);assert.equal(s.completed,5);assert.equal(s.mistakes,5);assert.equal(s.score,90);assert.equal(s.stars,4.5);
}
P.setSound(false);P.setTeacherMode(true);delete require.cache[require.resolve('../content/game-progress.js')];P=require('../content/game-progress.js');assert.equal(P.settings().sound,false);assert.equal(P.settings().teacherMode,true);P.setTeacherMode(false);assert.equal(P.settings().teacherMode,false);assert.equal(P.summary('find').score,90);
P.restart('find');assert.equal(P.summary('find').completed,0);assert.equal(P.summary('puzzle').completed,5);assert.equal(P.summary('matching').completed,5);
assert.equal(P.score(0),100);assert.equal(P.score(1),90);assert.equal(P.score(5),90);assert.equal(P.score(6),80);assert.equal(P.score(500),0);
assert.throws(()=>P.record('find',6,0));assert.throws(()=>P.record('other',1,0));
console.log('Three separate games: five-level completion, real mistakes, score/star boundaries, no duplicate records, persistence, sound/teacher preferences and independent replay verified.');
