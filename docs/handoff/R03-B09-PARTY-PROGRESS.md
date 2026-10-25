# R03 B09/B10: only party-earned progress, kept until saved

2026-10-25, Claude (R03 takeover). Base: B08 docs on top of runtime `a43e26f`. Source change in `gpu/patches/bbsc/0001-profile-storage-and-clang64.patch` (`bloodborne_re.cpp` only). The mod-file hunks are unchanged; the patch is regenerated as `git diff` of the pinned reference.

## Demonstrated gaps

- **G2-01 (B08, native):** shared progress ORs everything the host has into the guest. In B08 that was 14 boss flags and 272 world flags of older host history, merged into a level-10 character.
- **Durability (found in the B09 native run):** the merge renamed the pending file `.merged` immediately after setting the live flags. The game writes those flags to the save only at its next save. The window was closed about 35 s after the merge, the flags were lost, and nothing re-merged them. B08 was saved by chance within its minute.

## Change

**B09, party baseline.** It sits in the existing collector, with no new protocol, storage or switch.

- **Party.** A party is the host whose packets we take (`BbscRelayHostForPackets`) plus a counter raised by `ClearBbscHostWorldSnapshots`. That function already runs when the relay lock is released after 5 s outside state 4/6, and when the lock moves away from a stale host. A new host or such a reset starts a new baseline.
- **Eligibility.** It opens at the first `bbsc_join_teleport_done` of the party (the guest is placed beside the host). It stays open through death and loading in the same party and closes only with the party.
- **Host boss flags (`0x26`).** Everything in the first packet of a party, and in any packet before eligibility, is baseline. Later flags not in the baseline are collected. The night flags follow the same rule, so the host's later night is no longer imported unless it moved during the party.
- **Kind-1 world groups.** The baseline is the first sight of each group key in the party plus everything before eligibility. While eligible, only bits that turn on later are collected. A block first seen after placement only becomes a baseline. That is conservative: it loses rather than imports.
- **Kill-time reward event.** When our own copy of one of the 19 boss reward events reaches its wait, while eligible and in the boss's area, its own flag bit (event ID = group key × 1000 + bit) is collected. B05 and B08 observed this signal firing at a real kill and not at a pre-killed load. `AdmitBbscRewardEvent` runs before `NoteBbscBossRewardEvent`, so it does not depend on guest items.
- **Pending file magic.** Changed from `BBSP` to `BBS2`. A legacy unfiltered file is rejected and left in place; this is the existing loader behaviour for a different magic.

**B10, merge kept until saved.**

- `BbscActiveSaveSlot` records the write time of the slot it finds (`bbsc_active_slot_written`).
- After a merge, the pending file stays as `pending-…bin` until that slot's save file is written later than the merge. Then it is finished (`.merged`).
- Until then the recovery path does not reload it in the same process.
- A new co-op session cancels the wait; its own collection owns the file.
- If the game ends before saving, the next time the character is home it is merged again. The merge only adds bits, so a repeat is harmless.

## Fixture evidence (actual functions, controlled dependencies)

- New `tests/test_bbsc_party_progress.py`. It compiles the real collector state, `TickBbscSharedProgress` and `OnBbscProgressPacket` from the prepared reference.
  - **RED** on the pre-change source: `Assertion failed: !has(2401) && !has(2200)`, the host's older flags were collected.
  - **GREEN** on the change: party baseline, flags/bits earned after placement, first-sight blocks, the reward event in and out of the boss area, death/load continuity, a new party after a lock reset, and a new host.
- `tests/test_bbsc_progress_backup.py`, now in the B10 contract. After a merge the file is kept until a save is simulated, and a no-save tick keeps it.
  - **RED** on the pre-B10 source: `Assertion failed: sets == 1 && finishes == 0 && pending_file …`.
  - **GREEN** on the change.
- Stubs for the new symbols were added to the existing ordering and backup fixtures.
- `test_bbsc_*.py`: 4 OK. `test_native_bbsc.py`: 2 OK.
- DLL builds: B09 `74524ca4…`, B10 `89138993…`. Both use `tools/build_bbsc_mod.py`, exit 0.

## Native evidence

All runs used two online copied clients on the owner's self-hosted server, the same protected before-saves as B08 (host Kaori after-a, guest U-I-AHH before-b), and BBSC defaults with **shared progress ON**. Amelia (12401800) was OFF on both before each run. The debug aids of B08 were used again: position write and HP-0 after the native boss bar.

**B09 DLL (22:33-22:42):**
- On placement the guest logged `only new progress is collected (baseline: 12 flag(s), 160 group(s))`. These are the counts B08 imported.
- At the kill the guest collected:
  - 17 world bits the host set during the fight;
  - `boss event 12401800 earned in this party`;
  - `the host set 2 boss flag(s) during the party`.
  - The reward was queued and finished for sd1/slot 3, then `BlockClear2_1` ran on both.
- Merge after the Parting Blank: **2 boss flags, 19 world flags in 3 groups**. B08 had 14 / 272 / 160 for the same scenario.
- The live guest diff against pre-join is only Amelia's progress (12400580-582, 12401800-804, 12404 boss-area bits, 2402, 9455, 9187). No older host bosses, for example no 12301800. The guest is at its exact origin and the Gold Pendant is still carried.
- **Host independent reload:** Amelia flags persisted; the host is at the arena. This answers the PR #5 review point.
- **Guest independent reload:** the Gold Pendant persisted. The merged flags were **lost**, because the window was closed before the game saved. That is the B10 gap above.

**B10 DLL (22:52-23:02):**
- Same join, baseline (12/160), kill and collection.
- Merge at 22:57:59 (2 boss, 19 world in 3 groups), then the window was closed at 22:58:00, before any save. The file stayed `pending-sd1-3.bin`.
- Fresh offline process: `2 boss flag(s) and 3 world group(s) from the file … (an earlier session that did not get home)`, merged again at 22:59:17 with the same counts.
- Quit to title saved slot 3 at 22:59:57. The tick doesn't run at the title. After Continue the game wrote the save at 23:01:35, BBSC logged `the game saved the merged progress - done`, and the file became `.merged`.
- The loaded save has 12401800 = 1 and 2402 = 1. Its diff against pre-join is only 12400580-582, 12401800-804, 2402, 9187 and 9455. The 12404 boss-area bits are not in the saved state, as in B08. Inventory shows the Gold Pendant, 15535 Echoes and Insight 1. Origin exact.

The protected source saves are unchanged. All test processes were closed; no game is running.

## Result

| Goal / case | Result |
|---|---|
| G2-01 older host history excluded | PASS (native, one boss scenario, fixtures for the rules) |
| G2-02 joint boss kept by both after their own reload | PASS for this scenario: host reload (B09), guest reload after save (B10) |
| G2-20 positive / reward to original owner | PASS (again) |
| Crash/close between merge and save | PASS: re-merged from the kept file, then finished after the save |

**Not covered:**
- C3 live reordered input (G2-17);
- same-host rejoin under 5 s and host character change in the same process (G2-22 d/g);
- dead or loading guest at the kill;
- a block first seen after placement losing a joint change;
- NPC or other world progress beyond this boss;
- the 12404 boss-area bits that the game itself does not keep.

Custom managed admission flags are still not involved; shared progress stays on its existing switch.
