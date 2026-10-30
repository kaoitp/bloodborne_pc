# R03 two-player playtest: investigation leads

2026-10-31 update: user subsequently authorized source fixes and took over playtest. [Source delivery](R03-PLAYTEST-SOURCE-FIX.md) records the bounded changes and offline checks; the no-code restrictions below describe the earlier investigation phase and are superseded. Gameplay conclusions in this evidence record remain unproved unless later user evidence establishes them.

2026-10-31: [execution/tracking plan PT00–PT09](../superpowers/plans/2026-10-31-r03-playtest-follow-up.md) now organizes these findings into ordered investigation, proposal and later implementation/validation tasks. This document remains the evidence record; no-code instruction remains active.

2026-10-30 (Asia/Bangkok). User requests investigation and possible remedies only: **do not change code yet**. Status: investigation checkpoint complete; all three gameplay issues remain open. No game launched, save changed, runtime setting changed, build or fixture run. Read-only source, captured native traces, event data and journal inspection provide the evidence below; these are not successful native reproductions or verified fixes.

## Composition and evidence boundary

User logs: private installed game's mod logs `212439-9084` and `223534-8828`, corresponding timelines and JSONL captures. Friend logs: private `r03-playtest-logs/friend`, particularly `221306-14380` mod log and `221307-14380` timeline. See [tracker](../WINDOWS-PROGRESS.md#two-player-playtest-follow-up--in_progress-2026-10-30) for original log hashes. Raw logs, assets, journals and saves stay outside Git.

Read-only SHA256 checks match the installed DLL to the [Echoes checkpoint](R03-RECOVERY-ECHOES.md). Relevant functions were inspected in its matching isolated source `.superpowers/echo-fix/source/emulator/src/core/bloodborne_re.cpp`; the older reference source was used for initial navigation only.

| Input inspected | SHA256 |
| --- | --- |
| Installed `bbsc.dll` | `0fc1e26aa2cc8763ed1d5daab078e39228a11a6c3f19aedbd2040e6ffea7800d` |
| Matching isolated `bloodborne_re.cpp` | `afd30f71c2286511b3f68aeebdda67a432bddd0dd960164dc8d05a75e1ade410` |
| Tracked integrated patch | `3ea98666374d56f165d151bd1711a9b3e8caa3277318201cf8b79d0c56a77408` |
| Installed `bin/bb-probe.exe` | `507b8528b33a5bff9055ffd1324867934018808325f9afbb295d24a98fb27139` |
| Existing diagnostic `r03-retry/profile-a/out/eboot.elf` | `cec1b276e7f9e4db978e57f524f41fbaac594530a3437b002e23f3fab14b4f86` |
| Game `m24_01_00_00.emevd.dcx` | `f6a580b0e827dd113393bd115fa0ce54f84b9f8f8ec1451ee62ba84d532fba17` |
| Latest archived `pending-sd1-4.bin.merged` | `086a1e9d12e50eda5b5e7d489144a5910929c0d0ed342a8f626c5388f35fc6dc` |

The probe differs from the earlier small-window diagnostic probe; this investigation does not attribute a source build to it. The friend's DLL was not supplied/hashed; matching build timestamps and hooks alone do not prove binary identity. Static disassembly uses an existing diagnostic ELF, not a byte-for-byte dump of the running patched game.

## 1. Boss gauge after interruption, before joining

Both cases are solo. Friend: own-world restore at 22:13:50.265, merge of 125 world bits in 5 groups at 22:13:55.369, Cleric Beast line at 22:13:55.485. User: restore at 22:36:10.407, merge of 94 world bits in 7 groups at 22:36:15.517, Gascoigne line at 22:36:15.528. Discord's separate local gauge read reports the same bosses about one second later. `TickBbscBossLine` reads the local gauge when there is no fresh host boss packet; a new process before joining cannot be explained by a prior process's in-memory host boss ID alone. It does not prove the boss was alive or attacking.

Strongest lead: `TickBbscSharedProgress` accumulates newly ON kind-1 map bits, and `MergeBbscSharedProgress` ORs them into the own-world table. It does not distinguish durable progress from temporary combat bits. A bit that later turns OFF on the host remains in that accumulated set.

Read-only parsing of the **latest** archived pending journal confirms `12414800`, `12414802`, `12414807`, `12414223` and boss reward-event bit `12411800` are all ON in its collection. This file belongs to the later completed visit, not the exact pre-22:36 crash input; do not claim it proves the earlier replay contents.

Using the existing EMEVD reader on the local game event file shows:

- Event `12414702` reads Cleric Beast start flags `12414700` / `12415400` and contains instruction `2003[11]` with boss name `500000`.
- Event `12414802` reads `12414800`, sets `12414223` / `12414800`, branches on `12414807`, and contains `2003[11]` for Gascoigne names `271000` / `272000`.
- Event `12414807` contains the transformation path and another `2003[11]` for `272000`.
- These event entries also reference completion flags `12411700` / `12411800`. Full instruction/control-flow semantics and event scheduling during delayed restore have not been dynamically validated.

Ranked hypotheses: (1) accumulated combat bits are replayed as permanent progress; (2) the 15-second own-world restore and later merge occur after map events have already initialized, leaving an event running even when completion is restored; (3) gauge state persists independently of event state. The first two can coexist. No evidence yet establishes boss resurrection or the crash cause.

Candidate remedy to investigate: exclude proven transient combat bits from durable collection/replay while retaining completed bosses, rewards and verified persistent map progress; inspect restore/merge timing if filtering alone is insufficient. Do not merely hide the gauge or clear whole map groups: those changes could conceal a live fight or destroy legitimate progress. Before implementation, enumerate the affected event bits and consumers rather than applying a broad numeric-range filter.

Discriminator: on copied profiles with protected pre-interruption input, read completion/start/transform flags and all three gauge slots before restore, after restore and after merge; observe the actual boss and map event state. Compare with normal solo load and normal co-op return. A remedy must preserve earned completion/rewards after independent save/restart and allow a genuinely unfinished boss fight to start normally.

## 2. Host -> guest wrong role, repeated bells and changed leave menu

The wrong role has a stronger static explanation than the UI text:

| User log time | Observed state |
| --- | --- |
| 22:06:04.549 | Host kept-death/reinsert path logs player type 0 |
| 22:06:08.849 | Host has `pending_type=0`; it remains 0 after respawn |
| 22:10:30.046 | Session is solo, own-world true; `pending_type=0` still present |
| 22:18:08.594 | Joining as guest: session 6, phase 3, sign -1, pending type 0 |
| 22:18:14.626 | `ReloadFinish` then `ApplySummonType` hooks execute |
| 22:18:15.929 | Own-world false, pending consumed to -1, but slot/character type both 0 |
| 22:18:18.925 | Warning confirms neither game counts the guest as a cooperator |
| 22:20:41.750 | Next join starts with pending type -1 |
| 22:20:48.283 | Next join finishes with slot/character type both 1 |

`llvm-objdump` at `0x0193949C..0x019394DB` shows native character creation reads slot manager `+0x8C`; if not -1 it copies that value to local slot `+0xA4`, applies it and clears pending to -1. It runs after the reload-finish call that invokes `ApplySummonType`. Thus a stale pending 0 can overwrite the normal phantom selection and is consumed on the failed join, explaining why the following join succeeds. Trace arguments and call chains for the two reloads match; these entries do not capture every memory write inside them.

The matching BBSC source writes `slots+0x8C` in `ArmBbscReinsertV8` only for `type > 0`. Its host-type-0 call therefore does not itself explain the producer of 0. Native death/respawn writers and cleanup are the next targets; the exact writer has not been identified. The earlier 21:54 respawn also leaves pending 0, while other respawns consume/reset it, suggesting a path/timing distinction. Blank alone is not established as the trigger.

Repeated banners occur roughly every 2.5 seconds in the bad visit; Insight rises 5 -> 14. Banner text was captured as empty, so the exact Hunt Bell/Blank wording and refund origin remain unproved. Do not implement an Insight subtraction from this observation. The kit defines Parting Blank `11251` from vanilla Blank `111`; the log detects an actual Parting Blank use at 22:18:59 and `OnLeaveMagic` follows. No trace currently proves which item/animation produced the unusual menu reported by the user.

Candidate remedy to investigate: correct the stale pending-role lifecycle before a new summon consumes it, preferably at its producer/cleanup boundary. Avoid forcing every guest to type 1 each tick: invader/duel modes and phantom creation flags need their legitimate native paths. Scope reaches native death/respawn, join handoff, own-world return and role consumers (cooperator count, menus, bell/search, drops and progress eligibility).

Discriminator: compare host respawn -> close session -> guest join against a fresh-process guest and host-without-death -> guest. Trace/watch `slots+0x8C` writes with caller and lifecycle context; record pending/sign/slot/character types immediately around character creation. A future fix needs first-attempt type1/cooperator success, normal bells/Blank/menu/return, no extra Insight, and death/rejoin/invader-role regression checks on copies.

## 3. Enemy-drop notice

Confirmed source path: `NoteBbscGuestEnemyDeath` -> `TickBbscGuestDrops` -> `GiveBbscGuestDrop` -> `AddBbscCarriedGoods`. After successful goods delivery, a separate block calls `BbscAnnounce(u"An item was added to your items.", "enemy drop")`, throttled to 15 seconds. Mod log entries pair the add and notice, e.g. 22:21:20.902. The notice is deliberate feedback, not evidence of reward failure.

2026-10-31 user clarification supersedes the notice-only proposal: the user confirms that, while a guest, monster loot is visible on the ground and can be picked up normally, and considers automatic compensation unnecessary. This is user gameplay evidence; the logs show automatic grants and pickups but do not identify both as the same enemy's drop. Duplicate delivery from a single enemy remains unproved.

Revised candidate: retire only the automatic ordinary-enemy compensation path (`NoteBbscGuestEnemyDeath` -> queue -> `TickBbscGuestDrops` -> `GiveBbscGuestDrop`) and its notice, preserving ground pickup and boss rewards. Check all callers/helpers before removal. The shared `SHADPS4_BBSC_GUEST_ITEMS` switch also gates `ApplyBbscGuestLootView`, `NoteBbscBossRewardEvent` and `TickBbscGuestItemsPickable`; turning it OFF globally would affect more than the compensation. No code or switch change yet, under the user's investigation-only instruction.

Before a later implementation, compare inventory counts immediately before death, after death without pickup, and after manual pickup on copied profiles; identify the same enemy/drop and compare host/guest, normal return and independent save/reload. Include Wandering Madness (the historical reason for compensation) and verify boss rewards separately. Acceptance is normal ground loot once, no automatic compensation/banner, and retained pickup persistence/boss rewards. Do not call duplication confirmed until the paired test demonstrates it.

## Checks and next action

Commands run: scoped `rg`, `Get-Content`, `Get-FileHash -Algorithm SHA256`; `llvm-objdump -d` on the existing ELF at `0x015C9850..0x015C9990` and `0x01939430..0x01939530`; read-only inline Python using existing `Emevd`/`bbfiles` with bytecode writing disabled; inline binary journal decode asserting magic, 125-byte group width and exact file length. All completed successfully. The objdump synthetic-section warning was present but the requested instructions were emitted. Initial searches for root `tools/gamedata` and shell-style wildcard arguments failed; the existing reader was found under the ignored BBSC reference. No gameplay or regression PASS is claimed.

Next: investigate native pending-role writer first, then capture the protected crash journal/event/gauge timeline. The later item change should target redundant ordinary-enemy compensation, per the 2026-10-31 clarification above. Gascoigne key and Echoes are confirmed received by the user; do not reopen a reward-loss claim based on `goods 4000` (item ID) or the later inventory warning alone.
