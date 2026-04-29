# Experiment Design

## 核心問題

當 workflow 成敗依賴外部事實時，完成判定是否可以只靠 prompt？

本實驗用 Markdown footnote cleanup 做展示。任務本身不重要，重點是三種控制配置：

1. prompt only
2. tool no readback
3. tool with readback

## 共用設定

三個實驗共用同一份 task prompt 與 result.json schema；唯一的操縱變因是 completion gate 的位置。

Prompt 的 common 段也會列出 checker 認可的 defect 類別名稱（`missing_definitions`、`unused_definitions`、`duplicate_definitions`、`reference_order_errors`、`definition_order_errors`），讓三個實驗在「知道哪些東西可能會錯」這層詞彙上對齊，避免實驗 3 因為 repair 步驟點名這些類別而比實驗 1 / 2 多得提示。

## Experiment 1: prompt only

agent 不准呼叫 checker，只能自我檢查。

目的：展示 prompt 可以描述流程，但完成判定仍可能只是模型自述。

## Experiment 2: tool no readback

agent 必須呼叫 checker，但只拿到 accepted/run_id。`model_status="completed"` 需要 `tool_invocation` 同時帶有 `status` 與 `run_id`（presence gate）；缺一就視為 failed。

目的：展示 tool invocation 不等於 validation —— 這個 gate 只能擋下「完全沒呼叫工具」的情況，並無法判斷文件是否正確。

## Experiment 3: tool with readback

agent 必須先對原始 input 呼叫 checker full mode，讀回 pass/fail 和錯誤細節。這一步稱為 preflight。若 preflight 失敗，agent 必須根據錯誤進入 repair；只有 repair 後仍失敗、需要再次修正時，才算 retry。

目的：展示 tool result + gate 才是真的控制責任外移；同時區分 preflight failure、repair triggered 與 retry used。

## 主要指標

- Actual Pass
- False Completion
- Tool Called
- Readback Used
- Preflight Failures
- Repair Triggered
- Retry Used
- Agent Failures

## 解讀

最重要的對比不是「哪一組產生的 Markdown 最漂亮」，而是：

- agent 是否宣告完成但 checker 判失敗
- tool 是否只是被呼叫，還是真的回到判斷流程
- pass=false 是否能擋下完成宣告
