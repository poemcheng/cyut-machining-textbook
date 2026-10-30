# 製造程序｜場域與品牌教學版 4.0

15 種原創代表性場域、27 筆原廠設備案例、30 章完整學習流程。**UR5e 與 TM5-900 已實際導入原廠公開的視覺三角網格與名義關節鏈**，其餘機台仍為通用機構重建，原廠案例卡不是原廠 CAD。

[公開平台](https://poemcheng.github.io/cyut-machining-textbook/manufacturing30/) · [品牌與授權來源](docs/REALWORLD_SOURCES.md) · [操作手冊](docs/USER_GUIDE.md)

依 Groover《製造程序》（滄海書局 ME0348C）公開的 30 章目錄獨立編寫。**每章各一個代表性互動單元，三十章均提供完整學習流程；不是原書全文、原圖或原書題庫的重製，也不涵蓋每個小節的所有設備。**

[開啟課程](https://poemcheng.github.io/cyut-machining-textbook/manufacturing30/) · [使用手冊](docs/USER_GUIDE.md) · [模型登錄與算例](docs/MODEL_REGISTER.md) · [18 週教學安排](docs/TEACHING_PLAN.md)

每章包含導讀、三個觀念、三個學習目標、專屬 Three.js 場景、帶單位參數、三項解析計算、假設與限制、A/B 實驗、兩題概念與一題參數化計算評量。共 30 場景、30 模型、90 個評量題位。模型是教學解析式與幾何／運動示意，不是經實驗校正的 CAE。

## 本機執行

解壓縮，進入本資料夾：

```sh
python -m http.server 8000
```

Windows 可使用 `py -m http.server 8000`；macOS/Linux 可使用 `python3 -m http.server 8000`。瀏覽 `http://localhost:8000`，不要直接雙擊 HTML。提供 Windows 啟動檔 `start-windows.bat` 與 `start-unix.sh`。

通過 CI 的正式版本與下載套件包含 `vendor/`：固定版本 Three.js 0.164.1、OrbitControls 與其 MIT 授權。資源全部由同一網站或本機提供，執行課程不需要 CDN、Node.js、API 金鑰或付費服務。Node.js 僅用於維護與測試。

## 學習與紀錄

選章 → 理解模型限制 → 寫下預測 → 擷取 A → 修改參數並擷取 B → 引用數值與單位解釋 → 完成三題 → 匯出 JSON。完成條件是實驗已存且最高答對至少 2/3；這是教學設定，不是實機能力認證。

紀錄只在瀏覽器 localStorage；沒有雲端資料庫或跨裝置同步。使用匿名代碼，教師可匯入多份 JSON，在本機檢視，不自動合併同一人的多份紀錄。CSV 僅提供章節摘要。

## 重現測試

```sh
node --test tests/models.test.mjs
npm install
npx playwright install chromium
python -m http.server 8020
# 另一個終端機
npm run test:browser
```

110 項單元測試檢查內容、輸入域、單位與公式關係。瀏覽器測試要求真實 WebGL，逐章檢查 30 個場景與 90 個結果面板，另測 A/B、評量、重載保存、JSON 匯出、教師匯入及手機版。實際執行狀態請查看 [GitHub Actions](https://github.com/poemcheng/cyut-machining-textbook/actions/workflows/manufacturing30-check.yml) 與其 `manufacturing30-verification` artifact。軟體測試不代表實機、材料模型或教學成效已獲驗證。

## 維護結構

`src/chapters/part1–3.mjs` 保存原創文字、參數與概念題；`course.mjs` 彙整章節與來源；`models.mjs` 保存 30 章解析式；`scenes.mjs` 保存獨立程序化場景；`app.mjs` 負責互動、評量及紀錄。`node scripts/build-register.mjs` 由同一份資料生成模型登錄與 curriculum.json，避免文件與程式分離。

本子目錄獨立於既有車銑床教材，未覆寫原首頁。原創程式 MIT；原創文字 CC BY 4.0；第三方及教科書不在本授權內。參數是教學假設，禁止直接當成機台安全設定。
