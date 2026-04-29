# Official CLI Notes

本 bundle 的設計假設：你已經在本機安裝並登入 Claude Code CLI 或 Codex CLI。

## Claude Code CLI

Claude Code 官方 CLI reference 列出：

```bash
claude -p "query"
```

這是非互動式查詢方式，會 query 後退出。官方 CLI reference 也列出 `--output-format text/json/stream-json`、`--permission-mode`、`--print/-p` 等選項。

Runner 把 prompt 緊接在 `-p` 後面：

```bash
claude -p "<task prompt>" --output-format text --permission-mode bypassPermissions
```

參考：

- https://code.claude.com/docs/en/cli-reference

## Codex CLI

Codex 官方文件列出：

```bash
codex exec "task prompt"
```

這是 non-interactive mode，適合 scripting / CI。`exec` 預設 approval=never；用 `--sandbox <mode>` 控制工作區寫入權限（runner 預設 `workspace-write`）。

參考：

- https://developers.openai.com/codex/noninteractive
- https://developers.openai.com/codex/cli/reference
