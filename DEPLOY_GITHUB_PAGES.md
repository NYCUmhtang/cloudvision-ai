# GitHub Pages 發布操作｜CloudVision AI Phase 5

目前**尚未公開發布**。使用者需在自己的 GitHub 帳號執行以下步驟，取得真正的公開網址。

1. 解壓縮 `CloudVision-AI_Phase5_PublicSafe.zip`，進入 `CloudVision-AI/`。**不要將含原始 PDF 的 Full 版上傳公開 GitHub**。
2. 在 GitHub 建立全新公開 Repository，建議名稱 `cloudvision-ai`，初始不加入 README（避免與本機產生衝突）。
3. 上傳 `CloudVision-AI/` **目錄內的全部檔案與子目錄**至 Repository 根目錄；須包含 `index.html`、`wiki/`、`cards/`、`assets/`、`.agents/`（如網頁介面無法上傳隱藏資料夾，可用 Git CLI）。
4. 到 Repository 的 `Settings` → `Pages` → `Build and deployment` → `Deploy from a branch`，選擇 `main`、`/(root)`，儲存。
5. 等候 GitHub Pages 顯示正式網址後，以無痕視窗開啟網站、用手機或裝置模擬驗證換頁、來源視窗及第 10 頁遮罩切換。
6. 若 Repo 名稱為 `cloudvision-ai`，典型網址形式為 `https://<GitHub使用者名稱>.github.io/cloudvision-ai/`，**這僅是格式範例，不是已驗證的發布網址**。
7. 將真實網址填入 `SUBMISSION.md`，並保留 GitHub Pages 開啟畫面及測試截圖。

### 在本機用 Git CLI（選用）

```
git init
git add .
git commit -m "Release CloudVision AI LLM Wiki and teaching slides"
git branch -M main
git remote add origin https://github.com/<你的帳號>/cloudvision-ai.git
git push -u origin main
```

`<你的帳號>` 是佔位符，不要原樣貼上。若已有 Git repository，切勿重複 init 或覆寫 remote。不要把 `raw/` PDF、憑證或私人資料 push 到公開專案。

### 發布後驗收（尚未執行）

- [ ] 公開 URL 可在未登入狀態打開
- [ ] 12 頁內容能正常換頁
- [ ] 第 10 頁示意圖切換成功且標示為示意
- [ ] 每頁知識來源視窗正常，DOI 可點擊
- [ ] 手機端無重大溢出
- [ ] 公開 GitHub 沒有受限制的 PDF
