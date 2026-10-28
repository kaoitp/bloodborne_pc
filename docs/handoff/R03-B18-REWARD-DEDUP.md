# R03 B18: no second boss reward for a boss beaten in the guest's own world

2026-10-28, revision 2 after PR #17 review 1. Claude (R03 takeover). Source change, fixture-tested and built. **Native not run here** (steps below for the friend).

## Gap

[B15 normal replay](R03-B15-NORMAL-REPLAY.md) (Codex, native, default configuration, reward-once OFF):
- The guest had already beaten Amelia and held a Gold Pendant. It helped a host that had not beaten Amelia.
- After the kill, the guest got another reward obligation. Delivery retried while the old Pendant filled the one-item capacity.
- Once the old Pendant was used, a new one was inserted, and it survived a restart.
- The capacity only delayed the duplicate; it did not prevent it.

## Change

`NoteBbscBossRewardEvent`, the producer that queues a guest's boss reward:
- **Before** the B15 record check and the queue, it now asks `BbscOwnWorldHasFlag(event)`: is the boss's own event flag ON in the guest's **own** world?
- "Own world" is the own-world journal's copy of the flag's group (`bbsc_own_world`). It is kept before the join load (`CaptureBbscOwnWorldBeforeJoin`, map groups of kinds 1/5/6/7, areas 21–99, which covers every boss event group).
- The live table is not used: in the host's world it holds the host's flags.

| Journal copy of the group | Result | Log line |
|---|---|---|
| boss flag ON | not queued | `BBSC boss drop: event E - user U slot S has beaten this boss in its own world - not again` |
| boss flag OFF | unchanged (queued as before) | — |
| no copy of the group | unchanged (queued as before) | `BBSC boss drop: event E - own world unknown (no journal copy of group G)` |

This mirrors the game, which drops a boss reward once per world. The guard is **default ON** and needs no switch. It cannot add a grant; it can only skip one. It applies to every row in `BbscBossRewards`, with or without a taken flag, and independently of `SHADPS4_BBSC_REWARD_ONCE`.

### Owed ledger (revision 2)

Review 1 (P1): the guard alone loses a real obligation. A legitimate joint kill queues the reward while the add is refused (capacity); the shared-progress merge saves the boss bit; the game closes before delivery. The in-memory queue ends with the process, and the guard then refuses the next kill. B15's opt-in record does not hold it either: a failed add removes its attempt line, and a reward not attempted yet has no line at all.

So a queued reward is now also **owed on disk**, kept apart from the dedup decision:
- `<mod>/boss-rewards/owed-<user>-<slot>.txt`, one event per line. It is written when the reward is queued (`NoteBbscBossRewardEvent`).
- The line is removed only when the reward counts as given in `TickBbscBossRewards`: after the add or award, or when B15's record or the inventory says it was given (`NoteBbscBossRewardDelivered`, the only place that fills the given list).
- At start (`QueueBbscBossRewardsOwedAtStart`, right after B15's start settle), every owed line is queued again for its owner. Delivery stays owner-bound: another character's entry waits in the queue.
- A write or removal that fails is retried every second (`TickBbscBossRewardSaves`). The reward is delivered from memory meanwhile.
- Default ON, independent of `SHADPS4_BBSC_REWARD_ONCE`. Delivery is never inferred from boss progress: the guard only stops a **new** obligation.

Flag bit layout: the same as the other readers of the flag group bytes in the source (`0x80 >> (bit % 8)` in byte `bit / 8`, as in `AdmitBbscRewardEvent`, whose merges were confirmed natively in B09/native04).

## Evidence

- Fixtures, in `tests/test_bbsc_reward_once.py`. They reuse the actual `NoteBbscBossRewardEvent` and `TickBbscBossRewards` source:
  - default OFF: with the guest's journal holding 12401800 ON, two kills across a restart give nothing;
  - another bit of the same group ON with the boss bit OFF: given once;
  - no journal copy: given (existing behaviour);
  - reward-once ON with the boss bit ON: nothing given and no record line;
  - **review 1 sequence, both record modes:** add refused, kill (queued, owed line written), save, boss bit ON in the journal, restart (queued again from the owed line), add OK, kill: given **once**, owed line gone, nothing after a further restart;
  - **owner isolation:** A's owed reward is not given while B is loaded (B beaten, nothing for B); it is given to A once A is active;
  - **normal replay:** delivered at the first kill (no owed line left), used up, boss bit ON, restart, another kill: nothing, nothing owed.
- Queue checks in that fixture now count only the current character's entries: other characters' owed rewards wait in the queue too. The delivery fixture only gains the journal stub.
- RED, mutated sources in `.superpowers/claude-r03/b18/` (revision 1) and `b18/v2/` (revision 2):
  - check removed: fails ("adds == before_beaten");
  - LSB-first bit order: fails;
  - unknown own world treated as beaten: fails on the earliest grant;
  - no owed line written at the queue: fails the review 1 sequence;
  - owed lines not queued again at start: fails it too;
  - owed line kept after delivery: the reward is given again after a restart, which fails.
- All three fixtures pass on the change. The full Python suite gives the same result as on `seamless` 56bed5e (with B19) before the change: 181 ran, 48 skipped, 5 failures and 11 errors, all in the Linux-only `test_mods`, `test_packaged_vulkan`, `test_run_settings` and `test_cpu_compat`, identical on both.
- Patch regenerated from the reference tree (`git diff` equal to the tracked patch). DLL built locally with `tools/build_bbsc_mod.py`, revision 2 on 56bed5e (B19 included): `bbsc.dll` SHA256 `2d47822d91ceb5d3e8ce52253d56687e336ab908337132c2e6b1966adbf89056`. Not packaged.

## Limits

- **The journal must hold the guest's own copy.** The join capture runs from the `JoinSession_White` Lua event in the trace pipeline. If it were skipped, the group's first copy would come from another keeper (for example the host flag write). That copy is taken before the host's bits are written, but it is not proved natively for this guard.
- **Owed ledger write failures.** The owed line is written when the reward is queued and retried every second. A game that closes while that write is still failing, after the merge saved the boss bit, loses the obligation. A removal that fails until the game closes gives the reward again at the next start. Both need storage failing across the whole retry window. They are rare write-failure cases, like B15's, and are not fixture-proved beyond the retry.
- **An obligation from before this build** (queued by an older DLL) has no owed line.
- **The host's own drop** and a guest that never beat the boss are unchanged.
- **Other bosses:** covered by the same table and fixture logic. Natively, only Amelia is planned.

## Native check (friend's side, not run here)

This session does not run two instances (the user's session limit: token cost and RAM). Use the B15 normal replay setup unchanged, with this DLL:

1. Guest = native04's saved guest (Amelia ON, Pendant x1). Host = a copied pre-Amelia host. Reward-once OFF.
2. Join, then the guarded Amelia HP-zero as before.
3. **Expect** in the guest log, at the kill: `has beaten this boss in its own world - not again`. There must be no `queued for user`, no add line and no `finished` line.
4. At home, use the old Pendant: no new Pendant arrives (wait at least 60 s; read the inventory). Restart: Pendant count 0, Gold Blood Gem x1.
5. Control: a guest that never beat Amelia (native04's before-save guest) gets exactly one Pendant, as in native04. Its `owed-sd1-3.txt` appears at the kill and is gone after the `finished` line.
6. Optional, for the review 1 case: the control guest with the one-item capacity already full (holding a Pendant from a copied save of another run). Kill, then check that the owed line is there and the add is refused. Exit at the title after the save. Restart: `owed ... from an earlier run - queued again`. Use the Pendant: given once, the owed file is gone.

`tools/check_r03_native.py` has no case for this yet; grep the log lines above.
