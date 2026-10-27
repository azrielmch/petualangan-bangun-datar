(async function(){
const game=document.body.dataset.game,meta=GameProgress.GAMES[game],host=document.getElementById(game==='find'?'find-game':'game'),level=document.getElementById('level'),button=document.getElementById(game==='find'?'new-scene':'replay'),history={};if(!meta)return;
const config=await fetch('content/game-content.json?v=home-results-1').then(r=>r.json());
for(const o of level.options)o.dataset.label=o.textContent;
const requested=GameProgress.settings().teacherMode?Number(new URLSearchParams(location.search).get('level')):0;level.value=String(requested>=1&&requested<=5?requested:GameProgress.summary(game).nextLevel);
function labels(){const progress=GameProgress.summary(game);for(const o of level.options)o.textContent=o.dataset.label+(progress.levels.some(l=>l.level===Number(o.value))?' (selesai)':'');}
function render(){const n=Number(level.value),r=GameContent.createRound(config,game,n,history[n]);history[n]=r;
if(game==='find')document.getElementById('theme').textContent=r.scene.name;
if(game==='puzzle')document.getElementById('theme').textContent=r.theme.name;
function completed(state){GameProgress.record(game,n,state.mistakes);labels();if(GameProgress.summary(game).complete){const b=host.querySelector('.find-next,.jigsaw-win button,.match-win button');if(b)b.textContent='Lihat hasil akhir';}}
function next(nextLevel){const s=GameProgress.summary(game);if(s.complete){location.href='results.html?game='+game;return;}level.value=String(s.levels.some(l=>l.level===nextLevel)?s.nextLevel:nextLevel);render();}
const options={onNext:next,onComplete:completed};if(game==='find')FindFrameGame.mount(host,r,options);if(game==='puzzle')JigsawGame.mount(host,r,{...options,shapeName:config.shapes.find(s=>s.id===r.shapeId).name});if(game==='matching')MatchingGame.mount(host,r,options);labels();window.AppShell?.fit();}
button.addEventListener('click',render);level.addEventListener('change',render);render();window.AppShell?.intro(game);
})();
