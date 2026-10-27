(function(root){
'use strict';
const active=new WeakMap(),DELAY=2000;
function clear(host){active.get(host)?.();active.delete(host);}
function attach(host,selector,{level=1}={}){
 clear(host);const win=host.querySelector(selector);if(!win)return;
 let timer=null,scheduled=false,destroyed=false;
 const dialog=document.createElement('dialog');dialog.className='level-popup';dialog.setAttribute('aria-label',`Level ${level} selesai`);
 const close=document.createElement('button');close.type='button';close.className='level-popup-close';close.setAttribute('aria-label','Lihat kembali permainan');close.innerHTML='<img src="assets-3d/ui/icon-close.svg" alt="">';
 const title=document.createElement('h2');title.textContent=`Level ${level} selesai!`;title.className='level-popup-title';
 const note=document.createElement('p');note.className='level-popup-note';note.textContent='Hebat! Kamu berhasil menyelesaikan tantangan ini.';
 const next=document.createElement('button');next.type='button';next.className='level-next-arrow';next.hidden=true;next.innerHTML='<img src="assets-3d/ui/icon-next-level.svg" alt="">';
 const stage=host.querySelector('.find-framed,.jigsaw-game,.match-game')||host;
 stage.append(next);host.append(dialog);dialog.append(close,title,win,note);
 function show(){if(!destroyed&&!win.hidden&&dialog.isConnected&&!dialog.open){next.hidden=true;dialog.showModal();win.querySelector('button')?.focus();}}
 function schedule(){if(!win.hidden&&!scheduled&&!destroyed){scheduled=true;timer=setTimeout(()=>{timer=null;show();},DELAY);}}
 close.addEventListener('click',()=>dialog.close());
 next.addEventListener('click',()=>{next.hidden=true;win.querySelector('button')?.click();});
 dialog.addEventListener('close',()=>{if(!destroyed&&dialog.isConnected&&!win.hidden){next.setAttribute('aria-label',win.querySelector('button')?.textContent||'Lanjut level berikutnya');next.title=next.getAttribute('aria-label');next.hidden=false;}});
 const observer=new MutationObserver(()=>{if(win.hidden){clearTimeout(timer);timer=null;scheduled=false;next.hidden=true;if(dialog.open)dialog.close();}else schedule();});observer.observe(win,{attributes:true,attributeFilter:['hidden']});
 active.set(host,()=>{destroyed=true;clearTimeout(timer);observer.disconnect();if(dialog.open)dialog.close();dialog.remove();next.remove();});schedule();return {show,close:()=>dialog.close()};
}
root.LevelCelebration={attach,clear};
})(typeof globalThis!=='undefined'?globalThis:this);
