import {chapters,references} from '../src/course.mjs';import {calculate,defaults,format} from '../src/models.mjs';import fs from 'node:fs/promises';
await fs.mkdir('docs',{recursive:true});
let text='# 30 章模型登錄與預設算例\n\n版本 2.0，2026-10-30。所有算例是程式解析值，不是實測數據。每章代表性模型不等同完整章節所有子題。\n\n';
for(const c of chapters){text+=`## ${c.id}. ${c.title}\n\n${c.summary}\n\n**公式：** ${c.formula}\n\n**假設與限制：** ${c.limit}\n\n|輸入|預設|單位|允許範圍|\n|---|---:|---|---|\n`+c.params.map(([k,l,u,lo,hi,s,v])=>`|${l}|${v}|${u||'無因次'}|${lo}–${hi}|`).join('\n')+'\n\n|預設輸出|解析值|單位|\n|---|---:|---|\n'+calculate(c,defaults(c)).outputs.map(o=>`|${o.label}|${format(o.value)}|${o.unit}|`).join('\n')+'\n\n**驗證任務：** '+c.experiment.join(' ')+'\n\n**來源脈絡：** '+c.sources.map(k=>`[${references[k].name}](${references[k].url})`).join('；')+'\n\n';}
text+='## 驗證層級\n\n110 項 Node 測試檢查內容結構、輸入範圍、輸出有限值、單位、守恆或縮放關係及 CSV 安全。瀏覽器測試另外檢查 30 個 WebGL 場景、操作流程與紀錄。軟體測試不等於材料參數校正、物理模型有效性驗證或教學成效驗證。請查看 GitHub Actions 與 test-results/browser-report.json 的實際結果。\n';
await fs.writeFile('docs/MODEL_REGISTER.md',text);await fs.writeFile('docs/curriculum.json',JSON.stringify(chapters,null,2));
