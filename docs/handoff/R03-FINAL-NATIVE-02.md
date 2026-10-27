# R03 final-composition boss attempt 02

2026-10-27 (Asia/Bangkok), Codex. **INCONCLUSIVE staging; no boss kill or reward acceptance.** User asked to begin acceptance and explicitly proposed command-assisted boss death.

## Scope and composition

Separate copied profiles under `.superpowers/r03-final-native-02`, made from the existing authorized retry profiles; pre-savedata hashes retained. Same source/DLL/probe as [checkpoint01](R03-FINAL-NATIVE-01.md), no product changes. Shared progress ON only for these copies; spectate OFF; experimental admission/home recovery/reward-once OFF. No default or live-service changes. Existing private credentials and routes reused without publishing them.

PID14004 host Kaori, PID20528 guest U-I-AHH. Both have independent 1250-group prejoin snapshots, native Amelia12401800 OFF verified with the game's MSB-first flag bit order. Password join succeeded. Guest phase4/type1/own_world0 in Cathedral0x18000000; 23:53:19 collector opened after placement with baseline12 flags/160 groups.

## Debug aids and observed limits

A private Python/ctypes helper reuses the documented transform pointer chain and arena-entrance coordinates (51.90,35.71,312.30). It writes only copied test character positions; every write has readback. The HP operation checks host identity/type, real boss gauge502000, target type7 and positive bounded HP before permitting HP=0. It never writes boss completion flags or inventory. These are test aids, not product implementation or acceptance fixtures.

- Initial position aid put the host in Grand Cathedral; pad movement triggered the Amelia cutscene. The host and guest logged the actual Vicar Amelia boss line at23:55:45/46, and the host screen showed the full live boss bar. The host died before the manual HP command; it respawned with party state retained.
- Guest died around23:53:53 during staging, before any HP-zero operation. At23:54:10 it respawned retaining guest state. Later readback: type1/own_world0 but map0x18010000 (Clinic) at its own-origin region, rather than the host's0x18000000. The subsequent position-only aid was applied in that wrong map and caused falling coordinates, including y=-1072/-1501. Do not count this invalid staging as boss participation, safe movement, or a confirmed product regression. No clean no-aid discriminator was run.
- A bounded gauge watcher was added to avoid manual delay. First aborted on active loading; retry waited through loading and then stopped on a pointer precondition. **No `AMELIA_HP_ZERO_CONFIRMED` readback occurred, and no HP write completed.** The helper's handle decoding is not validated by this attempt. Do not claim it as a successfully tested kill command.
- Further host position attempts overlapped renewed loading/respawn; no completed joint kill, item award, own-world merge/reload or reward deduplication result is claimed.

## Cleanup and next action

Stopped only these two test game processes. Their per-process DLL logs and RE/HTTP captures remain under native01/dll/logs and native02/profile-*/user/captures respectively; copied after-saves and stdout/stderr retained under native02. Fresh original manifest exactly equals checkpoint01's before manifest:3171 files/path set unchanged. No original save or protected reference source overwritten. No release package/server deployment.

Next: preserve the successful checkpoint01. For the positive, use clean copied before-saves, place both in the same actual host map and verify native state after any death/load. First validate the read-only live boss-handle lookup against known native character-table evidence; only then use the authorized HP-zero operation. Keep the guest in its already-correct host map during staging or replay a clean rejoin after death. Recheck stable map/loading before any position aid. The current attempt does not establish the cause of the guest's respawn-map mismatch; separate that from artificial falling in the wrong map. Shared-progress/native reward and all B15/B17 gates remain open.

Commands: same launch/read-world/read-position recipes as checkpoint01; private native-aid.py PID goto|gauge|kill and wait-kill.py PID; existing BB_PAD_FILE. Initial positive process launch succeeds outside sandbox. No additional fixture run was necessary: product source is unchanged and the same-source12-test pass remains current; private aids used syntax/precondition/readback checks only.
