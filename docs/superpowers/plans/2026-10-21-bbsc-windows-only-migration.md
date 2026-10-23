# Windows development direction

Updated: 2026-10-23. Retained filename for plan continuity; development now starts fresh in the new fork on `seamless`.

The [active alignment plan](2026-10-23-bbport172-bbsc002-alignment.md) is authoritative for pins, scope and tasks. Deliver only supported-map join, jointly earned progress and self-hosted support on Windows using complete BBport 1.7.2 + BBSC 0.0.2. Preserve other upstream systems and licenses/credits.

Reproduce baseline behavior first; implement only demonstrated gaps. Historical W checklists and old custom mechanisms are not a migration backlog. Do not import old runtime patches, worktrees or test acceptance with these documents.

Use copied profiles for diagnostics, preserve original saves and validation, keep custom admission/application OFF until relevant native gates pass, and stop before release packaging or live-server redeployment. Publish checkpoints to `origin/seamless`; preserve the existing `windows` branch/history without force pushes.
