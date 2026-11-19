# TAICA 作業繳交文字（待填姓名、學號及公開網址）

## 繳交標題

`學校 學號 系級 姓名 CloudVision AI`（請自行填寫真實資訊）

## 1. LLM Wiki 主題與介紹

CloudVision AI：AI 衛星影像雲影辨識。以 5 篇論文作為資料來源，建立六個知識模組及 19 個 Markdown Wiki 條目；從衛星影像、光譜、雲與雲影遮罩，到 Fmask、深度學習分割與模型評估，採取基礎與進階分層教學。

## 2. LLM Wiki 連結或成果

GitHub Repository：[**發布後填入真正 URL**]

成果：`wiki/index.md`（知識索引）、`wiki/W-*.md`（19 條目）、`sources.md`（5 篇來源）、`wiki/log.md`（Ingest 紀錄）。

## 3. 教學 HTML 簡報

GitHub Pages：[**發布後填入真正 URL**]

12 頁單一 HTML 簡報，具換頁、來源查閱與第 10 頁教學示意遮罩切換。繳交前請確認公開網址可實際瀏覽。

## 4. Loop / Graph 設計

原始論文分批 Ingest → Wiki 條目與索引 → Wiki Query → Coverage Check → Evidence Cards → 引用／來源一致性檢查 → 教學大綱 → 逐頁稿 → HTML Render → 靜態及瀏覽器檢查。

當證據卡頁碼錯誤，退回 Cards 節點修正；逐頁稿與輸出不一致，退回逐頁稿生成；缺少 Wiki 條目時最多重查 3 輪，仍不足就停止，不虛構資料。

## 5. 一次實際執行與檢查紀錄

- 正常 Phase 3：5 來源、19 條目、26 張證據卡、12/12 頁覆蓋，靜態驗證 PASS。
- 注入錯誤頁碼：首次檢查失敗，退回 Cards 修正一次後 PASS（控制性故障測試）。
- 注入不存在 Wiki ID：重查三次仍無證據，安全停止（預期 FAIL）。
- Phase 4：12 份逐頁稿，HTML 靜態檢查 PASS，Chromium 桌機＋手機 46/46 項測試 PASS。
- Phase 5：見 `report.md` 及 `runs/phase5_release_validation.json`；外部 GitHub Pages 驗證待發布後填寫。

## 6. 反思與修正

正常執行並沒有足夠失敗次數用來統計「最常出錯」節點；已觀察到 Batch 1 真實的來源頁碼格式缺失，並透過故障注入確認證據卡及逐頁稿階段是需要提早檢查的風險點。因此將引用格式檢查前移到 Wiki Ingest 與 Evidence Card 產生之後，不等 HTML 完成才驗證；並在渲染之前增加逐頁稿一致性檢查。重試上限三輪，證據不足時停止並回報。

**注意：** 控制性錯誤注入不是論文真實錯誤，也不表示某節點在自然執行中失敗率最高。
