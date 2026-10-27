# R03 B17: durable origin after a guest crash, bound to its owner

2026-10-27, Claude (R03 takeover). **Base:** seamless `c06819d` (with PR #10 and PR #11). The source change is in the tracked patch (`bloodborne_re.cpp`). Matrix: G2-08 (interruption below 10 s) and the B16 case 2 origin GAP. A02 is the cross-character failure that kept the return behind an opt-in.

## The gap

In B16 case 2, the guest's game closed 5.8 s after the summon. After the restart, its own flags were back: 0 differences in 1250 groups between the named snapshots. But it woke **in its own world at the host's spot**: a level-10 Clinic character in Cathedral Ward. The game's own save during the visit holds the summon placement.

The return to the journaled home spot already existed (R02). It only ran with `SHADPS4_BBSC_EXPERIMENTAL_HOME_RECOVERY=1`, because in A02 a pending return crossed from EiEi to Kaori after Quit Game → title → Load. The quit hook that should have dropped it was not seen on that path.

## Change

The return runs **by default**. Three guards bind it to its owner and to a bounded outcome. Without those guards, enabling it by default would be no more than flipping the switch.

**1. Owner-bound arming (unchanged, now relied on).** The return is armed only from `RecoverBbscOwnWorldFile`. That runs only when the journal's save slot is the active slot (PR #11: owner = save slot, confirmed after the slot's save is written).

**2. A load from the title drops it.**
- `NoteBbscOwnWorldCharacterLoad` (PR #11's title hook, `Warp.StageDescriptor.Finalize` rdi 0) now calls `SuspendBbscHomeRecovery()`. The in-memory state is cleared and the journal file stays on disk.
- The owner takes the return up again the next time it is home: `TickBbscOwnWorld` → `RecoverBbscOwnWorldFile`, as before.

**3. Every step checks the owner.**
- `TickBbscHomeRecovery` reads `BbscActiveSaveSlot()` before any warp or settle.
- If the slot is unknown (right after a load, until the game saves), it waits.
- If another slot is loaded, the return is dropped and the file kept.
- So even if a title load is missed, nothing reaches another character. That was A02's hole: the other character's title load was accepted as "the return's load".

**Bounded fallback.**
- The order is unchanged: the journaled point first, then the recorded lamp if the arrival is more than 5 m off.
- New: an unsupported target (no lamp recorded), or 5 unaccepted requests (`BbscHomeRecoveryMaxTries`), ends the return.
- `SettleBbscHomeRecovery(false)` keeps the own world, renames the journal to `.restored`, and tells the player to travel from a lamp.
- Before this change such a return stayed pending forever, retrying every 2 s.

**Refactor.** The recovery's part of the `Warp.RespawnPoint.Resolve` hook is now `NoteBbscHomeRecoveryLoad()`, unchanged in behaviour, so the fixture can call it. Arrival settle and give-up share `SettleBbscHomeRecovery`.

**Opt-out.** `SHADPS4_BBSC_HOME_RECOVERY=0`.

**Not changed:**
- `SHADPS4_BBSC_EXPERIMENTAL_HOME_RECOVERY` still gates only A04's native-join admission guard (`ProtectBbscNativeJoin`).
- The graceful trip home (`PutBbscHomeSpot`, B16 case 1).
- No packaging and no deployment.

## Fixture

`test_bbsc_home_recovery.py` compiles the actual code with ASan: everything from `struct BbscHomeSpot` through `NoteBbscHomeRecoveryLoad`, plus `NoteBbscOwnWorldCharacterLoad`. It uses the real `bbsc_home_spot.h`, a real journal file, and controlled memory and save slot.

Scenarios:
1. **B16 case 2, defaults.** The return is armed and asks for the Clinic spot. After the warp load it waits while the slot is unknown, then settles: the journal becomes `.restored`.
2. **A02.** Return asked, then a title load, then Kaori is loaded on the same map. No further warp, the U-I-AHH journal is kept, nothing is settled.
3. **A02 with the title load missed.** The other character's load is accepted as the return's load. The active-slot check drops it at Kaori's first step: no lamp warp, file kept.
4. **Another load before the return (a death).** The return is dropped and the file kept. A later arming asks again.
5. **No way back** (point refused, no lamp). After 5 requests the return gives up once: settled, the player told.
6. **Opt-out `=0`.** Nothing is armed.

**RED/GREEN**, by mutating copies of the actual source in `.superpowers/claude-r03/b17/`:

| Mutation | Result |
|---|---|
| The old gate (`EXPERIMENTAL...=1` only) | RED at scenario 1: not armed by default. This is the B16 GAP. |
| Both owner guards removed (title drop and slot check) | RED at scenario 2: A02. |
| Only the slot check removed | RED at scenario 3: a missed title load reaches Kaori. |
| Only the title drop removed | GREEN: the slot check alone covers it. Both are kept as defence in depth. |
| The try limit removed | RED at scenario 5: it never gives up. |
| Current source | GREEN |

`test_bbsc_own_world_owner.py` gained a `SuspendBbscHomeRecovery` stub, because `NoteBbscOwnWorldCharacterLoad` now calls it. Its scenarios are unchanged.

**Union** (seamless `c06819d` + this change, CLANG64 Python, clang64 on PATH):
- All 8 `test_bbsc_*` modules: 9 tests OK.
- With `test_patches`, `test_native_bbsc` and `test_run_bbsc`: 32 tests OK, 1 skip (a patches case).

PR #12 (B15 rev 2) is a separate branch. The two changes touch different functions. The composed union is to be run when the second one rebases.

**Hashes:**
- Patch: `520125e83b15b075fa5aa8f145c9d262bcfa14cb3a42e7331e7e93023abff34e`.
- LF source: `53415c39cd5d59b71f407aca8b0c0a02ec27479a135a9d551cbc350093b2fb3e`.
- `bbsc.dll` (`tools/build_bbsc_mod.py`): `0a9ddf062e537bf6e30e7953e43a0a8a65f7caf20ecbc2462490002c1d41807a`.

## Native: NOT run here (needs the friend's side)

**Why not here:** the R03 rule keeps long two-instance native runs out of this session. These cases also need a guest killed within seconds of placement and, for A02, menu steering through Quit Game → title → another character. B16 case 2 is the only setup that reached that state, and it took a full rig session.

Defaults throughout, with the DLL above, spectate off, copied profiles, host Kaori, and guest U-I-AHH (level 10, Clinic).

**N1. B16 case 2 again.**
1. Join. Within 10 s of `placed`, kill the guest process.
2. Restart the guest and load U-I-AHH.

Expected in the log:
- `was left with another player's world in it`;
- `home recovery: user sd1 slot 3 goes back to 0x18010000 (where it joined)`;
- `requested original point into 0x18010000`;
- `own world and return point settled`.

Then compare: the position read is within 5 m of the journaled spot, on map 0x18010000. Flags are S1-equal apart from B07's transients.

**N2. A02.**
1. Repeat N1 up to `requested`.
2. Before the arrival, or during the return's 2 s window, Quit Game to the title and load **another** character (EiEi or Kaori in profile a).

Expected:
- `a character is loading from the title`;
- the other character neither warps nor gets `settled`;
- no flag difference against its own baseline;
- `own-sd1-3.bin` still on disk.

Then load U-I-AHH again. Expected: it returns as in N1.

**N3. Opt-out.** With `SHADPS4_BBSC_HOME_RECOVERY=0`, N1 behaves as in B16: no warp.

**N4 (optional). Lamp fallback.** If a journaled point is unreachable (more than 5 m off after the load), expect `recorded lamp`. If neither the point nor the lamp works, expect `home recovery gave up` and the notice.

## Limits

- Fixture evidence only. The game-side warp and the title hook's timing are as natively observed in B11, B14 and B16, not re-run for this change.
- `ProtectBbscNativeJoin` (A04) stays opt-in.
- An interruption before the journal's first write is unchanged: there is no journal and so no return. The A04 guard covers that only when it is on.
