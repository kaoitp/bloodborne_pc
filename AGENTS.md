# BBSC development entry point

Claude R03 takeover (2026-10-25): read [the active implementation handoff](docs/handoff/R03-CLAUDE-TAKEOVER.md). Claude now owns R03 across source/build/config/tests/native gameplay/docs with freedom of method consistent with the unchanged project goals and general baseline-reuse approach. Earlier audit allowlists and Codex-only process/usage rules are superseded for this assignment. The remaining instructions below describe Codex's development workflow.

For development, setup, review or resumption, read [the Windows handoff](docs/handoff/WINDOWS-RESUME.md), then its linked plan and progress tracker.

Work on `seamless` in this repository. The baseline is Supermedo BBport `windows-v1.7.2` plus CLSAMG22 BBSC `v0.0.2`. Reproduce the complete pinned releases first; change only demonstrated gaps in supported-map seamless join, jointly earned progress sync and self-hosted service support. Preserve other upstream systems.

Before implementation, identify the task, dependencies and acceptance checks; mark it `IN_PROGRESS`. Update the tracker and plan checkboxes at checkpoints and before commits. Record tested source/artifact hashes, actual commands/results, limitations and next action. Keep fixture, native and gameplay evidence separate. Prior-repository tests do not qualify this repository.

Codex works inline without subagents. External Claude Code now follows [the R03 takeover](docs/handoff/R03-CLAUDE-TAKEOVER.md); its previous four-document audit package is historical.

Use copied test profiles; keep secrets, saves, assets and logs out of Git. Custom managed admission/progress application stays OFF until the relevant native gates pass. No release EXE/ZIP packaging or live-server redeployment. Preserve history and unrelated work; publish checkpoints to `origin/seamless` without force pushes. Check usage periodically; below 10% remaining in either available window, stop new work, record and commit the checkpoint.
