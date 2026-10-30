import {chromium} from 'playwright';import assert from 'node:assert/strict';import fs from 'node:fs/promises';
await fs.mkdir('test-results',{recursive:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox','--enable-unsafe-swiftshader']});
const page=await browser.newPage({viewport:{width:1500,height:1120},deviceScaleFactor:1});
const errors=[],failures=[],report={startedAt:new Date().toISOString(),models:[],layouts:[],checks:[]};
page.on('pageerror',e=>errors.push(e.message));page.on('requestfailed',r=>failures.push(r.url()));
try{
 await page.goto((process.env.BASE_URL||'http://127.0.0.1:8020/')+'#ch-29');await page.waitForFunction(()=>window.__mfg30?.sceneReady,null,{timeout:30000});await page.evaluate(()=>__mfg30.realworld.ready);
 for(const key of ['ur5e','tm5-900']){
  await page.locator('#rwRobot').selectOption(key);await page.evaluate(()=>__mfg30.realworld.ready);
  assert.equal(await page.evaluate(()=>__mfg30.realworld.status),'ready');
  const evidence=await page.evaluate(()=>{const a=__mfg30.realworld,r=a.robot,m=r.model;let meshes=0,invalid=0;r.root.traverse(o=>{if(o.isMesh)meshes++;for(const v of [...o.position,...o.scale])if(!Number.isFinite(v))invalid++;});const residuals=[];for(const f of m.fkFixtures){r.setDegrees(f.degrees);const expected=f.positionMetres,actual=r.pose.positionMetres;residuals.push(Math.max(...actual.map((v,i)=>Math.abs(v-expected[i]))));}r.setDegrees(m.homeDegrees);return {key:m.key,parts:m.parts.length,joints:m.joints.length,triangles:m.triangles,meshes,invalid,residuals,revision:m.sourceRevision};});
  assert.equal(evidence.parts,7);assert.equal(evidence.joints,6);assert.ok(evidence.meshes>=7);assert.equal(evidence.invalid,0);assert.ok(evidence.residuals.every(r=>r<1e-9));report.models.push(evidence);
  await page.locator('#rwClose').click();await page.locator('#rwField').uncheck();await page.locator('#parts').uncheck();await page.waitForTimeout(300);
  await page.locator('#viewport').screenshot({path:`test-results/oem-${key}.png`});
  await page.locator('#rwField').check();await page.locator('#rwOverview').click();await page.waitForTimeout(300);await page.screenshot({path:`test-results/workcell-${key}.png`,fullPage:true});
  await page.locator('#rwJoints [data-joint="0"]').evaluate(el=>{el.value='20';el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));});assert.equal(await page.evaluate(()=>__mfg30.realworld.robot.degrees[0]),20);await page.locator('#rwHome').click();
  await page.locator('#viewMode').selectOption('concept');assert.equal(await page.evaluate(()=>__mfg30.realworld.robot.root.visible),false);await page.locator('#viewMode').selectOption('industrial');assert.equal(await page.evaluate(()=>__mfg30.realworld.robot.root.visible),true);
 }
 for(const id of [3,4,5,8,14,16,19,21,22,26,27]){
  await page.evaluate(id=>__mfg30.select(id),id);await page.evaluate(()=>__mfg30.realworld.ready);await page.locator('#rwOverview').click();
  const result=await page.evaluate(()=>({id:__mfg30.current.id,field:__mfg30.realworld.field.stats,brand:document.querySelector('#rwBrand').textContent,flow:document.querySelectorAll('#rwFlow button').length}));assert.equal(result.flow,4);assert.ok(result.brand.length>1);report.layouts.push(result);
  if([8,16,22,27].includes(id))await page.screenshot({path:`test-results/field-ch${id}.png`,fullPage:false});
 }
 await page.evaluate(()=>{__mfg30.select(29);__mfg30.select(28);__mfg30.select(30);});await page.evaluate(()=>__mfg30.realworld.ready);await page.waitForTimeout(200);
 assert.equal(await page.evaluate(()=>__mfg30.scene.scene.children.filter(x=>x.userData.oem).length),0);report.checks.push('chapter-change asynchronous model race guarded');
 await page.evaluate(()=>__mfg30.select(29));await page.evaluate(()=>__mfg30.realworld.ready);await page.setViewportSize({width:390,height:844});await page.locator('#rwOverview').click();await page.waitForTimeout(200);
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2),true);assert.equal(await page.locator('#rwJoints input').count(),6);await page.screenshot({path:'test-results/realworld-mobile.png',fullPage:true});report.checks.push('390px mobile source cards and six-joint controls');
 assert.equal(errors.length,0);assert.equal(failures.length,0);report.success=true;report.status='passed';
}finally{report.errors=errors;report.failedRequests=failures;report.finishedAt=new Date().toISOString();await fs.writeFile('test-results/realworld-browser.json',JSON.stringify(report,null,2));await browser.close();}
