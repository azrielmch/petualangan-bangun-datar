(function(root){
  'use strict';
  const sample=(xs,n,rng)=>shuffle(xs,rng).slice(0,n);
  function shuffle(xs,rng=Math.random){const a=[...xs];for(let i=a.length-1;i>0;i--){const j=Math.floor(rng()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
  const signature=ids=>[...ids].sort().join('|');
  function chooseTheme(c,ids,previous,rng){const candidates=c.themes.filter(t=>ids.includes(t.id)&&t.id!==previous?.themeId);return sample(candidates.length?candidates:c.themes.filter(t=>ids.includes(t.id)),1,rng)[0];}
  function createRound(c,game,level,previous=null,rng=Math.random){
    const def=c[game]?.levels.find(l=>l.level===Number(level));if(!def)throw new Error('Level tidak tersedia');
    if(game==='find'){
      if(c.find.scenes?.length){
        const available=c.find.scenes.filter(s=>def.sceneIds.includes(s.id)),fresh=available.filter(s=>s.id!==previous?.sceneId);
        const scene=sample(fresh.length?fresh:available,1,rng)[0];
        const objects=scene.hotspots.map(o=>({...o,id:scene.id+':'+o.id,isTarget:o.shape===def.targetShape}));
        const targetIds=objects.filter(o=>o.isTarget).map(o=>o.id),distractorIds=objects.filter(o=>!o.isTarget).map(o=>o.id);
        return {game,level:def.level,sceneId:scene.id,scene,themeId:scene.themeId,theme:{id:scene.themeId,name:scene.themeName,background:scene.asset},targetShape:def.targetShape,shapeName:c.shapes.find(s=>s.id===def.targetShape).name,targetCount:Math.min(def.targetCount,targetIds.length),targetIds,distractorIds,objects};
      }
      const theme=chooseTheme(c,def.themeIds,previous,rng),pool=theme.objectPools[def.targetShape];
      let targets;for(let i=0;i<30;i++){targets=sample(pool,def.availableTargetCount||def.targetCount,rng);if(signature(targets)!==signature(previous?.targetIds||[]))break;}
      if(signature(targets)===signature(previous?.targetIds||[])){const replacement=pool.find(id=>!targets.includes(id));if(replacement)targets[targets.length-1]=replacement;}
      const otherShapes=c.shapes.filter(s=>s.id!==def.targetShape);
      const mandatory=otherShapes.map(s=>sample(theme.objectPools[s.id],1,rng)[0]);
      const extras=sample(otherShapes.flatMap(s=>theme.objectPools[s.id]).filter(id=>!mandatory.includes(id)),def.distractorCount-mandatory.length,rng);
      const distractors=[...mandatory,...extras];
      const slots=shuffle([[24,18],[43,15],[62,20],[28,38],[49,39],[69,40],[23,68],[41,72],[60,68],[78,73]],rng);
      const objects=shuffle([...targets,...distractors],rng).map((id,i)=>({...c.objects.find(o=>o.id===id),isTarget:targets.includes(id),position:{x:slots[i][0],y:slots[i][1]}}));
      return {game,level:def.level,themeId:theme.id,theme,targetShape:def.targetShape,targetCount:def.targetCount,targetIds:targets,distractorIds:distractors,objects};
    }
    if(game==='puzzle'){
      const theme=chooseTheme(c,def.themeIds,previous,rng);
      const shapes=def.shapeIds.filter(id=>id!==previous?.shapeId);
      const shapeId=sample(shapes.length?shapes:def.shapeIds,1,rng)[0];
      const variant=c.puzzle.variants.find(v=>v.theme===theme.id&&v.shape===shapeId);if(!variant)throw new Error('Variasi puzzle belum tersedia');
      const pieceOrder=shuffle(def.layout.pieces.map(p=>p.id),rng);
      return {game,level:def.level,themeId:theme.id,theme,shapeId,variant,pieceCount:def.pieceCount,layout:{...def.layout,shape:shapeId},pieceOrder};
    }
    if(game==='matching'){
      const objects=c.shapes.map(s=>sample(c.objects.filter(o=>o.shape===s.id&&o.id!==previous?.objectIds?.[s.id]),1,rng)[0]);
      const objectIds=Object.fromEntries(objects.map(o=>[o.shape,o.id]));
      const side=(type,s)=>{const o=objects.find(o=>o.shape===s.id);return {id:type+'-'+s.id,shapeId:s.id,type,text:type==='name'?s.name:type==='features'?s.features:type==='object'?o.name:s.name,asset:type==='shape'?s.asset:type==='object'?o.asset:null,objectId:type==='object'?o.id:null};};
      const left=shuffle(c.shapes.map(s=>side(def.leftType,s)),rng),right=shuffle(c.shapes.map(s=>side(def.rightType,s)),rng);
      return {game,level:def.level,name:def.name,leftType:def.leftType,rightType:def.rightType,left,right,objectIds,pairs:c.shapes.map(s=>({shapeId:s.id,leftId:def.leftType+'-'+s.id,rightId:def.rightType+'-'+s.id}))};
    }
    throw new Error('Permainan tidak tersedia');
  }
  const api={createRound,shuffle};if(typeof module!=='undefined'&&module.exports)module.exports=api;root.GameContent=api;
})(typeof globalThis!=='undefined'?globalThis:this);
