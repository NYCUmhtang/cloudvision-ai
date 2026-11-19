# CloudVision AI

AI 衛星影像雲影辨識 LLM Wiki ＋ 互動式 HTML 教學簡報。

## 進度
- Phase 1：完成專案初始化及 AGENTS.md 工作規則。
- **Phase 2 Batch 1：已 Ingest 2 篇論文，建立 10 個知識條目**。
- 後續：仍需第 3～5 篇、完整 Graph、HTML 簡報、實際測試及反思。

## 學習路徑
- `wiki/index.md`：依六個模組找到條目。
- `sources.md`：每篇論文的 DOI、作者與原始檔資訊。
- `wiki/log.md`：Ingest／Query 紀錄。
- `report.md`：來源抽查、查詢範例與檢查紀錄。

## 使用方式
1. 解壓縮 ZIP 到本機，使用 VS Code 開啟 `CloudVision-AI`。
2. 執行 `python tests/check_scaffold.py` 及 `python tests/check_ingest.py`。
3. 將後續 PDF 存入 `raw/`，以分批方式繼續 Ingest。
4. PDF 已被 `.gitignore` 排除；**請勿將 raw 原文上傳公開 GitHub**。本 ZIP 中的 PDF 只供私人研究與查核。

## 後續完成標準
至少 5 篇成功 Ingest、Wiki 引用可追溯、Graph 明確退回條件、有真實測試紀錄，以及可瀏覽的互動 HTML 簡報。

## Phase 3 — 可執行 Workflow（2026-11-19）

已新增 Wiki Query、Coverage Gate、原文證據卡、引用忠實度檢查及教學大綱生成。執行方法：

```bash
python .agents/workflows/graph.py --run-id phase3_normal
python tests/check_graph.py
```

詳細 Graph 節點、回退規則、三次重試、故意注入錯誤的測試方法請讀 [.agents/workflows/README.md](.agents/workflows/README.md)。

**Phase 3 不產生 HTML**。目前的 Fidelity Check 是自動化的 Wiki 原文／引用一致性查核，並非獨立科學事實查核；最終還需要人工確認教學大綱。

## Phase 4：HTML 教學簡報（已實作／未發布）

- 直接開啟 `deck.html` 即可瀏覽 12 頁教學內容，無需安裝套件、CDN 或推論模型。
- 第 10 頁可以切換原圖、二元遮罩、多類別遮罩、疊合圖；均為**人工概念示意圖**，不是實際衛星影像或 AI 預測。
- 每頁有「查看知識來源」，可查看來源 Wiki 摘錄、原始文獻 DOI 與 PDF 頁碼。
- 逐頁文字及引用映射見 `drafts/`、`assets/slide_content.json`。
- 重新生成：`python .agents/workflows/phase4_graph.py --run-id phase4_repeat`
- 靜態檢查：`python tests/check_deck.py`
- 瀏覽器測試（需安裝 Playwright 與 Chromium）：`python tests/browser_check.py`
- 各項真實紀錄請見 `runs/` 與 `report.md`。論文忠實度的獨立審查、人工大綱核准和 GitHub Pages 發布尚待完成。

## Phase 5｜發布準備（尚未上傳 GitHub）

- `index.html` 是與 `deck.html` 完全相同的 GitHub Pages 入口。
- 請先讀 `PHASE5_REVIEW.md`、`DEPLOY_GITHUB_PAGES.md`、`SUBMISSION.md`。
- 發布前測試：`python tests/check_release.py`、`python tests/check_deck.py`。
- **網頁尚未發布；不可將未驗證的網址視為正式成果。**
