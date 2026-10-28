# B15 normal replay: repeated Amelia reward

2026-10-28 (Asia/Bangkok), Codex. User requested ordinary reward-duplication testing instead of rare write-failure/save-race cases, and authorized unattended command-assisted gameplay on copied profiles. No product source/default changes.

## Result

**REPRODUCED-GAP with reward-once OFF:** a guest that already earned Amelia's Pendant in native04 restarts, joins a live-Amelia host, and earns a second reward obligation. While its old Pendant fills the one-item capacity, delivery retries. Using the old Pendant normally after returning home yields Gold Blood Gem x1; the queued reward then inserts a new Pendant. Capacity is not deduplication.

This is a test of the default configuration, not a failed test of the opt-in B15 implementation. B15 ON, rare persistence failures, other bosses, alternate character ownership and broader R03 acceptance remain untested by this run. No fix or default enablement is included.

## Composition

Checkout at start `a4d37b7`; unchanged native01/native04 composition:

| Input | SHA256 |
|---|---|
| DLL | `87319fd9c2bbf748d5ab3e9ad06fbab7376fb075edba86be5c451f9f8ea12cf6` |
| Probe | `6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14` |
| Reconstructed source, CRLF | `ee21b5e71dee64b3c39dcda8107fd34c4e703676f5dade701f9f07220910aad2` |
| Working patch, CRLF | `66be824139a15d74bf9862fb955b8fd2fe7816b1bcd4de4b3a3c4828f7de8ad1` |

Shared progress/items/Dream ON, spectate OFF, no-death=1, reward-once=0, home recovery=0, managed admission/application OFF. Existing distinct authorized accounts and self-hosted configuration; no service changes. Full private profiles under `.superpowers/r03-b15-replay`: host copied from native01 (before Amelia), guest copied from native04 after-save **with its existing journal retained**. The guest's save was never rolled back for this test. Resetting the copied host models helping another host who has not killed the boss; a third account/host identity was not tested.

## Native observations

1. Host PID14132, guest11068; 1250-group independent preconditions: host12401800 OFF, guestON. Guest's existing goods4001 x1 in slot84; visible U-I-AHH level10, held1/1, stored0/1. Host Kaori level34.
2. Verified existing native warp aid stages only the copied host at `(51.90,35.71,312.30)` in Cathedral. Host Hunt Bell and guest Kin Bell through ordinary inventory use. Guest placed20:36:23.757; collector baseline20:36:28.920. Guest own_world0/type1 at host map0x18000000. No guest position/flag/inventory writes.
3. Short scripted stick movement triggers the actual introduction. Read-only boss lookup confirms Amelia502000, handle268501105, type7, HP8051/8051. Existing guarded `native-aid.py 14132 kill` writes only this verified boss HP=0, with readback `AMELIA_HP_ZERO_CONFIRMED`.
4. Guest20:38:57.696:12401800 earned in party and queued for sd1/slot3.20:38:57.698 and later: direct goods4001 add refuses with fits0/slot-1/there=false. No successful second item while capacity is full.
5. Automatic return: exact original Clinic map0x18010000/lamp2412950/position/rotation, own_world1/type0. The pending duplicate continues retrying after return.
6. Use the old Pendant via Inventory -> Gold Pendant -> Use. Visible native Gold Blood Gem x1 popup confirms normal conversion.20:40:21.329: direct goods4001 x1 add now succeeds, fits1/slot85/there=true;20:40:21.340 lot50000001 finished. Independent read-only inventory confirms a **new** Pendant x1 in slot85. The original item was slot84. This process has exactly one successful new grant, in addition to native04's earlier grant.
7. Both Exit Game -> YES normally, then reached title. Guest slot3 last-write20:41:50; host slot0 last-write20:42:50. Saved copies protected privately; verified test processes stopped after title. Independent guest restart PID15248 uses the same saved profile/configuration and separate stdout/stderr filenames.

8. Fresh PID15248 visibly settled in Clinic: independent inventory confirms Pendant x1 in slot85, with zero fresh reward grants in this process. Exact original map/lamp/position/rotation and own_world1/type0 retained. Two settled snapshots of all1250 groups are identical; Amelia remainsON. This establishes persistence of the duplicate on the configured save+journal, not every auxiliary flag's semantics or raw-save independence.
9. `assert-result.py` exit0: timeline/one successful new grant/no restart grant, boss preconditions, exact origin, stable1250 and original3171 paths/SHA256 all PASS. The fresh process was explicitly stopped after these read-only reload checks; both initial clients had saved/exited to title before stopping. No game remains running.

## Commands and evidence

CLANG64 Python: `C:/msys64/clang64/bin/python.exe`. Private `prepare.py` copies profiles, records originals3171 and verifies source/artifact hashes. `launch-test.ps1 -Client a|b`, then `launch-reload.ps1 -Client b` uses the existing launch recipe outside the sandbox (known PS4 address-reservation limitation). Inputs use existing BB_PAD_FILE; 60ms directional pulses gave single steps, while110ms could move twice. Initial comma-separated CLI tokens did not form a PowerShell array; corrected before bell use. Computer Use screenshot approval initially timed out, then refresh/activation recovered; no permission bypass.

Existing `.superpowers/r03-close/read-position.py PID OUT`, `read-world.py PID OUT`; native04 guarded warp/boss helpers; private `read-pendant.py` reuses the existing bounded inventory reader with count validation instead of assuming count1. `assert-result.py` checks log ordering, grants, boss preconditions, restart state/origin and original-file integrity. Private logs: native01 DLL `bbsc-mod-20261028-201326-14132.log`, `201345-11068.log`, `204326-15248.log`. Raw saves/accounts/logs remain out of Git.

No fixture/build/full-suite rerun: runtime source is unchanged; this is native reproduction evidence. No packaging, deployment or message to the friend.
