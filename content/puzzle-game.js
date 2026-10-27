(function(root){
'use strict';
const BOARD={x:218,y:342,scale:1.16};
function createState(round){return {placedIds:[],mistakes:0,complete:false,pieceCount:round.pieceCount};}
function place(round,state,id,x,y){
 const p=round.layout.pieces.find(p=>p.id===id);
 if(!p||state.complete||state.placedIds.includes(id))return 'ignored';
 if(Math.hypot(x-BOARD.x,y-BOARD.y)<=48){state.placedIds.push(id);state.complete=state.placedIds.length===state.pieceCount;return 'correct';}
 state.mistakes++;return 'wrong';
}
function trayPositions(round,rng=Math.random){
 const cols=round.layout.columns,rows=round.layout.rows,cw=500/cols,ch=440/rows;
 return round.pieceOrder.map((id,i)=>{const p=round.layout.pieces.find(p=>p.id===id),b=p.bounds;const scale=Math.min((cw-22)/b.width,(ch-24)/b.height,1);
 return {id,scale,x:900+(i%cols)*cw+(cw-b.width*scale)/2-b.x*scale+(rng()-.5)*8,y:330+Math.floor(i/cols)*ch+(ch-b.height*scale)/2-b.y*scale+(rng()-.5)*8};});
}
function mount(container,round,{onNext,onComplete,shapeName='Bangun Datar'}={}){
 root.LevelCelebration?.clear(container);
 const state=createState(round),ns='http://www.w3.org/2000/svg',uid='jg-'+Math.random().toString(36).slice(2),positions=trayPositions(round),nodes=new Map();let drag=null,selected=null,notified=false,soundEnabled=root.GameProgress?.settings().sound??true;
 container.innerHTML=`<div class="jigsaw-game"><img class="jigsaw-shell" src="assets-3d/ui/puzzle-biru-shell.png" alt="" draggable="false"><a class="jigsaw-back" href="index.html" aria-label="Kembali ke beranda"></a><button class="jigsaw-sound" type="button" aria-label="Matikan suara" aria-pressed="true"></button><div class="jigsaw-level ${shapeName.length>10?'long':''}">Level ${round.level} · ${shapeName}</div><div class="jigsaw-counter" aria-live="polite">0/${round.pieceCount} keping</div><svg class="jigsaw-overlay" viewBox="0 0 1536 1024" aria-label="Papan puzzle kosong dan kepingan terpisah"><defs></defs><g class="jigsaw-placed"></g><g class="jigsaw-loose"></g></svg><p class="jigsaw-instruction">Susun ${round.pieceCount} keping puzzle!</p></div><p class="jigsaw-feedback" role="status">Geser keping dari kanan ke papan kiri. Bisa juga pilih keping, lalu klik papan.</p><div class="jigsaw-win" hidden><img src="assets-3d/ui/banner-completed.png" alt="Completed"><button type="button">${round.level<5?'Lanjut level berikutnya':'Main lagi dari level 1'}</button></div>`;
 const svg=container.querySelector('svg'),defs=svg.querySelector('defs'),loose=svg.querySelector('.jigsaw-loose'),placed=svg.querySelector('.jigsaw-placed'),feedback=container.querySelector('.jigsaw-feedback');
 function elem(name,attrs){const e=document.createElementNS(ns,name);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);return e;}
 for(const pos of positions){const p=round.layout.pieces.find(p=>p.id===pos.id),clip=elem('clipPath',{id:uid+'-'+p.id});clip.append(elem('path',{d:p.path}));defs.append(clip);
 const g=elem('g',{'data-piece':p.id,role:'button',tabindex:0,'aria-label':'Keping '+(p.id+1),class:'jigsaw-piece'});
 g.append(elem('image',{href:round.variant.asset+'?v=biru-ceria-2',width:480,height:360,'clip-path':`url(#${uid}-${p.id})`}));g.append(elem('path',{d:p.path,fill:'transparent',stroke:'#94602b','stroke-width':2}));loose.append(g);nodes.set(p.id,{g,pos,p});transform(g,pos);}
 function transform(g,p){g.setAttribute('transform',`translate(${p.x} ${p.y}) scale(${p.scale})`);}
 function point(e){const p=svg.createSVGPoint();p.x=e.clientX;p.y=e.clientY;return p.matrixTransform(svg.getScreenCTM().inverse());}
 function tone(){root.GameAudio?.play(state.complete?'complete':'correct');}
 container.querySelector('.jigsaw-sound').addEventListener('click',e=>{soundEnabled=!soundEnabled;root.GameProgress?.setSound(soundEnabled);e.currentTarget.setAttribute('aria-pressed',String(soundEnabled));e.currentTarget.setAttribute('aria-label',soundEnabled?'Matikan suara':'Nyalakan suara');e.currentTarget.classList.toggle('muted',!soundEnabled);});
 function finish(id,x,y){const n=nodes.get(id),result=place(round,state,id,x,y);n.g.classList.remove('selected');selected=null;
 if(result==='wrong')root.GameAudio?.play('wrong');if(result==='correct'){tone();transform(n.g,BOARD);placed.append(n.g);n.g.setAttribute('aria-disabled','true');n.g.setAttribute('tabindex','-1');feedback.textContent=state.complete?'Hebat! Puzzle sudah lengkap.':'Benar! Lanjutkan keping berikutnya.';}
 else{transform(n.g,n.pos);feedback.textContent='Belum pas. Coba letakkan di posisi lain, ya.';}
 container.querySelector('.jigsaw-counter').textContent=`${state.placedIds.length}/${round.pieceCount} keping`;container.querySelector('.jigsaw-win').hidden=!state.complete;if(state.complete&&!notified){notified=true;onComplete?.(state);}}
 svg.addEventListener('pointerdown',e=>{const g=e.target.closest('[data-piece]');if(!g||g.getAttribute('aria-disabled')==='true')return;e.preventDefault();const id=Number(g.dataset.piece),n=nodes.get(id),q=point(e),b=n.p.bounds;selected=id;loose.append(g);g.classList.add('selected');drag={id,start:q,offsetX:b.x+b.width/2,offsetY:b.y+b.height/2,moved:false};svg.setPointerCapture(e.pointerId);});
 svg.addEventListener('pointermove',e=>{if(!drag)return;const q=point(e);if(Math.hypot(q.x-drag.start.x,q.y-drag.start.y)>5)drag.moved=true;if(drag.moved)transform(nodes.get(drag.id).g,{x:q.x-drag.offsetX*BOARD.scale,y:q.y-drag.offsetY*BOARD.scale,scale:BOARD.scale});});
 svg.addEventListener('pointerup',e=>{if(!drag)return;const d=drag;drag=null;if(svg.hasPointerCapture(e.pointerId))svg.releasePointerCapture(e.pointerId);if(d.moved){const q=point(e);finish(d.id,q.x-d.offsetX*BOARD.scale,q.y-d.offsetY*BOARD.scale);}});
 svg.addEventListener('pointercancel',()=>{if(drag){const n=nodes.get(drag.id);transform(n.g,n.pos);n.g.classList.remove('selected');drag=null;selected=null;}});
 svg.addEventListener('click',e=>{if(e.target.closest('[data-piece]')||selected===null)return;const q=point(e),n=nodes.get(selected),b=n.p.bounds;finish(selected,q.x-(b.x+b.width/2)*BOARD.scale,q.y-(b.y+b.height/2)*BOARD.scale);});
 svg.addEventListener('keydown',e=>{const g=e.target.closest('[data-piece]');if(!g||g.getAttribute('aria-disabled')==='true')return;const id=Number(g.dataset.piece),n=nodes.get(id);if(e.key==='Enter'||e.key===' '){e.preventDefault();selected=id;n.g.classList.add('selected');feedback.textContent='Gunakan tombol panah untuk menggeser, lalu Enter untuk meletakkan.';if(n.keyboard){finish(id,n.keyboard.x,n.keyboard.y);delete n.keyboard;}else n.keyboard={x:BOARD.x+90,y:BOARD.y+90,scale:BOARD.scale};}else if(e.key.startsWith('Arrow')){e.preventDefault();n.keyboard=n.keyboard||{x:BOARD.x+90,y:BOARD.y+90,scale:BOARD.scale};const step=e.shiftKey?5:20;if(e.key==='ArrowLeft')n.keyboard.x-=step;if(e.key==='ArrowRight')n.keyboard.x+=step;if(e.key==='ArrowUp')n.keyboard.y-=step;if(e.key==='ArrowDown')n.keyboard.y+=step;transform(g,n.keyboard);}});
 container.querySelector('.jigsaw-win button').addEventListener('click',()=>onNext?.(round.level<5?round.level+1:1));const soundButton=container.querySelector('.jigsaw-sound');soundButton.setAttribute('aria-pressed',String(soundEnabled));soundButton.setAttribute('aria-label',soundEnabled?'Matikan suara':'Nyalakan suara');soundButton.classList.toggle('muted',!soundEnabled);root.LevelCelebration?.attach(container,'.jigsaw-win',{level:round.level});return {state,place:(id,x,y)=>finish(id,x,y)};
}
const api={BOARD,createState,place,trayPositions,mount};if(typeof module!=='undefined'&&module.exports)module.exports=api;root.JigsawGame=api;
})(typeof globalThis!=='undefined'?globalThis:this);
