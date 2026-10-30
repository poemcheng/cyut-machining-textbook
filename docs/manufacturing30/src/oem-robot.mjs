import * as THREE from 'three';
/** Licensed manufacturer VISUAL geometry. Nominal URDF FK, no real-machine control. */
const cache=new Map();
const rad=THREE.MathUtils.degToRad;
export function rpyQuaternion(rpy){return new THREE.Quaternion().setFromEuler(new THREE.Euler(...rpy,'ZYX'));}
export function originMatrix(xyz,rpy){return new THREE.Matrix4().compose(new THREE.Vector3(...xyz),rpyQuaternion(rpy),new THREE.Vector3(1,1,1));}
export function forwardKinematics(model,degrees){
 if(degrees.length!==6||degrees.some(v=>!Number.isFinite(v)))throw Error('六個關節角度必須為有限數值。');
 const T=originMatrix([0,0,0],model.baseRPY);
 model.joints.forEach((j,i)=>T.multiply(originMatrix(j.xyz,j.rpy)).multiply(new THREE.Matrix4().makeRotationAxis(new THREE.Vector3(...j.axis),rad(degrees[i]))));
 return T.multiply(originMatrix(model.tool.xyz,model.tool.rpy));
}
async function readModel(key){
 if(!['ur5e','tm5-900'].includes(key))throw Error('未登錄的官方模型。');
 const url=new URL(`../assets/oem/${key}/model.json`,import.meta.url),r=await fetch(url);if(!r.ok)throw Error(`模型來源載入失敗：${r.status}`);const model=await r.json();
 if(model.schema!=='mfg30/oem-visual-v1'||model.parts.length!==7||model.joints.length!==6)throw Error('官方模型結構不完整。');
 const b=await fetch(new URL(model.binary,url));if(!b.ok)throw Error(`視覺網格載入失敗：${b.status}`);const buffer=await b.arrayBuffer();
 if(!crypto.subtle)throw Error('模型校驗需要 HTTPS 或 localhost。');
 const digest=[...new Uint8Array(await crypto.subtle.digest('SHA-256',buffer))].map(x=>x.toString(16).padStart(2,'0')).join('');
 if(digest!==model.binarySha256)throw Error('官方視覺網格 SHA-256 校驗失敗，停止呈現。');
 const parts=model.parts.map(p=>({spec:p,meshes:p.groups.map(g=>{
   if(g.vertexOffset<0||g.indexOffset<0||g.vertexOffset+g.vertexCount*24>buffer.byteLength||g.indexOffset+g.indexCount*4>buffer.byteLength)throw Error('網格位移超出檔案範圍。');
   const vertices=new Float32Array(buffer,g.vertexOffset,g.vertexCount*6),indices=new Uint32Array(buffer,g.indexOffset,g.indexCount);
   const geometry=new THREE.BufferGeometry(),interleaved=new THREE.InterleavedBuffer(vertices,6);
   geometry.setAttribute('position',new THREE.InterleavedBufferAttribute(interleaved,3,0));geometry.setAttribute('normal',new THREE.InterleavedBufferAttribute(interleaved,3,3));geometry.setIndex(new THREE.BufferAttribute(indices,1));geometry.computeBoundingBox();geometry.computeBoundingSphere();
   return {geometry,color:g.color,name:g.material};
 })}));
 return {model,parts};
}
export async function loadOfficialRobot(key){
 if(!cache.has(key))cache.set(key,readModel(key).catch(e=>{cache.delete(key);throw e;}));
 const {model,parts}=await cache.get(key);return new OfficialRobot(model,parts);
}
export class OfficialRobot{
 constructor(model,parts){
  this.model=model;this.root=new THREE.Group();this.root.name=model.name+' / original manufacturer visual meshes';this.root.userData.oem=true;
  // Source data are metres, Z up. This outer group is exclusively display placement.
  this.root.rotation.x=-Math.PI/2;
  this.kinematicRoot=new THREE.Group();this.kinematicRoot.quaternion.copy(rpyQuaternion(model.baseRPY));this.root.add(this.kinematicRoot);
  this.links={};this.jointGroups=[];this.materials=[];this.degrees=[...model.homeDegrees];
  for(const {spec,meshes} of parts){
   const link=new THREE.Group();link.name=spec.link;this.links[spec.link]=link;
   const visual=new THREE.Group();visual.position.fromArray(spec.xyz);visual.quaternion.copy(rpyQuaternion(spec.rpy));link.add(visual);
   for(const m of meshes){
    const material=new THREE.MeshStandardMaterial({color:new THREE.Color().setRGB(...m.color),metalness:.32,roughness:.38});this.materials.push(material);
    const mesh=new THREE.Mesh(m.geometry,material);mesh.name=`${model.name} / ${spec.link} / ${m.name}`;mesh.userData.sourcePart=spec.source;mesh.castShadow=true;mesh.receiveShadow=true;visual.add(mesh);
   }
  }
  this.kinematicRoot.add(this.links[model.baseLink]);
  for(const j of model.joints){
   const origin=new THREE.Group();origin.position.fromArray(j.xyz);origin.quaternion.copy(rpyQuaternion(j.rpy));origin.name=j.name+' / nominal origin';
   const rotation=new THREE.Group();rotation.name=j.name;rotation.add(this.links[j.child]);origin.add(rotation);this.links[j.parent].add(origin);this.jointGroups.push(rotation);
  }
  this.tool=new THREE.Group();this.tool.name='tool0 — uncalibrated nominal flange';this.tool.position.fromArray(model.tool.xyz);this.tool.quaternion.copy(rpyQuaternion(model.tool.rpy));this.links[model.joints.at(-1).child].add(this.tool);
  const axes=new THREE.AxesHelper(.12);axes.name='tool0 axes';this.tool.add(axes);this.axes=axes;
  this.setDegrees(this.degrees);
 }
 setDegrees(degrees){
  if(degrees.length!==6)throw Error('必須提供六個關節角度。');
  degrees.forEach((v,i)=>{const [min,max]=this.model.joints[i].limitsDegrees;if(!Number.isFinite(v)||v<min||v>max)throw Error(`J${i+1} 超出名義角度範圍。`);});
  this.degrees=[...degrees];this.jointGroups.forEach((g,i)=>g.quaternion.setFromAxisAngle(new THREE.Vector3(...this.model.joints[i].axis),rad(degrees[i])));this.root.updateMatrixWorld(true);
 }
 get pose(){const m=forwardKinematics(this.model,this.degrees),p=new THREE.Vector3().setFromMatrixPosition(m),q=new THREE.Quaternion().setFromRotationMatrix(m);return {positionMetres:p.toArray(),quaternionXYZW:q.toArray(),matrix:m.toArray(),reference:'source base_link, not display coordinates'};}
 setWire(value){for(const m of this.materials)m.wireframe=value;}
 dispose(){this.root.removeFromParent();for(const m of this.materials)m.dispose();this.axes.geometry.dispose();this.axes.material.dispose();/* Geometries stay in the two-model cache. */}
}
