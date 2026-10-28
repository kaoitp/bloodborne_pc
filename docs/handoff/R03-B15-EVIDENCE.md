# R03 B15: game evidence for a held reward (failed add vs used-up delivery)

2026-10-27, revised 2026-10-28 after review 1. Claude (R03 takeover). Static research only: game data from the dump and the BBSC source. No game run and no code change.

## Question

B15's open protocol gate (`R03-B15-REWARD-ONCE.md`, Limits) concerns one record state: an `attempt` line with no outcome, followed by a save. The record cannot tell whether:
- the add **failed** and its removal was never written, or
- the add **worked** and the item was later used up.

The question is whether anything in the game or the save tells the two apart, row by row.

## Method

**Data.** Taken from the game dump (APP_VER 01.09, CUSA03173), folder `dvdroot_ps4`. The archives and the param data stay private; only the hashes and the reader are in the repository.

| File | sha256 |
|---|---|
| `param/gameparam/gameparam.parambnd.dcx` | `581e28302a231a10ad333806dfc90f41425db4f9f146799dca625f8d83c760c3` |
| `paramdef/paramdef.paramdefbnd.dcx` | `8a3f7ffed82c2c99903105ab151f51ad271017b291b37c721e10052e252b2296` |

**Reproduce.** `python tools/r03_goods_rows.py <dump>/dvdroot_ps4` reads the two archives and prints the table's goods fields. It writes nothing. Its docstring gives every format offset it uses: DCX (DFLT/zlib), BND4, the paramdef field records and the param row table.

**Layout.** It is computed from the `EquipParamGoods.paramdef` field list (88 fields), not from spacing alone:
- each field's type and internal name are read from the paramdef;
- an `x:N` name is an N-bit field; consecutive bit fields of one type share one unit, `dummy8` bit fields pack into `u8` units, and a field that does not fit starts the next unit;
- the check: the computed row size (108 bytes) must equal the spacing of the row data (108), across 295 rows. The script stops if they differ.

Fields used, as byte offset `.` bit in the row: `maxNum` @54 (u16), `goodsType` @58 (u8), `isConsume` @68.7, `isOnlyOne` @69.2, `isDrop` @69.3, `isDeposit` @69.4 (1-bit each).

Two readings cross-check the parse:
- Gold Pendant (4001) has `isConsume` 1, and its English description says "Use to change into a blood gem".
- Third Umbilical Cord (4323) has `isConsume` 1, `isDrop` 1 and `isOnlyOne` 1.

**Source.** Pinned BBSC 4f11faf plus the tracked `gpu/patches/bbsc/0001-profile-storage-and-clang64.patch` at `seamless` 27366a686b8ff543d0d7c815e47ce2f89267cae1 (patch sha256 `7871e606f8d2c90d59ae58abc02abd4456cf6b7e7075cef2c300ecfc16cc25cf`, unchanged up to `seamless` 3772880). The patched `emulator/src/core/bloodborne_re.cpp` has sha256 `4a94e78ac2ca8a54b10c7ace0ba3cd44ce8787943c56c30bf73b94960557cbcf`. Line numbers below are in that file.

## Source facts

**The get flag.** `GiveBbscBossGoods` (11165) sets the lot's get flag (`BbscBossGoodsLots[].flag`) through the game's flag setter (`0x0132E5A0`) right after an add that worked (`there`: slot >= 0 and the goods found in the carried items), and only then. A failed add never sets it. Nothing in the reward path writes the flag into the own-world journal.

**What the own-world journal holds.** Flag group key = flag / 1000.
- `CaptureBbscOwnWorldBeforeJoin` (6262) keeps, before the join load, every map group (`BbscIsMapFlagGroup`, 6135: kind 1/5/6/7, area 21–99) **and** every key in `BbscDreamStateKeys` (5232). That 57-key list includes **5** (flags 5000–5999, the chalice get flags) and **50000** (the cord's 50000305).
- Other callers keep a group the first time they write it: the host world flags (around 5582), the host's Dream state (`ApplyBbscHostDreamState`, 5782) and the guest loot view (`ApplyBbscGuestLootView`, 6812, groups 50000 + area·100 + 0..99). `KeepBbscOwnWorldGroup` (6182) keeps the **first** copy only.

**How the trip home puts groups back** (`RestoreBbscOwnWorld`, 6483):
1. If the guest still holds Dream state, `RestoreBbscOwnDreamState` (5836) runs first. For each Dream key, bits the game changed after the host's Dream state was written stay as they are now; all others get the guest's own copy, which is the journal's first copy. Shop unlock flags are taken from the guest's own copy. `NoteBbscOwnDreamRestored` (6350) then overwrites the journal copy of every non-map Dream key (5 and 50000 among them) with the result.
2. Then every journal group whose key / 10000 == 5 is put back by OR: a set bit is never cleared. That covers 50000 (the cord) and 53501 (the Astral Clocktower Key) but **not key 5**: 5 / 10000 == 0.
3. Every other group, **key 5 included**, is copied back whole: the journal copy replaces the live group.

## What that means for the get flags (static reading, unproved)

- **Chalices (flags 5000 / 5006 / 5009, key 5).** Key 5 is kept before the join and copied back whole at home. A get flag set during the party is not in that copy, so the trip home is expected to clear it again, unless the Dream path (step 1) kept it in the journal first. **A clear chalice flag after the trip home therefore does not mean the add failed.** It is not evidence for either outcome.
- **Third Umbilical Cord (50000305, key 50000).** Put back by OR, so a bit set when the trip home starts is kept. But step 1 can clear it first: if the guest entered the host's Dream after the kill, the Dream write replaced the live group with the host's, and the restore gives back the pre-join copy for every bit the game did not change after that write. The flag is evidence only on a path without a Dream visit, and that path is unproved.
- **Astral Clocktower Key (53501850, key 53501).** A kind 5 map group in area 35, OR-restored, and also inside the guest loot view's range, which rewrites item flags for what the guest may see. Unknown.
- **Where the flag is saved.** While a guest is away, the save is written from the own-world snapshot (comment above `BbscDreamStateKeys`: `0x0156AA50`, global+0x1592 == 0). Whether a flag set in the host's world reaches any save is unknown.

So **no get flag is independent evidence** by static reading. Destination, producer and save provenance of each flag stay unknown until a native run shows them.

## Rows without a taken flag (the rows B15 records)

Consumed = `isConsume`, droppable = `isDrop`, storable = `isDeposit`, one only = `isOnlyOne`, as printed by the script.

| Event | Lot | Goods | Consumed | Droppable | Storable | One only | Get flag (key) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 12201800 | 21002950 | 7150 Bloodshot Eyeball ×4 | 1 | 1 | 1 | 0 | — | **none** |
| 12301800 | 80000000 | 6109 Pthumeru Chalice | **0** | **0** | 1 | 1 | 5000 (5) | **item only, candidate**; the flag is not evidence (cleared at home, see above) |
| 12401800 | 50000001 | 4001 Gold Pendant (Amelia) | 1 | 0 | 1 | 0 | — | **none** |
| 12411800 | 31000 | 4000 Oedon Tomb Key | 1, see below | 0 | 0 | 0 | — | **none** confirmed |
| 12421800 | 80000300 | 6539 Great Isz Chalice | **0** | **0** | 1 | 1 | 5009 (5) | **item only, candidate**, as for 12301800 |
| 12601800 | 55100000 | 4323 Third Umbilical Cord | 1 | 1 | 0 | 1 | 50000305 (50000) | **none proved**; the flag survives only a path without a Dream visit |
| 12601850 | 21000 | not a goods lot (native award) | — | — | — | — | — | **none**; the award has no success signal |
| 12801800 | 50700000 | 7131 Yellow Backbone ×3 | 1 | 1 | 1 | 0 | — | **none** |
| 13201800 | 51001900 | 1591 Kin Coldblood (12) | 1 | 1 | 1 | 0 | — | **none** |
| 13301800 | 80000200 | 6429 Ailing Loran Chalice | **0** | **0** | 1 | 1 | 5006 (5) | **item only, candidate**, as for 12301800 |
| 13501850 | 3501850 | 4020 Astral Clocktower Key | 1 | 0 | 0 | 0 | 53501850 (53501, kind 5, area 35) | **none proved**; loot view and OR restore both touch it |
| 13601800 | 3601800 | not a goods lot (native award) | — | — | — | — | — | **none** |

**Oedon Tomb Key.** It has `isConsume` 1, but the game is not known to remove keys on use. Nothing here proves either way, so it counts as no evidence.

## Answer

- **The gate cannot be closed for every row.** Amelia's **Gold Pendant**, the review's example, is consumable (it turns into a blood gem), cannot be dropped, and has no get flag. Every other row except the three chalices is in the same position, the cord and the Astral Clocktower Key included.
- **It may narrow for the three chalices, through the item alone.** A chalice can be neither used up nor dropped, and the inventory is not part of the flag journal. If the chalice is in the carried items or storage, the add worked. If it is not, that alone is not proof of a failed add: an in-flight save could hold neither (see Limits). This is a candidate, unproved natively.
- **No row has a get flag that can decide it.** A clear flag cannot safely mean a failed add, on any row, until a native run shows where the flag lands and whether the trip home keeps it.

## Proposed narrowing (not implemented; conditional)

Only after native check 1 below passes:

1. **The held tick**, only with the owner's slot active, in its own world (session state 0), with the character loaded, for the **chalice rows only**: the chalice found in the carried items **or storage** (`BbscStorageInventory`) counts as given, final.
2. **Chalice not found:** unchanged: held, with the manual release logged. Removing the line on a missing chalice needs the in-flight save question answered first.
3. **Every other row** is unchanged: held, with the manual release logged.

The get flags are dropped from the proposal. They come back only if native runs show that a flag set in the host's world is in the guest's own save after the trip home, on every path (with and without a Dream visit).

**Limits, all unproved natively:**
- **In-flight save.** A save the game began before the add, and finished after the attempt time, would hold neither the item nor the flag. This is the same assumption B15 already lists. For the chalice rows (`isOnlyOne`) a second add is expected to be refused by the fit check (`0x014D9A80`), which is untested.
- **The chalice in storage.** Whether `BbscStorageInventory` sees the guest's own storage at the held tick is untested.

## Native checks needed (friend's side)

These are not done here because they need a two-instance session, which this session does not run (the user's session limit: token cost and about 17 GB of RAM per instance). Use copied profiles with `SHADPS4_BBSC_REWARD_ONCE=1`.

1. **Chalice across the trip home.** A joint Blood-starved Beast kill (12301800) with a guest that never had the Pthumeru Chalice.
   - After the trip home and a save: the chalice is carried. Record flag 5000 too (BBSC log or a flag read); the static reading expects it clear.
   - Restart, load: the chalice is still there.
2. **Optional, for the flags:** the same with a Dream visit between the kill and the trip home, and for the cord (12601800, flag 50000305) with and without one.

If 1 passes, step 1 of the narrowing above can be implemented, with fixtures and RED, as a B15 revision.
