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

## 2. The save writer takes the flags LIVE, also while away (correction)

My first reading (PR #17 comment 6490479535) said the save writes the event flags from the own-world snapshot while the guest is away. **That was wrong.** I disassembled the 01.09 eboot with `tools/r03_flags/dis.py`; the fake SELF's text segment is entry 1, va 0 at file `0x28EB0`, checked against BBSC's known `0x01332C14 mov rcx,[rip+..]; cmp [rcx+0x1520]`.

**`0x0156AA50`, the save writer:**
- `0x0156AB75` tests `global+0x1592` only to choose the map id for the save header: `+0x14F0` while away.
- `0x0156AC8C` then **always** calls `0x01399DE0`.
- `0x01399DE0` reads `[0x0553B100]` (`0x01399DF5 lea rbx,[rip+0x41A1304]`, which is `EventFlagMan`) and serializes its `+0x28` data: the **live** flag table. The BBSC source already says the same in "Shared progress on disk".
- The three snapshot swaps behind `global+0x1592 == 0` (`0x0156ACD6`, `0x0156AF66`, `0x0156B13B`) cover the objects `0x0131E5C0` builds:
  - `+0x1698` from `0x0553E878` (WorldChrMan, a "CHR " block);
  - `+0x16B8` from `0x0553B168`;
  - `+0x16D8` from `0x0553E928` (a "DECL"/"LCED" block).

  **None of them is the event flag manager.**
- The inventory is written live (`bbsc_patch_tables.h`, GuestItems).

**So while the guest is in the host's world, its next game save holds its live inventory and its live flag table.** Group 60000 is never written by BBSC's host world sync, own-world journal or Dream state, so its live copy is the guest's own all the time.

## 3. Design: in-party delivery, atomic in the game's save

Two bits per reward row in group 60000, both in the guest's live table:
- **OWED** = `60000000 + row`;
- **DONE** = `60000500 + row`.

**At the kill** (eligible, guard passed): set **OWED**. The next game save holds the obligation. No mod file is involved.

**In-party delivery**, in one game-thread step:
1. fit check;
2. add the item (live inventory);
3. clear OWED;
4. set DONE.

The next game save holds both changes, or neither:
- a crash before the save leaves OWED ON, so the item is delivered again once;
- after the save, there is no second item.

**Refused delivery** (capacity): OWED stays ON in the save. Delivery is retried in the party or at home until it fits, with the same single step.

**Restart:** the tick scans the 19 OWED bits of the active character and queues those that are ON. That delivers the **original obligation without a second kill**, bound to the character whose save holds it.

**Guard** for a new obligation: DONE ON, OWED ON (already owed), or the boss's own-world bit ON (journal copy), as in revision 1.

**DONE and NG+:** DONE is cleared at home once the own-world boss bit is ON, which the shared progress merge provides. From then on the boss bit is the guard. NG+ then clears the boss bits as the game does, and nothing of ours blocks the next cycle.

**Remaining boundaries (to verify, not assumed):**
- **A crash before the first game save after the kill.** No save holds the party's kill yet, so the obligation is lost with it. That is how the game itself treats an unsaved kill.
- **The save serialization thread.** If `0x01399DE0` and the inventory serializer could run between steps 2 and 4 on another thread, the step would not be atomic. The save writer's call path and thread are to be checked natively.
- **A DONE bit whose boss bit never reached the own world** (shared progress pending file lost): it blocks that boss in the next NG+ cycle. The NG+ clear count could remove this residual; its offset is not known yet.
- **Whether NG+ resets group 60000.** A pending OWED at the NG+ transition is kept or dropped accordingly.

## 4. Evidence needed (native, copied profiles)

1. **Persistence.** Set `60000000` while a guest, let the game save, Quit, reload: ON. In a fresh process: ON. Clear it: OFF after the next save.
2. **Atomicity.** In one tick, add an item and set the bit, then kill the process before a save: neither is there. After a save: both are.
3. **Trip home.** After the return home, the bit is still ON in the live table: no journal, Dream state or restore touches group 60000.
4. **NG+**, as above.
5. **End to end.** Never-beaten guest: delivered in the host's world. Restart: nothing more. Capacity full at the kill: OWED survives a restart, and is delivered once when it fits, without a second kill. Use the item, rejoin, kill: nothing. The other character of the same user sees no bit.

The owner's question about home-only delivery is withdrawn: this design keeps delivery in the party.
