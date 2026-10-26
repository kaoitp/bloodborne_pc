# Graphify local code index

Graphify 0.9.95 is installed in the current Windows user profile, with the Codex skill. Generated outputs are local and ignored; a fresh clone must build its own graph.

From the repository root:

```powershell
graphify extract . --code-only --no-dedup --max-workers 4
graphify cluster-only .
graphify query "summon_service" --budget 1500
graphify export html
```

Repeat the extract command after source changes; it supports incremental extraction. Run cluster-only again to refresh the report and HTML. In Codex, ask a code question normally or explicitly use `/graphify query "your question"`.

`.graphifyignore` excludes external dependency trees and private/generated directories; `.gitignore` keeps all of `graphify-out/` out of commits, including graphs, caches and absolute interpreter paths. No background watcher or Git hook is installed.

This index is **code-only**: documentation, images and patch files are not semantically indexed. In particular, the BBSC implementation represented by the tracked patch must still be read directly; the ignored reference checkout is not scanned. A graph is navigation assistance, not proof that all callers or runtime behavior are represented. AST extraction reported 15 partially parsed files and 43 files without symbols; np_manager.cpp needed a cp1252 decoding fallback. Community labels are automatic file/symbol labels without an LLM pass. The large HTML graph uses an aggregated community view.
