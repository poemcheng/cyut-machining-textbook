# 場域、品牌、設備與官方模型來源登錄 — v4.0

查核日期：2026-10-31。這是代表性案例選編，不是市占排行、廠商推薦、實際校內設備盤點或某工廠數位孿生。

## 三種證據必須分開

- 官方視覺模型：UR5e、TM5-900，來自各製造商 GitHub 公開的 VISUAL 網格；以固定 commit 保留來源、BSD-3-Clause 授權及雜湊。轉換為 float32 索引網格，不簡化三角面，也不用 collision 模型代替。
- 原廠案例：其他品牌僅以原廠產品頁佐證設備類別與系列。沒有重新授權的 CAD 不下載、不複製圖片或商標、不把通用模型改名冒充 OEM。
- 場域與周邊：15 種原創教學布局，地坪、物流區、周邊與主機尺度正規化；不是實地測繪、BIM、碰撞分析或職安審查結果。

## 全書 30 章對應

|章|代表場域|原廠案例|官方機器人可選|
|---|---|---|---|
|1|精密零件加工廠|東台 Tongtai TMT2000-T2Y1；Haas VF-2；Universal Robots UR5e|UR5e / TM5-900|
|2|材料試驗實驗室|Instron 6800 系列|—|
|3|材料試驗實驗室|Instron 6800 系列|—|
|4|恆溫品管量測室|Mitutoyo 三豐 CRYSTA-Apex V|—|
|5|鑄造與壓鑄工作區|DISA DISAMATIC D3|—|
|6|鑄造與壓鑄工作區|Bühler Carat|—|
|7|玻璃容器成形線|Bucher Emhart Glass AIS|—|
|8|塑膠射出加工廠|富強鑫 FCS FA 系列|—|
|9|複合材料成形工坊|Schuler Hydraulic Press Technology|—|
|10|粉末冶金工作區|DORST Technologies TPA120 HS|—|
|11|熱處理與燒結區|Nabertherm Chamber Furnaces；DORST Technologies TPA120 HS|—|
|12|沖壓與金屬成形廠|Schuler MH 系列|—|
|13|沖壓與金屬成形廠|SMS group Tandem Cold Mills|—|
|14|沖壓與金屬成形廠|金豐 Chin Fong OCP-EW 系列|—|
|15|精密零件加工廠|Haas ST-20|—|
|16|精密零件加工廠|東台 Tongtai TMT2000-T2Y1；Haas ST-20|—|
|17|精密零件加工廠|Haas VF-2|—|
|18|精密零件加工廠|福裕 Chevalier FSG-1216ADIV|—|
|19|精密零件加工廠|慶鴻 CHMER CM434C|—|
|20|熱處理與燒結區|Nabertherm Chamber Furnaces|—|
|21|表面處理產線|Atotech GMF Plating Equipment|—|
|22|焊接與接合工作站|Fronius TPS/i|—|
|23|焊接與接合工作站|TECNA Spot Welding Stations|—|
|24|裝配與機器人工作站|Nordson EFD EV 系列|—|
|25|裝配與機器人工作站|Atlas Copco Tensor IxB；Universal Robots UR5e；達明 Techman Robot TM5-900|UR5e / TM5-900|
|26|積層製造實作室|UltiMaker S5|—|
|27|微製造無塵室單元|ASML TWINSCAN NXT:1980Di；SUSS MA/BA Gen4|—|
|28|裝配與機器人工作站|東台 Tongtai TMT2000-T2Y1；Universal Robots UR5e；達明 Techman Robot TM5-900|UR5e / TM5-900|
|29|裝配與機器人工作站|Universal Robots UR5e；達明 Techman Robot TM5-900|UR5e / TM5-900|
|30|恆溫品管量測室|Mitutoyo 三豐 CRYSTA-Apex V|—|

## 設備來源與使用限制

### 東台 Tongtai — TMT2000-T2Y1

類型：複合車削中心。證據層級：manufacturer-reference。

[原廠來源](https://www.tongtai.com.tw/en/product-detail.php?id=70)。

比較主軸、刀塔、棒材進料與工件移交。選配與年度規格須回到原廠頁核對。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### Haas — VF-2

類型：立式加工中心。證據層級：manufacturer-reference。

[原廠來源](https://www.haascnc.com/machines/vertical-mills/vf-series/models/small/vf-2.html)。

觀察 X/Y 工作台、Z 主軸與刀庫；區分刀具進給與主軸轉速。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### Haas — ST-20

類型：CNC 車削中心。證據層級：manufacturer-reference。

[原廠來源](https://www.haascnc.com/machines/lathes/st/models/standard/st-20.html)。

辨認主軸夾持、X/Z 進給、刀塔與排屑位置。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### Instron — 6800 系列

類型：萬能材料試驗機。證據層級：manufacturer-reference。

[原廠來源](https://www.instron.com/en/products/testing-systems/universal-testing-systems/6800-series/)。

觀察夾具、荷重元與伸長量量測；量測剛性和設備剛性不可混為一談。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### Mitutoyo 三豐 — CRYSTA-Apex V

類型：三次元座標量測機。證據層級：manufacturer-reference。

[原廠來源](https://www.mitutoyo.com/products/coordinate-measuring-machines/standard-coordinate-measuring-machines/crysta-apex/)。

由基準建立、探點、座標擬合到報告；量測前要考慮溫度與探針校驗。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### DISA — DISAMATIC D3

類型：垂直綠砂造模線。證據層級：manufacturer-reference。

[原廠來源](https://www.disagroup.com/d3/)。

比較垂直無砂箱造模與課堂砂箱示意；不可把相同澆道公式當作相同機構。

DISAMATIC 是垂直造模案例；此章仍以通用砂箱展示鑄造基本原理，非 D3 機構複製。

### Bühler — Carat

類型：雙模板壓鑄機。證據層級：manufacturer-reference。

[原廠來源](https://www.buhlergroup.com/global/en/products/carat_die-castingmachine.html)。

辨認合模、射出與取件順序，並比較壓鑄與重力砂模充填。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### Bucher Emhart Glass — AIS

類型：玻璃容器成形設備。證據層級：manufacturer-reference。

[原廠來源](https://www.emhartglass.com/Products/Equipment/FormingEquipment/ContainerForming/AIS)。

從料滴、初模到成形模，分清玻璃容器加工各工站。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### 富強鑫 FCS — FA 系列

類型：伺服節能射出成形機。證據層級：manufacturer-reference。

[原廠來源](https://zh-tw.fcs.com.tw/products_i_hydraulic-injection-molding-machine)。

辨認料斗、塑化料筒、合模機構；場域加入乾燥與冷卻周邊，但不當作標準配備承諾。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### Schuler — Hydraulic Press Technology

類型：複材液壓成形設備。證據層級：manufacturer-reference。

[原廠來源](https://www.schulergroup.com/major/us/technologien/hydraulic_press_technology/index.html)。

比較纖維鋪層、加熱、加壓與固化；單一混合法則不代表完整製程模型。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### DORST Technologies — TPA120 HS

類型：粉末壓製機。證據層級：manufacturer-reference。

[原廠來源](https://www.dorst-technologies.com/en/products/axial-powder-presses/product/tpa120-hs)。

觀察送粉、上下沖頭、模穴與脫模；壓坯仍需後續燒結。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### Nabertherm — Chamber Furnaces

類型：箱型熱處理／燒結爐。證據層級：manufacturer-reference。

[原廠來源](https://nabertherm.com/en/products/industrie/additive-fertigung/binderfrei/furnaces-protective-gas-boxes/chamber-furnaces-1)。

區分批次爐與連續爐；材料、氣氛、升降溫歷程須依實際工藝驗證。

本案例為箱型爐；第 11 章連續式燒結爐只作機構比較，不能視為同一設備。

### Schuler — MH 系列

類型：液壓鍛造壓機。證據層級：manufacturer-reference。

[原廠來源](https://www.schulergroup.com/major/us/technologien/produkte/anlagen_warmumformung_schmiedepressen_hydraulisch/index.html)。

比較主缸、滑塊、砧座及模具；理想鍛壓力不等於機台額定能力驗證。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### SMS group — Tandem Cold Mills

類型：串列冷軋設備。證據層級：manufacturer-reference。

[原廠來源](https://www.sms-group.com/plants/all-plants/tandem-cold-mills-steel/)。

比較工作輥、支撐輥、張力與多機架；教材雙輥算例只呈現局部變形原理。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### 金豐 Chin Fong — OCP-EW 系列

類型：C 型單曲軸沖床。證據層級：manufacturer-reference。

[原廠來源](https://zh-tw.chinfong.com/c-frame-single-crank-power-presses-ocp-ew-series1)。

沿飛輪／曲軸／連桿／滑塊辨認力的傳遞；本章折彎算例不代表沖床操作設定。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### 福裕 Chevalier — FSG-1216ADIV

類型：精密平面磨床。證據層級：manufacturer-reference。

[原廠來源](https://www.chevaliertw.com/en/products/FSG-1216ADIV-Series)。

觀察砂輪護罩、磁性工作台、冷卻及修整；周速與主軸轉速的單位不同。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### 慶鴻 CHMER — CM434C

類型：成形放電加工機。證據層級：manufacturer-reference。

[原廠來源](https://www.chmer.com/en/products/die-sinker-edm/die-sinker-cnc-series)。

觀察電極、介電液槽與間隙控制；這是成形放電，不是線切割。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

X/Y/Z 行程：400 × 300 × 350 mm（原廠參考值；未套用到通用網格尺寸）。
原廠外形 W/D/H：1240 × 1380 × 2230 mm（原廠參考值；未套用到通用網格尺寸）。
### Atotech — GMF Plating Equipment

類型：掛鍍與滾鍍產線。證據層級：manufacturer-reference。

[原廠來源](https://www.atotech.com/products/general-metal-finishing/equipment/)。

辨認前處理、水洗、鍍槽、排氣與廢液處理；教材銅沉積公式不指定商用藥水。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### Fronius — TPS/i

類型：MIG/MAG 焊接系統。證據層級：manufacturer-reference。

[原廠來源](https://www.fronius.com/en-gb/uk/welding-technology/product-information/tpsi-mig-mag-welding-system)。

沿電源、送絲、保護氣、焊槍觀察；淨熱輸入不等於焊接品質判定。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### TECNA — Spot Welding Stations

類型：電阻點焊工作站。證據層級：manufacturer-reference。

[原廠來源](https://www.tecna.net/industrial-resistance-welding-systems/spot-welding-stations/)。

觀察電極加壓、通電、維持及釋放；I²Rt 是簡化熱量而非焊核模型。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### Nordson EFD — EV 系列

類型：三軸點膠機。證據層級：manufacturer-reference。

[原廠來源](https://www.nordson.com/en/products/efd-products/3-axis-ev-series-automated-fluid-dispensing-robot)。

觀察膠筒、針頭、治具與路徑；接合面積公式不取代黏著劑固化試驗。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### Atlas Copco — Tensor IxB

類型：電動鎖付工具。證據層級：manufacturer-reference。

[原廠來源](https://www.atlascopcogroup.com/en/media/press-releases/2021/20210428-red-dot-awards)。

比較扭矩、轉角與預緊力；扭矩係數要由材料、潤滑與實驗確認。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### UltiMaker — S5

類型：材料擠出式 3D 列印機。證據層級：manufacturer-reference。

[原廠來源](https://ultimaker.com/3d-printers/s-series/ultimaker-s5/)。

辨認熱床、噴頭、耗材及層高；教學時間估算未含切片加減速與換料。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### ASML — TWINSCAN NXT:1980Di

類型：浸潤式 DUV 投影曝光設備。證據層級：manufacturer-reference。

[原廠來源](https://www.asml.com/en/en/products/duv-lithography-systems/twinscan-nxt1980di)。

以投影曝光討論波長、數值孔徑與解析尺度；本場景沒有重建商用光學系統。

網站機台為通用教學重建，非此品牌型號的原廠 CAD。

### SUSS — MA/BA Gen4

類型：掩模／鍵合對準機。證據層級：manufacturer-reference。

[原廠來源](https://www.suss.com/tw/products-solutions/imaging-solutions/mask-alignment/maba-gen4-series)。

比較接觸式／接近式對準與投影曝光；不要直接將投影 NA 算式套用此案例。

只作曝光方式比較；章內投影解析算式不是 MA/BA Gen4 的性能預測。

### Universal Robots — UR5e

類型：協作機械手臂。證據層級：official-visual。

[原廠來源](https://github.com/UniversalRobots/Universal_Robots_ROS2_Description)。

原廠七個視覺連桿、六旋轉關節與名義正運動學，可獨立調整角度。

已導入官方視覺網格及名義運動學；未經單機校正、碰撞或實機安全驗證。

### 達明 Techman Robot — TM5-900

類型：協作機械手臂。證據層級：official-visual。

[原廠來源](https://github.com/TechmanRobotInc/TM_Cobots_ROS2_Description)。

原廠七個視覺連桿與名義 URDF 關節，可與 UR5e 比較構形。

已導入官方視覺網格及名義 URDF；未校正到實驗室的特定機台。


## 官方模型再現與授權

UR：`UniversalRobots/Universal_Robots_ROS2_Description@81f7c9fe003c2f0e02eec5a7253f1b262ad38b61`。只取 UR5e，不把其他型號不同授權的素材納入。
TM：`TechmanRobotInc/TM_Cobots_ROS2_Description@377e2aacd95318903bc293bf694a044801e78128`，取 TM5-900。
個別授權與原始 README 位於 `assets/oem/{ur5e,tm5-900}/`。`model.json` 列出每個視覺來源檔案的 SHA-256、視覺位移、材質、關節座標與三個 NumPy 正運動學測試姿態；`index.json` 記錄輸出校驗碼。網格改動只包括 COLLADA 內部變換烘焙、索引整理及 float32 轉換。原有顏色保留為數值材質，並非重新製作商標。
UR elbow（J3）沿用官方描述庫的規劃用 ±180° 限制，不能把此數值當成實機硬限位。兩種模型的工具座標、原點定義不同，須分別閱讀來源。
所有商標及產品名稱屬原權利人；來源授權不表示廠商背書。官方網格本身不構成完整參數式 CAD、經序號校正的幾何、碰撞安全、載重驗證或實機可用軌跡。

## 重建

CI 先取得上述固定來源，執行 `python scripts/prepare-manufacturer-assets.py --intake /tmp/mfg-intake --output assets/oem`，再執行 `node scripts/build-realworld-register.mjs`。完整建置流程在儲存庫的 GitHub Actions。

## 課堂建議

以「原料 → 主機 → 周邊 → 在製品 → 品管」辨認場域。學生在原有實驗反思欄記錄：品牌來源、模型層級、一個吻合處、一個不能由此模型推論的真實條件。不能用瀏覽器模型測試通過當作教學成效證明。