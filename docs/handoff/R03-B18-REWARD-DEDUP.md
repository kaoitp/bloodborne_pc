# R03 B18: no second boss reward for a boss beaten in the guest's own world

2026-10-28. Claude (R03 takeover). Source change, fixture-tested and built. **Native not run here** (steps below for the friend).

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

Flag bit layout: the same as the other readers of the flag group bytes in the source (`0x80 >> (bit % 8)` in byte `bit / 8`, as in `AdmitBbscRewardEvent`, whose merges were confirmed natively in B09/native04).

## Evidence

- Fixtures, in `tests/test_bbsc_reward_once.py`. They reuse the actual `NoteBbscBossRewardEvent` and `TickBbscBossRewards` source:
  - default OFF: with the guest's journal holding 12401800 ON, two kills across a restart give nothing;
  - another bit of the same group ON with the boss bit OFF: given once;
  - no journal copy: given (existing behaviour);
  - reward-once ON with the boss bit ON: nothing given and no record line.
- The delivery fixture only gains the journal stub.
- RED, mutated sources in `.superpowers/claude-r03/b18/`:
  - check removed: fails ("adds == before_beaten");
  - LSB-first bit order: fails;
  - unknown own world treated as beaten: fails on the earliest grant.
- All three fixtures pass on the change. The full Python suite gives the same result as on `seamless` 28c85ba before the change: 181 ran, 48 skipped, 5 failures and 11 errors, all in the Linux-only `test_mods`, `test_packaged_vulkan`, `test_run_settings` and `test_cpu_compat`, identical on both.
- Patch regenerated from the reference tree (`git diff` equal to the tracked patch). DLL built locally with `tools/build_bbsc_mod.py`: `bbsc.dll` SHA256 `08b4f00fe918f51d23b0d8f6b5784f044509c1516cd6f09bc231bdf8f19bbe47`. Not packaged.

## Limits

- **The journal must hold the guest's own copy.** The join capture runs from the `JoinSession_White` Lua event in the trace pipeline. If it were skipped, the group's first copy would come from another keeper (for example the host flag write). That copy is taken before the host's bits are written, but it is not proved natively for this guard.
- **Delivery that never happened.** If an earlier party queued the reward and then the shared-progress merge saved the boss flag into the guest's own world without the item ever being delivered (game closed mid-retry), the next party will not give it either. The B15 record (opt-in) is the place for that case; it is not changed here.
- **The host's own drop** and a guest that never beat the boss are unchanged.
- **Other bosses:** covered by the same table and fixture logic. Natively, only Amelia is planned.

## Native check (friend's side, not run here)

This session does not run two instances (the user's session limit: token cost and RAM). Use the B15 normal replay setup unchanged, with this DLL:

1. Guest = native04's saved guest (Amelia ON, Pendant x1). Host = a copied pre-Amelia host. Reward-once OFF.
2. Join, then the guarded Amelia HP-zero as before.
3. **Expect** in the guest log, at the kill: `has beaten this boss in its own world - not again`. There must be no `queued for user`, no add line and no `finished` line.
4. At home, use the old Pendant: no new Pendant arrives (wait at least 60 s; read the inventory). Restart: Pendant count 0, Gold Blood Gem x1.
5. Control: a guest that never beat Amelia (native04's before-save guest) gets exactly one Pendant, as in native04.

`tools/check_r03_native.py` has no case for this yet; grep the log lines above.
