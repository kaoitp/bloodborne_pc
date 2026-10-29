# Recovery Blood Echoes protection: PASS

2026-10-29–30, Asia/Bangkok. User authorized fixing Echoes lost in the synthetic T4 void recovery. This follows [the destination/flag correction](R03-T4-SETTLEMENT-FIX.md); recovery remains OFF by default. Work and native testing use copied profiles only.

## Change and evidence boundary

The game applies the death penalty through `DropBloodstain` at offset `0x013D2910`: it transfers held Echoes into the stain record, zeroes the held balance and can replace a previous stain. The existing entry-hook mechanism can skip that whole function before these writes. The tested flat game image's six entry bytes are `55 48 89 e5 41 57` (whole non-relative instructions); installation verifies them.

The new callback skips only when a recovery is pending, the game is in its own world, the call targets the local character with penalty argument1, and the active user/save slot matches the journal owner. Every entry first clears the skip flag; the existing trampoline also clears it after use. Unknown/other owners, another character, non-penalty calls, title cancellation and completed recovery retain normal behavior. There is no currency snapshot/refund/addition and no new journal format, so the change does not create a second claim on the same Echoes.

Protection installs independently of optional spectating/death-penalty settings. Recovery does not arm if the verified protection hook is unavailable; its journal remains on disk. Existing floor stability, fallback, ownership, retry bounds and default-OFF switches are retained. Only the integrated BBSC source patch and its actual-handler fixture change; other compatibility/profile-storage sources remain unchanged.

## Matching composition and tests

Pinned BBSC reference `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`. Isolated source/build/evidence under `.superpowers/echo-fix`; all four integrated destinations use LF, and the tracked patch reverse-checks against the source. Mandatory DLL notices are present.

| Tested artifact | SHA256 |
| --- | --- |
| `bbsc.dll` | `0fc1e26aa2cc8763ed1d5daab078e39228a11a6c3f19aedbd2040e6ffea7800d` |
| `bloodborne_re.cpp`, LF | `afd30f71c2286511b3f68aeebdda67a432bddd0dd960164dc8d05a75e1ade410` |
| Integrated patch, LF | `3ea98666374d56f165d151bd1711a9b3e8caa3277318201cf8b79d0c56a77408` |
| Small-window probe | `3f2cad58ab15c1f7146cff42d809e4d7145a99d5ef0e94a2f8233efb553d84bb` |
| Edited T4 journal, reused exactly | `d21a34910f0f324a4b435476b7a5f8e98f84c593f2f219db326556e28b405824` |

With CLANG64 on PATH, workspace TEMP/TMP, and `BBSC_FIXTURE_SOURCE` selecting the tested source:

```powershell
python -m unittest discover -s tests -p test_bbsc_home_recovery.py
python -m unittest discover -s tests -p test_r03_native_check.py
python tools/build_bbsc_mod.py .superpowers/echo-fix/source .superpowers/echo-fix/dll
```

The actual-handler fixture goes RED on the preceding T4-fixed composition: held535 is lost and the modeled old stain317 is replaced. GREEN on this candidate,1 compiled ASan fixture test with20 numbered cases including the existing recovery cases. The new cases cover repeated guarded drops, zero held balance preserving an older stain, normal penalty after settlement, six ownership/call boundaries and unavailable-hook refusal. The fixture models the native penalty body; actual game behavior is checked separately below. Nine log-checker tests pass; standard DLL builder exits0.

## Native guarded replay

PID20940, log `bbsc-mod-20261029-235206-20940.log`, fresh protected B17 crash saves and the exact edited journal. HOME_RECOVERY1, EXPERIMENTAL_HOME_RECOVERY0, SHARED_PROGRESS0, REWARD_ONCE0, SPECTATE0, **cheat_no_death0**,900×506 window,1280×720/30FPS, existing authorized online service/account.

- 23:52:07.582: protection hook ready despite SPECTATE0.
- 23:55:09.113: edited original point requested.
- 23:55:21.760: `prevented Echoes drop for user sd1 slot 3 (held 535)`.
- 23:55:22.888: additional load before settlement fails the point; recovery remains pending.
- 23:55:35.877: recorded lamp2412950 requested.
- 23:55:48.775: settled at the lamp after the existing ground check.

Read-only native snapshots show535 held before the request and535 after return; the HUD agrees. Three settled snapshots15 seconds apart retain535, own_world1/loading0/type0, map `0x18010000`, lamp2412950, position `[-199.74000549316406,-50.75874328613281,179.4199981689453,1]` and all1,250 prejoin flag groups exactly. The prior stain record remains exists1, amount−1, map `0x18010000`, position `[-189.10940551757812,-50.60334777832031,151.9554901123047]`; no duplicate535 stain is created. The native input has no positive recoverable old-stain balance; preservation of positive317 is covered by the fixture, not claimed as a native nonempty-stain test.

Normal save→title→close exits0. The resulting535 save and restored journal are protected separately under `.superpowers/echo-fix/protected-after-recovery` before any ordinary-death negative control. The retained journal is byte-exact to the edited input; no active journal remains.

Independent PID27328, `bbsc-mod-20261030-000138-27328.log`, installs the same hook and loads the normally saved copy without replaying recovery. Three settled snapshots15 seconds apart retain535 held, the exact lamp/map/transform and the unchanged prior stain record. All1,250 groups match the preceding independent ordinary-respawn control; only its already-classified six group12705 bits differ from prejoin. No new unexplained flag difference appears.

After these acceptance snapshots, a bounded test writes only the disposable local character's HP to0, with own_world1/loading0/type0/535 held and no active journal asserted beforehand. The protected535 save already exists. The native game executes the ordinary death path:50 read-only samples show **0 held and535 in the stain**, and the game displays Acquire Blood Echoes at that stain. The reloaded process logs the protection hook as ready but no prevented-drop message, proving protection does not remain active after recovery. No Echoes, stain or flag values are injected. This is native death-path evidence with injected damage, not a new combat/party qualification. Normal save/title/close exits0; both test processes are closed.

Final assertions: six settled currency snapshots preserve535 and the prior stain fields; both normal exits0; edited journal retained byte-exact as restored; source/DLL/patch/probe unchanged; original3,171 paths/hashes exact. The native535→535 recovery/save/reload and535→0 ordinary-death negative control are PASS. The raw negative-control profile ends with0 held and535 in its legitimate stain; the successful535 save is preserved separately.

## Private evidence and limits

Evidence includes `hashes.json`, RED/GREEN/checker/build logs, source/patch/DLL/notices, per-case launch/log/exit files, read-only money/position/world/time snapshots, the initial money timeline, protected535 save, negative-control injection record and final assertions/manifests. Raw data, assets, logs and credentials stay out of Git.

The engine can still pass through its death-style Dream transition before fallback; this change protects the penalty rather than claiming that transition never happens. Native other-character cancellation, nonempty prior-stain balance, a new party/reward run and broader R03 acceptance are not qualified by this case. No default activation, release packaging or server redeployment.
