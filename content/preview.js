(async function(){
  const game=document.getElementById('round-game'),level=document.getElementById('round-level'),button=document.getElementById('round-shuffle'),status=document.getElementById('round-status'),output=document.getElementById('round-preview');
  if(!game)return;
  const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let config,history={};
  try{config=await fetch('content/game-content.json?v=webp85-9').then(r=>{if(!r.ok)throw Error('Data level tidak dapat dimuat');return r.json();});try{history=JSON.parse(localStorage.getItem('shape-content-preview')||'{}');}catch{history={};}}
  catch(error){status.textContent=error.message;return;}
  function remember(key,round){history[key]=round.game==='find'?{sceneId:round.sceneId,themeId:round.themeId,targetIds:round.targetIds}:round.game==='puzzle'?{themeId:round.themeId,shapeId:round.shapeId}:{objectIds:round.objectIds};try{localStorage.setItem('shape-content-preview',JSON.stringify(history));}catch{}}
  function render(){
    const key=game.value+'-'+level.value,r=GameContent.createRound(config,game.value,Number(level.value),history[key]);remember(key,r);output.dataset.game=r.game;output.dataset.level=r.level;
    function complete(state){GameProgress.record(r.game,r.level,state.mistakes);if(GameProgress.summary(r.game).complete){const b=output.querySelector('.find-next,.jigsaw-win button,.match-win button');if(b)b.textContent='Lihat hasil akhir';}}
    function nextLevel(next){if(GameProgress.summary(r.game).complete){location.href='results.html?game='+r.game;return;}level.value=String(next);render();}
    if(r.game==='find'){
      const shape=config.shapes.find(s=>s.id===r.targetShape);
      if(r.scene){
        status.textContent=`Level ${r.level} · ${r.theme.name}`;
        FindFrameGame.mount(output,r,{onNext:nextLevel,onComplete:complete});
        return;
      }
      status.textContent=`Level ${r.level} · ${r.theme.name} · Temukan ${r.targetCount} benda berbentuk ${shape.name.toLowerCase()}`;
      output.innerHTML=`<div class="random-scene"><img class="scene-bg" src="${r.theme.background}" alt="${escape(r.theme.name)}">${r.objects.map(o=>`<img class="scene-object" src="${o.asset}" alt="${escape(o.name)}" style="left:${o.position.x}%;top:${o.position.y}%">`).join('')}</div><div class="round-tags"><span class="round-tag">Cari ${r.targetCount} dari ${r.targetIds.length} benda benar</span><span class="round-tag">${r.distractorIds.length} pengecoh</span><span class="round-tag">5 tema tersedia</span></div><details class="answer-summary"><summary>Daftar aset target pada contoh sesi ini</summary><p>${r.objects.filter(o=>o.isTarget).map(o=>escape(o.name)).join(', ')}.</p></details>`;
    }else if(r.game==='puzzle'){
      const shape=config.shapes.find(s=>s.id===r.shapeId);
      status.textContent=`Level ${r.level} · ${r.theme.name} · ${shape.name} · ${r.pieceCount} keping`;
      JigsawGame.mount(output,r,{shapeName:shape.name,onNext:nextLevel,onComplete:complete});
    }else{
      status.textContent=`Level ${r.level} · ${r.name}`;
      MatchingGame.mount(output,r,{onNext:nextLevel,onComplete:complete});
    }
  }
  document.getElementById('round-level-table').innerHTML='<table><thead><tr><th>Level</th><th>Temukan Benda</th><th>Puzzle</th><th>Mencocokkan</th></tr></thead><tbody>'+config.find.levels.map((l,i)=>`<tr><td>${l.level}</td><td>${escape(config.shapes.find(s=>s.id===l.targetShape).name)} · ${l.sceneIds?.length||5} gambar acak</td><td>${config.puzzle.levels[i].pieceCount} keping · 25 gambar</td><td>${escape(config.matching.levels[i].name)}</td></tr>`).join('')+'</tbody></table>';
  button.disabled=false;button.addEventListener('click',render);game.addEventListener('change',render);level.addEventListener('change',render);render();
})();
