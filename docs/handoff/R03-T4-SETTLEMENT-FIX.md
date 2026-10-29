# T4 recovery settlement correction: destination/flags PASS

2026-10-29, Asia/Bangkok. The user authorized fixing the demonstrated T4 failure inline. This checkpoint supersedes the destination/flag result of [the earlier failed T4](R03-T4-LAMP-FALLBACK.md) for the corrected composition below. It does not close broad R03 acceptance or activate recovery by default.

## Confirmed cause and correction

A fresh copied replay with the unchanged B19 DLL reproduced the failure. Read-only sampling at100 ms intervals found118 samples at `(19999,-10000,19999)`; **all had character floor pointer0**, including when recovery logged successful settlement. The old check accepted the matching map/coordinates after2 seconds from the request, archived the journal, and stopped tracking recovery. The engine subsequently loaded Hunter's Dream. This is a native confirmation of the false arrival, not just a source hypothesis.

The integrated BBSC patch now:

- Reuses the existing `ChrFloorOffset`/`BbscFloorReadsBack` validator through `BbscHomeRecoveryGrounded`; requires usable ground and matching destination continuously for2 seconds before archiving the journal. Loading, unknown owner, unavailable character or dead character reset that interval.
- Keeps the existing map/5-metre original-point check, including rejection of non-finite distance. Lamp settlement also checks the recorded lamp ID. A loaded target without stable ground has a30-second bounded wait; failures use the existing point→lamp retry budget.
- Treats an additional in-world load before settlement as a failed target, retaining owner recovery and its journal for fallback. Title/other-character cancellation remains separate and unchanged.

Only recovery settlement/load handling and reuse of its floor validator changed in the applied source. The other three integrated compatibility/profile-storage files remain text-identical to T1. No header/export, party-progress, service or default-switch change. Native controls use the existing scripted pad interface; memory sampling is read-only.

## Matching artifacts

Pinned BBSC reference: `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`; isolated source/build/evidence: `.superpowers/t4fix`. The tracked integrated patch reverse-checks against that source. Required LICENSE/NOTICE/SUPPORTERS files are beside the DLL.

| Artifact | SHA256 |
| --- | --- |
| Corrected `bbsc.dll` | `f057271c2547c796e21e41400f59a6dd3ad279253be94ee249abd70afd0cd08e` |
| Tested `bloodborne_re.cpp`, LF bytes | `ddc3ba5b60ffdecc074f105b395512e6b5fa04f68448e21afbf70baa9abfbb6b` |
| Tracked integrated patch, LF bytes | `a78c9dd56e943a5dcee007fad9ec7a73f64cc397c28f2029fd624d5800b765ca` |
| Small-window probe | `3f2cad58ab15c1f7146cff42d809e4d7145a99d5ef0e94a2f8233efb553d84bb` |
| Protected original journal | `0df56bc97b367bce1f7245681a2b8644d4433f0e7e1f6683ae89c363d37ffdab` |
| T4 edited-point journal | `d21a34910f0f324a4b435476b7a5f8e98f84c593f2f219db326556e28b405824` |

The display-only probe from the preceding checkpoint was copied to the existing `out/bb-probe.exe` path for these tests; the old probe remains protected in `.superpowers/t4/bb-probe-before-windows.exe`. Thus these are matching **new-composition** native results, not claims that the old T1 probe hash is unchanged. Windows are900×506, render/output1280×720/30FPS. Copied recovery cases use HOME_RECOVERY1, EXPERIMENTAL_HOME_RECOVERY0, SHARED_PROGRESS0, REWARD_ONCE0; the independent control has HOME_RECOVERY0 and no active journal. Existing authorized online services/accounts are reused without redeployment.

## Fixture and build evidence

With CLANG64 on PATH, workspace-local TEMP/TMP, and `BBSC_FIXTURE_SOURCE` selecting the source under test:

```powershell
python -m unittest discover -s tests -p test_bbsc_home_recovery.py
python -m unittest discover -s tests -p test_r03_native_check.py
python tools/build_bbsc_mod.py .superpowers/t4fix/source .superpowers/t4fix/dll
```

Actual-function recovery fixture: **RED** on the preserved T1 source at the assertion requiring an active journal while coordinates match but no floor exists; **GREEN**,1 compiled ASan fixture test, on the corrected source. Its17 numbered cases retain the previous opt-in/owner/title/cancel/refusal/timeout/budget checks and add no-ground timeout, transient floor, interrupted stability, in-world second load and wrong-lamp checks. Floor availability is controlled in that fixture; the production pointer condition is calibrated natively above.

The log checker initially returned INCOMPLETE for the successful new fallback because its whitelist did not recognize the new failure reason. Two corresponding synthetic subcases went RED; after adding exactly `another load before settlement` and `no stable ground at the return target`, all9 checker tests pass. Point→lamp→settlement ordering and the manual reload requirement remain intact.

Standard DLL builder exit0, final hash above. Setup failures were corrected before the tested build: sandbox default TEMP denied fixture cleanup, so TEMP/TMP moved inside the workspace; initial patch regeneration mixed CRLF/LF in the three copied compatibility files, so all four isolated destinations were normalized to LF and the integrated patch regenerated/reverse-checked. No failed build artifact was used for acceptance.

## Native corrected T4 and persistence

Guest owner sd1 slot3/U-I-AHH, fresh protected B17 crash-save copy and the byte-exact edited T4 journal. PID21496 log `bbsc-mod-20261029-230047-21496.log`:

| Local time | Actual event |
| --- | --- |
| 23:02:55.357 | Original edited point requested, accepted, try1 |
| 23:03:09.848 | Another load before settlement: point1 fails; journal remains pending |
| 23:03:23.087 | Engine reaches Dream during its own respawn path |
| 23:03:23.148 | Recorded lamp2412950 requested into `0x18010000`, accepted, try1 |
| 23:03:34.137 | Engine resolves lamp2412950 on the correct map |
| 23:03:36.245 | Settles after the usable-ground interval; journal becomes `.restored` |

Three20-second-apart settled samples agree on own_world1/loading0/type0, map `0x18010000`, lamp2412950, position `[-199.74000549316406,-50.75874328613281,179.4199981689453,1]`, rotation `[0,0,0,0]`. Every one of the1,250 flag groups equals prejoin. Separate read-only sampling gives840 samples on usable ground at that lamp. The retained journal equals the edited input byte-for-byte; no active journal remains.

Normal System→Exit Game→Yes, title, window close: exit0. Independent PID27520 (`bbsc-mod-20261029-230835-27520.log`) loads that normally saved character with **no recovery replay**. Three further samples retain the exact lamp/map/transform and own-world state. Its only baseline differences are six group12705 bits,1→0: `12705098,12705301,12705520,12705521,12705531,12705532`. The independent control below classifies this complete difference set. Normal save/title/close again exits0.

The updated `b17-n3` checker returns actual exit3/MANUAL: point failure, recorded-lamp request, settlement and retained journal all found; location/reload/flags are qualified by the independent snapshots/control, not by relabeling the checker as automated PASS.

## Valid-point regression and independent ordinary-respawn control

PID2012, `bbsc-mod-20261029-231948-2012.log`, uses another fresh protected crash copy and the unmodified journal. One accepted original-point request at23:22:34.164, settlement at23:22:48.354, no fallback. Three snapshots give the **exact original** position `[-190.1808319091797,-50.62248992919922,166.48239135742188,1]` and rotation `[0,0.06571602821350098,0,0]`,0.0 m error, and all1,250 groups equal prejoin. Normal save/title/close exit0. `b17-n1` returns3/MANUAL. This is a valid-point arrival/flags regression; independent original-point reload was not repeated on this composition.

For the six flags, `.superpowers/t4fix/control/profile-b` is an independent copy of T2's ordinary no-party control, not a copy of the recovered T4 save. No active `.bin` journal, HOME_RECOVERY0. PID17016, `bbsc-mod-20261029-231820-17016.log`, has **zero home-recovery messages**. Its initial native snapshot is at the original point and equals all1,250 prejoin groups. Two short ordinary walking inputs leave those groups unchanged. Then the ordinary inventory Hunter's Mark→Use→Yes returns it to lamp2412950. No bell, party, forced memory write or recovery is used. Hunter's Mark intentionally spends this disposable copy's535 Echoes.

Three settled ordinary-respawn snapshots have the same lamp/map/position/rotation as T4 reload and are **byte-exact across all1,250 groups to every T4 reload sample**. Their only prejoin differences are those same six1→0 bits. Thus the complete T4 reload difference set is reproduced by ordinary game respawn; no additional recovery-specific flag difference remains. This extends [T2's loading control](R03-T2-SAVE-RELOAD.md) to the actual lamp/respawn state; it does not assign undocumented gameplay meaning to individual bits. The control is normally saved/closed, exit0.

T4's defined destination, own-world flags and independent save/reload acceptance is **PASS** for this prepared fault. Twelve settled snapshots cover fallback before/after restart, valid-point return and independent lamp control; the control also has an independent pre-action baseline snapshot. Original3,171 paths/hashes and protected journal remain exact. All four candidate processes and the separate B19 reproduction close normally, exit0; no game is left running.

## Limits and next action

The deliberately out-of-world point still invokes the engine's death-style Dream transition before the retained recovery returns to the recorded lamp. The copied character displays535 Echoes before this fault and0 afterward. This fix does **not** establish Echoes preservation or avoidance of death during arbitrary bad-point recovery. Ordinary Hunter's Mark also spends Echoes by design; matching that control qualifies the world-flag comparison, not currency protection. Do not advertise this as complete safe recovery for every unreachable position.

No new party, fight/reward, every-map, native pre-arrival title/other-character cancellation or independent original-point reload qualification. Fixture ownership/cancellation cases pass; broad R03 gates and default-OFF switches remain unchanged. No release EXE/ZIP or live-server deployment. Next investigate avoiding the engine's death path/currency loss for unreachable points, then the remaining broader native gates before default activation.

Private evidence: `.superpowers/t4fix/{hashes.json,source-change.diff,fixture-red.log,fixture-green.log,checker-red.log,checker-green.log,build.log,verify.py,assert-result.json,original-before.json,original-after.json}`, preserved source/DLL/notices and per-case launch scripts/logs/exits, raw position/world/time snapshots, before/after journals and floor samples. `verify.py` asserts all12 settled snapshots against the appropriate independent baseline/control, exact transforms/journals/artifacts/originals and normal exits. Saves, credentials, raw logs and assets stay out of Git.
