# R03 playtest source corrections — offline delivery

2026-10-31 (Asia/Bangkok). User authorizes implementing the three playtest corrections, removes agent-run game tests, and will playtest with their friend. Source/offline delivery complete; gameplay acceptance remains open. No game launched, original/installed game files or saves changed, server deployed or release packaged.

## Changes

- **Stale role override:** `ClearBbscStaleHostSummonType` runs at the existing reload-finish hook before character creation consumes pending role. Only session6/co-op sign -1/pending host type0 is cleared to the native unset sentinel -1, with readable/writable guards. Native summon selection then chooses the role. Valid pending phantom/invader roles, other signs, solo/host/return paths are retained. This guards the demonstrated consumer; the exact producer of the stale host value is still unknown. Bell/menu/animation/Insight behavior needs user confirmation; no Insight compensation is added.
- **Boss-state replay:** `BbscDurableProgressByte` removes only `12414700`, `12414702`, `12415400`, `12414800`, `12414802`, `12414807` from newly collected and merged progress bytes. These cover the inspected Cleric Beast/Gascoigne combat paths. Merge filtering also handles already-written pending journals. It never clears existing live flags or whole groups; completion flags, adjacent progress and cutscene-seen `12414223` remain. This prevents that bounded combat-state import; it does not prove that all gauge symptoms or delayed event initialization are resolved. Already-saved unwanted state is not retroactively repaired.
- **Enemy compensation:** removed `NoteBbscGuestEnemyDeath`, its queue, `TickBbscGuestDrops`, `GiveBbscGuestDrop`, the now-unused add helper/row constant/RNG and their calls. The automatic-add banner disappears with that path. Native ground pickup, guest loot view/pickability/journaling, boss reward producer/consumer and the shared GUEST_ITEMS switch are retained. User reported ground loot works; no claim of a proven single-enemy duplicate. Rare-loot gameplay remains unverified.

Runtime source is carried by `gpu/patches/bbsc/0001-profile-storage-and-clang64.patch`, not only the ignored checkout. Isolated matching source/build/evidence is `.superpowers/playtest-fix`; frozen `.superpowers/echo-fix` remains unchanged. Other integrated `bbsc_http.cpp`, `bbsc_mod.cpp`, `bbsc_relay.cpp` inputs remain byte-identical to the frozen composition.

## Offline checks

CLANG64 `clang++` on PATH; TEMP/TMP set to the workspace `.superpowers/playtest-fix/tmp`; `BBSC_FIXTURE_SOURCE` selects the isolated candidate `emulator/src/core/bloodborne_re.cpp`.

```powershell
C:/msys64/clang64/bin/python.exe -m unittest discover -s tests -p 'test_bbsc_*.py'
C:/msys64/clang64/bin/python.exe -m unittest discover -s tests -p test_native_bbsc.py
C:/msys64/clang64/bin/python.exe tools/build_bbsc_mod.py .superpowers/playtest-fix/source .superpowers/playtest-fix/dll
```

- Final BBSC suite: **12 tests PASS, zero skips**, exit0. Actual helpers cover role guard boundaries and 6,000 affected/adjacent flag bits; actual party collector excludes combat state; actual merge rejects combat bytes from old pending input and preserves existing own-world bytes. Ownership, reward delivery/deduplication, recovery, reordering and backup checks pass.
- Native-header suite: **2 tests PASS**, exit0. These are compilation/fixture checks, not native gameplay.
- Previous frozen source with the new merge case fails the real merge assertion (unfiltered byte, expected `0x5E`); candidate passes. New helper tests on the frozen source report a missing helper and compensation-presence failure, not a native reproduction.
- Initial run used an inaccessible sandbox TEMP, producing filesystem errors. Rerun with workspace TEMP resolved these. Subsequent failures exposed an owner fixture missing the new helper and old delivery/ordering fixtures selecting the stale reference rather than the candidate. Updated the extraction and consistent `BBSC_FIXTURE_SOURCE` selection; no runtime workaround or weakened assertions. Remaining fixture macro-redefinition warnings are nonfatal.
- DLL builder exit0, mandatory notices copied. Integrated patch reverse-check passes. Fresh files from pinned HEAD accept the patch and reproduce all four destinations after LF normalization; initial byte comparison detected CRLF differences in copied mod sources, not a semantic mismatch. `git diff --check` passes.

Usage checkpoint: 71% primary / 14% secondary remaining at final review; no stop threshold reached. Final source delivery is ready for publication; no additional native work is scheduled for the agent.

| Output | SHA256 |
| --- | --- |
| Candidate source, LF | `279f2f68a35630b75cc1d87aca6ebb9ee1435a3a04246466a34cfa25dbd2ed5e` |
| Integrated patch, LF | `c4a3f65839affd1ab8224d32e3a3a3b491770623f2cd5c535be724beb4df2c8e` |
| Candidate `bbsc.dll` | `fc4d851a321abf59c5a57d211e1154d9b9cbc39880e4fa5bc8082eca8249307c` |

## Handoff

New DLL and mandatory notices are in `.superpowers/playtest-fix/dll`. With both games closed, user can back up the previous installed `bbsc/bbsc.dll` and use this DLL on both clients, retaining the existing notices/configuration. No EXE replacement or switch change is needed for these source corrections. The agent has not installed it over the user's game.

The [revised plan](../superpowers/plans/2026-10-31-r03-playtest-follow-up.md) removes agent game testing and gives the user a short playtest observation list. Review returned two-client logs/timelines/captures before declaring bells/menu/gauge/rare drops fixed. Source guards are bounded; exact role writer, late map-event scheduling and broader map coverage remain limitations, not verified repairs.
