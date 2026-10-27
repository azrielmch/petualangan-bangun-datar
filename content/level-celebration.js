(function(root){
'use strict';
const active=new WeakMap();
function clear(host){active.get(host)?.();active.delete(host);}
function attach(host,selector,{level=1}={}){
 clear(host);const win=host.querySelector(selector);if(!win)return;
 const dialog=document.createElement('dialog');dialog.className='level-popup';dialog.setAttribute('aria-label',`Level ${level} selesai`);
 const close=document.createElement('button');close.type='button';close.className='level-popup-close';close.setAttribute('aria-label','Lihat kembali permainan');close.innerHTML='<img src="assets-3d/ui/icon-close.svg" alt="">';
 const title=document.createElement('h2');title.textContent=`Level ${level} selesai!`;title.className='level-popup-title';
 const note=document.createElement('p');note.className='level-popup-note';note.textContent='Hebat! Kamu berhasil menyelesaikan tantangan ini.';
 const reopen=document.createElement('button');reopen.type='button';reopen.className='level-popup-reopen';reopen.textContent='Lihat hasil level';reopen.hidden=true;
 host.append(dialog,reopen);dialog.append(close,title,win,note);
 function show(){if(!win.hidden&&dialog.isConnected&&!dialog.open){reopen.hidden=true;dialog.showModal();win.querySelector('button')?.focus();}}
 close.addEventListener('click',()=>dialog.close());reopen.addEventListener('click',show);dialog.addEventListener('close',()=>{if(dialog.isConnected&&!win.hidden)reopen.hidden=false;});
 const observer=new MutationObserver(()=>{if(win.hidden){if(dialog.open)dialog.close();reopen.hidden=true;}else show();});observer.observe(win,{attributes:true,attributeFilter:['hidden']});
 active.set(host,()=>{observer.disconnect();if(dialog.open)dialog.close();dialog.remove();reopen.remove();});show();return {show,close:()=>dialog.close()};
}
root.LevelCelebration={attach,clear};
})(typeof globalThis!=='undefined'?globalThis:this);
