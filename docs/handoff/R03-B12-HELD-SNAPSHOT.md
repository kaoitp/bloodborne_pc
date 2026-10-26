# R03 B12: native delayed older snapshot (G2-17 / CL03 C3)

2026-10-26, Claude (R03 takeover). Base: B11 branch (PR #7, not merged yet); first built on `e4e0f8c`, rebased onto the PR #7 review fix `2522e2f` (rebased DLL `e2f9ebde…`, fixtures OK). The native runs below used the pre-fix builds with the spectate option on, where the fix changes nothing. Source change in the tracked patch (`bloodborne_re.cpp` only), a default-off test seam. Same native setup as B09-B11:
- two online copied clients on the owner's self-hosted server;
- fresh copies of the protected Kaori host and U-I-AHH guest saves;
- shared progress ON;
- the disclosed debug aids (position write, HP-0 after the native boss bar, the guest's and host's own HP 0).

## Change: the CL04 A-37 seam

A live run never delivers an older world snapshot after a newer one, because the relay keeps the host's order. So the B06 receiver's ordering guard had only fixture evidence.

- `SHADPS4_BBSC_TEST_HOLD_WORLD=<ms>`, **default off**, read once.
- While the file `bbsc-test-hold-world` exists in the game's working directory, the next world snapshot (not the Hunter's Dream state) is held back, all chunks.
- If the file holds a packed map in hex (e.g. `18000000`), only that map's snapshot is held.
- Once `<ms>` have passed and a newer snapshot of that map is complete, the **same bytes go to the actual receiver** again, as a reordering network would deliver them.
- One log line reports the result: held and newer snapshot counters, the snapshot the cache kept, and how many bits the held one differs by. If the older one replaced the newer one, the line says so.
- Deleting the file arms the next hold.
- The receiver itself is unchanged; it is renamed `ReceiveBbscWorldFlagsPacket`, and `OnBbscWorldFlagsPacket` forwards to it when the switch is off.
- No protocol or storage change.

## Fixtures

- `test_bbsc_reorder_collect.py` adds a second binary (`-DHOLD`) that compiles the seam with the actual receiver and the actual collector:
  - the trigger file names map `18000000`;
  - snapshot 41 (an old bit `0x40`) is held after placement;
  - the host sets `0x80` in 42;
  - 43's first chunk releases 41 after the hold time.
  - Checks: the cache keeps 43, only `0x80` is collected, and deleting the file resets the hold.
- **RED** with the B06 guards removed (both the completed-snapshot check and the assembling check): both the direct test and the seam test fail. **GREEN** with them.
- `test_bbsc_world_ordering.py` now extracts the renamed receiver (no behaviour change).
- `test_bbsc_*`: 6 OK; `test_native_bbsc`: 2 OK.
- DLL builds: seam `565dfddc…` (run 1), with the map filter `6ee4cac6…` (run 2). Both exit 0.

## Native evidence

**Run 1** (seam without map filter, guest `SHADPS4_BBSC_TEST_HOLD_WORLD=15000`):
- The trigger file was created 2 s before the HP-0 kill. The first snapshot to arrive was of another block, `0x1b000000` (snapshot 492).
- 11:00:44 `snapshot 492 of map 0x1b000000 (5 chunk(s)) fed again 16256 ms late, after snapshot 524; the cache keeps snapshot 524 (0 bit(s) differ from the held one)`.
- So the seam works natively, but this held snapshot did not differ. That is why the map filter was added.
- The kill, reward and merge were as in B09: reward `lot 50000001 finished for user sd1 slot 3`, merge 2 boss + 19 world flags.

**Run 2** (map filter, fresh save copies, same switch):
- Joined at 11:14:23 (Clinic guest to the Cathedral Ward host), baseline 12 flags / 160 groups.
- Amelia's boss bar was up. The trigger file was written with `18000000`.
  - 11:17:24.0 `holding back snapshot 472 of map 0x18000000`.
  - HP 0 at 11:17:25.4.
- The kill as usual:
  - 11:17:26 / 11:17:33: 5 + 4 world flags collected;
  - 11:17:32.6: `boss event 12401800 earned in this party`; the reward was queued and finished for sd1 slot 3;
  - 11:17:36: 2 boss flags;
  - 11:17:37: `BlockClear2_1`, session kept.
- **11:17:39.1:** `snapshot 472 of map 0x18000000 (5 chunk(s)) fed again 15129 ms late, after snapshot 500; the cache keeps snapshot 500 (9 bit(s) differ from the held one)`.
  - 9 is also the count of world flags collected after the hold started (5 + 4); the per-bit match was not checked. So a pre-kill snapshot without the kill's bits reached the actual receiver after the post-kill one, and was dropped.
- Departure (Parting Blank, 11:21:27): merge **2 boss + 19 world flags in 3 groups**. That is the same as B09 and run 1 without a reorder, so nothing extra was collected and nothing was lost.

**No in-party load after the kill.** The plan was to also reach `ApplyBbscHostWorldFlags` through a load after the reorder (CL04 A-37 step 3). This rig gives no such load:
- The guest's death outside a boss fight is a `respawn in place (no boss fight)`, without a reload (11:14:53, 11:18:12).
- The host's death is also a respawn at the lamp without a reload ("The host died. They will respawn at the lamp.", reinsert v8 kept death).
- Lamps cannot be used while a cooperator is in the world, so the host cannot travel and pull the guest along.

The live apply after a reorder is therefore **not exercised natively**. It reads `bbsc_world_blocks`, the same cache that run 2 shows kept the newer snapshot.

All protected source saves are unchanged: no file under `r03-b06/native/after-a-savedata` or `before-b-savedata` was modified today. All test processes were closed and the trigger file was removed.

## Review fix: diagnostic bounds (PR #8 review, P2)

**The problem.** After the late feed, the seam compares the held snapshot with the cache. That comparison looped to `chunk.group_count`, which is the sender's word, while a packet holds only 8 groups (`BbscWorldChunkGroups`). So a held chunk claiming 9 or more read past `groups`. The actual receiver was not affected: it already clamps the count. The issue only arises with the default-off switch.

**The fix.** The comparison now applies the receiver's own bounds:
- It skips a chunk the receiver drops (wrong `chunk_count`, or a chunk index out of range).
- It compares at most `min(group_count, BbscWorldChunkGroups, BbscWorldGroupCount - first)` groups.

**Fixture.** In `test_bbsc_reorder_collect.py`, the held snapshot 41 now claims 255 groups in every chunk, and the seam binary is built with `-fsanitize=address`.
- **RED** with the old loop: ASan reports `stack-buffer-overflow` in `OnBbscWorldFlagsPacket`.
- **GREEN** now, with the same asserts as before: the cache keeps 43 and only `0x80` is collected.
- Results: `test_bbsc_*` 6 OK, `test_native_bbsc` 2 OK, `git diff --check` clean.
- DLL build `f14d8481…`, exit 0.

## Status after B12

| Case | Result |
|---|---|
| G2-17 / C3 (older snapshot after a newer one) | PASS (native injection through the actual receiver: 9-bit pre-kill snapshot dropped, cache kept the newer one, merge unchanged); fixture RED/GREEN |
| G2-17 live apply at a load after the reorder | Not exercised: no in-party load in this rig (deaths respawn in place, lamps disabled in co-op) |
| G2-03 kill before placement | Unchanged from B11: gate + fixture; native window not reproducible |
| Guest in a follow load at the kill | Unchanged: not tested (needs a host travel during co-op, which the game blocks at lamps) |
| Progress beyond bosses | Unchanged from B11 |

Private evidence (ignored): `.superpowers/claude-r03/coop7-run1` and `coop7` (mod logs, timelines, RE captures, screenshots), build logs `b12-build.log` and `b12b-build.log`.
