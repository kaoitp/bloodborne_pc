# R03 B17: durable origin after a guest crash, bound to its owner

2026-10-27, revised the same day after the PR #14 review. Claude (R03 takeover).

**Base:** seamless with PR #10 and PR #11. The source change is in the tracked patch (`bloodborne_re.cpp`). Matrix: G2-08 (interruption below 10 s) and the B16 case 2 origin GAP. A02 is the cross-character failure that kept the return behind an opt-in.

**State:** an owner-bound, bounded **opt-in candidate**. It is turned on by `SHADPS4_BBSC_HOME_RECOVERY=1`; the older `SHADPS4_BBSC_EXPERIMENTAL_HOME_RECOVERY=1` also works. It stays opt-in until the native gate below has evidence on a matching build. Fixtures cannot establish the game's warp, hook or save timing.

## The gap

In B16 case 2, the guest's game closed 5.8 s after the summon. After the restart its own flags were back, but it woke **in its own world at the host's spot**: a level-10 Clinic character in Cathedral Ward. That run was the pre-PR #11 composition. Its result is not attributed to this DLL.

The return to the journaled home spot (R02) existed only behind the experimental opt-in. In A02, a pending return crossed from EiEi to Kaori after Quit Game → title → Load.

## Change

**Owner binding.**
- The return is armed only from `RecoverBbscOwnWorldFile`, which runs only when the journal's save slot is the active slot (PR #11).
- A load from the title drops a pending return: `NoteBbscOwnWorldCharacterLoad` calls `SuspendBbscHomeRecovery()`. The journal file stays on disk, and the owner takes the return up again the next time it is home.
- Before every action, `TickBbscHomeRecovery` checks the owner. If the active save slot is unknown, it waits. If it is another character, the return is dropped and the file kept.

**Bounded per target (review P1).** Point first, then the recorded lamp. Each target gets `BbscHomeRecoveryMaxTries` = 3 tries.
- **An accepted request whose load never comes** times out after `BbscHomeRecoveryLoadTimeoutMs` = 30 s and counts as a failure of that target. Before this, it waited forever.
- **On any failure of the point** (refused, timed out, or arrived more than 5 m off or on another map), `FailBbscHomeRecoveryTarget` moves to a valid recorded lamp at once. It no longer repeats the point until the budget is gone. Without a valid lamp, the point is retried.
- **The arrival is checked before the budget.** A last try that arrives settles as a success.
- **An exhausted lamp**, or a point without a lamp, ends once. `SettleBbscHomeRecovery(false)` keeps the own world, keeps the journal as `.unreturned` (origin evidence; `.restored` only on arrival), and tells the player.

**Lamp request as a function.** The selector and transition are now `RequestBbscLampReturn(global, target)`, outside the recovery's code. The fixture stubs it, so the fallback is actually exercised.

**Unchanged:**
- A04's `ProtectBbscNativeJoin` (experimental variable only).
- The graceful trip home (`PutBbscHomeSpot`).
- No packaging, no deployment, and no local switch flipped on any profile.

## Fixture

`test_bbsc_home_recovery.py` compiles the actual code with ASan, from `struct BbscHomeSpot` through `NoteBbscHomeRecoveryLoad`, plus `NoteBbscOwnWorldCharacterLoad`. It uses the real `bbsc_home_spot.h`, a real journal file, a controlled save slot, and recorded point and lamp requests.

| # | Case | Expected |
|---|---|---|
| 0 | Default | Not armed (candidate). |
| 1 | B16 case 2 (opt-in) | Point → load → wait for the slot → `.restored`. |
| 2 | A02: title, then Kaori on the same map | No further warp, no lamp, file kept. The owner later takes it up again. |
| 3 | A02 with the title load missed | The slot check drops it at Kaori's first step. |
| 4 | A death before the return | Dropped, file kept, asked again on re-arming. |
| 5 | Accepted, but no load (review) | Still waiting at about 20 s; lamp asked after 30 s; lamp arrival `.restored`. |
| 6 | Point refused, valid lamp recorded (review) | One point try, then the lamp. |
| 7 | Last try works, no lamp (review) | Third point try arrives: `.restored`, no notice. |
| 8 | Point refused, lamp exhausted (review) | 1 point + 3 lamp tries, then `.unreturned` once, notice once. |
| 9 | No lamp, point never works | 3 point tries, then `.unreturned`. |
| 10 | Arrived on the map but far from the spot | Lamp, then `.restored`. |
| 11 | `=0` | Off. |

**RED/GREEN**, by mutating copies of the actual source in `.superpowers/claude-r03/b17/v2/`:

| Mutation | Result |
|---|---|
| No load timeout | RED at case 5 |
| Lamp only after an off-target arrival (the old behaviour) | RED at case 5 |
| Budget checked before the arrival (the old order) | RED at case 7 |
| Default on | RED at case 0 |
| No owner guards | RED at case 2 |
| Only the slot check removed | RED at case 3 |
| Only the title drop removed | GREEN: the slot check alone covers it |
| Current source | GREEN |

Against PR #14's first head `e149702`, the fixture stops at its source check, because there is no `FailBbscHomeRecoveryTarget` and no `RequestBbscLampReturn`.

`test_bbsc_own_world_owner.py` has a `SuspendBbscHomeRecovery` stub.

**Union** (seamless + this change, CLANG64 Python):
- All 8 `test_bbsc_*` modules: 9 tests OK.
- With `test_patches`, `test_native_bbsc` and `test_run_bbsc`: 32 OK, 1 skip.

**Hashes:**
- Patch `59dd1451d460a8c3f8b271ce73c3e42269c489bd43205e7d50bbcbaaa3ff9344`.
- LF source `19acf644bc1e188f9363a369177faf7f6e101e83a9fa2242030976dfb48064ee`; CRLF `586512e69c17632d553eee647a1fb3d950bef0942d96d38a3f1acc786d4f0c9c`.
- `bbsc.dll` `99733756b070059b25604941ee8209efc0bbf13316989d4e30b083da1f627f73`.

## Native gate: NOT run here (needs the friend's side)

**Why not here.** This is a practical limitation, not an R03 rule. The user set this session's limit: no long two-instance native runs, because of token cost and because each instance needs about 17 GB of RAM on the user's gaming PC. In-game steps go to the friend's side.

The gate also needs:
- a guest process killed within seconds of placement;
- for N2, menu steering through Quit Game → title → another character. Pad steering here could not do the menu typing reliably (see B16's assistance table).

**Concrete help needed:** one person running the host and the guest client on copied profiles for about 30–45 min, using the steps below.

Setup throughout: this DLL, `SHADPS4_BBSC_HOME_RECOVERY=1` on the guest, spectate off, copied profiles, host Kaori, guest U-I-AHH (level 10, Clinic).

**N1. Locked-map return.**
1. Join. Within 10 s of `placed`, kill the guest process.
2. Restart the guest and load U-I-AHH.

Expected in the log:
- `was left with another player's world in it`;
- `home recovery: user sd1 slot 3 goes back to 0x18010000`;
- `requested original point into 0x18010000 ... accepted true (try 1)`;
- `own world and return point settled`.

Then check: the position is within 5 m of the journaled spot on 0x18010000; the file is `own-sd1-3.bin.restored`; after quitting and reloading, U-I-AHH is still in the Clinic.

**N2. Title / other character.**
1. Repeat N1 up to `requested`.
2. Before the arrival, Quit Game to the title and load **another** character (EiEi or Kaori in profile a).

Expected:
- `a character is loading from the title`;
- the other character neither warps nor gets `settled`;
- no flag difference against its own baseline;
- `own-sd1-3.bin` still on disk.

Then load U-I-AHH again. It returns as in N1.

**N3. Lamp fallback, with save and reload.** Make the point fail. One way is to edit the journal's home-spot position to an unreachable value on a copy. Expected:
- `request refused` or `arrived elsewhere`, then `requested recorded lamp`;
- arrival at the lamp, then `settled`.

Quit, reload, and check that the character stays at the lamp with its own flags.

**N4. Without the variable,** N1 behaves as in B16: no warp.

## Limits

- Fixture evidence only, as above.
- An interruption before the journal's first write has no journal, so there is no return. A04 covers that only when it is on.
- The default stays off until N1, N2 and N3 pass on a matching build.
