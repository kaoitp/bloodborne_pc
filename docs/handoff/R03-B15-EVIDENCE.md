# R03 B15: game evidence for a held reward (failed add vs used-up delivery)

2026-10-27. Claude (R03 takeover). Static research only: game data from the dump and the BBSC source. No game run and no code change.

## Question

B15's open protocol gate (`R03-B15-REWARD-ONCE.md`, Limits) concerns one record state: an `attempt` line with no outcome, followed by a save. The record cannot tell whether:
- the add **failed** and its removal was never written, or
- the add **worked** and the item was later used up.

The question is whether anything in the game or the save tells the two apart, row by row.

## Method

**Data.** Taken from the game dump `E:\Bloodborne-Dump\CUSA03173\dvdroot_ps4`:

| File | sha256 |
|---|---|
| `param/gameparam/gameparam.parambnd.dcx` | `581e2830...60c3` |
| `paramdef/paramdef.paramdefbnd.dcx` | `8a3f7ffe...2296` |

**Parsing.** Each archive goes DCX (DFLT/zlib) → BND4 → `EquipParamGoods.param` with its `EquipParamGoods.paramdef`, which has 88 fields.
- Field layout: 108 bytes per row. It matches the spacing of the row data, with `dummy8` bitfields packed into the `u8` groups.
- Names come from the English item name and description FMGs.
- Two readings confirm the parse:
  - Gold Pendant (4001) has `isConsume` 1, and its description says "Use to change into a blood gem".
  - Third Umbilical Cord (4323) has `isConsume` 1, `isDrop` 1 and `isOnlyOne` 1.

**Source facts** (`bloodborne_re.cpp`, pinned 4f11faf + the tracked patch):
- `GiveBbscBossGoods` sets the goods lot's **get flag** (`BbscBossGoodsLots[].flag`) right after an add that worked (`there`), and only then. A failed add never sets it.
- Flag group key = flag / 1000. The own-world journal holds only map groups (`BbscIsMapFlagGroup`: kind 1/5/6/7, area 21–99).
  - Groups outside that set are never journaled, so the trip home does not put them back.
  - Kind 5 map groups (item pickups) are put back by OR: a bit set during a session is never cleared.

## Rows without a taken flag (the rows B15 records)

| Event | Lot | Goods | Consumed on use | Can discard | Get flag (group) | Evidence |
|---|---|---|---|---|---|---|
| 12201800 | 21002950 | 7150 Bloodshot Eyeball ×4 | yes | yes | — | **none** |
| 12301800 | 80000000 | 6109 Pthumeru Chalice | **no** | **no** (storable) | 5000 (key 5, global) | **decisive**: get flag, and the chalice in the carried items or storage |
| 12401800 | 50000001 | 4001 Gold Pendant (Amelia) | yes (into a blood gem) | no (storable) | — | **none** |
| 12411800 | 31000 | 4000 Oedon Tomb Key | flagged yes, see below | no | — | **none** confirmed |
| 12421800 | 80000300 | 6539 Great Isz Chalice | **no** | **no** (storable) | 5009 (key 5, global) | **decisive**, as for 12301800 |
| 12601800 | 55100000 | 4323 Third Umbilical Cord | yes | yes | 50000305 (key 50000, global) | **get flag only** |
| 12601850 | 21000 | not a goods lot (native award) | — | — | — | **none**; the award has no success signal |
| 12801800 | 50700000 | 7131 Yellow Backbone ×3 | yes | yes | — | **none** |
| 13201800 | 51001900 | 1591 Kin Coldblood (12) | yes | yes | — | **none** |
| 13301800 | 80000200 | 6429 Ailing Loran Chalice | **no** | **no** (storable) | 5006 (key 5, global) | **decisive**, as for 12301800 |
| 13501850 | 3501850 | 4020 Astral Clocktower Key | flagged yes | no | 53501850 (key 53501, kind 5 map group, area 35) | **get flag, less certain**: set in the host's live table during the session, then OR-restored at home (untested) |
| 13601800 | 3601800 | not a goods lot (native award) | — | — | — | **none** |

**Oedon Tomb Key.** It has `isConsume` 1, but the game is not known to remove keys on use. Nothing here proves either way, so it counts as no evidence.

## Answer

- **The gate cannot be closed for every row.** Amelia's **Gold Pendant**, the review's example, is consumable (it turns into a blood gem), cannot be discarded, and has no get flag. Six more rows are in the same position.
- **It can be narrowed.** Three chalice rows have **two independent** pieces of evidence:
  - the get flag;
  - the chalice itself, which can be neither used up nor discarded.
- **Two rows have the get flag only:**
  - Third Umbilical Cord (global flag);
  - Astral Clocktower Key (kind 5 map group, less certain).

## Proposed narrowing (not implemented; for review)

1. **At the attempt.** When the lot's get flag is a global flag and it is clear, the attempt line also records the flag: `attempt <event> <time> <flag>`.
   - The current parser reads the event and time and ignores a third field, so old and new files stay readable.
   - A flag that is already set records nothing, and that entry keeps today's behaviour.
2. **The held tick**, only with the owner's slot active, in its own world (session state 0), with the character loaded:
   - **Flag set:** given, final.
   - **Flag clear:** the add failed. The line is removed (the same as today's manual release), and the next qualifying kill gives the lot once.
   - **Chalice rows:** the chalice found in the carried items **or storage** (`BbscStorageInventory`) also counts as given.
3. **Rows without evidence** are unchanged: held, with the manual release logged.

**Limits of the proposal, all unproved natively:**
- **In-flight save.** A save the game began before the add, and finished after the attempt time, would hold neither the item nor the flag. A delivery that worked would then read as failed, and the lot would be given twice. This is the same assumption B15 already lists. For the chalice rows (`isOnlyOne`) a second add is expected to be refused by the fit check (`0x014D9A80`), which is untested.
- **Where the flag lands while a guest.** The get flag is written while the character is in the host's world. Global groups are believed to be the guest's own, but no native run has checked that the flag is in the guest's next save.
- **The Astral Clocktower Key's map group** is the host's live table during the session. Whether the bit reaches the guest's save is untested.

## Native checks needed (friend's side)

These are not done here because they need a two-instance session, which this session does not run (the user's limit: token cost and about 17 GB of RAM per instance). Use copied profiles with `SHADPS4_BBSC_REWARD_ONCE=1`.

1. **Get flag across the trip home.** A joint Blood-starved Beast kill (12301800) with a guest that never had the Pthumeru Chalice.
   - After the trip home and a save, check that flag 5000 is set for the guest (BBSC log or a flag read) and that the chalice is carried.
   - Restart, load: still set.
2. **Same for the Third Umbilical Cord** (12601800, flag 50000305), and also after using the cord.
3. **Optional: Astral Clocktower Key** (13501850, flag 53501850, area 35 group).

If 1 and 2 pass, the narrowing above can be implemented, with fixtures and RED, as a B15 revision.
