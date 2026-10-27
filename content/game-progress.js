(function(root){
'use strict';
const GAMES={find:{name:'Temukan Benda',url:'find.html',icon:'assets-3d/ui/thumbnail-find.svg'},puzzle:{name:'Puzzle Bangun Datar',url:'puzzle.html',icon:'assets-3d/ui/thumbnail-puzzle.svg'},matching:{name:'Ayo Mencocokkan',url:'matching.html',icon:'assets-3d/ui/thumbnail-match.svg'}},KEY='bangun-datar-progress-v1';
let memory={version:1,games:{},settings:{sound:true,teacherMode:false}};
function read(){try{const d=JSON.parse(root.localStorage?.getItem(KEY)||'null');if(d?.version===1&&d.games)return d;}catch{}return memory;}
function write(d){memory=d;try{root.localStorage?.setItem(KEY,JSON.stringify(d));}catch{}return d;}
function valid(game){if(!GAMES[game])throw Error('Game tidak tersedia');}
function score(errors){return Math.max(0,100-10*Math.ceil(Math.max(0,errors)/5));}
function summary(game){valid(game);const r=read().games[game],levels=Object.values(r?.levels||{}).filter(x=>x.level>=1&&x.level<=5).sort((a,b)=>a.level-b.level),mistakes=levels.reduce((n,l)=>n+l.mistakes,0),complete=levels.length===5;return {game,name:GAMES[game].name,runId:r?.runId||null,levels,completed:levels.length,complete,mistakes,score:complete?score(mistakes):null,stars:complete?score(mistakes)/20:0,nextLevel:[1,2,3,4,5].find(n=>!levels.some(l=>l.level===n))||1};}
function record(game,level,mistakes=0){valid(game);if(!Number.isInteger(level)||level<1||level>5)throw Error('Level harus 1 sampai 5');const d=read();if(!d.games[game])d.games[game]={runId:Date.now().toString(36)+'-'+Math.random().toString(36).slice(2),levels:{}};const r=d.games[game];if(!r.levels[level])r.levels[level]={level,mistakes:Math.max(0,Math.floor(Number(mistakes)||0)),finishedAt:new Date().toISOString()};write(d);return summary(game);}
function restart(game){valid(game);const d=read();d.games[game]={runId:Date.now().toString(36)+'-'+Math.random().toString(36).slice(2),levels:{}};write(d);return summary(game);}
function settings(){const s={sound:true,teacherMode:false,...read().settings};if(root.document){try{s.teacherMode=s.teacherMode&&root.sessionStorage.getItem('teacher-authorized')==='yes';}catch{s.teacherMode=false;}}return s;}
function setSound(value){const d=read();d.settings={...settings(),sound:!!value};write(d);return settings();}
function setTeacherMode(value){if(root.document){try{if(value)root.sessionStorage.setItem('teacher-authorized','yes');else root.sessionStorage.removeItem('teacher-authorized');}catch{}}const d=read();d.settings={...settings(),teacherMode:!!value};write(d);return settings();}
const api={GAMES,summary,record,restart,score,settings,setSound,setTeacherMode};if(typeof module!=='undefined'&&module.exports)module.exports=api;root.GameProgress=api;
})(typeof globalThis!=='undefined'?globalThis:this);
