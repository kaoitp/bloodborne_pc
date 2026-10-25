# R03 B11: party boundaries, dead guest, pre-placement rewards

2026-10-26, Claude (R03 takeover). Base: seamless `4492dd5` (B09/B10 merged). Source change in the tracked patch (`bloodborne_re.cpp` only). Same native setup as B09/B10:
- two online copied clients on the owner's self-hosted server;
- fresh copies of the protected Kaori host and U-I-AHH guest saves;
- shared progress ON;
- the disclosed debug aids (position write, HP-0 after the native boss bar, and now the guest's own HP 0).

## Changes

1. **Leaving ends the party.**
   - Native evidence: B08 showed session state 6 holding through the guest's death and the whole wipe reload, and changing only at a real departure (6→7→0).
   - `TickBbscSharedProgress` now raises the existing party-reset counter on any 6→not-6 transition.
   - This covers what the 5 s relay-unlock rule did not separate (CL03 C4 / G2-22): a rejoin to the same host before the unlock, and a host that quits and comes back with another character under the same relay id.
2. **Reward item only after placement** (CL02 A-27 / G2-03 contract). `NoteBbscBossRewardEvent` now also requires `bbsc_join_teleport_done`. A boss whose wait reaches the guest during its join load is logged `before we were placed in the host's world - not ours` and not queued. The flag holds through death and loads in the session, and is set again after a rejoin.

## Fixtures

- `test_bbsc_party_progress.py` adds a scenario: the guest leaves and rejoins the same host while the relay lock is still held. Flags the host gained in between are history, and earlier collected progress is kept. **RED** on the B10 source (`!has(2601)` fails). **GREEN** now.
- `test_bbsc_reward_delivery.py` adds a scenario: a reward event before placement is not queued. **RED** on the source before this gate (`queue.empty()` fails). **GREEN** now.
- `test_bbsc_*`: 4 OK. `test_native_bbsc`: 2 OK.
- DLL builds: departure rule `539b96a7…`; with the reward gate `89b4043e…`. Both exit 0.

## Native evidence

**Dead guest at the kill** (B11 DLL, 23:52-00:00):
- After the boss bar, the guest's HP was set to 0. `PartyGhostDeath` at 23:56:41, then spectating (`watch camera`).
- Amelia was killed while the guest was dead. At 23:56:55 the guest logged `boss event 12401800 earned in this party`, and the reward was queued.
- At 23:57:00 `the host set 2 boss flag(s) during the party`; boss clear with `the spectating player respawns`.
- Death penalty: the 15000 kill echoes were given back, and only the 535 held at death went into the bloodstain.
- Respawn in place at 23:57:03. The reward (`lot 50000001 finished`) was delivered **after** the respawn: the B02 delivery waits for a living character.

**Leave and rejoin the same host** (same session):
- Parting Blank, then merge at home (2 boss flags, 20 world flags in 3 groups). B10 finished it as soon as the game saved (23:58:37).
- Kin Bell again. At 23:59:00 `new party (host cf224863) - the baseline starts again`. Placement baseline: **14 flags** (the 12 older ones plus Amelia's 2, now history).
- Second Parting Blank at 00:00:16: `home again, nothing from the host to merge`.
- The rejoin took about 11 s, so the relay lock had also been released. The under-5 s case is covered by the fixture only.

**Host quits and returns with another character** (G2-22 g, reward-gate DLL, 00:03-00:16):
- The host quit to title at 00:07:57. The guest was sent home (state 6→0 at 00:10:30) to its **exact origin**; this is also a host-loss return. Its merge (Amelia) was finished once the game saved (00:13:32).
- The host loaded **EiEi (level 55) in the same process**. No GPU crash this time; B05 had hit PM4 errors here.
- The host rang again and the guest rejoined. The relay id was unchanged (95a5a909, as CL03 B-31 predicted), but the guest logged `new party`, and EiEi's history was the baseline (16 flags).
- Leaving: `nothing from the host to merge`.

**G2-03 attempts (kill before placement): not reproduced natively.**
- In both attempts the external HP-0 write landed during Amelia's opening sequence, and the host only processed the death after the joining guest had arrived.
- Second attempt: guest placed at 00:20:59; host `ForceSummonSuccess` trace hit=1 at 00:21:04.6; guest reward event at 00:21:04.7; host `BlockClear2_1` at 00:21:09. In game order the kill came after placement, so the admission was correct.
- The pre-placement window was not hit. The gate and the latch are covered by fixtures; B05's pre-party negative stands.

**CL03 B-30 settled:** the trace site labelled `ForceSummonSuccess` (`0x013849A0`) fired at the boss kill (hit=1 at 00:21:04.6, just before the guest's reward event and the host's `BlockClear2_1`). It is the BlockClear2 entry, as the source comment says.

**G2-17 / C3 (stale or reordered host data):**
- The collector admits only 0→1 bits against its party baseline.
- Host flag packets are whole-state, so a delayed older packet is a subset and admits nothing.
- The only harmful input would be an older snapshot carrying a since-cleared bit. B06's receiver rejects older completed and partial snapshots per map (actual-function fixture), and the collector reads only that receiver's cache.
- New `tests/test_bbsc_reorder_collect.py` compiles the **actual B06 receiver together with the actual collector**. History snapshots arrive (one with a transient bit), the guest is placed, the host sets a bit, and then delayed older snapshots arrive: one with an old bit, and a stale copy of the transient one. Only the party bit is collected.
  - **RED** with the B06 ordering guard removed: `collected() == 0x80` fails, because the old bit was collected.
  - **GREEN** with it.
- **Not done:** the default-off native injection seam (CL04 A-37), so there is still no native injection proof.

All protected source saves are unchanged. All test processes were closed.

## Status after B11

| Case | Result |
|---|---|
| G2-01 history excluded (B09) | PASS (native) |
| G2-02 joint boss kept after own reloads (B09/B10) | PASS (native, Amelia) |
| G2-04/G2-18 death in the same party | PASS (native, dead at the kill; earlier wipe kept the session) |
| G2-22 (d) rejoin same host | PASS (native, about 11 s; under 5 s by fixture) |
| G2-22 (g) host character change | PASS (native) |
| G3 host-loss return | PASS (native, exact origin) |
| G2-03 kill before placement | Gate added and fixture GREEN; native window not reproducible with this rig |
| G2-17 / C3 | Actual receiver + collector fixture RED/GREEN; native injection not done |
| Guest **loading** (follow load) at the kill | Not tested |
| Progress beyond bosses (doors, lamps, NPCs) | Kind-1 bits are collected only when they turn on in the party; kinds 5/6/7 (items, NPC states) are never merged, so guest NPC choices stay its own. Not exercised natively beyond the boss area |
