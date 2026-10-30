import * as THREE from 'three';
import {CATALOG,profileFor} from './realworld-catalog.mjs';
import {buildField} from './field-scenes.mjs';
import {loadOfficialRobot} from './oem-robot.mjs';
const $=id=>document.getElementById(id),esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
/** Separate provenance-aware world layer; never renames generic geometry as OEM CAD. */
export class RealWorldExperience{
 constructor(lab,onEvent=()=>{}){
  this.lab=lab;this.onEvent=onEvent;this.currentId=0;this.field=null;this.robot=null;this.pedestal=null;this.token=0;this.ready=Promise.resolve();this.status='idle';this.assetKey='ur5e';this.overview=true;this.showField=true;
  $('rwCase').onchange=()=>{this.showCase($('rwCase').value);this.onEvent('manufacturer-reference',{case:$('rwCase').value});};
  $('rwRobot').onchange=()=>{this.assetKey=$('rwRobot').value;this.ready=this.changeRobot(this.assetKey);this.onEvent('manufacturer-model',{model:this.assetKey});};
  $('rwField').onchange=()=>{this.showField=$('rwField').checked;this.syncVisibility();};
  $('rwOverview').onclick=()=>{this.overview=true;this.focusCamera();};$('rwClose').onclick=()=>{this.overview=false;this.lab.reset();};
  $('rwFlow').onclick=e=>{const b=e.target.closest('[data-stage]');if(!b)return;this.stage=Number(b.dataset.stage);this.field?.setStage(this.stage);for(const x of $('rwFlow').querySelectorAll('button'))x.setAttribute('aria-pressed',String(x===b));this.onEvent('field-flow',{stage:this.stage,field:this.field?.field.id});};
  $('rwHome').onclick=()=>{if(!this.robot)return;$('rwAnimate').checked=false;this.setJoints(this.robot.model.homeDegrees);};
  $('rwZero').onclick=()=>{if(!this.robot)return;$('rwAnimate').checked=false;this.setJoints([0,0,0,0,0,0]);};
  $('rwJoints').oninput=e=>{if(!e.target.matches('[data-joint]')||!this.robot)return;$('rwAnimate').checked=false;const q=[...this.robot.degrees];q[Number(e.target.dataset.joint)]=Number(e.target.value);this.setJoints(q);};
  $('rwJoints').onchange=()=>{if(this.robot)this.onEvent('oem-joints',{model:this.robot.model.key,degrees:this.robot.degrees,tool0:this.robot.pose});};
 }
 selectChapter(id){
  if(id===this.currentId){this.syncVisibility();return;}
  this.currentId=id;this.profile=profileFor(id);const f=CATALOG.fields[this.profile.field];this.stage=0;
  if(this.field)this.field.dispose();this.field=buildField(f);this.lab.scene.add(this.field.root);
  $('rwFieldTitle').textContent=f.name;$('rwFieldNote').textContent=f.note;
  $('rwFlow').innerHTML=f.flow.map((t,i)=>`<button type="button" data-stage="${i}" aria-pressed="${i===0}"><span>0${i+1}</span>${esc(t)}</button>`).join('');
  $('rwCase').innerHTML=this.profile.cases.map(k=>`<option value="${k}">${esc(CATALOG.cases[k].brand+' · '+CATALOG.cases[k].model)}</option>`).join('');this.showCase(this.profile.cases[0]);
  $('rwRobotPanel').hidden=!this.profile.robot;$('rwRobotLabel').hidden=!this.profile.robot;
  $('rwModelBoundary').textContent=id===29?'右側工程參數仍為本章「平面二連桿」解析練習，與這裡的官方六軸模型不是同一個運動學模型。六軸 tool0 位置另依原廠名義關節鏈計算。':'本章右側工程參數是教學解析算例；品牌設備的額定規格、控制器設定與性能不能由算例直接推得。';
  this.ready=this.changeRobot(this.profile.robot?this.assetKey:'none');this.syncVisibility();
 }
 showCase(key){
  const c=CATALOG.cases[key];if(!c)return;
  $('rwBrand').textContent=c.brand;$('rwModel').textContent=c.model+' · '+c.kind;
  $('rwEvidence').textContent=c.evidence==='official-visual'?'具官方視覺模型（由模型選單選取）':'原廠設備參考；畫面非該機型 CAD';
  $('rwObservation').textContent=c.observation;$('rwDistinction').textContent=c.distinction;
  $('rwSource').href=c.url;$('rwSource').textContent='原廠來源 ↗';$('rwVerified').textContent='查核日期 '+c.verified;
  $('rwSpecs').innerHTML=c.spec.map(([label,value])=>`<div><dt>${esc(label)}</dt><dd>${esc(value)}</dd></div>`).join('');
 }
 async changeRobot(key){
  const ticket=++this.token;if(this.robot){this.robot.dispose();this.robot=null;}
  if(this.pedestal){this.pedestal.removeFromParent();this.pedestal.geometry.dispose();this.pedestal.material.dispose();this.pedestal=null;}
  $('rwJoints').innerHTML='';$('rwPose').textContent='';$('rwAnimate').checked=false;
  if(key==='none'){this.status='generic';$('rwAssetStatus').textContent='通用設備教學重建；品牌資料只作實際案例參考。';this.syncVisibility();this.refreshSummary();return;}
  this.status='loading';$('rwAssetStatus').textContent='正在載入官方分件視覺模型並核對 SHA-256…';this.syncVisibility();
  try{
   const robot=await loadOfficialRobot(key);
   if(ticket!==this.token){robot.dispose();return;}
   this.robot=robot;robot.root.scale.setScalar(3);
   // Layout is normalized; the robot's internal geometry/kinematics remain in metres.
   const solo=this.currentId===29;robot.root.position.set(solo?0:5.1,1.05,solo?0:-.6);
   this.pedestal=new THREE.Mesh(new THREE.BoxGeometry(1.1,1.05,1.1),new THREE.MeshStandardMaterial({color:0x6c8692,roughness:.6}));this.pedestal.position.set(robot.root.position.x,.525,robot.root.position.z);this.pedestal.name='Authored pedestal (not manufacturer accessory)';this.pedestal.castShadow=true;this.pedestal.receiveShadow=true;this.lab.scene.add(this.pedestal,robot.root);
   this.status='ready';this.robot.setWire(this.lab.wire);
   $('rwJoints').innerHTML=robot.model.joints.map((j,i)=>`<label>J${i+1}<input aria-label="官方模型關節 J${i+1}" type="range" min="${j.limitsDegrees[0]}" max="${j.limitsDegrees[1]}" step="1" value="${robot.degrees[i]}" data-joint="${i}"><output id="rwQ${i}">${robot.degrees[i]}°</output></label>`).join('');
   $('rwAssetStatus').textContent=`${robot.model.name}｜官方視覺網格 · 7 連桿 / 6 軸 · ${robot.model.triangles.toLocaleString()} 三角面 · BSD-3-Clause · SHA-256 已核對`;
   $('rwAssetSource').href=`https://github.com/${robot.model.sourceRepository}/tree/${robot.model.sourceRevision}`;
   $('rwAssetLicense').href=`assets/oem/${key}/LICENSE.txt`;$('rwAssetSource').textContent='固定來源版本 '+robot.model.sourceRevision.slice(0,8)+' ↗';
   this.updatePose();this.syncVisibility();this.refreshSummary();this.lab.reset();
  }catch(error){if(ticket!==this.token)return;this.status='error';$('rwAssetStatus').textContent='官方模型未載入：'+error.message+'。不以通用模型冒充該品牌。';this.syncVisibility();this.refreshSummary();}
 }
 setJoints(q){try{this.robot.setDegrees(q);this.updatePose();}catch(e){$('rwPose').textContent=e.message;}}
 updatePose(){if(!this.robot)return;const pose=this.robot.pose;this.robot.degrees.forEach((q,i)=>{const out=$('rwQ'+i);if(out)out.textContent=q.toFixed(1)+'°';const input=$('rwJoints').querySelector(`[data-joint="${i}"]`);if(input)input.value=q;});$('rwPose').textContent='名義 tool0 / source base_link：X '+(pose.positionMetres[0]*1000).toFixed(1)+' mm · Y '+(pose.positionMetres[1]*1000).toFixed(1)+' mm · Z '+(pose.positionMetres[2]*1000).toFixed(1)+' mm（未含工具、未單機校正）';}
 syncVisibility(){const show=this.lab.mode==='industrial';if(this.field)this.field.root.visible=show&&this.showField;if(this.robot)this.robot.root.visible=show;if(this.pedestal)this.pedestal.visible=show;
  if(this.lab.industrial)this.lab.industrial.root.visible=show&&!(this.currentId===29&&this.profile?.robot&&this.assetKey!=='none');
  $('rwRobotPanel').hidden=!this.profile?.robot||this.assetKey==='none';
 }
 refreshSummary(){
  if(this.currentId===29&&this.robot){$('equipmentTitle').textContent=this.robot.model.name;$('equipmentComponents').textContent='官方視覺連桿與名義關節鏈；原創底座，未含工具';$('partsCount').textContent='7 個來源連桿 · 6 旋轉關節 · '+this.robot.model.triangles.toLocaleString()+' 三角面';}
  const caption=document.querySelector('.scene-caption');if(caption)caption.textContent=this.robot?'含官方機器人模型；其他機台／場域為教學重建':'通用機台＋代表性場域；品牌參考不等於 OEM CAD';
 }
 setWire(value){this.robot?.setWire(value);}
 beforeRender(phase){
  this.syncVisibility();if(this.robot){this.robot.axes.visible=this.lab.parts;
   if($('rwAnimate').checked){const q=this.robot.model.homeDegrees.map((v,i)=>v+Math.sin(phase*Math.PI*2+i*.3)*[12,5,7,7,5,10][i]);this.robot.setDegrees(q);if(this.lastPhase===undefined||Math.abs(phase-this.lastPhase)>.01){this.updatePose();this.lastPhase=phase;}}
  }
 }
 focusCamera(){
  if(this.lab.mode!=='industrial')return false;
  const {camera,controls}=this.lab;controls.maxDistance=55;
  if(this.overview&&this.showField){const aspect=Math.max(.55,camera.aspect);const distance=Math.max(20,22/aspect);controls.target.set(0,1.2,0);camera.position.copy(controls.target).add(new THREE.Vector3(.45,.72,1).normalize().multiplyScalar(Math.min(48,distance)));controls.update();return true;}
  if(this.currentId===29&&this.robot){const b=new THREE.Box3().setFromObject(this.robot.root);b.expandByObject(this.pedestal);const size=b.getSize(new THREE.Vector3()),center=b.getCenter(new THREE.Vector3());const aspect=Math.max(.5,camera.aspect),d=Math.max(size.y,Math.hypot(size.x,size.z)/aspect)/(2*Math.tan(THREE.MathUtils.degToRad(camera.fov/2)))*1.6;controls.target.copy(center);camera.position.copy(center).add(new THREE.Vector3(1,.7,1.4).normalize().multiplyScalar(Math.max(5,d)));controls.update();return true;}
  return false;
 }
 dispose(){++this.token;this.field?.dispose();this.robot?.dispose();if(this.pedestal){this.pedestal.removeFromParent();this.pedestal.geometry.dispose();this.pedestal.material.dispose();}}
}
