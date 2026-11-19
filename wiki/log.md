# Wiki Operation Log

| 日期 | 操作 | 來源／條目 | 驗證結果 | 備註 | Git commit |
|---|---|---|---|---|---|
| 2026-11-19 (Asia/Taipei; 本批作業日期) | Ingest Batch 1 | P01、P02；10 個條目 | PDF 可讀、來源 DOI 與頁數核對；Lint 結果見 report.md | PDF 存於 raw/，已被 Git 忽略 | 尚未 commit |
| 2026-11-19 (Asia/Taipei; 本批作業日期) | Query 檢查（人工設計問題） | W-M02-002、W-M04-001、W-M06-002 | 詳見 `report.md`，查詢依 Wiki 已寫入之條目進行 | 目前非全自動 RAG 系統 | 尚未 commit |

| 2026-11-19 | Lint 第 1 輪 | W-M06-001 | FAIL（1 issue） | 缺乏符合格式的 PDF 頁碼標記 | 尚未 commit |
| 2026-11-19 | 修正＋Lint 第 2 輪 | W-M06-001 | PASS（0 issues） | 補足來源頁碼，重新執行檢查 | 尚未 commit |

**注意：** Phase 2 Batch 1 是兩篇文獻，不代表全部五篇已完成；尚未執行完整 Graph 或產生 HTML。

| 2026-11-19 | Ingest Batch 2 | P03 CloudSEN12、P04 AI Survey；6 個新條目（含跨來源條目） | DOI、頁碼與主要圖表對讀；見 report.md | 注意 CloudSEN12 49,400 / 49,250 來源內部數字差異 | 尚未 commit |
| 2026-11-19 | Ingest Batch 3 | P05 CloudS2Mask；3 個新條目 | 方法、實驗指標、資料集與速度條件查核；見 report.md | 不將不同論文 OA/BOA 直接排名 | 尚未 commit |
| 2026-11-19 | Lint Batch 2–3 | 5 篇 PDF、19 條 Wiki | PASS（0 issues） | `tests/check_ingest.py`：SHA256、ID、索引、頁碼引用；`tests/check_scaffold.py` PASS | 尚未 commit |

## 2026-11-19 — Phase 3 Graph implementation

- Read existing `wiki/index.md` and 19 Wiki entries associated with P01–P05. Original entries and raw PDFs were preserved.
- Created 12 proposed slide/query specifications and 26 machine-traceable evidence cards derived from existing Wiki paragraphs.
- Executed normal, controlled fidelity-error and missing-coverage test runs. Detailed node-by-node JSON is in `runs/`.
- Fidelity error injection: intentionally changed one generated card's page field; verifier detected mismatch and regenerated the card from the Wiki (one correction).
- Coverage error injection: asked for nonexistent `W-M99-999`; three re-query attempts failed, graph stopped safely without publishing partial results.
- Did **not** independently reread and semantically verify every original PDF claim, approve final outline, or produce HTML. These remain pending.
