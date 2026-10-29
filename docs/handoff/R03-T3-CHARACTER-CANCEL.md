# T3: pending recovery cancellation and character ownership

2026-10-29 (Asia/Bangkok), Codex. **PASS for pending settlement after arrival.** Actual in-memory recovery is canceled on another character load, EiEi retains its independently captured own state, and the original owner retries successfully with the original journal. **Quit before physical arrival is not tested**; do not use this bounded result to close that broader B17 N2 timing case or all R03 recovery gates.

## Task, composition and method

User requests T3 after [T2](R03-T2-SAVE-RELOAD.md). Branch seamless `d4fb17c2d96a466fb33e026798330a586d32f395`. Same isolated [T1 B19 build](R03-T1-POINT-RECOVERY.md), mandatory notices, copied-profile input controls and existing authorized online configuration. No build, fixture or product source/default/server change in this test. Native PID3808, one process retained through all character switches; image verified,50 patch sites,160/160 hooks. Mod log `.superpowers/t1/dll/logs/bbsc-mod-20261029-195747-3808.log`.

SHA256, independently rechecked before/after:

| Input | Hash |
|---|---|
| patch | `0d152637899ab4c0fbff97aa874da44d955b7e7090ff0a0b13ca0553de852608` |
| source | `464a21d71a212d5c64201c352571f2756b935f95aa7be59e87bf7d3c77ff7d39` |
| dll | `642a16933d7d821b301b3c4a9e373787800fadc7ba33023d972471972cfc5b5b` |
| probe | `6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14` |
| journal | `0df56bc97b367bce1f7245681a2b8644d4433f0e7e1f6683ae89c363d37ffdab` |

Private `.superpowers/t3/profile-b` starts as a native01 profile copy with savedata entirely replaced by protected B17 crash-state/savedata. Original owner is U-I-AHH, sd1 slot3; other character is EiEi, sd1 slot1. Original3171 files and all prior protected test inputs remain untouched. Effective settings: HOME_RECOVERY1, EXPERIMENTAL_HOME_RECOVERY0, SHARED_PROGRESS0, REWARD_ONCE0, items/Dream1, spectate0, no-death1,1280x720/30FPS. No party, bells, combat or player movement.

To obtain an independent EiEi baseline, the protected owner journal is initially parked outside the profile. EiEi is explicitly selected/confirmed from Load Game; three settled baseline snapshots precede recovery. Normal exit saves EiEi20:03:34. Owner userdata0003 is hash-verified unchanged from the protected crash input after this setup.

At title, activate the byte-identical owner journal. A **nonempty directory** occupies only this copy's `own-sd1-3.bin.restored` destination, preserving any older restored file under a separate name. Source SettleBbscHomeRecovery returns on rename error without clearing its pending owner. This permits a real menu quit while the same recovery remains pending in memory, after the position has arrived. The later native cancellation message confirms that the state remained active; this is more than disk-only journal isolation. No injected memory writes, callback stubs or new runtime hooks were used.

This fault deliberately holds settlement, not the physical warp. The result does not establish menu cancellation during the loading screen or before arrival. The original journal contents are never edited; at release the blocker directory is moved aside intact within `.superpowers/t3`, then the original owner retries.

## Actual sequence and evidence

All times Asia/Bangkok:

1. EiEi baseline: own_world1/type0/loading0, Cathedral map0x18000000/lamp2402950, position `(14.02819538116455,-9.508328437805176,105.31204986572266,1)`, rotation `(0,-0.8688969612121582,0,0)`. All three1250-group snapshots identical.
2. Owner loaded explicitly.20:05:32.612 finds owner3 journal/arms recovery;20:05:32.664 original-point request accepted, try1. Visible Clinic at exact journal point, repeated1250 groups equal B17 prejoin. No settlement message; active journal remains byte-identical and .restored is still the blocker directory.
3. Actual System -> Exit Game -> YES while pending; userdata0003 saved20:07:03, title/menu observed. Journal still byte-identical. Explicitly load EiEi. **20:08:32.734: `another load canceled pending return; journal retained for user sd1 slot 3`.** No warp request or settlement between this cancellation and owner retry.
4. EiEi after: all three settled1250-group dictionaries and complete position/rotation/map/lamp/role snapshots exactly match its independent baseline. Journal remains byte-identical throughout, including normal EiEi exit/save20:10:39.
5. Move blocker aside intact; owner3 journal still exact. Explicitly select owner again, without replacing savedata or journal.20:13:01.084 owner re-arms;20:13:01.118 point request accepted, try1; **20:13:12.434 own world and return point settled**, journal retained as restored. No lamp fallback/give-up or arrived-elsewhere.
6. Three repeated owner-retry snapshots: map0x18010000/lamp2412950, own_world1/type0/loading0, exact origin `(-190.1808319091797,-50.62248992919922,166.48239135742188,1)` and rotation `(0,0.06571602821350098,0,0)`, distance0.0m; all1250 groups exact to B17 prejoin. Active journal absent, restored file byte-identical to protected crash journal.
7. Normal owner Exit Game -> YES saves20:14:41, title observed. Window closes, runner exit0, no game remains. Independent original profile comparison: **3171 identical paths/hashes**. Copied savedata, journal, blocker, logs and snapshots retained privately.

Snapshot timing (three samples20s apart per phase):

| Phase | First–last read | Comparison |
|---|---|---|
| other-before | 20:01:58–20:02:38 | baseline1250 stable |
| owner-pending | 20:05:28–20:06:08 | prejoin1250 exact; pending, not settled |
| other-after | 20:08:55–20:09:35 | EiEi baseline1250 and transform exact |
| owner-retry | 20:12:58–20:13:39 | prejoin1250 and origin exact |

## Commands and checks

CLANG64 `C:/msys64/clang64/bin/python.exe`:

- `.superpowers/t3/prepare.py`: exit0. Assert-guarded copied paths, exact protected owner save/journal and matching T1 artifacts, baseline setup and original manifest. Launch `.superpowers/t3/launch.ps1 b` outside sandbox as required for the known emulator address-space reservation limitation.
- `.superpowers/t3/capture.py 3808 <phase>`: four phases above,12 read-only snapshots; invokes existing read-position.py and read-world.py, checks own-world/type/loading and retains UTC timestamps. All exit0. Acceptance also requires observed loaded world and repeated stable groups.
- Checkpoint assertions verify owner userdata0003 unchanged before the first owner load, byte-exact journal at title/other-character load/after-state/release, and no recovery action in the other-character interval.
- `.superpowers/t3/assert-result.py`: exit0. Complete group-dictionary and transform comparisons across all12 samples, exact journal retention/restoration, request -> cancellation -> owner retry -> settlement ordering, no stray other-character recovery, unchanged source/artifact hashes and original3171 path/hash integrity. Private assert-result.json retains results.
- `tools/check_r03_native.py b17-n2 .superpowers/t1/dll/logs/bbsc-mod-20261029-195747-3808.log --user-dir .superpowers/t3/profile-b/user`: actual exit3/MANUAL, all automatic rows pass. It still requests manual other-character flag comparison; the independent comparison above passes. No automated checker PASS claim, and its log matching alone cannot distinguish the physical-arrival timing boundary.

## Remaining boundary

This T3 case proves cancellation of a still-active owner recovery on a real title/other-character load, unchanged other-character own flags/transform, durable original-journal retention and successful original-owner retry. It does not prove a quit before physical arrival, process-crash survival at this new boundary, inventory equality or another character's independent restart. Defaults remain OFF; no broad R03 gate closed. T4 recorded-lamp failure/fallback/save-reload is next; retain the protected B17 inputs. The historical B17 N2 disk-only result remains historical, superseded only for the bounded pending-settlement case established here.
