# Validation tests

- `python tests/check_scaffold.py`：Phase 1 專案結構。
- `python tests/check_ingest.py`：Phase 2 兩篇 PDF 檔案完整性、來源登錄、Wiki ID 唯一性、索引、來源與頁碼格式。

注意：程式靜態檢查**不能證明所有論文釋義正確**；科學主張須核對原始 PDF。實際驗證結果記錄於 `report.md`。
