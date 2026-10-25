# R03 B08: first native joint boss kill (Vicar Amelia)

2026-10-25, Claude (R03 takeover). Runtime unchanged from B06 (`a43e26f`); frozen B06 DLL `faf8227f…` on both clients; local `out/bb-probe.exe` `598d4616…` (see [B07](R03-B07-INDEPENDENT-RELOAD.md)). No source change. This is the first actual jointly earned boss event in R03: the positive side of G2-20 and G2-02, plus a native reproduction of the G2-01 history import.

## Setup

- Two copied profiles, both online, on the self-hosted server reported by the owner. TCP 31313, 31315, 20443 (http) and the 20444 relay were connected by both DLLs. Accounts were supplied by the owner and kept in an ignored local file.
  - Host A: copy of `native/after-a-savedata`, Kaori slot 0, Cathedral Ward.
  - Guest B: copy of `native/before-b-savedata`, U-I-AHH slot 3, Iosefka's Clinic.
  - Both copies were per-file byte-exact before launch, and both protected sources were unchanged afterwards.
- Switches: BBSC defaults with nothing overridden. **Shared progress was ON**, as a default-on switch; earlier Codex runs had it OFF. Dream, guest items, spectate and timeline were also ON (default). 30 FPS, render 1280x720.
- Both clients installed 160/160 hooks, plus the boss-clear and Dream install lines.
- Preconditions read natively before joining: flag 12401800 (Amelia) was **OFF** on both host and guest.

## Test aids (debug, outside the game; disclosed)

- **Position write.** The local player's transform (the `read-position.py` chain, +0x1E0) was written from outside the game. The write held right after a load and was overwritten at other times. It was used to put the host, and after the wipe both players, inside the Grand Cathedral entrance, next to the MSB region `Event_ボス_霧壁埋まりワープ先` (51.90, 35.71, 312.30). The regions came from `map/mapstudio/m24_00_00_00.msb.dcx`.
- **HP-0 kill.** After the native boss bar appeared, Amelia's HP was set to 0 from outside the game. She was the type-7 character found by a WorldChrMan scan; her max HP was doubled by BBSC scaling for one guest. The game then ran its own death, event, reward and boss-clear path. This is the same aid as the old fork's `killmark`. Combat itself was not tested.
- **Movement and menus.** These used the existing `BB_PAD_FILE`, plus a walker that steers by measuring camera-relative stick movement.

## Native sequence (local wall times, same PC)

1. **Bell and join.**
   - Host rang the Hunt Bell (bell icon on the HUD). Guest used the Kin Bell from the inventory at 21:59:33.
   - 22:00:06 host `ringing the sign of user …`, state 0→3. 22:00:09-10 guest state 0→4→6, connect-first placement written at handoff. Guest `relay: our host is player …`.
   - 22:00:16 the join load copied the host's map flags (30 groups). 22:00:27 host `lua event: SummonSuccess_White (caller 0x15bccf7)`. 22:00:29 guest `join teleport` and `load cover … guest placed beside the host`.
   - Guest type 1, about 1 m from the host.
2. **First attempt.**
   - 22:06:26 both clients logged `boss line: "Vicar Amelia" (boss 502000)`. Host and guest boss-bar memory showed slot 0 = 502000.
   - The host died (22:06:50 SoloPlayDeath), then the guest (22:07:10 PartyGhostDeath). That was a wipe, and everyone reloaded. **The session survived the wipe**: 22:07:23 host `SummonSuccess_White` again, 22:07:50 guest `arrived beside the host` at the lamp, respawned as type 1. Amelia was alive.
3. **Joint kill.**
   - Both were moved inside again; the boss bar appeared at 22:09:27. HP 0 was set at 22:09:40 (max 7514, one character).
   - **Guest, 22:09:47:** `boss drop: event 12401800 queued for user sd1 slot 3`. Then `goods 4001 x1 put into the carried items (fits 1, slot 84, there now: true, get flag 0)`. Then `lot 50000001 finished for user sd1 slot 3`. Also +15000 Echoes and Insight 0→1.
   - **Host, 22:09:47:** +15000 Echoes, Insight +3.
   - **22:09:52:** `boss clear: BlockClear2_1` on the host (type 0) and on the guest (type 1), both with the session kept. Guest gates: flags 4000/4092, mission-clear menu 1.
   - The reward wait reached the guest about 5 s **before** `BlockClear2_1`.
4. **Departure.**
   - Guest Parting Blank → End co-op → Yes. 22:11:15 `OnLeaveMagic`; state 6→7→0 by 22:11:16. Home load 22:11:22: 979 own-world groups put back.
   - 22:11:31 guest in Central Yharnam, at **exactly** the pre-join map, lamp, position and heading. 22:11:36 `goods 4001 after the trip home - still in the carried items`.
   - Shared progress, 22:11:35: `merged into our own world - 14 boss flag(s) newly set (of 14 the host has), 272 world flag(s) newly set in 160 group(s); saves backed up first: true`.
5. **Independent reload.** Both games were closed and after-saves preserved. A fresh offline guest process (PID 15252) loaded U-I-AHH:
   - same origin; flag 12401800 = 1;
   - inventory shows **Gold Pendant** (Vicar Amelia's item), Blood Echoes 15000, Insight 1 (screenshot).

## Result against the goals

| Check | Result |
|---|---|
| G1 join, Clinic guest to Cathedral host, beside host; session kept through a wipe | PASS (native, this run) |
| G2-20 positive: reward wait fires on a real joint kill | PASS: queued at the kill, delivered to the original owner (sd1 slot 3), confirmed after the trip home and after an independent reload |
| G2-02: joint boss kept by both players after their own save/reload, without older host history | **PARTIAL**. Kept: the guest's reward and flag 12401800 after the guest's independent reload. Not established: no host reload was run, and older host history was imported into the guest in the same run (G2-01), which the case forbids |
| G2-01 older host history | **REPRODUCED-GAP**, natively: shared progress ON imported 14 boss flags (e.g. 12301800) and 272 world flags into a level-10 character that never earned them; 239 of the bits persist after reload |
| G3 return to own world/origin | PASS: exact origin |

**Unclassified:** after the independent reload, 57 bits that were set live after the merge are clear; 2 others went the other way. They are in groups 1, 9, 12204, 12404, 12405, 12406 and 12415. They are not classified here.

**Next:**
- History exclusion (the G2-01 fix), using the reward-wait signal now observed to fire at a real kill. CL03 M1 is partly answered: B05 found no wait at a pre-killed load; this run found a wait at a real kill.
- C4 party boundary.
- Dead/loading guest earning: this run's wipe shows a dead guest gets no clear before the reload.

Private evidence (ignored): `.superpowers/claude-r03/coop` contains timelines, mod logs, RE captures, pre/after/reload world and position JSON, after-saves with hashes, and screenshots. Helpers: `chr.py`, `goto.py`, `walk.py`, `gauge.py`, `msb.py`, `pad.ps1`, `shot.ps1`.
