(function(root){
  'use strict';
  function createState(round){return {sceneId:round.sceneId,targetCount:round.targetCount,foundIds:[],wrongIds:[],mistakes:0,complete:false};}
  function answer(round,state,id){
    if(state.complete)return {kind:'complete',state};
    const object=round.objects.find(x=>x.id===id);
    if(!object)return {kind:'background',state};
    if(state.foundIds.includes(id))return {kind:'already-found',state};
    if(object.shape===round.targetShape){
      state.foundIds.push(id);state.wrongIds=state.wrongIds.filter(x=>x!==id);state.complete=state.foundIds.length>=state.targetCount;
      return {kind:'correct',state,object};
    }
    state.mistakes++;if(!state.wrongIds.includes(id))state.wrongIds.push(id);
    return {kind:'wrong',state,object};
  }
  function mount(container,round,{onNext,onChange}={}){
    const state=createState(round),escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    container.innerHTML=`<div class="find-topline"><strong>Cari ${round.targetCount} benda bentuk ${escape(round.shapeName.toLowerCase())}</strong><span class="find-counter" aria-live="polite">0/${round.targetCount}</span></div><div class="find-scene" data-scene-id="${escape(round.sceneId)}"><img decoding="async" fetchpriority="high" src="${round.scene.asset}?v=${round.scene.revision||'clean25d-final'}" alt="${escape(round.scene.name)}" width="${round.scene.width}" height="${round.scene.height}" draggable="false"><svg class="find-overlay" viewBox="0 0 100 100" preserveAspectRatio="none" aria-label="Benda dalam gambar">${round.objects.map(o=>{const r=o.region;const hit=r.polygon?`<polygon class="find-hit" points="${r.polygon.map(p=>p.join(',')).join(' ')}"/>`:`<ellipse class="find-hit" cx="${r.cx}" cy="${r.cy}" rx="${r.rx}" ry="${r.ry}"/>`;return `<g role="button" tabindex="0" aria-label="${escape(o.label)}" data-hotspot="${escape(o.id)}">${hit}</g>`;}).join('')}<g class="find-rings" aria-hidden="true" pointer-events="none"></g></svg></div><div class="find-feedback" role="status" aria-live="polite">Klik benda yang bentuknya sesuai permintaan.</div><div class="round-tags"><span class="round-tag">${escape(round.scene.name)}</span><span class="round-tag find-errors">Kesalahan: 0</span><span class="round-tag">Gambar utuh · benda menyatu</span></div><div class="find-win" hidden><img loading="lazy" decoding="async" src="assets-3d/ui/banner-great.webp" alt="GREAT!"><p>Semua benda yang diminta sudah ditemukan.</p><button type="button" class="find-next">${round.level<5?'Lanjut level berikutnya':'Main lagi dari level 1'}</button></div>`;
    const svg=container.querySelector('.find-overlay'),rings=container.querySelector('.find-rings'),feedback=container.querySelector('.find-feedback');
    function draw(){
      container.querySelector('.find-counter').textContent=state.foundIds.length+'/'+state.targetCount;
      container.querySelector('.find-errors').textContent='Kesalahan: '+state.mistakes;
      rings.innerHTML=[...state.foundIds.map(id=>[id,'correct']),...state.wrongIds.map(id=>[id,'wrong'])].map(([id,kind])=>{const r=round.objects.find(o=>o.id===id).region;return `<ellipse class="find-ring ${kind}" cx="${r.cx}" cy="${r.cy}" rx="${r.rx}" ry="${r.ry}"/>`;}).join('');
      for(const g of svg.querySelectorAll('[data-hotspot]'))g.setAttribute('aria-disabled',String(state.complete||state.foundIds.includes(g.dataset.hotspot)));
      container.querySelector('.find-win').hidden=!state.complete;
      onChange?.(state);
    }
    function select(id){const result=answer(round,state,id);feedback.dataset.kind=result.kind;if(['correct','wrong'].includes(result.kind))root.GameAudio?.play(state.complete?'complete':result.kind);
      feedback.textContent=result.kind==='correct'?(state.complete?'BENAR! Semua benda sudah ditemukan.':'BENAR! Cari benda berikutnya.') : result.kind==='wrong'?'SALAH — Coba lagi, ya!': result.kind==='already-found'?'Benda ini sudah ditemukan.':result.kind==='complete'?'Level selesai. Lanjutkan ke level berikutnya.':'Klik salah satu benda dalam gambar.';
      if(result.kind==='wrong'&&round.targetShape==='persegi'&&result.object.shape==='persegi-panjang')feedback.textContent='SALAH — Itu persegi panjang. Ada sisi panjang dan sisi pendek.';
      if(result.kind==='wrong'&&round.targetShape==='persegi-panjang'&&result.object.shape==='persegi')feedback.textContent='SALAH — Itu persegi. Keempat sisinya sama panjang.';
      draw();}
    svg.addEventListener('click',event=>select(event.target.closest('[data-hotspot]')?.dataset.hotspot));
    svg.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){const target=event.target.closest('[data-hotspot]');if(target){event.preventDefault();select(target.dataset.hotspot);}}});
    container.querySelector('.find-next').addEventListener('click',()=>onNext?.(round.level<5?round.level+1:1));
    return {state,select};
  }
  const api={createState,answer,mount};if(typeof module!=='undefined'&&module.exports)module.exports=api;root.FindSceneGame=api;
})(typeof globalThis!=='undefined'?globalThis:this);
