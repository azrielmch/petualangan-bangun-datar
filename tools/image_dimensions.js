'use strict';
module.exports=function dimensions(data){
 if(data.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])))return {width:data.readUInt32BE(16),height:data.readUInt32BE(20)};
 if(data.toString('ascii',0,4)==='RIFF'&&data.toString('ascii',8,12)==='WEBP'){
  for(let pos=12;pos+8<=data.length;){const type=data.toString('ascii',pos,pos+4),size=data.readUInt32LE(pos+4),n=pos+8;
   if(type==='VP8X')return {width:data.readUIntLE(n+4,3)+1,height:data.readUIntLE(n+7,3)+1};
   if(type==='VP8 ')return {width:data.readUInt16LE(n+6)&0x3fff,height:data.readUInt16LE(n+8)&0x3fff};
   if(type==='VP8L'){const bits=data.readUInt32LE(n+1);return {width:(bits&0x3fff)+1,height:((bits>>>14)&0x3fff)+1};}
   pos=n+size+(size%2);
  }
 }
 throw Error('Unsupported image format');
};
