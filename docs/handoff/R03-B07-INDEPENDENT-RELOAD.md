# R03 B07: independent settled reload of the protected co-op after-save

2026-10-25, Claude (R03 takeover). Repository checkpoint `c981c62` on seamless; runtime source unchanged from B06 (`a43e26f`). This answers the pending B06 question about the six unclassified `12705` reload bits. No source, patch or configuration change.

## Task and acceptance

B06's same-process Quit/Continue after co-op differed from the prejoin baseline at 12705098, 12705301, 12705520, 12705521, 12705531 and 12705532. Its no-party control showed 12705301 changing transiently on a fresh baseline load. Acceptance for this checkpoint:

- a fresh process loads the protected co-op guest after-save (`native/after-b-savedata`) with the frozen B06 DLL, no party;
- early and settled snapshots are kept separate;
- all 1250 settled groups are compared to `native/guest-before-world.json`;
- the loaded position is compared to `native/journal-origin.json`.

## Setup (this machine)

- New PC: clone of seamless at `c981c62`, pinned BBSC `4f11faf` reference, private support archive (SHA256 `0cc68e44…`, 87 payload files verified against its manifest).
- `core.autocrlf=false` was required in the clone, the BBSC reference and the submodules. With the global Windows default the tracked patch did not apply. The prepared `bloodborne_re.cpp` then equals B06's file with LF endings. Its CRLF form hashes to B06's `76287a32…`; the tracked patch hashes to `6dec09c7…` exactly.
- `tools/build_bbsc_mod.py` exit 0. Fixtures: `test_bbsc_*.py` 3 PASS, `test_native_bbsc.py` 2 PASS.
- `build.sh` under MSYS2 CLANG64 exit 0. The local `out/bb-probe.exe` is SHA256 `598d4616b9de54c612e69daf34917c9c51ba214d4794fb0f14b5b9196fed6539`. This is a local build, not the original machine's `6696d7d3…`.
- Test DLL: the frozen B06 `ordered-dll/bbsc.dll` (`faf8227f…`), with the archived baseline injector and notices. The locally built DLL was not used for this run.
- Profile: a new isolated copy under the ignored `.superpowers/claude-r03/reload`. Its savedata is byte-exact to `native/after-b-savedata`, checked per file before launch. Settings: offline, 30 FPS, upscaler off, skip intro. No original profile was used.

## Native run

- PID 38768. The mod log shows the image verified with 52 patch writes, `Bloodborne RE trace installed 160/160 hooks`, and the boss-clear and Dream install lines.
- Title → Play Offline → Load Game. The list showed U-I-AHH (level 10, Iosefka's Clinic) as the latest character; it was selected and confirmed at 21:31:30.
- **Early** (21:31:39, first read with loading byte 0):
  - map `0x18010000`, lamp 2412950;
  - position (-190.181320, -50.627991, 170.588699), heading 0.065716, identical to the journal origin;
  - flag groups differ from the prejoin baseline at 12415461 and 12415770-12415773, and at all six B06 `12705` bits.
- **Settled:** the visible world was confirmed by screenshot (21:31:52). Six further snapshots were taken at 21:32:24, 21:32:44, 21:33:05, 21:33:26, 21:33:46 and 21:34:07. **Every one equals the prejoin baseline in all 1250 groups** (compare result `{}`). The final position, lamp and map are still identical to the journal origin.
- No input after the load, no party, no movement.
- The window was closed with CloseMainWindow; the process exited (WaitForExit true) and no bb-probe remains. The protected after-b savedata is unchanged (per-file hashes).

## Result

The six `12705` bits from B06, and five `12415` bits, are **early-load transients**. They are present right after the loading byte clears and gone within about 45 s. The settled independent reload of the co-op after-save is exact to the prejoin world, and the position is exact to the accepted origin. Together with B06's immediate-return exact match and its no-party control, this closes the "classify six reload bits and independent candidate reload" item. It does not address the other open items:

- joint earning;
- first-playable / party epoch;
- history exclusion;
- C3 / G2-17 live reorder.

Snapshots taken at loading 0 are not settled state; take acceptance snapshots after the visible world plus at least one stable repeat.

Private evidence (ignored): `.superpowers/claude-r03/reload/` contains early/settled world and position JSON, deltas, screenshots, the mod log, the RE capture and the per-file hashes of the after-b copy. Next: an actual joint boss kill with two accounts on the self-hosted server (TCP 31313/31315/20443/20444 reachable from this PC; WebAPI summon route answers), which needs a gameplay window with the owner.
