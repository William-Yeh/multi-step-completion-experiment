# Prompt Preview

直接用 CLI 查看最新 prompt：

```bash
uv run run.py prompt 1 case_01
uv run run.py prompt 2 case_01
uv run run.py prompt 3 case_01
```

## Prompt 設計重點

### Experiment 1

- 明確要求整理 footnotes
- 明確禁止呼叫 external checker
- 讓完成判定停留在 agent 自我檢查

### Experiment 2

- 要求呼叫 checker
- 但只能使用 `--mode accepted`
- 讓 agent 知道 tool 被呼叫，卻不知道結果
- 加上 presence gate：`model_status="completed"` 需要 `tool_invocation` 同時帶有 `status` 與 `run_id`；少了任一個就必須設為 `failed`，避免 prompt 退化成 Experiment 1 的純自評

### Experiment 3

- 先對原始 `input.md` 呼叫 checker `--mode full`，作為 preflight
- 要求讀回完整 pass/fail 與錯誤細節
- 若 preflight 失敗，才進入 readback-driven repair
- repair 後仍失敗，才算 retry；preflight 本身不算 retry
- 只有 `final_tool_result.pass=true` 才能 completed
