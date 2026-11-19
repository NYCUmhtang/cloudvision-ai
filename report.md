# CloudVision AI — Verification & Reflection Report

## Phase 1（承接原專案）
已完成基本架構；`tests/check_scaffold.py` 可重新驗證。此階段尚未產生 HTML。

## Phase 2｜Batch 1（2026-11-19）

- 使用者提供 **P01（42 頁）**、**P02（20 頁）** 原始 PDF；已保留在 `raw/`，不進 Git。
- 核對論文題名、作者、年份、DOI、PDF 頁數及來源授權資訊。
- 建立 **10 個 Wiki 條目**、六模組索引及來源登錄表，均有來源 ID／章節或 PDF 頁碼。
- **成功 Ingest：2 / 5 篇**（只統計本次實際解析與整理成功的文獻）。

### 內容抽查：實際對照 PDF 的關鍵證據

| 條目 | 要點 | 出處 |
|---|---|---|
| W-M02-002 | 二元遮罩可只分雲，也可把雲與雲影合併為污染類別；必須記錄定義 | P01 §3，PDF pp.7–8，Fig.4 |
| W-M04-001 | Fmask 4.0 雲影演算法沿用 MFmask；Figure 5 為整體流程 | P02 §3，PDF pp.5–6，Fig.5 |
| W-M04-002 | Sentinel-2 缺熱紅外，Fmask 4.0 用 HOT-based probability 補充 | P02 §3.2.2–3.2.3，PDF p.8 |
| W-M06-002 | Sentinel-2 overall accuracy：Fmask 4.0 94.30%；Sen2Cor 2.5.5 87.10% | P02 Table 5，PDF p.16 |
| W-M06-002 | Sentinel-2 雲影 UA：Fmask 4.0 62.90%；Sen2Cor 2.5.5 73.33%；不可只宣稱前者所有指標較好 | P02 Table 5，PDF p.16 |

### Wiki Query 範例（根據條目答案檢查，非自動索引引擎測試）

**Q1：二元雲遮罩一定排除雲影嗎？** 否。P01 區分 cloud-only 與 cloud-contaminated 兩種二元定義。來源 `W-M02-002`／P01 pp.7–8。

**Q2：Fmask 4.0 的雲影投影是新發明嗎？** 否。P02 §3 指出沿用 MFmask。來源 `W-M04-001`／P02 p.5。

**Q3：Fmask 在 Sentinel-2 的所有雲影指標都勝過 Sen2Cor 嗎？** 否。該實驗的 Sen2Cor 雲影 User’s Accuracy 更高。來源 `W-M06-002`／P02 p.16。

### 已辨識的風險及處理

- **跨文獻比較風險：** P01 為跨研究綜述，P02 為特定實驗，已在 W-M05-001 註明不可直接跨資料集比 Accuracy。
- **雲影指標誤導：** 已在 W-M06-002 同列 Producer’s/User’s Accuracy；避免只突出 overall accuracy。
- **著作權風險：** P02 原始 PDF 為 Elsevier 版權文獻；Git 忽略 `raw/`，ZIP 僅供使用者私人離線使用，不應公開轉發。

### 當前尚未完成

- 第 3–5 篇文獻 Ingest。
- 獨立的 AI 二次審查及完整 Graph 執行。
- HTML 簡報與瀏覽器渲染／互動測試。
- 正式的「最常出錯節點」統計及流程改進反思：**待累積真實執行數據**。

## Lint 真實執行紀錄

| 順序 | 檢查 | 結果 | 發現的問題／處理 |
|---|---|---|---|
| 1 | `python tests/check_ingest.py` | FAIL（1 issue） | `W-M06-001` 的來源沒有符合 `PDF pp.` 的頁碼引用格式 |
| 2 | 引用修正 | 已修改 | 在 `W-M06-001` 補充 P01/P02 的 PDF 頁碼 |
| 3 | `python tests/check_ingest.py` | PASS（0 issues） | 10 個 Wiki ID、來源登錄、索引、SHA256 完整性檢查皆通過 |
| 4 | `python tests/check_scaffold.py` | PASS（0 issues） | 原 Phase 1 結構保持完整 |

**檢查前移的初步觀察：** 已看到引用格式在索引／Wiki 條目整理階段就應檢查，避免到逐頁簡報才發現缺頁碼。這只是 Batch 1 的一次失敗案例；尚不能據此統計完整 Graph「最常出錯節點」。

這些檢查僅涵蓋結構、參照及原始檔案完整性，不代表逐句科學核對，也不代表 Graph 已能自動執行。

## Phase 2｜Batch 2–3（2026-11-19）

使用者另外提供 P03 CloudSEN12（17 頁）、P04 Deep Learning Survey（32 頁）、P05 CloudS2Mask（25 頁）。已複製原始 PDF 至 `raw/`，新增 9 個 Wiki 條目（P03/P04 跨來源條目包括 W-M03-002）；連同 Batch 1 共 **5 篇來源與 19 個 Wiki 條目**。本次沒有訓練或執行雲影偵測模型。

### 實際與來源對讀的範例

| Wiki 條目 | 來源頁面 | 已核對要點及警示 |
|---|---|---|
| W-M02-003 | P03 PDF p.5，Table 3 | Clear / Thick / Thin / Cloud Shadow 四類標籤，以及 cloud/non-cloud、valid/invalid 不同合併方式 |
| W-M05-002 | P03 PDF pp.1–2 | 摘要 49,400 patches；正文 p.2 記載 49,250 的分項總數，屬來源內部差異，未擅自修正 |
| W-M06-003 | P03 PDF pp.8–10，Figures 8–9 | 空間區塊切分、PA/UA/BOA 和跨演算法的類別對應 |
| W-M05-003 | P04 PDF pp.2–3、10–12 | 深度學習語意分割的網路類別與侷限 |
| W-M06-004 | P04 PDF p.10，§3.2 | Precision/Recall/F1/IoU/OA 的混淆矩陣公式 |
| W-M05-004 | P05 PDF pp.3–5 | U-Net + RegNetY_006、三類來源資料到四類目標資料的遷移學習 |
| W-M05-005 | P05 PDF pp.6–7，Figures 3–6 | overlap、offset grid、融合預測時對邊緣及角落降權 |
| W-M06-005 | P05 PDF pp.8–10 | CloudSEN12 / PixBox BOA；在指定工作站的 2.2 秒／場景，不可視為通用速度 |

### 交叉文獻比較關卡

- **P02 vs P05：** P02 在特定 Sentinel-2 驗證的 Overall Accuracy 為 94.30%（P02 p.16）；P05 的 CloudSEN12 BOA 為 0.932/0.918/0.924（P05 p.8）。兩者的測試資料、定義與指標不一致，禁止直接比大小做排名。
- **P03 vs P05：** P03 的四類標籤提供 P05 的分類目標；P05 的模型成績不等於本作業自行重現的成績。
- **P04 vs P05：** P04 為綜述，P05 為特定研究，需分別呈現「方法概觀」與「具體實驗」。

### 真實執行的驗證

- `python tests/check_ingest.py` → **PASS (0 issues)**，5 篇 PDF SHA256 檢查通過，19 個 Wiki 檔案且 ID 唯一，索引及頁碼標記存在。
- `python tests/check_scaffold.py` → **PASS (0 issues)**，Phase 1 結構及尚未生成 HTML 的限制維持不變。
- 本次並無驗證失敗或自動重試，不能編造 Batch 2/3 的失敗案例。Batch 1 曾有引用格式缺失，詳見前段。

### 已知限制與後續工作

1. 「頁碼／來源 ID」靜態檢查並不保證每一句話必然被原文支持；正式生成教學簡報前仍需獨立忠實度審查。
2. 需實作 Wiki → 證據卡 → 教學大綱 → 逐頁稿 → HTML 的真正 Graph 並保留節點執行與回退紀錄。
3. 原始 PDF 被 Git 忽略；請勿將任何完整 PDF 直接推送到公開 GitHub（即便部分來源為 CC BY，也要遵循標示及重用條件）。
4. 尚未產生 HTML，且沒有做瀏覽器互動測試。

---

# Phase 3 — 可執行 Loop / Graph 測試報告（2026-11-19）

## 實際新增內容

- `.agents/workflows/graph.py`：可在 Python 標準函式庫下執行的節點及修正循環。
- `.agents/workflows/slide_plan.json`：12 頁提案，各自綁定 Wiki IDs 和教學目標。
- `cards/CARD-S*.json`：26 張已通過原文／引用格式檢查的證據卡。
- `outline.md`：由通過證據卡建立的大綱，狀態為待人工核准。
- `tests/check_graph.py`：重讀當前 Wiki 檢查卡片、引用與大綱。
- `runs/`：三組真實執行 trace 及 coverage JSON。

## 實際執行紀錄

| 測試 | 來源／Wiki | 覆蓋頁數 | 證據卡 | 修正或重查 | 結果 |
|---|---|---:|---:|---|---|
| `phase3_normal` | 5 篇／19 條 | 12/12 | 26 | 0 次 | PASS：格式、來源及原文一致性 |
| `phase3_fidelity_repair`（刻意錯誤注入） | 5 篇／19 條 | 12/12 | 26 | 1 次局部修正 | PASS：偵測來源頁碼不一致後返回 Cards |
| `phase3_coverage_stop`（刻意錯誤注入） | 5 篇／19 條 | 11/12 | 25（未發布） | 3 次重查 | 預期 FAIL：缺少 Wiki ID 而停止 |

兩種失敗測試是為了驗證 Graph 控制流程的**模擬故障**，不代表原始論文、Wiki 或正常輸出有該項問題。覆蓋失敗時，舊有成功的 cards 和 outline 未被覆蓋。

正常流程成功後還執行：`tests/check_graph.py`（26 cards、12 slides、PASS 0 issues）、`tests/check_ingest.py`（5 source PDF SHA256、19 IDs、PASS 0 issues）、`tests/check_scaffold.py`（PASS 0 issues）。

## 資訊流與責任分離

Wiki Index → Query → Coverage Gate → Evidence Cards → Literal Fidelity Gate → Outline → Human Approval Gate。

- Query 不得讀未匯入的外部資料；Coverage 只測 Wiki ID 是否可取得與對應，不宣稱教育涵蓋已經人工確認。
- Fidelity Gate 只報告錯誤，不直接偷改內容；Graph 控制器將錯誤路由回 Evidence Cards，最多三輪。
- 若 Coverage 無對應來源，最多重查三次，停止並等待新 Ingest，不虛構證據。
- HTML Render 和逐頁語意審查尚未開始，不能宣稱 Graph 的所有未來節點已測試。

## 反思（根據此次真實測試）

在本階段的正常執行中，沒有出現未預期的證據卡驗證失敗。因此目前**不能聲稱某個節點在實際資料中最常出錯**。但控制性失敗測試證明證據卡來源頁碼欄位是必須檢查的風險點，並已在卡片產生後、進入大綱前設置 Fidelity Gate，防止錯誤一路傳到 HTML。三次重試後停止的覆蓋測試也顯示缺資料時不能靠反覆重生成解決。

## 尚待完成

- 由獨立審查者針對重要數字／表格與原始 PDF 做語意忠實度檢查。
- 人工確認 `outline.md` 的 12 頁教學順序及所有建議素材權利。
- Phase 4：逐頁稿、HTML、瀏覽器互動測試與版面檢查。
- Git 提交與對外 GitHub Pages 發布。

---

# Phase 4 — 逐頁稿、HTML 與 Browser Graph（2026-11-19）

## 產出

- `drafts/slide_01.md` ～ `slide_12.md`：12 份根據 Phase 3 的 26 張證據卡改寫的教學稿，逐頁記錄 Wiki ID、證據卡與來源頁碼。
- `assets/slide_content.json`：機器可讀的逐頁知識／來源對應資料。
- `deck.html`：單一可執行的 12 頁互動式教學簡報，不依賴第三方 CDN、網路、API；可按上一頁／下一頁、方向鍵，查看來源 DOI、Wiki 原文證據，第 10 頁可切換 4 種人工繪製的示意遮罩。
- `.agents/workflows/build_deck.py`：由 12 頁教學稿的既定來源內容重建草稿及 HTML 的可重複生成器。具體的科學說明寫在此生成器中的 `LESSONS`，新增主張須先回寫並驗證 Wiki。
- `.agents/workflows/phase4_graph.py`：後半段可執行 Graph（檢查 Phase 3 cards 數量 → 生成 draft/HTML → 靜態檢查 → 失敗重建最多 3 輪 → 審查待辦）。
- `tests/check_deck.py`：檢查 12 頁資料、26 張證據卡與逐頁稿是否一致，並核對 DOM 基本控制與來源映射。
- `tests/browser_check.py`：Chromium + Playwright 實測換頁、引用視窗、遮罩切換與手機／桌機水平溢出。

## 真實執行紀錄

| 測試情境 | 預期與實際結果 | 回退方式 | trace |
|---|---|---|---|
| 正常 Phase 4 graph | PASS：12 份逐頁稿、HTML 及引用映射靜態檢查 | 不需重試 | `runs/phase4_normal_trace.json` |
| 人為注入逐頁稿錯誤（CloudSEN12 → CloudSENXX） | 第一次 G03 FAIL，偵測 slide 04 主說明不一致，第 1 次重建後 PASS | 回 N05 重建產物 | `runs/phase4_injected_draft_trace.json` |
| 人為注入來源卡缺失 | G01 FAIL，重查 3 次仍缺，安全停止且未覆寫既有 deck | 不編造來源 | `runs/phase4_missing_source_trace.json` |
| Chromium 桌面 1440×900 / 手機 390×844 | 46/46 PASS，包括 12 頁逐頁導航、引用視窗、示意遮罩切換、基本水平溢出 | 無 | `runs/phase4_browser_report.json` |
| 原 Phase 3 的證據卡檢查 | PASS：26 cards / 12 slides | 無 | `tests/check_graph.py` |

**測試界線：** 瀏覽器測試採用 Chromium 的 `page.set_content` 載入 HTML 文字，因測試執行環境封鎖 `file://` 和 `localhost` 的實際導航；因此測試可證實 DOM 互動與渲染，但不代表 GitHub Pages 的外部部署已實測。DoI 為外部網路連結，未驗證所有外站網路可用性。26 張卡片的 SHA/來源格式保留 Phase 3 驗證；本次改寫的科學語義未經獨立 AI 或真人完成最終逐句驗收。

**忠實度界線：** HTML 本身是教學文字轉述，而非 Wiki 字面上的逐字引文；每頁保留條目/原始論文來源，獨立語意審查仍待完成。第 10 頁是人工 SVG 圖，明確標為「示意」，非真實衛星影像或模型產出的結果。

## Graph 反思更新

本階段透過**人為故障注入**驗證：「逐頁稿與生成資料不一致」能在 G03 偵測並返回 N05；證據缺失不能靠重新生成而被修復。因此將逐頁稿一致性檢查提前到渲染發佈前，降低錯誤傳遞到公開版的機會。尚不能根據故障注入測試宣稱真實資料哪個節點最常出錯。正式作業的反思應保留正常運行與控制性故障測試之區別。

## 待完成（Phase 5）

1. 人工確認 12 頁教學大綱與逐頁稿；進行獨立科學忠實度審查。
2. 上傳 GitHub、GitHub Pages，從公開網站實際檢查連結及手機排版。
3. 補充正式發佈版 URL 與最終完整驗收紀錄。


# Phase 5 — 來源抽查與發布準備（2026-11-19）

已對 12 頁講稿的重點科學陳述和特定研究數據抽查原始 PDF，細節見 `PHASE5_REVIEW.md`。建立 `index.html`（與 deck.html 位元組相同）、GitHub Pages 操作手冊及可貼上課程平台的繳交草稿。

本次執行的檢查報告見 `runs/phase5_release_validation.json`。此前 Phase 4 的 46/46 Browser 檢查保留，**本階段未宣稱重新完成真實公開網址測試**。

**完成與未完成的明確界線：** Wiki、證據卡、HTML 與本機靜態檢查已有成果；但 GitHub 尚未實際發布，使用者尚須檢查公開 Pages URL、進行人工總驗收及填寫繳交資料。
