# T1: original-point recovery after interruption

2026-10-29 (Asia/Bangkok), Codex. **PASS for the protected B17 crash replay.** No product source/default/server changes. T2–T4 and broad R03 acceptance remain open.

## Test and composition

User requests T1 from the return-to-own-world plan. Checkout `351ec3e7a68f1ed39b7b5c28fd8be25747ceee3e`, branch seamless, includes [B19](R03-B19-HOME-POINT.md). Isolated pinned BBSC source at `.superpowers/t1/source`, pin `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`; fmt `ec73fb72477d80926c758894a3ab2cb3994fd051`, xbyak `44a72f369268f7d552650891b296693e91db86bb`. Fresh local DLL with mandatory LICENSE.txt, NOTICE.txt and SUPPORTERS.txt. Native startup verifies image, 50 patch sites and 160/160 hooks.

SHA256:

| Input | Hash |
|---|---|
| patch | `0d152637899ab4c0fbff97aa874da44d955b7e7090ff0a0b13ca0553de852608` |
| normalized_patch | `082bc6e9d2f526bc5f567efbf99d1518eacf4f1359f1ab8437e57f7860ed5169` |
| source | `464a21d71a212d5c64201c352571f2756b935f95aa7be59e87bf7d3c77ff7d39` |
| dll | `642a16933d7d821b301b3c4a9e373787800fadc7ba33023d972471972cfc5b5b` |
| probe | `6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14` |
| journal | `0df56bc97b367bce1f7245681a2b8644d4433f0e7e1f6683ae89c363d37ffdab` |

Patch hash is the tracked file's actual CRLF bytes; normalized_patch is the identical text with LF endings used for initial application. Source is the tested LF file. The standard builder subsequently verified reverse application of the tracked patch and built successfully.

Fresh profile copied from native01; its savedata replaced entirely with protected `.superpowers/r03-b17-native/crash-state/savedata`, owner journal copied byte-for-byte from crash-state/own-sd1-3.bin. Historical interruption was 0.004162s after placement; this test replays that input, without creating a new interrupted party. Owner sd1 slot3, U-I-AHH. No host/gameplay earning needed.

Effective copied-guest configuration: HOME_RECOVERY=1; EXPERIMENTAL_HOME_RECOVERY=0; SHARED_PROGRESS=0; REWARD_ONCE=0; GUEST_ITEMS=1; DREAM=1; SPECTATE=0; no-death1, 1280x720/30FPS. Existing authorized online account/service settings reused privately. Do not publish launch helper, profiles, saves or raw logs. Default recovery remains OFF.

## Actual checks

- Isolated local Git clone and only fmt/xbyak submodule initialization succeed outside sandbox. Initial patch attempt fails because of line endings; normalize the four isolated destinations and a private patch copy to LF, apply private patch, then standard build succeeds. No modification of tracked runtime patch.
- `C:/msys64/clang64/bin/python.exe tools/build_bbsc_mod.py .superpowers/t1/source .superpowers/t1/dll`: exit0, hash above.
- `python.exe -m unittest discover -s tests -p test_bbsc_home_recovery.py`, BBSC_FIXTURE_SOURCE set to isolated source: 1 actual-function test PASS, no skips. First attempt cannot write sandbox TEMP; rerun with TEMP/TMP in `.superpowers/t1/tmp` succeeds. Fixture is separate from native evidence.
- Initial sandbox launch fails reserving PS4 address space, error487, before gameplay. Preserved launch-sandbox stdout/stderr. Same copied profile launched outside sandbox; native PID9236, log bbsc-mod-20261029-191723-9236.log. Play Online -> Continue via existing BB_PAD_FILE test input. Early screenshots while loading are not settlement evidence.
- 19:19:55.197: finds owner3 crash journal and arms return to 0x18010000. 19:19:55.231: full point reload accepted, try1. **19:20:06.777: own world and return point settled**, journal retained as restored. Exactly one point request; no arrived-elsewhere, lamp request, give-up or forced-warp removal during recovery.
- Read-only `.superpowers/r03-close/read-position.py 9236 .superpowers/t1/settled-position.json`: own_world1, type0, loading0, map0x18010000, lamp2412950, position `(-190.1808319091797,-50.62248992919922,166.48239135742188,1)`, rotation `(0,0.06571602821350098,0,0)`. **Distance0.0m**, map and rotation exact to protected journal-origin.json. Visible Clinic world settled.
- Read-only read-world.py: all1250 groups exact to B17 guest-before-world.json. This is immediate settled preservation, not T2 save/restart proof. Restored journal remains byte-identical to protected crash input.
- `python.exe tools/check_r03_native.py b17-n1 .superpowers/t1/dll/logs/bbsc-mod-20261029-191723-9236.log --user-dir .superpowers/t1/profile-b/user`: verdict MANUAL. All automatic checks pass; its remaining text also requests post-reload location, which belongs to T2. Manual settled position assertion above passes; no full checker PASS claimed.
- Assert-based distance/map/rotation/role, one-request/no-fallback, 1250-group comparison and journal checks exit0. Private assert-result.json retains results.
- Normal System -> Exit Game -> YES; userdata0003 written19:21:28, title startup logo observed. Test window closed, runner exit0. Protected after-t1-savedata and after-t1-own-world copies available for T2.
- Original profile independently hashed before/after: **3171 identical paths/hashes**. Private original-before/after.json retained. No original profile launched.

## Boundary and next action

T1's replay acceptance passes and supplies matching-build native evidence for B19's point fix. It does not test a new crash, multiplayer earning, other-character cancellation, lamp fallback or independent save/reload integrity. Next T2: use protected T1 save+journal, independently restart owner and compare repeated settled1250 groups/position against prejoin and a no-party save/reload control. Keep the earlier six12705 bits unclassified until that control is done. T3/T4 remain separate; PR17 reward persistence is deferred. No release packaging, service redeployment or production switch changes.
