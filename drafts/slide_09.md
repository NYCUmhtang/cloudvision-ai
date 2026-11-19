# Slide 09｜U-Net 與 CloudS2Mask

**教學目標：** 認識常見架構和訓練概念

## 主標題：U-Net 與 CloudS2Mask

U-Net 採編碼器–解碼器架構；CloudS2Mask 結合 U-Net 與 RegNetY_006。

## 教學重點
- 先使用三類資料學習，再遷移學習到四類標籤。
- 逐步調整影像尺寸（Progressive Resizing）。
- 可用集成與測試時增強改善表現，但會增加成本。

## 概念限制
這是論文所描述的模型，不代表本作業已重新訓練或執行。

## 證據卡與 Wiki
- CARD-S09-01 → W-M05-003；P04 PDF pp.2–3、10–12，§1、§4.1–4.2
- CARD-S09-02 → W-M05-004；P05 PDF pp.1–5，§2.1–2.5、Table 2、Figure 2

> 內容狀態：以 Wiki 為依據的教學改寫；數據來源已對照 Wiki，人工最終核准仍待完成。
