const assert=require('node:assert/strict');
const c=require('../content/game-content.json'),R=require('../content/randomizer.js'),G=require('../content/puzzle-game.js');
for(let level=1;level<=5;level++)for(let session=0;session<50;session++){
 const r=R.createRound(c,'puzzle',level),s=G.createState(r),positions=G.trayPositions(r);
 assert.equal(r.pieceCount,[4,4,6,6,8][level-1]);assert.equal(new Set(positions.map(p=>p.id)).size,r.pieceCount);
 for(const pos of positions){const b=r.layout.pieces.find(p=>p.id===pos.id).bounds;assert(pos.x+b.x*pos.scale>=890);assert(pos.x+(b.x+b.width)*pos.scale<1420);assert(pos.y+b.y*pos.scale>=320);assert(pos.y+(b.y+b.height)*pos.scale<790);}
 const id=r.layout.pieces[0].id;assert.equal(G.place(r,s,id,1000,300),'wrong');assert.equal(s.placedIds.length,0);
 assert.equal(G.place(r,s,id,G.BOARD.x,G.BOARD.y),'correct');assert.equal(G.place(r,s,id,G.BOARD.x,G.BOARD.y),'ignored');
 for(const p of r.layout.pieces.slice(1))G.place(r,s,p.id,G.BOARD.x,G.BOARD.y);
 assert(s.complete);assert.equal(s.placedIds.length,r.pieceCount);assert.equal(s.mistakes,1);
}
console.log('250 rounds: shuffled separate pieces, tray bounds, incorrect drop, snap, no double count, all five levels complete.');
