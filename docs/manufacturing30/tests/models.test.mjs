import test from 'node:test';
import assert from 'node:assert/strict';
import {chapters,references} from '../src/course.mjs';
import {defaults,validate,calculate,csvCell} from '../src/models.mjs';
const calc=(id,overrides={})=>calculate(chapters[id-1],{...defaults(chapters[id-1]),...overrides});
const near=(a,b,t=1e-9)=>assert.ok(Math.abs(a-b)<=t*Math.max(1,Math.abs(b)),`${a} ≠ ${b}`);
test('exactly thirty unique ordered chapters',()=>assert.deepEqual(chapters.map(x=>x.id),Array.from({length:30},(_,i)=>i+1)));
for(const c of chapters){
 test(`Ch${c.id} content, parameter domains, units, quiz and sources`,()=>{
  assert.ok(c.summary.length>40);assert.equal(c.topics.length,3);assert.equal(c.questions.length,2);assert.equal(c.experiment.length,3);assert.ok(c.limit.length>20);assert.ok(c.formula.length>10);
  for(const q of c.questions){assert.equal(q.options.length,3);assert.ok(q.correct>=0&&q.correct<3);assert.ok(q.explain.length>5);}
  assert.equal(new Set(c.params.map(x=>x[0])).size,c.params.length);
  for(const r of c.sources)assert.ok(references[r]?.url.startsWith('https://'));
  const p=defaults(c);validate(c,p);const x=calculate(c,p);assert.equal(x.outputs.length,3);
  for(const o of x.outputs){assert.ok(Number.isFinite(o.value));assert.ok(o.label);assert.ok(o.unit);}
 });
 test(`Ch${c.id} rejects missing, NaN, infinity and out-of-domain input`,()=>{
  const d=c.params[0],base=defaults(c);for(const bad of [NaN,Infinity,-Infinity,d[3]-1,d[4]+1,undefined])assert.throws(()=>calculate(c,{...base,[d[0]]:bad}));
 });
 test(`Ch${c.id} samples all parameter ranges without nonfinite outputs`,()=>{
  const base=defaults(c);for(const [key,,u,min,max] of c.params)for(let i=0;i<=10;i++){
    const p={...base,[key]:min+(max-min)*i/10};
    if(c.id===13&&p.h0<=p.h1)continue;if(c.id===20&&p.initial<=p.ambient)continue;
    const r=calculate(c,p);r.outputs.forEach(o=>assert.ok(Number.isFinite(o.value),`${c.id} ${key} ${i} ${o.key}`));
  }
 });
}
test('cost exact default 80 currency per piece',()=>near(calc(1).outputs[0].value,80));
test('beam displacement inversely proportional to E',()=>near(calc(2,{modulus:100}).outputs[1].value/calc(2,{modulus:200}).outputs[1].value,2));
test('elastic stress doubles with force',()=>near(calc(3,{force:20000}).outputs[0].value/calc(3,{force:10000}).outputs[0].value,2));
test('clearance worst case calculation',()=>near(calc(4).outputs[0].value,.02));
test('Chvorinov similar scaling quadruplicates time',()=>near(calc(5,{radius:40,height:80}).outputs[0].value/calc(5).outputs[0].value,4));
test('isotropic sintering cube law',()=>{const p=defaults(chapters[10]);near(calc(11).outputs[0].value,p.length*Math.cbrt(p.green/p.final));});
test('rolling must reduce thickness',()=>assert.throws(()=>calc(13,{h0:10,h1:20})));
test('Taylor speed-life relation',()=>{const p=defaults(chapters[16]);near(calc(17).outputs[0].value,(p.C/p.speed)**(1/p.n));});
test('EDM capacitor energy quadratic in voltage',()=>near(calc(19,{voltage:200}).outputs[0].value/calc(19,{voltage:100}).outputs[0].value,4));
test('Newton cooling asymptote monotone',()=>assert.ok(calc(20,{time:120}).outputs[0].value<calc(20,{time:10}).outputs[0].value));
test('Faraday charge doubling doubles deposition',()=>near(calc(21,{time:40}).outputs[0].value/calc(21,{time:20}).outputs[0].value,2));
test('arc net input includes thermal efficiency',()=>near(calc(22,{efficiency:40}).outputs[0].value/calc(22,{efficiency:80}).outputs[0].value,.5));
test('resistance welding heat quadratic in current',()=>near(calc(23,{current:10}).outputs[0].value/calc(23,{current:5}).outputs[0].value,4));
test('layer count uses ceiling',()=>{const p=defaults(chapters[25]);near(calc(26).outputs[0].value,Math.ceil(p.height/p.layer));});
test('Rayleigh proportional to wavelength',()=>near(calc(27,{wavelength:300}).outputs[0].value/calc(27,{wavelength:150}).outputs[0].value,2));
test('bottleneck capacity',()=>near(calc(28,{t1:30,t2:60,t3:40}).outputs[0].value,60));
test('2R straight configuration',()=>{const p=defaults(chapters[28]),r=calc(29,{q1:0,q2:0});near(r.outputs[0].value,p.L1+p.L2);near(r.outputs[1].value,0);});
test('centered capability Cp=Cpk',()=>{const r=calc(30,{mean:50});near(r.outputs[0].value,r.outputs[1].value);});
test('CSV quotes and spreadsheet formula injection',()=>{assert.equal(csvCell('=1+1'),'"\'=1+1"');assert.equal(csvCell('a"b'),'"a""b"');assert.ok(csvCell('  @SUM(A1)').includes("'"));});
