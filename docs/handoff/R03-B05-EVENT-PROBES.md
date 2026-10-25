# R03 B05: older-host reward negative and native probe limits

2026-10-25, scheduled18:11 resumption. R03 remains IN_PROGRESS. Runtime unchanged from B03; no new hook, admission/progress rule, backend or release artifact. CL03 handback is now integrated (PR3); its C1-C4 constraints still apply.

## Bounded native result

G2-20 negative input: copied host A14184, EiEi1 in Cathedral Ward from the protected C01 before-b checkpoint; copied guest B19056, U-I-AHH3 in Clinic/Central Yharnam. Distinct existing accounts. Actual native preparty snapshots show flag12401800 ON for H and OFF for G. These are played save copies, not synthetic defeated flags. Both clients load frozen B03 DLL96e398b2 and install160/160 hooks. Existing Dream and guest-items switches are ON for this diagnostic; shared progress staysOFF. New managed application remainsOFF.

Host first claim18:31:58 precedes a later ring18:33:01. Guest JoinSession_White18:33:05, state4 at18:33:06, state6 at18:33:09, host-world load copy18:33:16, host SummonSuccess_White18:33:28, guest adjacent placement/load-cover fade18:33:32. Do not assert the initial claim delay was fixed. Guest loading0/type1/own0/map0x18000000, point(13.286061,-9.501885,106.785088); host's baseline point(14.028195,-9.508328,105.312050). Actual guest visited-world snapshot has12401800 ON.

No fight or boss interaction occurred. Both timelines contain zero queued-for-user reward lines and zero BlockClear2_1 lines through18:34:41+, over60s after placement. Guest trace contains zero ForceSummonSuccess/BlockClear records. End-position/world snapshots remain identical to placed snapshots. This is the bounded negative side of G2-20 and G2-21; no positive kill has established producer sensitivity, no all19/general-load guarantee, no earned-event/admission/C3/C4 PASS.

Normal guest Parting Blank return restores map0x18010000, lamp2412950, point(-190.180832,-50.622490,166.482391), heading0.065716. All1250 groups equal fresh prejoin exactly; before/returned JSON SHA2567a587d3a791c04da39cff1af0890fa56db9ac8f91250ba7e234d804e9cfa18a7. Independent save/reload is not yet rerun in B05. A later pre-positive own-world snapshot differs only at12415010 (the bell/search bit also observed in B04); preserve that delta separately rather than claiming indefinite full equality. After frozen negative observation, cleanup navigation mistakenly used Duel Bell once (PvPON), without combat; it was then observed/corrected to Parting Blank. Existing code resets PvP at co-op end. Do not treat that post-observation toggle as a death/earning test.

## Graphics blocker, not a G2 verdict

Setup attempt0 Continue loaded EiEi1 in Dream rather than intended Kaori0. After normal Quit/title, Load Game exits3740 with GPU Unimplemented PM4 type0/base87/size1, runner23. Fresh9288 title/list was normally closed, CloseMainWindow/WaitForExit true. A preserved played Cathedral EiEi1 save is then used for the actual negative above. After that negative and normal host Quit/title, Load Game in14184 again exits23 with PM4 type0/base17/size1. Both failed launcher helpers were waited, exit0. Logs/after-saves protected separately.

Thus G2-22(g) same-process character-change proof is BLOCKED by graphics in this configuration; no host change/rejoin completed. No renderer/system fix is inferred or attempted. Independent positive setup uses a fresh copied Kaori0 host8968 (HWND11208548), existing1280x720 render/output options to reduce two-client load, same DLL. Guest19056 remains the restored copied U-I-AHH world. This setup is IN_PROGRESS, not a positive result or proof the lower setting fixes graphics.

## Finite local script evidence, separate from gameplay

Existing gamedata Emevd parser decoded exactly the19 existing reward events from local read-only CUSA03173 assets; file hashes/raw instructions stay private. Direct2003[02] writes into the existing57-flag set are:

| Reward event | Direct listed flag writes |
|---|---|
| 12101800 | none |
| 12201800 | 2200, 9452, 5911 |
| 12301700 | 2301, 9454 |
| 12301800 | 2300, 9453 |
| 12401800 | 2400, 2401, 9455, 2402 |
| 12411700 | 2411, 9456 |
| 12411800 | 2412, 9457, 5910 |
| 12421700 | 2420, 9458 |
| 12421800 | 2421, 9459 |
| 12601800 | 2601, 9462 |
| 12601850 | 2600, 9461 |
| 12701800 | 2700, 2701, 9463 |
| 12801800 | 2800, 9464 |
| 13201800 | 3200, 9465 |
| 13301800 | 3300, 9466 |
| 13401800 | 3400, 3401, 3402, 3403, 9471 |
| 13401850 | 3400, 3400, 3401, 3402, 3403 |
| 13501850 | 3510, 3511, 3512, 3517 |
| 13601800 | 3600 |

There are 43 unique listed flags in these direct writes. Repeated3400 is retained in the summary because branch conditions matter. This is a direct-write relation, not a complete causal catalogue, proof every listed write is eligible, or permission to OR a group. Other native/indirect outputs, branch values, time-of-night encoding, event completion, stale world-state triggers and first-playable/party epoch still require validation. In particular, a source relationship does not make old host state jointly earned. No runtime filter is generated from this scan.

## Attribution and actual commands

- Native source bloodborne_re.cpp SHA2562ac893635c9944de6ac04709fd98575f740dd5bea5da97926155838a85fb505b.
- Complete tracked four-destination patch SHA2568a3ce6f9aa01da16b8bf503538d6b215b349f2d99ef2ae876f1c61fa02c086ec.
- Local B03 DLL SHA25696e398b23e0d48af4f220a7ca7534d529369e1f194bc65e60da55d884ca2303d.
- Source-built probe SHA2566696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14.
- C:/msys64/clang64/bin/python.exe .superpowers/r03-close/read-position.py PID OUTPUT and read-world.py PID OUTPUT: actual native position/1250group snapshots.
- Same Python: .superpowers/r03-b05/assert-input.py PASS; inspect-negative.py PASS for visited boss bit and zero clear trace; assert-negative.py PASS for frozen hook/placement/zero queue/clear logs. The observed wall time is recorded separately in negative-observed-at.txt; do not rerun that script against later positive logs and relabel them.
- Same Python: .superpowers/r03-a03/compare-world.py guest-before-world.json guest-negative-returned-world.json DELTA: {}. map-finite-event-writes.py:19events parsed, direct-write summary retained; this is static evidence, not fixture/native gameplay.
- Existing .superpowers/r03-a04/pad.ps1 with per-client private BB_PAD_FILE, fresh observed menus. No input runtime change. Private launch scripts contain supplied credentials; never print/stage them.

Private evidence: .superpowers/r03-b05 (before-a/b saves, fresh original-before3171 manifest, artifact hashes, host-attempt0/1, negative snapshots/logs/after-saves, finite event scan, positive setup). No raw logs/assets/saves/credentials are tracked. No new runtime fixture/build/full suite; earlier B03 results are not relabeled.

Next: actual positive joint kill (Kaori0 still has Amelia alive), then surviving/dead/loading producer discrimination and party boundary/stale-input cases. Keep no-older-history admission and delivery/own-progress persistence gates open. R03 cannot close from this negative alone. Before ending this session, normally close any remaining copied tests, verify originals, checkpoint current state and publish origin/seamless without force.

## Session completion addendum

Fresh B18888 independent PlayOnline/Continue reload after B19056 normal close preserves all1250 initial groups exactly (private positive/guest-reloaded-delta.json is{}), own map/lamp/origin restored. No positive kill occurred. CL04 readiness inspected on the actual negative logs:160/160 hooks, Dream/boss-clear active, required switches enabled; BBSC.LuaEvent maximum hit2 on each client, below throttle64, no ForceSummonSuccess record. This supports the bounded negative absence only; without positive sensitivity G2-20 remains inconclusive overall. Fresh Kaori0 host8968 was prepared but not fought; B18888 was normally closed without a new party before B06 guest16404. All B05/B06 tests are now normally closed except the two recorded graphics exits. B06 source candidate and its distinct reload limitation are in [the next checkpoint](R03-B06-WORLD-ORDERING.md). Do not reuse the old B05 source-hash checker against B06 and relabel it.
