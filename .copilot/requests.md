### Copilot / Prompt Requests

Use this file to save prompts and Copilot/assistant requests you want to keep.

How to save a prompt locally:

- Manual: open this file and paste your prompt under a timestamped heading.
- Scripted: use `scripts/copilot-save.sh` (or the shell function) to append prompts.

Example entry:

```
### 2026-02-14T12:34:56Z

Refactor `Buttons.click()` to avoid race when touchscreen disconnects.

Context: lib/pokelib/touchscreen.py uses reconnect logic that retries, but Buttons caches coords.

Goal: remove cache, query phone_db for fallback, add unit test for reconnect path.
```

Tip: commit this file regularly so your prompts are versioned alongside the code.
