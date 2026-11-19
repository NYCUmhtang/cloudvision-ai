# CloudVision AI

**AI Satellite Cloud & Shadow Detection — LLM Wiki & Interactive Learning**

CloudVision AI 是一個結合大型語言模型（LLM）與遙測知識的互動式教學專案，透過學術文獻建立知識庫，介紹 AI 如何辨識衛星影像中的雲、雲影與清晰像元。

## 專案特色

- **LLM Wiki**：整合五篇研究文獻，建立六個主題模組與 19 個知識條目。
- **互動式教學**：以 12 頁 HTML 簡報介紹雲影偵測原理、AI 模型與評估方法。
- **知識來源追蹤**：簡報內容可對應 Wiki 條目及原始文獻。
- **Workflow 驗證**：包含知識檢索、證據整理、內容檢查與錯誤回退機制。

## 教學內容

1. 衛星影像與雲影問題
2. 雲、雲影與地形陰影
3. 多光譜影像判釋
4. 傳統雲影偵測方法
5. AI 與深度學習方法
6. 辨識成果與評估指標

## 線上體驗

**Interactive HTML Slides**

GitHub Pages 網址：部署完成後填入

## 專案架構

- `wiki/` — LLM 知識庫
- `cards/` — 知識來源證據卡
- `.agents/workflows/` — Loop / Graph 工作流程
- `tests/` — 自動化驗證
- `index.html` — 互動式教學簡報
- `sources.md` — 參考文獻
- `report.md` — 實作與驗證摘要

## 技術架構

LLM Wiki → Knowledge Retrieval → Evidence Validation → Teaching Outline → HTML Presentation

本專案以 Markdown 建立知識庫，使用 Python 實作流程檢查，並透過 HTML、CSS 和 JavaScript 呈現互動式教學內容。

## 備註

簡報中的互動影像為教學概念示意，不代表實際 AI 模型預測成果。
