# 教材技術圖

本目錄的 17 張 SVG 是原創、可編輯的技術示意，**不是朝陽科技大學機台照片或原廠手冊**。圖中比例、外觀、手柄與附件均簡化；操作前須以教師講解、實機標示及原廠資料核對。

`site-mill.jpg`、`site-lathe.jpg` 是使用者提供的現場照片，對應兩張 `site-*-callouts.svg`。照片導覽只標示可見位置，不推定型號、手柄功能、轉速設定或安全裝置。照片中的工具堆放不是可開機配置。

重建方式（不需第三方 Python 套件）：

```powershell
python scripts/generate_figures.py
```

所有圖使用 SVG `viewBox`、白色背景與繁體中文；一般標籤為 24–34 px。箭頭、尺寸和圖說均是可搜尋文字及向量路徑。

方向箭頭採顯式三角形向量，不依賴 SVG marker；可保留 svglib → ReportLab 的 PDF 箭頭。

|圖檔|主題|
|---|---|
|lathe-anatomy.svg|車床構造|
|lathe-motion.svg|車削運動|
|lathe-setup.svg|夾持與刀尖中心高|
|lathe-facing.svg|端面車削|
|lathe-turning.svg|外徑車削|
|lathe-drilling.svg|尾座鑽孔|
|lathe-project.svg|階梯軸二次裝夾|
|mill-anatomy.svg|立式膝式銑床構造|
|mill-axes.svg|工作台座標與相對刀具運動|
|mill-workholding.svg|虎鉗、平行墊鐵及避讓|
|mill-direction.svg|順逆銑接觸處方向|
|mill-datum.svg|尋邊半徑與 Z 量塊補償|
|mill-face.svg|平面覆蓋與薄切|
|mill-slot.svg|槽銑入口及分層|
|mill-project.svg|銑床成品尺寸與座標|
|safety-workflow.svg|每刀停機量測循環|
|measurement.svg|卡尺與分厘卡接觸概念|
|site-mill-callouts.svg|銑床實機照片導覽|
|site-lathe-callouts.svg|車床實機照片導覽|

技術核對重點：逆銑的工作台進給與接觸處刀刃速度相反，順銑相同；圖中兩刀皆順時針。車削直徑變化為徑向切深的兩倍。尋邊器中心由左側接觸時為 X=-R。槽長30、刀徑8對應中心行程22；練習槽中心X=19..41、Y=20。實機圖示不授權用未知手柄或表格配速。
