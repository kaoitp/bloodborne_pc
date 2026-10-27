# R03 final-composition native checkpoint 01

2026-10-27 (Asia/Bangkok), Codex. IN_PROGRESS. Source checkout `27366a686b8ff543d0d7c815e47ce2f89267cae1`. No product source changes.

## Composition and preflight

The existing ignored reference does not reverse-check against the merged patch. Preserve it. An isolated copy under `.superpowers/r03-final-native-01/source` was reconstructed for the four patch destinations using pinned Git objects at `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`, normalized to the patch's CRLF convention, then the current tracked patch was applied. The initial LF-only reconstruction failed cleanly; the CRLF reconstruction applied successfully. Dependencies came from the existing reference.

The existing build script was reused via a private wrapper. Its revision query is supplied the independently verified pinned revision because this isolated directory has no Git metadata; its reverse patch check and compiler command run normally. No release packaging.

- Source CRLF SHA256 `ee21b5e71dee64b3c39dcda8107fd34c4e703676f5dade701f9f07220910aad2`.
- Patch LF SHA256 `7871e606f8d2c90d59ae58abc02abd4456cf6b7e7075cef2c300ecfc16cc25cf`; working-file CRLF `66be824139a15d74bf9862fb955b8fd2fe7816b1bcd4de4b3a3c4828f7de8ad1`.
- Built DLL SHA256 `87319fd9c2bbf748d5ab3e9ad06fbab7376fb075edba86be5c451f9f8ea12cf6`, build exit 0.
- Reused source-built probe SHA256 `6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14`.

## Fixture evidence

`C:/msys64/clang64/bin/python.exe .superpowers/r03-final-native-01/verify.py`: 12 actual-function/header tests PASS, no skips, 25.845 s. Each imported module's SOURCE is explicitly bound to the isolated source; local TEMP/TMP and CLANG64 PATH are set. Initial raw discovery used old default source paths in three modules and failed (two assertions, one missing symbol); that run is a harness composition error, not a final-source regression. Private logs preserve both results.

## Native configuration and observations

Fresh copies of existing authorized test profiles, with distinct accounts/ports, are under the private checkpoint directory. A fresh original-profile hash manifest was taken before launch. Shared progress OFF, guest items ON, Dream ON, spectate OFF, reward-once OFF, home-recovery OFF, experimental admission/recovery OFF, extra warp-join disabled by existing run.py. 1280x720 / 30 FPS. Game assets and account credentials remain private.

Sandboxed startup fails before the game with error 487 reserving the PS4 virtual-address range, exit 21. It reproduces with the baseline DLL, so it is not evidence against the candidate. The same copied-profile candidate launched successfully outside the sandbox. Hidden launch helper initially did not survive; the active foreground exec session was used. Stale exit files from the failed attempt must not be read as completion of the active process.

Both native processes loaded this DLL, verified the image and installed 160/160 hooks. Both connected to the gameplay relay; authenticated online menus and self-hosted summon create/search/claim/delete exchanges were observed. This is bounded route evidence, not a full required-service inventory or outage proof.

Host Kaori level 34, guest U-I-AHH level 10. Host in Cathedral (`0x18000000`), guest visibly settled at Clinic (`0x18010000`). Captured independent 1250-group snapshots. Native loading=0 occurred while the loading screen was still visible; keep early and settled snapshots separate.

Guest rang Kin Bell with the existing password and joined host. Handoff 23:38:09; summoned reload finished 23:38:17. Guest own_world=0/type=1 in the host map. Measured host/guest separation 0.848277359 m, both models visible on the guest screen. No memory writes or debug kill were used; the existing BB_PAD_FILE test input was used for menu controls. No jointly earned event occurred.

Guest used Parting Blank / Return to Your Own World, confirmed YES; OnLeaveMagic at 23:40:10. Subsequent native position equals all four original position coordinates and map/lamp, but visible settled return and reload comparisons are still pending at this entry.

## Remaining

Do not close broad R03 or reward/recovery gates from this run. Finish settled return, normal save/title/reload, stable repeated full-flag comparisons, original manifest readback and process cleanup. Then perform final-composition positive earning and pending recovery/owner/fallback gates on separately prepared copies with explicit effective switches. No production defaults enabled.

## Completed bounded result

- Visibly settled Clinic return: `guest-returned-world.json` exactly matches all 1250 prejoin groups, and map/lamp/position/rotation exactly match the prejoin origin.
- Normal Exit Game to title saved slot 3 at 23:42:32, followed by Continue in PID12328. All 1250 groups exact and origin exact; a repeated stable snapshot is identical.
- Host also exited normally to title. The two session processes were then explicitly stopped for independent reload; this is not recorded as normal application-window shutdown.
- Fresh guest PID24924 loaded the same saved character: visible Clinic, all 1250 groups equal, origin/map/lamp/rotation exact. The snapshot JSON hashes differ only because PID differs. A stable repeat remains to be captured before cleanup.
- Host post-session differs in groups12415,2,9 from its prejoin snapshot; not classified by this run. Do not infer host full integrity from guest success. No positive earning occurred; shared progress and experimental persistence switches were OFF.
- Fresh original manifest: all3171 files/path set unchanged. Raw native logs/captures and saves remain private. The guest restart reused stdout/stderr names, overwriting the first guest stdout/stderr; per-process DLL logs and RE/HTTP captures remain retained. Subsequent cases must use separate launch-output names.
- User explicitly requested whether command-assisted boss killing is possible; next positive uses a disclosed HP-0 aid on test copies only, with real game reward/event/save handling.

Commands used: private `build.py` wrapping tools/build_bbsc_mod.py; private `verify.py`; `pwsh -NoProfile -File .superpowers/r03-final-native-01/launch-test.ps1 -Client a|b` (outside sandbox); `.superpowers/r03-close/read-world.py PID OUTPUT` and `read-position.py PID OUTPUT` read-only snapshots; existing BB_PAD_FILE input. No full suite, product implementation, release packaging, default enablement or service deployment.
