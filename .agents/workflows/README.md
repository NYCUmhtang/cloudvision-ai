# CloudVision AI — Phase 3 可執行 Graph v1.0

**目前可執行範圍**：Wiki Query → Coverage Check → Evidence Cards → Fidelity Check（原文及來源一致性）→ proposed Outline → Outline Check → Human Approval Gate（等待人工）。本階段**不會**產生逐頁稿、AI 模型輸出或 HTML。

## 在專案根目錄執行

```bash
python .agents/workflows/graph.py --run-id phase3_normal
python tests/check_graph.py
python tests/check_ingest.py
python tests/check_scaffold.py
```

無需安裝第三方套件。每次 Graph 執行將記錄 `runs/<run-id>_trace.json`、`runs/<run-id>_coverage.json`，並且在全部關卡通過時更新 `cards/CARD-S*.json` 和 `outline.md`。

## 節點資料權限

| 節點 | 讀取 | 寫入 | FAIL 退回 |
|---|---|---|---|
| Query | `wiki/index.md`、`wiki/W-*.md`、`slide_plan.json` | run trace | 重新查詢；無可用 Wiki 則停止等待 Ingest |
| Coverage | 指定 Wiki ID 與檢索結果 | coverage JSON | 最多 3 次重試，仍失敗則 BLOCK |
| Evidence Cards | Wiki 既有段落與來源標記 | cards JSON（僅全部通過時） | 自動重建受到影響的卡片 |
| Fidelity Check | card、相應 Wiki、`sources.md` | trace（不偷偷改卡片） | 返回 Evidence Cards，最多 3 輪 |
| Outline | slides 配置與通過的卡片 | `outline.md`（僅全部通過時） | 檢查失敗則不發布 |
| Human Approval | outline | 無（等待使用者決定） | 未批准不進 Phase 4 |

**重要實作限制**：

- Query 會從索引中讀取**預先指定的 Wiki ID** 並記錄字詞比對分數；不是任意自然語言的語意檢索服務，分數不構成內容充分性的證明。
- Coverage Gate 檢查每頁的指定 Wiki ID 是否完整，不會自行擴充外部知識。
- Evidence Card 完整保留 Wiki 節錄、來源與原始 Wiki SHA256。Fidelity Gate 能偵測證據卡遭竄改、來源 ID 或頁碼不一致，但**不能證實原始 Wiki 文字與 PDF 科學意義完全相符**。
- 修正的內容來自**同一 Wiki 原文**，不是以模型臆測補充來源。
- 必須另行由獨立審查者核對重要科學結論、數字與 PDF，並由使用者核准大綱。
- 每個問題最多 3 次修正嘗試，超過即停止。測試錯誤注入不代表真實論文存在同類錯誤。
- 沒有資料就記錄 `INSUFFICIENT_WIKI_EVIDENCE` 並停止，不可直接跳過或默認通過。

## 可重現的錯誤注入測試

```bash
python .agents/workflows/graph.py --run-id phase3_fidelity_repair --inject-card-failure
python .agents/workflows/graph.py --run-id phase3_coverage_stop --inject-coverage-failure
```

第一個測試把第一張卡的頁碼改成測試用錯誤值，Fidelity Check 應發現 mismatch、退回 Evidence Cards 並修復。第二個測試給第一頁不存在的 Wiki ID，Coverage 應在重查 3 次後阻擋；因此該命令預期以退出碼 **1** 結束，並保留先前成功生成的卡片和大綱。

## 未來 Phase 4

人工批准大綱後，才開發 Slide Draft → Scientific Fidelity Review → HTML Render → UI Validation。這三段目前尚未實作，不得在作業報告中宣稱已執行。

## Phase 4：逐頁稿 → HTML（已實作）

執行 `python .agents/workflows/phase4_graph.py --run-id phase4_normal`，會檢查 26 張證據卡、產生 12 份逐頁稿及獨立的 `deck.html`，然後執行來源格式與逐頁內容一致性檢查。若生成檔案不一致，返回 N05 重建，最多 3 輪；若卡片來源缺失則停止，不能靠自動重新寫作補足證據。

- 故障注入：`--inject-draft-error`、`--inject-missing-evidence`，僅用於測試，不是研究論文或正常 Wiki 內容有錯。
- `tests/check_deck.py` 是**確定性格式／映射檢查**，不是獨立文獻語意驗證。
- 逐頁草稿與原始 Wiki 的科學忠實度、12 頁大綱人工核准、公開網址部署仍待 Phase 5。
