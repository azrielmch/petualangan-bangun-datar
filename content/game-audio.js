(function(root){
let context;
function unlock(){try{const C=root.AudioContext||root.webkitAudioContext;if(!C)return;context||=new C();if(context.state==='suspended')context.resume();}catch{}}
function play(kind='click'){
 if(root.GameProgress?.settings().sound===false)return;unlock();if(!context)return;
 const notes={click:[520],correct:[660,880],wrong:[240,180],complete:[523,659,784,1047]};
 (notes[kind]||notes.click).forEach((hz,i)=>{const o=context.createOscillator(),g=context.createGain(),t=context.currentTime+i*.12;o.type='sine';o.frequency.value=hz;o.connect(g);g.connect(context.destination);g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(.16,t+.01);g.gain.exponentialRampToValueAtTime(.001,t+.2);o.start(t);o.stop(t+.22);});
}
document.addEventListener('pointerdown',unlock,{capture:true});document.addEventListener('keydown',unlock,{capture:true});document.addEventListener('click',e=>{if(e.target.closest('button,a,select'))play('click');});root.GameAudio={unlock,play};
})(window);
