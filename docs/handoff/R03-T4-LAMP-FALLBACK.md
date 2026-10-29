# T4 recorded-lamp fallback: FAIL; side-by-side test windows: PASS

2026-10-29, Asia/Bangkok. User requested T4 after T1–T3 and smaller game windows placed beside each other. Work stayed inline on `seamless`. Recovery/admission defaults, recovery implementation and services were not changed. The display override below is a separate, explicitly requested source change.

## T4 inputs and artifacts

Fresh `.superpowers/t4/profile-b` copied the protected B17 crash saves and owner journal, independently of T1–T3. Owner: sd1 slot3, U-I-AHH; origin map `0x18010000`, recorded lamp `2412950`. Original position `[-190.1808319091797,-50.62248992919922,166.48239135742188,1]`. The prepared B17 N3 method changed only its four position floats to `[19999,-10000,19999,1]`. An assertion verified every byte outside that 16-byte range stayed exact; map, lamp, rotation and flag payloads were preserved. Both journal versions are retained privately.

| Tested input/artifact | SHA256 |
| --- | --- |
| Protected original journal | `0df56bc97b367bce1f7245681a2b8644d4433f0e7e1f6683ae89c363d37ffdab` |
| Edited T4 journal | `d21a34910f0f324a4b435476b7a5f8e98f84c593f2f219db326556e28b405824` |
| T1 B19 `bbsc.dll`, reused | `642a16933d7d821b301b3c4a9e373787800fadc7ba33023d972471972cfc5b5b` |
| Its `bloodborne_re.cpp`, reused | `464a21d71a212d5c64201c352571f2756b935f95aa7be59e87bf7d3c77ff7d39` |
| Integrated tracked patch, CRLF bytes | `0d152637899ab4c0fbff97aa874da44d955b7e7090ff0a0b13ca0553de852608` |
| `out/bb-probe.exe`, both T4 processes | `6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14` |

Artifact hashes were asserted before preparation and again after both T4 processes closed. Required DLL notices remain present. These T4 results use the unchanged T1 composition, before the separate window build. See [T1](R03-T1-POINT-RECOVERY.md) for pinned source/build attribution and [T2](R03-T2-SAVE-RELOAD.md) for the control.

## Native result

First process PID25416, log `.superpowers/t1/dll/logs/bbsc-mod-20261029-221928-25416.log`; 160/160 trace hooks installed.

1. 22:21:43.700: recovered owner3 crash journal and began return to map `0x18010000`.
2. 22:21:43.741: requested edited original point `(19999,-10000,19999)`, result1/accepted true, try1.
3. 22:21:46.617: logged **own world and return point settled**, and moved the journal to `.restored`.
4. 22:21:47.803–.804: recognized the owner and put back979 own flag groups.
5. 22:22:11.196: respawn log changed recorded lamp2412950 to Hunter's Dream2102961, map `0x15000000`. No further gameplay movement or warp input was sent.

There is **no point-failure log and no recorded-lamp request**. Three read-only snapshots20 seconds apart subsequently agreed on own_world1/loading0/type0, map `0x15000000`, lamp2102961, position `[-9.199999809265137,-6.770590782165527,-19.399999618530273,1]`, rotation `[0,-2.356194496154785,0,0]`. The displayed scene was Hunter's Dream. The `.restored` journal is byte-exact to the edited input; the active journal is absent.

Normal System → Exit Game → Yes saved to title; normal window close exited0. Independent process PID10720, log `bbsc-mod-20261029-222557-10720.log`, loaded Continue from that save. Three further20-second snapshots gave the exact same Dream transform/map/lamp and own-world state. Normal save/title/close again exited0. Thus the wrong destination persists after independent restart.

T4 is **FAIL**: its required point-failure → recorded-lamp fallback → correct persistence sequence did not happen. The prepared finite out-of-bounds point is accepted long enough for settlement, followed by Dream. Source inspection shows settlement checks map/distance after2 seconds; premature settlement before the later transition is an investigation lead, not a proven complete root cause. Do not treat “settled” or `.restored` alone as a valid destination gate.

## Personal flags

Each set of three snapshots is internally byte-exact across all1,250 groups. Against the prejoin owner baseline, the first run has17 differing bits and the independent reload has16:

- Both: `12101024,12105030,12105100,12105300` change0→1; `12415461,12415770,12415771,12415772,12415773` change1→0; `12705098,12705301,12705520,12705521,12705531,12705532` change1→0.
- First run only: `12105800,72100133` change0→1.
- Reload only: `12105802` changes0→1.

T2 identifies the six group12705 bits as transient during its normal Clinic load/control. This run ends in a different map, so T2 does not classify the complete T4 difference set or prove its eventual convergence. The remaining differences are unclassified here. Personal flag preservation is **not qualified** by T4; these differences do not, by themselves, prove permanent progress loss. Private `flags-analysis.json` contains the complete directional comparison.

## Separate display change and native verification

The unchanged probe starts a1920×1080 window; native window menu/resize attempts did not change it. `gpu/shim/window.cpp` now accepts optional `BB_WINDOW_RECT=x,y,width,height` when `BB_FULLSCREEN` is not1. Parsing requires exactly four comma-separated integers, coordinates−32768…32767, width320…8192, height180…8192. Invalid input logs a warning and keeps the original centered size; absence preserves the original behavior. Fullscreen retains precedence. This changes window geometry only; render/output resolution and recovery behavior are untouched.

Command: with `C:/msys64/clang64/bin` prepended to PATH, `ninja.exe -C out/gpu bb-probe` completed exit0; only window.cpp compile, static-library link and probe link were reported. Display source SHA256 `3106bcc0ebffceed741edef4902136d71743490740ac96b6be52af70ea64d0d8`; separately built `out/gpu/bb-probe.exe` SHA256 `3f2cad58ab15c1f7146cff42d809e4d7145a99d5ef0e94a2f8233efb553d84bb`. The validated T4 `out/bb-probe.exe` remains unchanged; display launch scripts explicitly select `out/gpu/bb-probe.exe`.

Native invalid-height control `BB_WINDOW_RECT=0,0,900,0` logged rejection and `Window1920x1080`. This first online startup from the new EXE path opened a Windows Firewall permission prompt. No security UI was acted on; the startup-only process was stopped (exit−1), and layout validation switched to `BB_ONLINE=0`.

Two copied offline profiles then opened900×506 client windows at `(10,70)` and `(970,70)`. Both native logs confirm900×506. Computer Use screenshots measured outer rectangles `(9,39,902,538)` and `(969,39,902,538)`; an assertion verifies a58-pixel gap and no overlap. Both reached the title menu without the permission prompt. They are left open at title for the user's requested layout, with no party/gameplay load. Private launcher (run each command in a separate shell; each waits for its game to close):

```powershell
& .superpowers/t4/launch-window.ps1 a
& .superpowers/t4/launch-window.ps1 b
```

The launcher applies the respective rectangles and offline mode to the copied profiles. Existing online T4 launch scripts and their evidence are preserved separately. Native fullscreen and co-op/gameplay on the display-only probe were not retested.

## Commands, private evidence and next action

Private evidence is under `.superpowers/t4/`: `prepare.py`, `launch.ps1`, `launch-reload.ps1`, original/edited journals and edit assertion, launcher stdout/stderr/exit files, six `point-result-*`/`reload-*` position/world/time snapshots, `flags-analysis.json`, window build log/hashes/geometry, `verify.py`, `assert-result.json`, original-before/after manifests. Saves/logs/credentials/assets are not committed.

- Launched `launch.ps1 b` and `launch-reload.ps1 b` outside the sandbox; native address reservation and read-only memory access require it.
- Used existing `pad.ps1` for observed title/Continue and normal save/exit menus. `capture.py PID point-result|reload` runs existing `read-position.py` and `read-world.py` three times,20 seconds apart.
- `check_r03_native.py b17-n3 LOG --user-dir .superpowers/t4/profile-b/user` returned actual exit2, `INCOMPLETE`: missing point-failure, recorded-lamp and lamp-settlement evidence; reload is manual. Manual location evidence makes the T4 acceptance result FAIL.
- `verify.py` passed: reused artifacts and protected journal exact, edited `.restored` exact, both T4 normal exits0, original3171 files byte-exact, native valid/invalid display assertions and nonoverlap. Separate assertions confirmed all six settled positions and repeated1,250-group equality within each run.

Fixture/build evidence: display incremental build and native input/layout assertions above; no new recovery fixture run because recovery source/artifacts did not change. Native evidence: actual failed recovery/save/restart, plus offline two-window title display. Gameplay evidence: no new party, fight or reward qualification.

Next: investigate premature recovery settlement and the later Dream transition; retain/retry the journal until a valid supported origin/lamp is durably established, then rerun T4 and its flags control. Keep T4/B17 N3 and broad R03 acceptance open, recovery/admission defaults OFF. T3 pre-arrival cancellation remains a separate open boundary. No release packaging or server redeployment.
