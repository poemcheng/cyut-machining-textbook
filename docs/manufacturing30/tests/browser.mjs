import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
await fs.mkdir('test-results',{recursive:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox','--enable-unsafe-swiftshader']});
const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
const errors=[],failures=[],report={schema:'mfg30-browser-test/v1',startedAt:new Date().toISOString(),chapters:[]};
page.on('pageerror',e=>errors.push(e.message));page.on('requestfailed',r=>failures.push(r.url()+': '+r.failure()?.errorText));
try{
 const base=process.env.BASE_URL||'http://127.0.0.1:8020/';
 await page.goto(base,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.__mfg30?.sceneReady,null,{timeout:30000});
 for(let id=1;id<=30;id++){
  await page.evaluate(id=>window.__mfg30.select(id),id);await page.evaluate(()=>window.__mfg30.realworld.ready);assert.equal(await page.evaluate(()=>window.__mfg30.realworld.currentId),id);assert.equal(await page.locator("#rwFlow button").count(),4);
  assert.equal(await page.locator('#chapterNumber').innerText(),String(id).padStart(2,'0'));
  assert.equal(await page.locator('#metrics .metric').count(),3);assert.equal(await page.locator('#inputError').innerText(),'');
  const view=await page.evaluate(()=>{const a=window.__mfg30,s=a.scene;s.render(.15);s.render(.85);const label=s.labels.join('|');let invalid=0;s.root.traverse(o=>{for(const n of [...o.position,...o.scale])if(!Number.isFinite(n))invalid++;});let invalidIndustrial=0;s.industrial.root.traverse(o=>{for(const n of [...o.position,...o.scale])if(!Number.isFinite(n))invalidIndustrial++;});return {id:a.current.id,objects:s.root.children.length,labels:label,invalid,industrial:s.industrial.stats,invalidIndustrial,drawCalls:s.renderer.info.render.calls};});
  assert.ok(view.objects>2);assert.ok(view.drawCalls>0);assert.equal(view.invalid,0);assert.equal(view.invalidIndustrial,0);assert.ok(view.industrial.parts>=30,`Chapter ${id} lacks mechanical detail`);assert.ok(view.industrial.motionChannels>=1,`Chapter ${id} lacks motion`);
  if([16,29].includes(id)){
  await page.locator('#viewMode').selectOption('concept');assert.equal(await page.evaluate(()=>window.__mfg30.scene.root.visible),true);await page.locator('#viewMode').selectOption('industrial');assert.equal(await page.evaluate(()=>window.__mfg30.current.id===29?window.__mfg30.realworld.robot?.root.visible:window.__mfg30.scene.industrial.root.visible),true);await page.locator('#parts').uncheck();await page.locator('#parts').check();await page.locator('#xray').check();await page.locator('#xray').uncheck();await page.locator('#wire').check();await page.locator('#cut').check();await page.locator('#wire').uncheck();await page.locator('#cut').uncheck();
  }
  if([1,4,8,16,17,22,26,29,30].includes(id))await page.locator('#viewport').screenshot({path:`test-results/ch${String(id).padStart(2,'0')}.png`});
  report.chapters.push(view);
 }
 await page.evaluate(()=>window.__mfg30.select(16));
 await page.screenshot({path:'test-results/desktop.png',fullPage:true});
 await page.locator('[data-tab="lab"]').click();await page.locator('#prediction').fill('預測切削速度提高會增加主軸轉速。');await page.locator('#captureA').click();
 await page.locator('#n-speed').fill('150');await page.locator('#captureB').click();
 await page.locator('#observation').fill('A 與 B 的主軸轉速不同，單位為 rpm。');await page.locator('#reflection').fill('未計入刀具磨耗與機台轉速限制，真機前須確認。');await page.locator('#saveLab').click();
 assert.equal(await page.evaluate(()=>window.__mfg30.state.chapters[16].labDone),true);
 await page.locator('[data-tab="quiz"]').click();const quiz=await page.evaluate(()=>({questions:window.__mfg30.current.questions,expected:window.__mfg30.quiz.expected.value}));
 for(let i=0;i<2;i++)await page.locator(`input[name="q${i}"][value="${quiz.questions[i].correct}"]`).check();
 await page.locator('input[name="q2"]').fill(String(quiz.expected));await page.locator('#quizForm button').click();
 assert.equal(await page.evaluate(()=>window.__mfg30.state.chapters[16].bestScore),3);assert.equal(await page.locator('#completeCount').innerText(),'1 / 30 章完成');
 await page.reload({waitUntil:'networkidle'});await page.waitForFunction(()=>window.__mfg30?.sceneReady);assert.equal(await page.locator('#completeCount').innerText(),'1 / 30 章完成');
 await page.locator('#n-speed').fill('999999');assert.ok((await page.locator('#inputError').innerText()).length>0);await page.locator('#resetParams').click();assert.equal(await page.locator('#inputError').innerText(),'');
 const download=page.waitForEvent('download');await page.locator('#exportTop').click();await(await download).saveAs('test-results/learning-record.json');const data=JSON.parse(await fs.readFile('test-results/learning-record.json','utf8'));assert.equal(data.schema,'manufacturing30/v2');
 await page.locator('[data-tab="records"]').click();await page.locator('#teacherFiles').setInputFiles('test-results/learning-record.json');await page.waitForFunction(()=>document.querySelector('#teacherTable').textContent.includes('1 份有效檔案'));
 await page.setViewportSize({width:390,height:844});await page.locator('[data-tab="model"]').click();await page.locator('#menu').click();await page.locator('#search').fill('焊接');assert.equal(await page.locator('[data-chapter]').count(),2);await page.locator('[data-chapter="22"]').click();
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2),false);await page.screenshot({path:'test-results/mobile.png',fullPage:true});
 Object.assign(report,{labAB:true,quiz:true,reloadPersistence:true,invalidInput:true,jsonExport:true,teacherImport:true,mobile:true,webGL:true,errors,networkFailures:failures});
 assert.deepEqual(errors,[]);assert.deepEqual(failures,[]);report.status='passed';
}catch(e){report.status='failed';report.error=e.stack;report.errors=errors;report.networkFailures=failures;await page.screenshot({path:'test-results/failure.png',fullPage:true}).catch(()=>{});throw e;}
finally{report.finishedAt=new Date().toISOString();await fs.writeFile('test-results/browser-report.json',JSON.stringify(report,null,2));await browser.close();}
console.log(JSON.stringify(report,null,2));
