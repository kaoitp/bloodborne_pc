# R03 B14: another character's own-world journal is not put back

2026-10-26, Claude (R03 takeover). Base: seamless `4426543` (after PR #10; first written on `cc4858d`). Source change in the tracked patch (`bloodborne_re.cpp` only). This addresses the A02 blocker ([A02](R03-A02-RECOVERY.md), "Blocking final gate").

## The defect

On V5, Quit Game → title → Load Kaori (slot 0) put EiEi's (slot 1) pending journal into Kaori: 979 groups, 607 flags differed.

The journal lives in memory (`bbsc_own_world`). `RestoreBbscOwnWorldAtLoad` runs at the next load's `Warp.RespawnPoint.Resolve` and the load-finished hook. It put back whatever the memory held, for whichever character was loading.

The save slot cannot tell who is loading at that point:
- `BbscActiveSaveSlot()` picks the newest save written since the load started;
- the same hook resets that start time a moment before;
- the new character has not written a save yet.

The A02 V5 run had the experimental home recovery on. The same in-memory journal also exists in the default configuration while a guest is in a host's world, for example after Quit Game as a guest.

## Change (reworked after the PR #11 review)

**Identity.** The owner is the **save slot** (`bbsc_own_world_slot`, user + slot). The name (PlayerGameData `+0xA8`) is only diagnostic, because two characters can share one.

**Why the slot can't be checked at the load hook.** Natively, the loaded character's save is written about 10 s after `Warp.RespawnPoint.Resolve`. Example: U-I-AHH's hook ran at 17:00:30.5 and its save was written at 17:00:40.2.

**`bbsc_own_world_continuous`** means the same character has stayed loaded since the journal started.
- **Set** when the journal starts (the first group kept as a guest), and when a crash file is recovered for the verified active slot.
- **Ended** by a load from the title: `Warp.StageDescriptor.Finalize` with `rdi == 0`. Across 13 native loads in four runs:

| Load | `rdi` |
|---|---|
| From the title (Continue / Load Game) | `0` |
| Death reload | `0x5330400` |
| Summon load | `0x5330401` |
| Trip home | `0x5330400` |

**`BbscOwnWorldOwnerConfirmed`** decides in `RestoreBbscOwnWorld`:
- **continuous, with a readable name equal to the owner's name** → put back at once. This is the normal trip home, still before the map's events.
- otherwise it waits for the save slot:
  - **unknown** → writes nothing and drops nothing; retried every tick;
  - **the owner's slot** → put back;
  - **another slot** → writes nothing, drops the in-memory journal and the same character's Dream values, and keeps the file. Its owner gets the file back the next time that character is home, through the slot-checked crash recovery.

**First attempt, rejected natively.** A title check in the game tick (an empty name at the title) never fired. U-I-AHH's journal went into Six. That was DLL `cf6001ea…`, in a copied profile. The game tick does not run at the title.

## Fixture

`test_bbsc_own_world_owner.py` compiles the actual functions with controlled memory, plus a real journal file in a temporary folder, built with ASan. The functions are:
- `BbscLocalCharacterName`, `BbscNameForLog`;
- `KeepBbscOwnWorldGroup`;
- `WriteBbscOwnWorldFile`, `LoadBbscOwnWorldFile`;
- `BbscOwnWorldOwnerConfirmed`, `RestoreBbscOwnWorld`;
- `RecoverBbscOwnWorldFile`, `NoteBbscOwnWorldCharacterLoad`.

Scenarios:
1. Trip home: put back at once.
2. A02: EiEi's journal, then a title load of Kaori.
   - Not ready: nothing written, journal kept.
   - Kaori's slot: nothing written, memory dropped, file kept.
   - Kaori has no file of her own.
3. Back to EiEi: her file is recovered and put back, and renamed `.restored`.
4. Same name, other slot after a title load: nothing written.
5. Name unreadable: nothing written or dropped. The owner's slot then confirms it.
6. Title signal missed but another name is loaded: waits, then dropped for the other slot.

**RED**, built from copies of the source with the reviewed or weakened checks:
- **A:** accept the same name (the reviewed head's rule) → scenario 4 fails.
- **B:** accept an empty name → scenario 5 fails.
- **C:** ignore `continuous` (name only) → scenario 4 fails.
- **D:** no title signal → scenario 4 fails.

**GREEN** now. `test_bbsc_*` 6 OK, `test_native_bbsc` 2 OK, `git diff --check` clean.

## Native evidence (DLL `554e5ba200895a78bb224a5e748328985db317c6b9d2ee19c59cbe4327f0ddf3`)

**Source**
- Pinned `4f11faf` plus the tracked patch SHA256 `fe6f4fe79f644c45ba19b9497a2e8bf746a1c798454e7d2b9bde7c8c59cdada6`.
- `bloodborne_re.cpp`, LF: `8df7de56269810dd49381f5ee6e18ad3a0db9ff8b7c133baba4943b95b36cf25`.
- The patch was regenerated from the build tree and `cmp`-checked before the build.

**Build:** `C:\msys64\clang64\bin\python.exe tools\build_bbsc_mod.py .superpowers\reference\BBSC <out>`, with clang64 first on PATH.

**Tests:** from `tests/`:
```
python -m unittest test_bbsc_own_world_owner test_bbsc_reward_delivery test_bbsc_party_progress test_bbsc_progress_backup test_bbsc_reorder_collect test_bbsc_world_ordering test_native_bbsc
```

**Configuration:** mod defaults, `SHADPS4_BBSC_SPECTATE=0`, the experimental home recovery off. Fresh copies of both protected profiles.

**Run:**
- Host: profile b's U-I-AHH, level 10.
- Guest: profile a's own U-I-AHH (user sd1, slot 3), level 10.
- 17:25:08 the journal was kept (979 groups, file `own-sd1-3.bin`); 17:25:24 placed.
- Quit Game → title → Load Six (slot 2).
- 17:26:40 `a character is loading from the title - the journal now waits for its owner's save slot`.
- The BBSC session survived the title (state 6), so nothing was tried until the host was closed.
- 17:27:16 `the journal is user sd1 slot 3's (U-I-AHH) but user sd1 slot 2 (Six) is loaded - not put back, the file stays for its owner`. The file was unchanged.
- Shared progress merged nothing into Six.
- Quit → Load U-I-AHH, then:
  - 17:28:43 its own shared progress merged (pending file `pending-sd1-3.bin`);
  - 17:28:57 `user sd1 slot 3 was left with another player's world in it - putting our own back`, 979 groups;
  - the file was renamed `.restored`.

**Not covered natively**
- Two characters with the same name in one profile (fixture only).
- The experimental home-recovery path, which now also waits for the slot.

During an earlier attempt one client stopped with `Unimplemented PM4 type 0` / `STOP: GPU library assertion failed`, exit code 23, at a load. That is the emulator's GPU.

## Own world before shared progress (second PR #11 review)

**The blocker.** The mismatch path drops memory and keeps the owner's file. When the owner loads again within the process-wide 15 s recovery throttle, its pending shared progress, still in memory, could merge first. The later own-world recovery then copied the pre-visit bytes over the earned bits.

My native B14 timeline had exactly that order:
- 17:28:43: merge;
- 17:28:57: recovery.

The reviewer reproduced the loss with the actual functions: the result was 0x11 where 0x91 was required.

**Change.** `BbscOwnWorldReadyForProgress()` is now a prerequisite of both merge paths: `ApplyBbscSharedProgressAtLoad` and the `TickBbscSharedProgress` merge.
- A journal still in memory is put back first. If its owner is not confirmed, the merge waits.
- This character's own-world file still on disk is recovered first, for the active slot that equals the progress slot. Until the file is gone, renamed `.restored`, the merge waits.
- Waiting keeps the pending progress, in memory and in its file. Nothing is finalized.

**Fixture**, scenario 7 of `test_bbsc_own_world_owner.py`. It now also compiles the actual `MergeBbscSharedProgress` and `BbscOwnWorldReadyForProgress`:
1. EiEi's pre-visit journal (0x11) is on disk. Her earned bit 0x80 of group 1240 is pending in memory.
2. Title load of Kaori (another slot): Kaori's table is unchanged, and the merge waits or retries.
3. Title load of EiEi inside the throttle:
   - her own world is back first (0x11);
   - the merge gives 0x91;
   - the later throttled recovery finds nothing to undo, so it stays 0x91;
   - the journal file is renamed `.restored`.

**RED:** a copy with the prerequisite replaced by `return true` fails, because the own world is not back before the merge. **GREEN** now.

**Integration with PR #10.** The branch is rebuilt on `origin/seamless` `4426543`, which includes PR #10.
- `bloodborne_re.cpp` was combined with `git merge-file` (base `cc4858d`, ours = PR #11, theirs = seamless) with no conflicts.
- Three older shared-progress fixtures (`party_progress`, `progress_backup`, `reorder_collect`) stub the own world and got a `BbscOwnWorldReadyForProgress` stub. The ordering itself is tested in the owner fixture.

**Results:** the union of all fixtures passes: 10 tests OK, including PR #10's `test_bbsc_remote_show`:
```
python -m unittest test_bbsc_own_world_owner test_bbsc_party_progress test_bbsc_progress_backup test_bbsc_remote_show test_bbsc_reorder_collect test_bbsc_reward_delivery test_bbsc_world_ordering test_native_bbsc
```

**Hashes**
- Patch SHA256 `11853faca3d7a1ee4d1398d34c2e344fb5ebb2bf27045b55dd0d124addab5080`.
- LF `bloodborne_re.cpp` `daa5b07ece3342535437e4c9f99ec3c3176b9c11d947611750fed2a94c57badb`.
- DLL `700f22757e4ad65afc5c01b9e5b6a69a854df5e1ef2a95f0bdcd6e6461dca056`, exit 0.

**Not native.** No new run with this DLL. The B14 native run above used `554e5ba2…`, which has the slot identity but not this ordering.

## The 18 unclassified A02 flags

A02 listed 18 cleared global flags after its V3/V4 recovery runs: 2300, 2410, 2411, 2412, 2800, 70000030, and 70009260 through 70009370 in steps of 10.

**Classification by source.** All 18 sit in Hunter's Dream state groups (`BbscDreamStateKeys`):
- group 2 holds 2300, 2410, 2411, 2412 and 2800. These ids are BBSC's place-name ids: Old Yharnam, Central Yharnam, Iosefka's Clinic, Yahar'gul;
- group 70000 holds 70000030;
- group 70009 holds the rest. That group is the Dream shops' sold counts (`BbscDreamSoldGroup`).

A guest in a host's Dream gets the host's values for these groups. Its own copy is kept only in memory (`bbsc_dream_own`), not in the own-world journal file.

**Native check (default configuration, `d5250903` = the merged runtime).** Fresh copies of the protected saves; independent snapshots of the guest's 1250 groups with `read-world.py`.

| Step | 2300, 2410, 2411, 2412, 2800, 70000030 | 70009260–70009370 |
|---|---|---|
| U-I-AHH at home, before the join (S0) | 0 | 0 |
| In Kaori's Hunter's Dream (S1); log: `53 groups written, 119 bytes differed` | **1** (the host's values) | 0 |
| After the crash and restart (S2) | **0** (its own values) | 0 |

- Between S1 and S2, the guest saved at 15:46:22 during the stay and was killed at 15:48:37.
- At the restart it woke in its own Dream. The crash recovery put back 979 map groups.
- S0 → S2 differs in only 3 flags, all newly **set** by the guest's own Dream visit: 12105000, 12105062, 12415010. Nothing was cleared, and no Dream-state value leaked.

**Conclusion:**
- On the default path a crash in the host's Dream does not leak the host's Dream state into the guest's save. The game's save during the stay comes from the own-world snapshot, as the source comment says.
- The A02 differences came with the experimental home-recovery builds, which are already behind `SHADPS4_BBSC_EXPERIMENTAL_HOME_RECOVERY=1`. Their exact path was not reproduced here, because those builds' raw snapshots are not in this workspace.
- The sold counts (70009xxx) were 0 for both characters, so that group was not exercised.
