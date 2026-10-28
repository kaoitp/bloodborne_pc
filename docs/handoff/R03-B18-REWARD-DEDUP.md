# R03 B18: no second boss reward for a boss the guest has beaten, ON by default

2026-10-28/29. Claude (R03 takeover). Revision 4 follows the owner requirement on PR #17 (issuecomment-6477809673): dedup is ON by default, and the two persistence failures are addressed. Source change, fixture-tested and built. **Native: revision 3 (opt-in) passed the friend's repeat-kill and never-beaten runs ([R03-PR17-NATIVE-VALIDATION](R03-PR17-NATIVE-VALIDATION.md)). Revision 4 is not run natively.**

## Gap

[B15 normal replay](R03-B15-NORMAL-REPLAY.md), native, default configuration:
- A guest that had beaten Amelia and held her Gold Pendant helped a host that had not beaten her. It got a second reward obligation.
- The one-item capacity held the obligation back. Once the first Pendant was used, a new one arrived, and it survived a restart.

## Design

### The guard

`NoteBbscBossRewardEvent` does not queue a new reward when either of these holds:
- the boss's event flag is ON in the guest's **own** world. That means the own-world journal's copy kept before the join (`BbscOwnWorldHasFlag`), not the live table, which holds the host's flags;
- the character's ledger has a `done` line for the event.

With no journal copy of the group, the reward is queued as before.

### The ledger

`<mod>/boss-rewards/owed-<user>-<slot>.txt` holds one line per event:

| Line | Meaning | Written |
|---|---|---|
| `owed <event>` | earned, not delivered | when the reward is queued; at every start it is queued again for its owner |
| `done <event> <time>` | claimed for delivery | **before** the item is added, after a fit check (`BbscBossGoodsFit`, the add's own check `0x014D9A80`) |
| (no line) | nothing pending | a `done` line goes once the boss flag is in the own world and the owner's save was written after it; from then on, the flag is the guard |

A bare `<event>` line (a revision 2 file) reads as owed.

### The ordering

The boss flag reaches the guest's own world through the **shared progress**: the collection at the kill, the pending progress file, and the merge at home. It does not go through the ledger, so the ordering is what keeps the two consistent:

1. **No line on disk, no boss flag.** An earned obligation whose line (`owed` or `done`) is not on disk keeps its boss flag out of the pending progress file **and** out of the merge (`HoldBbscUndurableRewardBits`, called by `WriteBbscPendingProgress` and `MergeBbscSharedProgress`).
2. **No claim, no item.** The `done` line must be written before the add. A claim that cannot be written means no add, and the line stays `owed`.
3. **An add refused after its claim reopens the line.** The `done` line goes back to `owed`, and a failed write is retried every second.
4. **The `done` line survives until the flag is saved.** A consumed item is never given again, even when the boss flag has not reached a save yet.

### The two owner cases

| Case | Old (rev 2/3) | Revision 4 |
|---|---|---|
| 1. The owed line cannot be written until exit, while the shared progress saves the boss flag | the obligation is lost (the guard refuses the next kill) | Nothing is delivered (no claim possible), and the boss flag is held out of the pending file and the merge. The run ends with neither the item nor the flag, so the next joint kill earns it again: **not lost** |
| 2. The line cannot be rewritten until exit after it became owed (the removal or claim fails) | the reward is delivered, then queued again at the next start: **duplicate** | The claim fails, so there is no add. The reward is delivered once after the restart, and its `done` line refuses it after that, consumed or not: **not duplicated** |

`SHADPS4_BBSC_REWARD_DEDUP=0` turns all of it off, restoring the earlier behaviour. It is independent of `SHADPS4_BBSC_REWARD_ONCE`.

## Evidence

**Fixtures.** `tests/test_bbsc_reward_once.py`, on the actual producer, consumer, ledger and hold functions. These cases run in **both** `REWARD_ONCE` settings, each character in its own save slot:
- default (variable unset) is ON: a guest beaten at home gets nothing, and nothing is owed. `=0` gives the old behaviour with no ledger;
- never beaten: given once. The `owed` line becomes `done` (claimed). There is no second grant in the same process or after a restart, even before the flag is saved. Once the flag is in the own world and saved after, the `done` line goes, and the flag guards from then on;
- no journal copy of the group: given once;
- beaten at home: nothing, no record line, nothing owed;
- **case 1:** the ledger is unwritable for the whole run. No delivery, and the boss bit is held out of the progress. Restart with storage back, kill: given once. The bit is no longer held once the line is durable;
- **review 1:** delivery refused (fit), the owed line on disk keeps the bit in the progress, the bit is saved, restart (queued again), kill: given once, and never again;
- **case 2:** owed, then every rewrite fails for the whole run. No delivery. Restart: delivered once. Used up, restart, kill: nothing;
- add refused after its claim: the `owed` line is reopened, and the next try gives it once;
- **owner isolation:** A's owed reward waits while B (beaten at home) plays, and goes to A once A is active.

A structural test asserts that the real `WriteBbscPendingProgress` and `MergeBbscSharedProgress` call the hold **before** they write or set anything. The progress fixtures only stub it.

**RED.** Mutated sources in `.superpowers/claude-r03/b18/v4/`. Each fails the fixture:

| Mutation | Fails at |
|---|---|
| default OFF | the default-ON case |
| no hold | case 1's hold |
| no claim before the add | case 1's "no delivery" |
| no reopen after a refused add | the reopened owed line |
| done line ignored by the guard | the "not again" check |
| done line never dropped | the dropped-line check |
| claim without fit check | review 1's owed line |

Earlier revisions' mutations are in `b18/`, `b18/v2/` and `b18/v3/`.

**Other suites.**
- The reward-delivery fixture runs with `=0`, the legacy behaviour; B18 has its own cases.
- The home-recovery, own-world-owner, party-progress, progress-backup and reorder fixtures pass.
- Full Python suite: 182 ran, 48 skipped, 5 failures and 11 errors. The failures and errors are the same Linux-only tests as on the `seamless` baseline.

**Build.** Patch regenerated from the reference tree (on `seamless` 56bed5e, B19 kept). DLL `bbsc.dll` SHA256 `44391ea0a61fbb22a3d089ec2bc977074499baca075603ccb86f50861747a5a5`, local, not packaged.

## Remaining limits (explicit)

- **A refused add after a positive fit check, then a reopen that cannot be written until exit, after the boss flag reached a save.** The `done` line stays on disk, and it refuses the reward, so it is lost. The fit check and the add run back to back on the game thread, so this needs the game to refuse an add its own fit check accepted a moment earlier, **and** lasting storage failure.
- **A `done` line whose boss flag never reached the own world.** For example, the shared progress pending file could not be written, or was lost, until exit. That line is never dropped, so it refuses that boss's reward in a later cycle of the same character (NG+). Nothing is duplicated or lost in the current cycle.
- **Storage failing from the start.** An obligation held out by case 1 also holds that boss's flag out of the shared progress for that party. It comes back with the next joint kill.
- **The journal must hold the guest's own copy** (the join capture), as before.
- **Obligations queued by a DLL older than revision 2** have no ledger line.
- **Non-goods award lots** (the two `12601850` / `13601800` rows) have no success signal and no fit check. They are claimed and then awarded.

## Native checks (friend's side, not run here)

This session does not run two instances (the user's session limit: token cost and RAM). Run revision 4's DLL with **no** `SHADPS4_BBSC_REWARD_DEDUP` set (the default):

1. Repeat the revision 3 cases unchanged. Expect the same results as [R03-PR17-NATIVE-VALIDATION](R03-PR17-NATIVE-VALIDATION.md):
   - repeated Amelia kill with the guest beaten: `has beaten this boss in its own world - not again`, consume the old Pendant, no replacement, Pendant 0 after a restart;
   - never-beaten control: one Pendant.
2. In the never-beaten control:
   - the ledger reads `done 12401800 <time>` right after the `finished` line;
   - after the trip home, the merge, and a save, it is gone (`boss flag saved ... done line dropped`).
3. **Persistence change, case 2 (optional, copied profiles):**
   - Kill with the never-beaten guest while its one-item capacity is full. The ledger reads `owed 12401800`.
   - Exit normally, restart, then free the slot: given once, and the line reads `done`.
   - Use the item, restart, kill again: nothing.
4. **Case 1 (optional):**
   - Make `boss-rewards/owed-<user>-<slot>.txt` a folder before the kill. Expect no delivery, and the merge log shows the boss flag not newly set.
   - Exit, remove the folder, restart: a later joint kill gives it once.
