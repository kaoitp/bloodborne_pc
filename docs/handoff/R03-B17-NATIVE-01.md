# B17 native recovery: early interruption, point miss and lamp fallback

2026-10-28 (Asia/Bangkok), Codex. CHECKPOINT / acceptance open. User requests B17 after B15 normal replay, with copied-profile command-assisted control already authorized. No product source/default/server changes.

## Composition and boundaries

Checkout28c85ba; same integrated runtime as native04/B15 replay. DLL SHA256 `87319fd9c2bbf748d5ab3e9ad06fbab7376fb075edba86be5c451f9f8ea12cf6`, probe `6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14`, reconstructed sourceCRLF `ee21b5e71dee64b3c39dcda8107fd34c4e703676f5dade701f9f07220910aad2`, working patchCRLF `66be824139a15d74bf9862fb955b8fd2fe7816b1bcd4de4b3a3c4828f7de8ad1`. Earlier fixture/build evidence is unchanged, not new gameplay proof.

Private `.superpowers/r03-b17-native` copies both native01 profiles. HOME_RECOVERY=1 on guest only; experimental admission/recovery=0, reward-once=0, shared progress0, items/Dream1, spectate0, no-death1. Existing distinct accounts/self-hosted services,1280x720/30FPS. Original3171 manifest captured before launch. No source/build/default/config change outside copied tests.

## N1: measured early interruption, point return fails

- Host9160 failed before any party with GPU PM4 type0/base16 assertion, exit23. Same-composition host retry7888 loaded Cathedral successfully. Guest13996 U-I-AHH level10 loaded Clinic; independent baseline map0x18010000/lamp2412950/position`(-190.18083,-50.62249,166.48239)`, yaw0.065716, own_world1/type0. Two settled1250-group baselines identical.
- Native Hunt/Kin Bell use; no warp or boss aid needed. Guest summon placement log20:58:42.831, own_world0/type1/host map after ordinary summon load. Guarded private watcher validates PID/executable and terminates guest20:58:42.835162, **0.004162s** after the log. This is measured wall-time to the termination call, not a CPU-cycle timing claim. Exit99; crash savedata and active own-sd1-3 journal protected. Last guest save20:58:28, during join load before placement; do not claim a post-placement autosave was forced.
- Journal parses981 records of125bytes, correct BBOW header; home record version1/map0x18010000/lamp2412950 and exact baseline position/rotation. No journal edit in this run.
- Fresh owner19752:21:00:50.674 finds journal/arms owner recovery;21:00:50.707 original point request accepted, try1.21:00:59.920 **arrived elsewhere**;21:01:00.382 recorded lamp request accepted, try1.21:01:09.999 settles/restores journal. Thus **N1 exact original-point acceptance FAILS**, and the fallback executes naturally without corrupting a journal.
- Settled Clinic lamp position`(-199.740005,-50.758743,179.419998)`, yaw0, own_world1/type0, **16.086579m from original**. Independent flags before saving equal all1250 prejoin groups. This is successful own-world restoration and bounded lamp fallback, not exact-point success.

## N3 path exercised naturally; reload integrity remains open

The valid point missed in N1, so the real failure->lamp->settled path required by N3 was exercised without synthetic point modification. Prepared n3/n4 replay copies were not launched at this entry; they are not evidence.

Normal Exit Game -> YES saved guest21:05:40. Private after-lamp savedata protected, process stopped. Fresh17460 Online/Continue visibly at Clinic lamp; exact lamp map/position/rotation retained. Two stable snapshots1250 groups match each other but differ from prejoin in **six OFF bits**:12705098,12705301,12705520,12705521,12705531,12705532. Earlier immediate restoration was exact. No producer/control has classified this settled reload delta, so **full N3 own-flags save/reload acceptance stays open**. Do not label it corruption or harmless. Original3171 paths/hashes remain exact.

Checker commands (CLANG64 Python) against guest13996 then19752 logs, with copied `profile-b/user`:

- `tools/check_r03_native.py b17-n1 ...`: exit1/FAIL, two requests before settlement instead of one. Manual position assertion independently fails16.086579m>5m.
- `tools/check_r03_native.py b17-n3 ...`: exit3/MANUAL, all automatic failure/lamp/settlement/journal checks pass; the actual manual reload own-flags condition above is unresolved.

## Private reproduction and pending work

Use `C:/msys64/clang64/bin/python.exe`; private prepare/launch/pad/watch-crash helpers, existing read-position.py/read-world.py. `prepare.py` verifies artifact/source hashes and copied boundaries. `watch-crash.py13996` validates the exact process, watches actual placement, checks<10s, terminates only it and copies the crash inputs. Raw saves/journals/logs/accounts remain ignored. Native01 DLL logs:205159-13996,205914-19752,210616-17460; host failed205146-9160 and retry205430-7888. Host retry stopped after guest disconnect with no joint event; do not report a normal host save/exit from this run.

A scripted normal-exit sequence missed a directional pulse and entered copied Controls, toggling camera X; corrective opposite input/back was issued. No original profile/config touched. Re-observed menus were used for the actual successful normal save. Short native pad pulses can miss or repeat, so a scripted sequence alone is not menu success evidence.

## N2 bounded disk-journal isolation; full cancellation still open

Postlamp17460 later failed at the character menu with GPU PM4 type0/base0 assertion, exit23. This prevents the planned independent EiEi baseline; no full other-character flag-preservation claim follows from it.

Separate n2-profile-b replays the protected crash savedata and byte-identical active owner3 journal, without editing its home point. Fresh11296/log211733 loads EiEi level55 from Load Game (explicit selection and confirmation), with owner3 still pending on disk. Settled Cathedral map0x18000000/lamp2402950, own_world1/type0/loading0, position(14.028195,-9.508328,105.312050). Status screen confirms EiEi. No original-point/recorded-lamp recovery requests or recovery settlement are logged. Owner3 journal remains byte-identical to the protected crash input, SHA256 `0df56bc97b367bce1f7245681a2b8644d4433f0e7e1f6683ae89c363d37ffdab`, through normal Exit Game -> YES (userdata0001 saved21:21:28). The process was stopped after observing the title-startup logo. The early n2-other-world snapshot was taken in the confirmation menu and is not a gameplay baseline; use n2-other-settled-world only as the observed loaded state.

This proves only bounded disk-pending journal/other-character isolation. There was no in-flight owner return canceled by title, no independent EiEi before/after flag baseline, and no later owner retry in this N2 run. Do not close N2 or run its checker as a claimed PASS.

## Checkpoint and next action

Original profile rehashed:3171 paths/hashes exact. Test games closed; private crash input and case profiles retained. Usage primary90% used at cleanup, so stop new cases and checkpoint under the project quota rule. N4 and synthetic N3 point copies were prepared but not launched. No packaging, deployment, new implementation or external message. Defaults remain OFF and broad R03 acceptance open.

Next: diagnose the accepted exact-point request arriving16.086579m away; control the six group12705 reload bits independently; finish actual pending-return title cancellation, other-character flags and original-owner retry. Resume from protected crash-state plus the documented case copies, rather than overwriting the evidence.
