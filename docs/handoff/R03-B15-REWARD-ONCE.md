# R03 B15: a boss reward without a taken flag is given once per character

2026-10-26, revised 2026-10-27 four times after the PR #12 reviews. Claude (R03 takeover).

**State:** an **experimental opt-in, default OFF**, enabled by `SHADPS4_BBSC_REWARD_ONCE=1`. Without the variable the existing behaviour stays: once per event and character within a process, and nothing on disk. See the open gate under Limits.

**Base:** seamless `e7d0bc7`, with PR #10, PR #11, PR #13 and PR #14 merged. The source change is in the tracked patch (`bloodborne_re.cpp` only). Matrix rows G2-07/11/12 (reward deduplication) and G2-19 (deferred ownership).

## Revisions

- **Revision 2 (review 1).**
  - Rebuilt on the PR #11 union. The first branch, `7bed9e6`, started before PR #11 was integrated.
  - The record became save-confirmed. It had been written at the grant, 26 s before the save.
- **Revision 3 (review 2).** The revision 2 line was written before the add, and only memory knew whether the add had worked. A failed add, then a save, then an exit, therefore blocked the lot. Revision 3 moved the only line to after the add.
- **Revision 4 (review 3).** Revision 3 lost the confirmation while the record was unwritable. A successful add, a failed write, a save and an exit therefore gave the lot again. Revision 4 has:
  - an attempt line before the add, with no add if it cannot be written;
  - the outcome written at once after the add, whether it failed or succeeded;
  - an unknown outcome held at the next start, never given again and never called given without evidence.
- **Revision 5 (review 4).** One case is a held obligation that can never resolve itself: an add that **failed**, a removal that could not be written, then a save. That leaves the same bytes on disk as a delivery that worked and was used up. Nothing in the game or the save tells the two apart yet, so the record is now an **experimental opt-in** (`SHADPS4_BBSC_REWARD_ONCE=1`, default OFF):
  - the default keeps the existing behaviour, so there is no new permanent reward blocker;
  - under the opt-in, the held entry is neither given again nor dropped;
  - its log line names the file and the `attempt` line a person removes to release a reward that was never delivered.

## The gap

`BbscBossRewards` has two kinds of rows:
- **With a taken flag**, for example the Cleric Beast's badge (6645). The game's own rule applies: once the flag is set, the repeat lot is used.
- **Without a flag (flag 0).** Ten rows, including Amelia's Gold Pendant, Rom's and Mergo's Wet Nurse's One Third of Umbilical Cord, Micolash, and Gascoigne's area. Nothing in the save says the lot was given.

For flag-0 rows, the only guard against a second delivery was the in-memory `bbsc_boss_reward_given`, which ends with the process. A guest that restarted could therefore get a second Gold Pendant from a later joint kill.

## Change

**Rows covered.** `BbscBossRewardOnce(event)` is true for rows with flag 0, and only with `SHADPS4_BBSC_REWARD_ONCE=1` (`BbscBossRewardOnceEnabled`; the start settle also does nothing without it). Flagged rows are unchanged: the game's taken flag decides.

**Record file.** Per save slot, in `<mod>/boss-rewards/given-<user>-<slot>.txt`, written by an atomic temp-file rename through `SetBbscBossRewardLine`. Lines:

| Line | Meaning |
|---|---|
| `attempt <event> <time>` | Written **before** the add. If it cannot be written, the entry stays queued and **no item is given**. A delivery therefore always has a line on disk. |
| `granted <event> <time>` | The add worked. Replaces the attempt and is written at once after the add. |
| *(none)* | The add failed. The attempt is removed at once after the add. |
| `<event>` | The owner's save file (`BbscSaveSlotWritten`) was written after the grant: final. This is the v1 form. |

**Retries.** The process knows each outcome. If the outcome write fails, it is retried every second (`bbsc_boss_reward_unsaved` with its `recorded` mark, and `bbsc_boss_reward_unclaimed`). Meanwhile memory decides:
- a successful add blocks a second lot;
- a failed add allows a retry.

**Next start (`SettleBbscBossRewardsAtStart`).** This runs at the end of `InstallReverseEngineeringTrace`, before the game can write a save:

| Line | Owner's save not written after `<time>` | Save written after `<time>` | Save not readable |
|---|---|---|---|
| `granted` | Line goes; the lot can be earned again | Given (kept or used since) | Stays; waits |
| `attempt` (outcome not on disk) | Line goes; the lot can be earned again | **Held**: the outcome is unknown. The event waits. | Stays; waits |

**Held attempts.** The tick settles a held attempt as given when the lot's goods are in the owner's carried items (`BbscInventoryHas`). Otherwise it keeps waiting. It is never given again and never called given without that evidence. The warning names the file and line to remove when the reward was never delivered (**manual release**).

**When an attempt can be held.** An attempt line can outlive its outcome only if the record breaks, or the process dies, between two writes a moment apart: the attempt, then the outcome right after the add. If the record is unwritable before the add, nothing is given. That covers the review 3 case.

**Queue and tick checks.**
- `NoteBbscBossRewardEvent` does not queue an event the character already has.
- The tick skips it.
- An unreadable record waits.

**Original owner.** The owner stays bound to the queued entry and to its slot's record.

**Limits (honest).**
- **OPEN protocol gate: held without evidence.** If the add worked and the item was then used up, or the add failed but its removal could not be written, the attempt stays held. Both need the record to break in the moment between the two writes. These two cases cannot be told apart from the record, the save time or the inventory.
  - Until game or save evidence can separate them, the feature stays opt-in.
  - A held entry is resolved by its goods being seen, or released by hand through the logged line.
- **In-flight save, unproved natively.** A save the game had already begun before the add, but finished after `<time>`, counts as written after it. A file time does not prove the inventory snapshot.

## Fixtures

`test_bbsc_reward_once.py` compiles the actual functions with ASan, from `struct BbscBossRewardPending` through `NoteBbscBossRewardEvent` and `TickBbscBossRewards`. The record file is real. The save write time and the inventory are controlled.

**Restart model:** clear the memory lists, then run the real start settle.

Scenarios, all kept from earlier revisions plus the review 3 cases:
- First grant: `granted`, then final after the save.
- A fresh process does not queue, and skips an old queued entry.
- A second kill before the save gives no second lot.
- Another character gets its own reward.
- A flagged row is unchanged.
- An unreadable record waits.
- Exit before save: given again.
- Saved, final write blocked, item used up, restart: no second lot.
- An unreadable save at start waits.
- **Review 2:** failed add → save without the item → exit (no tick in between) → healthy kill: given once.
- **Review 3 (slot 13):** record unwritable at the kill, then a save, the counter rolled back, a restart while still unwritable, then the record writable, then another kill.
  - The first kill **gives nothing** (no line, no item).
  - The kill after the restart gives it **once**.
  - A further restart and kill: never again.
  - Against the old revision, the same steps give the item a second time.
- **The record breaks between the attempt and the outcome** (the add worked):
  - In the same process: no second lot.
  - Saved, used up, exit: held at the restart, and a kill gives no second lot.
  - Seen in the inventory: final.
- **The same break with no save before the exit:** the line goes, and the lot is given again.
- **Failed add:** no line, and the retry gives it once.
- **Review 4 (slot 15).** The add fails and its removal cannot be written, then a save, a restart while unwritable, storage back, a restart, and a kill plus 50 ticks.
  - The entry is **held**: no lot and no drop.
  - The logged manual release (removing the line) lets the next tick give it **once**, and it is then final.
- **Default OFF (slot 16).** Without the variable, no file is written. The reward is once per process and can be given again in a new process, which is the existing behaviour.

**RED**, by mutating copies of the actual source (`.superpowers/claude-r03/b15v5/red/`):

| Mutation | Fails at |
|---|---|
| `red-no-attempt-line` (revision 3: no line before the add) | `adds == before_unrecorded && record(thirteen).empty()`. Revision 3 gives while unwritable, then again after the restart. |
| `red-failure-written-later` (revision 2's deferred removal) | `adds == before_failed && record(eleven).empty()` |
| `red-held-dropped` (an outcome-less attempt treated as never saved) | `record(fourteen)` held. That is the duplicate path. |
| `red-default-on` (the record without the opt-in) | Slot 16: a file is written and the second process gives nothing. |
| `red-keep-unsaved` | `record(seven).empty()` |
| `red-drop-at-start` | `record(eight) == "12401800\n"` |

**GREEN:** the current source.

`test_bbsc_reward_delivery.py` has stubs for `BbscSaveSlotWritten`, `BbscCarriedInventory` and `BbscInventoryHas`. Its rows are flagged, so its scenarios are unchanged.

**Union** on seamless `e7d0bc7` + this change, CLANG64 Python:
- All 9 `test_bbsc_*` modules, including B17's `test_bbsc_home_recovery`: 10 tests OK.
- With `test_patches`, `test_native_bbsc` and `test_run_bbsc`: 33 OK, 1 skip.

**Hashes (revision 5):**
- Patch: `7871e606f8d2c90d59ae58abc02abd4456cf6b7e7075cef2c300ecfc16cc25cf`.
- LF source: `4a94e78ac2ca8a54b10c7ace0ba3cd44ce8787943c56c30bf73b94960557cbcf`.
- CRLF source: `ee21b5e71dee64b3c39dcda8107fd34c4e703676f5dade701f9f07220910aad2`.
- `bbsc.dll`: `908d5a1afe0209efc62bb441ead39eddbb6990ce69425b0c0e5d148ef2e4c96a`.

## Native evidence

### Revision 1 (pre-PR #11 composition only)

**Build:**
- DLL `e19397e80eebd0cd9dd2e8c4cc9de6599e94418ac2e953c4660814f4313aff82`.
- Patch `f4889473ad06b1322576ab7db8c3408bfb76cd270c7c7c16191c51cf73379f0c`.
- LF source `70ff36b4f4358635a8ed0e9761feaca1659fefff7ebb827463bee903687cbf8b`.

The build recorded the reward at the grant and had no PR #11 guards. It is an observation on that composition only.

**Configuration:** mod defaults, spectate off, self-hosted server. Host Kaori, guest U-I-AHH (sd1 slot 3).

**Rounds:**
- Round 1, 23:42:24: `goods 4001 x1 put into the carried items`, `lot 50000001 finished`. The guest's save was written at 23:42:50. That 26 s gap is the only native timing evidence behind the save-confirmation rule.
- Round 2, after both processes restarted: `already given ... not again`, and the inventory shows **Gold Pendant 1/1**.

### Revisions 2–5: NOT run natively (needs the friend's side)

**Why not here.** The user set this session's limit: no long two-instance native runs, because of token cost and because each instance needs about 17 GB of RAM on the user's gaming PC. In-game steps go to the friend's side.

The cases also need:
- a kill inside the add-to-save window (R4-N2);
- an unwritable record (R4-N3): read-only ACL on `<mod>/boss-rewards`.

**Steps:** copied profiles, the revision 5 DLL, `SHADPS4_BBSC_REWARD_ONCE=1` on the guest, other mod defaults, spectate off. R4-N0: without the variable, a restart and second joint kill gives a second Pendant (the existing behaviour, unchanged).

1. **R4-N1, normal grant.** Joint Amelia kill with a guest that never had the Pendant.
   - The file goes `attempt …` → `granted 12401800 <t>` (at once) → `12401800` (within about 30 s, with `is in the save … - final`).
2. **R4-N2, exit before save.** Fresh copy. Kill the guest right after `lot 50000001 finished`.
   - On restart: `never saved, can be earned again`, and no line in the file.
   - The next joint kill gives exactly one Pendant.
3. **R4-N3, unwritable record.** Make `<mod>/boss-rewards` read-only before the kill.
   - Expected: `record not writable, waiting`, and **no** Pendant.
   - Restore write access. Within a second the Pendant is given once, and R4-N1's lines follow.
   - Restart and kill again: `not again`.
4. **R4-N4, in-flight save boundary.** In R4-N1, compare the add's time with the first `userdata0003` write time after it. Record whether a save that began before the add could have finished after it.
5. **Optional, Umbilical Cord.** Use the cord, restart, kill again: no second cord.

### Checking the logs

`tools/check_r03_native.py` reads the guest's `bbsc-mod-*.log` files and prints each expected line with its time, then a verdict. Pass the files **in process order**, one per guest process. It starts nothing and only reads; `--user-dir` (the mod's user folder, which holds `boss-rewards/`) also checks the files on disk. Lines are ordered by their place in each file, not by their time, since consecutive lines often share a millisecond; times are only used for durations (wrapping past midnight). Every process's log is checked: for `b15-n3` a lot or an add in any process after the first fails; `b15-n0` takes exactly two logs and `b15-n1`/`b15-n4` exactly one, and another count is INCOMPLETE instead of ignored. A log PASS is not native acceptance: the position, flag and reload checks stay a person's.

```
python tools/check_r03_native.py b15-n3 p1/bbsc-mod-A.log p2/bbsc-mod-B.log --user-dir <mod user folder>
```

| Verdict | Exit | Meaning |
|---|---|---|
| PASS | 0 | Every automatic check passed. |
| FAIL | 1 | A line that must not appear did, or a count is wrong. |
| INCOMPLETE | 2 | An expected line is missing: the run may have stopped early. |
| MANUAL | 3 | The automatic checks passed; the rows marked `manual` are a person's check. |

Defaults: user `sd1`, slot 3, event 12401800 (Amelia), goods 4001 (Gold Pendant); `--event` and `--goods` change them. Its patterns are tested against the actual log format strings (`tests/test_r03_native_check.py`), so a changed message fails that test instead of the run. It has only been run on synthetic logs and on the revision 1 logs here, not on a native run of this revision. Cases: `b15-n0` .. `b15-n4`. R4-N4 always ends MANUAL: the log gives the add time and when the save was seen, and the in-flight question needs the `userdata` file times. Step 5 is not covered.

## Limits

- A consumed reward is not given again. The record, not the inventory, decides. This is covered in the fixture, not natively.
- Flagged rows were not exercised natively.
- The record is per mod folder.
- The two limits under Change.
