import fs from 'node:fs/promises';import {CATALOG} from '../src/realworld-catalog.mjs';
const lines=['# 場域、品牌、設備與官方模型來源登錄 — v4.0','',
'查核日期：2026-10-31。這是代表性案例選編，不是市占排行、廠商推薦、實際校內設備盤點或某工廠數位孿生。',
'','## 三種證據必須分開','',
'- 官方視覺模型：UR5e、TM5-900，來自各製造商 GitHub 公開的 VISUAL 網格；以固定 commit 保留來源、BSD-3-Clause 授權及雜湊。轉換為 float32 索引網格，不簡化三角面，也不用 collision 模型代替。',
'- 原廠案例：其他品牌僅以原廠產品頁佐證設備類別與系列。沒有重新授權的 CAD 不下載、不複製圖片或商標、不把通用模型改名冒充 OEM。',
'- 場域與周邊：15 種原創教學布局，地坪、物流區、周邊與主機尺度正規化；不是實地測繪、BIM、碰撞分析或職安審查結果。',
'','## 全書 30 章對應','', '|章|代表場域|原廠案例|官方機器人可選|','|---|---|---|---|'];
for(const p of CATALOG.chapters)lines.push(`|${p.chapter}|${CATALOG.fields[p.field].name}|${p.cases.map(k=>CATALOG.cases[k].brand+' '+CATALOG.cases[k].model).join('；')}|${p.robot?'UR5e / TM5-900':'—'}|`);
lines.push('','## 設備來源與使用限制','');
for(const c of Object.values(CATALOG.cases))lines.push(`### ${c.brand} — ${c.model}`,'',`類型：${c.kind}。證據層級：${c.evidence}。`, '',`[原廠來源](${c.url})。`, '',c.observation,'',c.distinction,'',...(c.spec.length?c.spec.map(([k,v])=>`${k}：${v}（原廠參考值；未套用到通用網格尺寸）。`):[]));
lines.push('','## 官方模型再現與授權','',
'UR：`UniversalRobots/Universal_Robots_ROS2_Description@81f7c9fe003c2f0e02eec5a7253f1b262ad38b61`。只取 UR5e，不把其他型號不同授權的素材納入。',
'TM：`TechmanRobotInc/TM_Cobots_ROS2_Description@377e2aacd95318903bc293bf694a044801e78128`，取 TM5-900。',
'個別授權與原始 README 位於 `assets/oem/{ur5e,tm5-900}/`。`model.json` 列出每個視覺來源檔案的 SHA-256、視覺位移、材質、關節座標與三個 NumPy 正運動學測試姿態；`index.json` 記錄輸出校驗碼。網格改動只包括 COLLADA 內部變換烘焙、索引整理及 float32 轉換。原有顏色保留為數值材質，並非重新製作商標。',
'UR elbow（J3）沿用官方描述庫的規劃用 ±180° 限制，不能把此數值當成實機硬限位。兩種模型的工具座標、原點定義不同，須分別閱讀來源。',
'所有商標及產品名稱屬原權利人；來源授權不表示廠商背書。官方網格本身不構成完整參數式 CAD、經序號校正的幾何、碰撞安全、載重驗證或實機可用軌跡。',
'','## 重建','',
'CI 先取得上述固定來源，執行 `python scripts/prepare-manufacturer-assets.py --intake /tmp/mfg-intake --output assets/oem`，再執行 `node scripts/build-realworld-register.mjs`。完整建置流程在儲存庫的 GitHub Actions。',
'','## 課堂建議','',
'以「原料 → 主機 → 周邊 → 在製品 → 品管」辨認場域。學生在原有實驗反思欄記錄：品牌來源、模型層級、一個吻合處、一個不能由此模型推論的真實條件。不能用瀏覽器模型測試通過當作教學成效證明。');
await fs.writeFile('docs/REALWORLD_SOURCES.md',lines.join('\n'));await fs.writeFile('docs/REALWORLD_CATALOG.json',JSON.stringify(CATALOG,null,2));
