# R03 native04: command-assisted Amelia party kill

2026-10-28, Codex, `seamless`. User authorized copied-profile tests, both players' existing no-death option, native warp staging and Amelia HP-zero. No product source/default/deployment changes. This supersedes the inconclusive staging of native02/03 for this bounded positive boss test; broader R03 gates remain open.

## Composition and scope

- Same integrated composition as native01: DLL SHA256 `87319fd9c2bbf748d5ab3e9ad06fbab7376fb075edba86be5c451f9f8ea12cf6`, probe `6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14`, reconstructed source `ee21b5e71dee64b3c39dcda8107fd34c4e703676f5dade701f9f07220910aad2`.
- Fresh copied native04 profiles, Kaori host / U-I-AHH guest; shared progress enabled, no-death=1 on both; managed admission/application, home recovery and reward-once record switches OFF. Private inputs and logs remain ignored.
- Existing fixture/build evidence is unchanged and separate from this gameplay observation. No new build or full-suite claim.

## Actions and observed results

1. Manual walking unavailable; user requested warp. The private `native-warp.py` calls the existing player vtable +0x5F8 method (image +0x18cd600), with exact executable, map 0x18000000, local host type, own-world, loading, no-death and prologue checks. SysV arguments passed through a private remote-thread adapter. Thread returned 0. Position stayed `(51.9000,35.7139,312.3000)` and visual inspection showed a standing player inside Grand Cathedral. This is a test aid, not a shipping warp implementation or general remote-thread safety proof.
2. Host Hunt Bell, guest Kin Bell through game inventory. Guest normal join moved from Clinic map 0x18010000 to Cathedral map 0x18000000, own-world=0/type=1, exactly at host staging position. No guest coordinate write.
3. Host walked toward altar; actual Amelia introduction and boss HUD appeared. Read-only live lookup: boss502000, handle268501105, block index4/index113/count140, type7, HP8051/8051. All pointer stages were readable. The existing lookup arithmetic worked; this does not establish why earlier attempts failed.
4. `native-aid.py 10488 kill` rechecked a unique live Amelia target and local host, wrote only boss HP=0 with readback, printed `AMELIA_HP_ZERO_CONFIRMED`. Host/guest remained alive. No progress flag or inventory write by test helpers.
5. Guest log at15:33:36.849: event12401800 earned in this party and queued; at15:33:36.851 goods4001 x1 inserted, slot84, present=true; at15:33:36.861 lot50000001 finished. Host showed Gold Pendant x1, echoes15000/insight9. Guest later showed echoes15535 (535 before), insight1 and shared-progress-saved message.
6. Game automatically returned guest after clear. Independent readback exactly matched original Clinic map, lamp2412950, position `(-190.18083,-50.62249,166.48239)` and rotation0.065716; own-world=1/type=0. At15:34:12.523 the guest log also confirmed goods4001 still carried after return.
7. Both exited normally through System → Exit Game → YES. Copied saves preserved under private `after-a-savedata` / `after-b-savedata`, then both verified test processes closed. Fresh processes22140/16796 launched with the same profiles/composition; Online → Continue, independently loaded outside party.
8. Both fresh-process1250-group snapshots retain Amelia12401800 ON, while both pre-party snapshots had it OFF. Read-only inventory lookup matching the runtime hash/slot layout found goods4001 count1 on both (host slot140, guest slot84). Guest grant count: one insertion before restart, zero insertions in the fresh-process log. This is one bounded reload observation, not proof against every duplicate scenario.

## Persistence and preservation boundary

The fresh guest log at15:37:20.989 reports importing three boss flags and three world groups from its existing shared-progress file. Thus the result proves restart persistence of the configured save **plus its normal shared-progress journal**. It does not prove raw savedata alone contains every shared flag without that journal. Gold Pendant was present after fresh load without another grant.

After settling, all1250 groups were compared against the guest's baseline. New ON flags:12400580,12400581,12400582,12401800,12401801,12401802,12401804,12404223,12404800,12404802,12404805,12404810,12404811,12404812,12404813,12404814,12404840,12404843,12705098,12705301,12705520,12705521,12705531,12705532,2402,9180,9455. New OFF:9187. None of these newly ON flags was ON in the host's pre-party snapshot. This rules out inherited host-before ON history in this observed flag set; it is not a semantic proof of every changed auxiliary flag.

Original user profile: all3171 paths and SHA256 hashes exactly match the fresh pre-test manifest after normalizing Windows path separators. Initial comparison failed on slash formatting only; normalized comparison passed with no file differences.

## Reproduction and private evidence

Use CLANG64 Python `C:/msys64/clang64/bin/python.exe`. Existing running game access/launch requires the authorized native execution context; sandbox startup has the separately recorded address-reservation limitation.

- `.superpowers/r03-final-native-04/native-warp.py 10488 --dry-run`, then without dry-run: guards pass/thread exit0. Missing `Path` import was corrected before any warp execution; initial generic `python` alias unavailable, corrected to CLANG64 Python.
- `boss-state.py 10488`: staged read-only lookup above; `native-aid.py 10488 kill`: HP-zero confirmation.
- `.superpowers/r03-close/read-world.py PID OUTPUT` and `read-position.py PID OUTPUT`: before, join, after-kill, own return, fresh reload and settled snapshots.
- `read-pendant.py 22140 16796`: read-only count1 on both, assertions PASS.
- `compare.py`: both beforeOFF/afterON/freshON and exact guest automatic origin assertions PASS.
- `finish-check.py`: original3171 exact, settled flag delta/no inherited host-before ON, one prior grant/zero fresh grant assertions PASS.
- Logs: `bbsc-mod-20261028-151605-10488.log`, `151617-8944.log`, `153532-22140.log`, `153544-16796.log` under native01 DLL logs. Raw saves, journal and logs are private, not Git artifacts.

## Remaining work

Both no-death flags read1; host alive at1HP, guest594/594. Actual boss-hit survival of **both** was not isolated/proven in this command-assisted kill. Keep that gate open, along with interruption/death recovery, wider supported-map and party-boundary cases, and raw-save/journal independence if required. No packaging, server redeployment, or custom managed-switch enablement.
