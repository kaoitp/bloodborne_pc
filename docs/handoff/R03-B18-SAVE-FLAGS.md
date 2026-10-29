# R03 B18: obligation flags in the character's own save (research)

2026-10-29. Claude (R03 takeover). Static research for the "path to default ON" in [R03-B18-REWARD-DEDUP](R03-B18-REWARD-DEDUP.md), requested on PR #17. **No code change. No native run.**

## 1. Candidate flags: groups 60000–60009 are unreferenced

**Groups that are never ON.** `tools/r03_flags/zero_groups.py` (reads the private snapshots under `.superpowers`) ORs every 1250-group world snapshot we hold: 33 snapshots, from several characters, before/after joins, reloads and boss kills. The non-map groups that are all zero in every snapshot are:
- 8;
- 10000–10009;
- 50004–50009;
- 60000–60009;
- 70001–70008;
- the 92xxx/93xxx blocks.

**References in game data.** `tools/r03_flags/scan_struct.py <dump>/dvdroot_ps4 <BBSC tools/gamedata>` (dump APP_VER 01.09) looks for references in the game data, file by file:

| Where | How | group 8 | 10000–10009 | **60000–60009** |
|---|---|---|---|---|
| event scripts (every `*.emevd.dcx`) | every instruction argument, aligned int32 | 10309 | 0 | **0** |
| ESD (every `*esdbnd.dcx`) | int32 literals (`0x82` + int32) | — | 324 | **0** |
| params (every param with its paramdef) | every integer field | many | many | **0** |
| MSB (`map/MapStudio`) | aligned int32 | many | 2 | **0** |
| Lua (`script/*.luabnd.dcx`) | float64 constants | 35 | 4 | **0** |
| `eboot.bin` | int32 at any alignment | many | 2399 | **95: none is a flag** |

The 95 `eboot.bin` hits are not flag constants:
- 85 follow a RIP-relative ModRM byte (`05`/`0d`/…), so they are memory displacements;
- the other 10 are overlaps of jump or call encodings (`0f 8c`, `e8`).

None is a `mov`/`push` immediate.

Candidate: one flag per reward row in group 60000, for example `60000000 + row index`.

There are 19 `BbscBossRewards` rows, and 1000 bits fit in one group.

The group key is 60000: kind 6, area 00. `BbscIsMapFlagGroup` (areas 21–99) and `BbscDreamStateKeys` both leave it out, so:
- the own-world journal, the host world sync and the Dream state never write it;
- the guest's live copy is the guest's own, even in the host's world.

**Not proved statically:**
- the code could compute such a flag at run time (base + index);
- that the group is written into, and read back from, the character's save;
- what NG+ does to it.

## 2. A save boundary that changes the design

The source documents (5204, 5231) that while the character is a guest (`global+0x1592 == 0`), the game writes its save from the **own-world snapshot** (`0x0156AA50`), not from the live flag table, as in vanilla co-op. Flag changes made in the host's world do not reach a save; that is why the shared progress merges at home. Inventory and echoes behave differently: native04 saw the guest's echoes (+535) persist, which suggests player data is saved live.

**Consequences for the proposal:**
- **The owed flag cannot be set at the kill.** It must travel with the shared progress (collection, pending file) and be set **by the merge at home**, in the same live table as the boss bit, so one game save holds both.
- **Delivery has to move home.** An item added in the host's world is saved, but the flag clear is not. Atomicity needs the add and the flag clear in the own world: owed flag ON, fit check, add, flag OFF, then the next game save holds both or neither. **Behaviour change:** the reward would arrive when the guest is back in its own world, not at the kill. This is for the owner to accept.
- **Before home, nothing from the party is in the game's save.** The boss bit and the owed flag exist only in the shared progress pending file, a mod file. With storage unwritable until a crash before home, both are gone together, and the character's state equals "no kill". This boundary belongs to the shared progress itself; no ordering can keep the obligation without any durable write. It is not a loss of an obligation the save already holds.
- **After home**, no mod file is involved:
  - the merge sets both bits;
  - a crash before the next save leaves the pending file (it is finished only after a save) and re-merges;
  - a crash after the add, before the save, keeps the owed flag ON, so the item is redelivered once;
  - after the save, the flag is OFF and the boss bit is ON, so there is no second reward, consumed or not.

## 3. What the requested acceptance would need

**Fixtures** (actual functions):
- the merge sets the owed flag with the boss bit;
- delivery only at home with the flag ON;
- add and clear in one step;
- the guard on the journal boss bit and the owed flag;
- restart before and after the save;
- refused delivery (flag stays ON);
- consumed delivery;
- wrong character (each save holds its own flag);
- both `REWARD_ONCE` modes.

**Native, copied profiles:**
1. **Persistence.** At home, set `60000000` in the live table. Save through Quit Game, reload, read: ON. Then a fresh process: ON. Clear it and repeat: OFF.
2. **Away-save boundary.** As a guest, set the flag and add an item, save through Quit Game, reload: the flag is OFF and the item is present. This confirms that delivery must be at home.
3. **NG+.** A character entering NG+ with the flag ON shows what the game does to group 60000. If it resets, a pending obligation at the NG+ transition is lost; if not, it carries over and is delivered once.
4. **End to end.** The never-beaten guest kills, returns home and gets the item once. A crash after the add and before the save, then restart, gives it once. Then use the item, restart, rejoin and kill: nothing.

## 4. Open questions for the owner

- Delivery at the return home instead of at the kill: acceptable?
- Is the shared-progress boundary in section 2 (storage failing until a crash **before** home) acceptable as the remaining case, given that nothing in the game's save exists yet at that point?
