(function(root){
'use strict';
const body=document.body;if(!body.dataset.game&&!['home','results'].includes(body.dataset.page))return;
const embedded=!!root.frameElement?.classList.contains('app-viewport'),standalone=!!navigator.standalone||matchMedia('(display-mode: standalone)').matches;
let wide=false,frame=null,screenButton=null;
const fullElement=()=>document.fullscreenElement||document.webkitFullscreenElement;
function fit(){
 if(frame){const rotated=innerHeight>innerWidth;frame.style.width=(rotated?innerHeight:innerWidth)+'px';frame.style.height=(rotated?innerWidth:innerHeight)+'px';frame.style.transform='translate(-50%,-50%)'+(rotated?' rotate(90deg)':'');return;}
 const main=body.querySelector(':scope > main');if(!main)return;
 const overview=!!main.querySelector('.overview-grid');
 if(overview){body.classList.add('result-overview');return;}
 if(body.dataset.page==='results')body.classList.add('result-canvas');
 const toolbar=body.dataset.game?main.querySelector('.controls,.find-controls'):null,extra=toolbar&&getComputedStyle(toolbar).display!=='none'?toolbar.offsetHeight:0;
 main.style.width=Math.max(1,Math.min(innerWidth,(innerHeight-extra)*1.5))+'px';
}
function teacher(){body.classList.toggle('teacher-mode',!!root.GameProgress?.settings().teacherMode);fit();}
function startShell(){
 if(frame)return;wide=true;body.classList.add('shell-host');frame=document.createElement('iframe');frame.className='app-viewport';frame.title='Petualangan Bangun Datar';frame.allow='fullscreen; autoplay';frame.src='index.html?inside=1';body.append(frame);fit();
 if(screenButton){screenButton.hidden=true;screenButton.setAttribute('aria-pressed','true');}
}
function installHelp(){
 let d=document.getElementById('install-help');if(!d){d=document.createElement('dialog');d.id='install-help';d.className='modal';d.innerHTML='<h2>Layar penuh di iPhone</h2><p>Buka situs ini di Safari, tekan Bagikan, lalu pilih <strong>Tambahkan ke Layar Utama</strong>. Buka game melalui ikon tersebut untuk bermain tanpa bilah browser.</p><p>Di tab browser ini, mode landscape tetap bisa digunakan.</p><button class="close" type="button">Lanjut bermain</button>';body.append(d);d.querySelector('button').onclick=()=>{d.close();startShell();};}d.showModal();
}
async function toggleFullscreen(){
 if(embedded){parent.postMessage({type:'game-fullscreen-toggle'},location.origin);return;}
 if(wide){try{await document.exitFullscreen?.();}catch{}frame?.remove();frame=null;wide=false;body.classList.remove('shell-host');if(screenButton){screenButton.hidden=false;screenButton.setAttribute('aria-pressed','false');}fit();location.reload();return;}
 let native=false;try{if(document.documentElement.requestFullscreen){await document.documentElement.requestFullscreen({navigationUI:'hide'});native=true;}else if(document.documentElement.webkitRequestFullscreen){await document.documentElement.webkitRequestFullscreen();native=true;}}catch{}
 try{await screen.orientation?.lock?.('landscape');}catch{}
 if(!native&&!standalone&&/iPhone|iPod/.test(navigator.userAgent)){installHelp();return;}startShell();
}
function intro(game){
 const names={find:'Temukan Benda',puzzle:'Puzzle Bangun Datar',matching:'Ayo Mencocokkan'},hints={find:'Klik benda yang bentuknya sesuai permintaan.',puzzle:'Geser keping dari kanan ke papan kiri. Bisa juga pilih keping, lalu klik papan.',matching:'Tarik garis dari titik sambungan, atau pilih satu kartu di tiap sisi.'};if(!names[game])return;
 const d=document.createElement('dialog');d.className='game-intro';d.innerHTML=`<h1>${names[game]}</h1><p>${hints[game]}</p><button class="intro-start" type="button">Mulai</button>`;body.append(d);d.oncancel=e=>e.preventDefault();d.querySelector('button').onclick=()=>{root.GameAudio?.unlock();d.close();d.remove();fit();};d.showModal();
}
if(body.dataset.page==='home'){
 screenButton=document.createElement('button');screenButton.className='ui-fullscreen';screenButton.type='button';screenButton.setAttribute('aria-label',embedded?'Keluar layar penuh':'Layar penuh');screenButton.innerHTML='<img src="assets-3d/ui/icon-fullscreen.svg" alt="">';screenButton.onclick=toggleFullscreen;body.append(screenButton);
}
root.addEventListener('message',e=>{if(e.origin!==location.origin)return;if(e.source===frame?.contentWindow&&e.data?.type==='game-fullscreen-toggle')toggleFullscreen();});
root.AppShell={fit,intro,toggleFullscreen};teacher();root.addEventListener('resize',fit);root.visualViewport?.addEventListener('resize',fit);root.addEventListener('orientationchange',fit);root.addEventListener('storage',teacher);root.addEventListener('pageshow',teacher);document.addEventListener('fullscreenchange',fit);
if(!embedded&&standalone&&body.dataset.page==='home')startShell();
})(window);
