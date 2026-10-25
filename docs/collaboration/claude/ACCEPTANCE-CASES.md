# CL01-C: executable acceptance cases

Owner: external Claude Code. These are specifications for Codex's R03/R04 runs. **Execution status of every case: NOT RUN.** Claims refer to A-xx in [BBSC-002-MAP.md](BBSC-002-MAP.md) and B-xx in [IDENTITY-PROTOCOL.md](IDENTITY-PROTOCOL.md). Symbols are from the pins listed there. No offsets, APIs or results are invented: wherever a value must be observed, the case says which log line or save to capture.

## Common setup (applies to every case unless stated)

- **Clients.** H (host) and G (guest) use two distinct existing authorized accounts. Each has its own copied `BB_USER_DIR`, its own DLL folder copy (A-C2), and `BBSC_SAVE_DIR=<its BB_USER_DIR>\savedata\<id>\CUSA00207\SPRJ0005` (A-C1). Use separate P2P ports if both run on one PC. Some cases need a third account H2 for a second host; mark them WAIT_DEP when none is available.
- **Builds and launch configurations.** Every run names one, with its source commit and the effective value of `SHADPS4_BBSC_WARP_JOIN`:
  - **BASE** (frozen baseline): K `f3734da` source build plus the official `bbsc.dll` / `bbsc-launch.exe` (hashes in R02), pinned defaults. `SHADPS4_BBSC_WARP_JOIN` is then on ([B bbsc_persistence.h L34](https://github.com/CLSAMG22/BBSC/blob/4f11faf88b6ba658ebde6fe5fbefdadedba4fa41/emulator/src/core/bbsc_persistence.h#L34)), so a cross-map join requests one more full reload.
  - **J01** (Codex R04-J01): the same binaries, launched by `run.py` from `seamless` `af235b3` or later, which sets `SHADPS4_BBSC_WARP_JOIN=0` when `BBSC_EMULATOR` is set and the variable is empty ([R04-JOIN-RELOAD.md at bd24679](https://github.com/kaoitp/bloodborne_pc/blob/bd24679c7655a97bd4d9fba2b11ee079e6033751/docs/handoff/R04-JOIN-RELOAD.md)).
  - Other delta runs name their source commit. Do not mix evidence from different configurations.
- **Services.** Placeholders `<S>` (shadNet) and `<G>` (game server). Use the copied `host_overrides.custom.json` through `SHADPS4_HTTP_HOST_OVERRIDES_JSON`, `BBSC_RELAY=<G>:20444` and `SHADPS4_P2P_RELAY=<G>:3478` (B-07 split table). The deployed version is UNKNOWN; record it if the user already knows it, without asking.
- **Every run.**
  - Before: copy both saves aside and record their SHA256.
  - Check the DLL log for `Image verified … byte patch sites written` and `HTTP: game's HTTP calls wrapped`.
  - Capture: DLL `logs/bbsc-mod-*.log` and `bbsc-timeline-*.txt`, BBport stdout/err, and the server logs when the user can provide them.
  - Keep logs private.
- **Startup retry.** A `bbsc.dll+0x1933` fault (A-C3) is a startup retry, counted separately. It is not a case result.
- **Cleanup.** Close normally (Blank or quit to title, then `CloseMainWindow`). Restore the copied saves before the next case. Never touch original saves.
- **Evidence types.** SRC (source), NAT (native log line), GP (user gameplay observation), SAVE (state after reload).

## Service and route cases

| ID | Required outcome / claims | Setup and action | Boundary (producer → consumer) | Expected | No-side-effect assertions | Evidence | Status / blocker |
|---|---|---|---|---|---|---|---|
| SVC-01 | Distinct identities (B-10) | Log in H and G. From the game-server log or the DLL log, take each `UserId` | `/basic_utils/login` → `identity_for` | The two `UserId`s differ. If they collide, pick other existing accounts; do not create any | — | NAT | NOT RUN |
| SVC-02 | No required public endpoint (outcome 11; B-03/04/07) | One H+G session. Capture every HTTP host the BBport log and the DLL `HTTP:` lines name | overrides → `ApplyBloodborneSeamlessRoute`; DLL wrappers | Only `<S>` and `<G>`. No thehuntersdream.com, play.seamlesshunt.com or bbbridge. The launcher pool is not `huntersdream` | — | NAT | NOT RUN |
| SVC-03 | Is :20444 required for cross-map join? (B-F1 conditional, A-03) | J01. (a) Channel only: :20444 unreachable for both clients (configuration only, no redeploy): same-map, then cross-map, with the same non-empty password. (b) :20444 reachable, as a control | host `RelaySendAimedPlacement` → relay **or** `P2PChannelSend` → guest `OnAimedHostPlacement` → `RewriteAreaId` → broker `Advertise` | Source does not decide (a) (B-F1 §2). Record: host claim time versus the first `signaling connection active` channel peer, whether the aimed frame reached a peer, any re-claim, and on G `host … rang our sign` / `connect-first - sign AreaId`. A REPRODUCED-GAP is only what is observed | G stays in its own world after a stall. G's save is unchanged | NAT + GP | (a) NOT RUN. (b) Codex 2026-10-24: relay connected, Cathedral Ward → Dream joined (relay-backed success only) |
| SVC-04 | P2P-channel fallback after a join (B-06, B-12) | Same-map join with :20444 unreachable. Then: H walks into the next area; H lights a lamp | `SendFrame` → `P2PChannelSend` → guest `Dispatch` `from_our_host()` | Record whether G logs channel peers, follows H, and receives world flags or progress (`shared progress: the host has … boss flag(s)`) | — | NAT + GP | NOT RUN |
| SVC-05 | UDP transport relay on the split host (B-07, B-13) | A session with a real peer exchange and `SHADPS4_P2P_RELAY=<G>:3478` | `RelaySetServer` → `Relay._shad` → other client | **Preflight only:** client `P2P relay fallback: server … (forced for every peer)`; server `shadPS4 relay: <npid> registered` for both. **Route proven:** during the exchange, both clients' `… frame(s) sent / … received through the relay so far; peers: …` lines show rising counts and name the other as `relay` (K p2p_sockets.cpp L754-772), or equivalent captured forwarded frames | — | NAT (both clients; server if available) | NOT RUN by this audit. Codex 2026-10-24 (R03 retry) recorded bidirectional counters with named counterparts in one same-map exchange |
| SVC-06 | Game-server outage mid-session (outcome 11 robustness) | Stop only the user's game server for 2 minutes during a joined session, then start it. Only with the user's permission and without a redeploy | relay reconnect loop (B-05) | Record the behavior. Required: G's saves are intact, and a later departure still returns G home | Saves intact | NAT + GP + SAVE | NOT RUN; needs the user's OK, otherwise WAIT_DEP |

## G1: join

| ID | Required outcome / claims | Setup and action | Boundary | Expected allowed / rejected | No-side-effect assertions | Evidence | Status / blocker |
|---|---|---|---|---|---|---|---|
| G1-01 | Cross-map join beside the selected host (1, 2; A-03, A-05) | **J01.** Same non-empty password "P". H in Cathedral Ward, G in Central Yharnam (both lamps lit). H rings the Hunt Bell, G rings the Kin Bell | as SVC-03, then `ApplyCrossMapSummonGuestPlacement` (native reload) and the join teleport | One native load into H's map. G ends within a few meters of H. Logs: `connect-first: placement written`, `summoned reload finished in host map` | J01: no second forced `StageTransition` during the join. H's world flags are unchanged. (Under BASE a second reload is expected from source and was observed by Codex; it is BASE evidence, not this case's expectation) | NAT + GP | NOT RUN |
| G1-02 | The same in the opposite direction, across areas (1) | H in Old Yharnam or Forbidden Woods, G in Cathedral Ward | same | same | same | NAT + GP | NOT RUN |
| G1-03 | Dream as source and target (1; A-04) | (a) H in the Dream, G in a story map. (b) G in the Dream, H in a story map. Password "P" | same, plus the Dream present/restore | Join succeeds both ways. After G goes home, G's Dream state (Doll, workshop, messengers' items) is G's own | G gets no Dream progress or starter items from H (B bloodborne_re.cpp L11081-11087 rule) | NAT + GP + SAVE | NOT RUN by this audit. Codex 2026-10-24 (R04-J01), (a) H in the Dream, G from Cathedral Ward: J01 joined, adjacent placement, Parting Blank returned G home; BASE did the extra reload and the return failed. (b) open |
| G1-04 | Same **non-empty** password required cross-map (2; A-01, B-09) | Different maps: (a) H none, G "P". (b) H "P", G "Q". (c) both none | broker `MatchesSearch` → `Search` (Preparing) | **Required:** no cross-map join and no warp in (a), (b) and (c). Source prediction for the baseline: (b) refused, (a) and (c) **joined**. A candidate gap becomes REPRODUCED-GAP only when observed | G never loads H's map, and its position and world are unchanged | NAT (shadNet `preparing cross-map` if the user provides it) + GP | NOT RUN |
| G1-05 | Wrong, stale or failed join leaves the guest's world unchanged (A-05, A-07, B-11) | (a) H rings G's sign, then quits before the join completes. Within 90 s H2 (password "P") rings. (b) G kills and restarts its game mid-handshake and rings again | `OnAimedHostPlacement` (90 s freshness), broker one-claim rule, first-create forced delete | G joins only the host whose claim was delivered, or none. It never loads one host's map and then sits beside the other. After the restart, G starts clean | No placement from an earlier attempt is applied. G's world and save are unchanged after a failed join | NAT + GP + SAVE | NOT RUN; (a) WAIT_DEP on a third account |
| G1-06 | Existing same-map rules are kept (2; A-02) | Same map, no password, levels far apart (more than 10 + level/5) | broker anywhere mode | Record the baseline. The source predicts a match. Decision for the user/Codex; not a goal blocker | — | NAT + GP | NOT RUN |
| G1-07 | A map locked in G's own world can be visited (3; A-06) | G has never reached H's map (e.g. G new in Central Yharnam, H in Cathedral Ward) | native summoned reload | Join succeeds. After going home, G has **not** unlocked that map's lamp or progress, apart from jointly earned events | G's own lamps are unchanged except for eligible events | GP + SAVE | NOT RUN |

## G2: progress and rewards

Before each case, record the selected boss flags, lamps and shortcuts of both saves. A dump tool is Codex's to choose. In-game observation (lamp list, boss arena state) is acceptable for GP evidence.

| ID | Required outcome / claims | Setup and action | Boundary | Expected | No-side-effect assertions | Evidence | Status / blocker |
|---|---|---|---|---|---|---|---|
| G2-01 | No import of older host history (5; A-09) | H has killed Cleric Beast and Father Gascoigne and opened the Cathedral shortcuts. G has none of these. G joins; nobody kills a boss. G uses a Blank, saves, quits and reloads | `TickBbscSharedProgress` → `MergeBbscSharedProgress` | **Required:** G gains none of H's earlier bosses, shortcuts or lamps. Source prediction for the baseline: they **are** gained (log `shared progress: … boss flag(s)`) | G's stats, items, echoes and Insight are unchanged | SAVE + NAT | NOT RUN |
| G2-02 | Jointly earned boss persists with its reward once (5, 6, 8; A-11) | Neither player has the target boss (e.g. Cleric Beast). G joins, they kill it together, G goes home, saves and reloads. H also reloads | boss-reward hook (19-event table) → native lot; collector → merge | Both saves show the boss dead after reload. G received the event's lot exactly once | No other H history (with a delta). NPC states unchanged | SAVE + GP | NOT RUN |
| G2-03 | Eligibility starts when G is playable (9; A-08) | H kills a boss while G is still in the first join load, before G is playable | collector start (state 6, player type 1) | That kill does **not** count for G | — | SAVE + NAT | NOT RUN; the exact "playable" observation point is defined by Codex |
| G2-04 | Eligibility continues through death and loading, and ends at departure (9; A-08) | (a) G dies (kept death / spectate) and H kills a boss while G is dead. (b) H follows a lamp to another area, then they kill a boss. (c) G leaves, then H kills a boss | collector across death and loads; end at departure | (a) and (b) count for G. (c) does not | — | SAVE + NAT | NOT RUN |
| G2-05 | Own progress is kept, no rollback (6; A-10) | G is ahead: it has a boss and a lamp that H lacks. G joins and goes home | own-world restore → add-only merge | After reload, G still has its own boss and lamp | No flag goes from 1 to 0 in G's save | SAVE | NOT RUN |
| G2-06 | Conflicting NPC choices are kept (6; A-10) | (a) H and G made different choices for one NPC quest before joining (e.g. a survivor sent to a different refuge). G joins, they play, G goes home. (b) During the joined session H changes or advances that NPC in a way that conflicts with G's state | kind-1 merge (kinds 6/7 excluded) | G's NPC quest state is unchanged in (a) and (b). A first-seen baseline (A-09) alone is expected to fail (b), because it imports every bit that changes during the session | No quest-phase flag is copied from H | SAVE + GP | NOT RUN; needs per-flag inspection |
| G2-07 | No duplicate or missing reward (8; A-11) | (a) G has already taken a boss's lot; the event repeats in a joint kill: the repeat lot or nothing, never a duplicate key item. (b) Where a boss flag reached G only through the merge (G2-01 baseline path), check whether its required item is now unobtainable | boss-reward table first/repeat lot; loot view | (a) no duplicate. (b) Record; a loss is a further gap tied to A-09 | — | SAVE + GP | NOT RUN |
| G2-08 | Each save/reload, and a crash while a guest (A-12) | After G2-02's kill, kill G's process: once less than 10 s later, once more than 10 s later. Restart G alone (offline is fine) and load the same character | pending file (10 s) → recovery when home: `RecoverBbscOwnWorldFile` then `LoadBbscPendingProgress` | More than 10 s: the kill merges at the next home load. Less than 10 s: it may be lost; report that honestly. Own-world groups come back before the merge | No H history in G's own world beyond eligible events. No double merge on a second reload | SAVE + NAT (`own world restored after a crash`) | NOT RUN |
| G2-09 | **Conditional on a persistence delta:** wrong character (A-C1, B-14) | G has characters in slots 0 and 1. It joins with slot 0, the process is killed, then G loads slot 1 first | newest-write slot selection → pending and journal file keys | Slot 1 receives nothing from slot 0's files. Slot 0 recovers on its next load | No cross-slot writes | SAVE + NAT | NOT RUN; required only if R04 changes persistence |
| G2-10 | **Conditional on a persistence delta:** write or backup failure (A-12) | Make the DLL's `save-backups/` or `shared-progress/` folder unwritable before going home | `BackupBbscSaves` → merge proceeds (baseline) | Baseline: record. A delta must not merge without a backup unless it shows an explicit warning, and the original saves must stay intact | Originals intact | SAVE + NAT | NOT RUN; required only if R04 changes persistence or merge |

## G3: departure and return

| ID | Required outcome / claims | Setup and action | Boundary | Expected | No-side-effect assertions | Evidence | Status / blocker |
|---|---|---|---|---|---|---|---|
| G3-01 | Normal departure returns G home (4, 7; A-13, A-15) | G joins from a known spot, they follow H through one lamp warp, then G uses a Silencing Blank. Repeat with H blanking G | `KeepBbscHomeSpot` → `PutBbscHomeSpot` at the forced-warp map choice | G loads at its pre-join spot in its own world, with its own flags plus eligible progress. Log: `trip home goes back to where we joined from` | G does not land in H's last area of its own world | GP + SAVE + NAT | NOT RUN |
| G3-02 | Disconnect (4; A-15) | Kill H's process during a session | `TickBbscStrandedGuest`; own-world restore | G gets home after the baseline grace period, with its own world | No H flags remain in G's world after reload | NAT + GP + SAVE | NOT RUN |
| G3-03 | Interrupted session: reload, fallback lamp (4, 7; A-13) | Kill G's process while it visits H in a map G has not unlocked. Restart G and load the character | save position + own-world journal recovery (the kept spot is memory-only) | Record where G loads. Required: its own world at a valid spot or its pre-party lamp, with the journal restored. Landing in a locked map, or being stuck, is a REPRODUCED-GAP against outcome 4 | Copied originals are not needed for recovery | NAT + GP + SAVE | NOT RUN |
| G3-04 | Save/reload on both sides after departure (acceptance) | After G3-01, both players save, quit and reload | native save | Each player has only their own world plus eligible events | — | SAVE | NOT RUN |
| G3-05 | Original point no longer valid (7; A-14) | G joins from a spot that newly earned progress invalidates (e.g. inside an arena or a gate area that changes when the boss dies). They earn that event, then G leaves | `PutBbscHomeSpot` with no validity check | Required: a valid spot or the pre-party lamp. Record what the baseline does | G is not stuck or out of bounds | GP + SAVE | NOT RUN; Codex picks a concrete spot |
| G3-06 | Host enters an unsupported area (10; A-16) | During a session, H enters a Chalice Dungeon. Separately: H in a Chalice Dungeon rings the bell while G is in a story map | follow (`OnBbscHostFollowPacket`) and placement with no area-29 filter | Required: co-op ends, G is notified and returns safely. Baseline: UNSUPPORTED, so record what happens. A delta is made only if the result is unsafe | G's save is intact after reload | NAT + GP + SAVE | NOT RUN |

## Coverage of the 11 product outcomes

| # | Outcome (short) | Cases | Evidence needed | Blockers / notes |
|---|---|---|---|---|
| 1 | Story maps and Dream; Chalice excluded | G1-01, G1-02, G1-03, G3-06 | NAT + GP | Name BASE or J01 per run. Relay necessity is open (SVC-03). Codex has one J01 Dream case (G1-03(a)) |
| 2 | Same non-empty password cross-map; same-map rules kept | G1-04, G1-06, SVC-03 | NAT + GP | candidate gap A-01/A-02. Deployed broker UNKNOWN |
| 3 | Locked own-world map does not block the visit | G1-07 | GP + SAVE | — |
| 4 | Pre-party map, position, heading and lamp kept, incl. after process exit | G3-01, G3-02, G3-03 | GP + SAVE + NAT | candidate gap A-13 (memory-only spot, no lamp) |
| 5 | Show host world; share only jointly earned events; no older-history import | G2-01, G2-02, G1-03 | SAVE + NAT | candidate gap A-09 |
| 6 | Add verified progress, keep own progress and NPC choices, no whole-group copy | G2-05, G2-06, G2-02 | SAVE + GP | candidate gap A-10 (whole kind-1 OR). A first-seen baseline does not satisfy it alone: it also needs the verified-event filter and G2-06(b) |
| 7 | Original point if valid, else the pre-join lamp | G3-01, G3-03, G3-05 | GP + SAVE | candidate gap A-14 (no validation) |
| 8 | Verified rewards, no duplicate or re-grant | G2-02, G2-07 | SAVE + GP | — |
| 9 | Eligibility from playable, through death and loading, until departure | G2-03, G2-04 | SAVE + NAT | Codex defines the "playable" observation point |
| 10 | Unsupported area: end, notify, safe return | G3-06 | NAT + GP + SAVE | UNSUPPORTED in the baseline (A-16) |
| 11 | Self-hosted services; no required public endpoint | SVC-01..SVC-06 | NAT (client + server) | Channel-only route open (SVC-03); UDP route needs transfer counters, not registration (SVC-05); SVC-06 needs the user's OK |

Persistence-failure cases G2-09 and G2-10 are conditional on an actual R04 persistence change.

**Suggested R03 order:**
1. SVC-01, SVC-02, SVC-05: identity and routes.
2. SVC-03(a) and SVC-04: the relay question.
3. G1-01 and G1-03 under J01 (G1-03(a) already has Codex evidence).
4. G1-04, G2-01: the two main candidate gaps.
5. G2-02, G2-05, G3-01..03, G2-08.
6. The rest.

Only observed failures feed R04, under the plan's five-part change rule.

## CL02-C: focused P01 progress matrix (2026-10-24)

CL02 section. It reuses the G2 IDs above and adds G2-11..G2-19. **Execution status of every row: NOT RUN.** Claims: A-17..A-32 ([BBSC-002-MAP.md § CL02-A](BBSC-002-MAP.md#cl02-a-progress-and-reward-contract-for-p01-2026-10-24)) and B-15..B-28, constraints C1-C4 ([IDENTITY-PROTOCOL.md § CL02-B](IDENTITY-PROTOCOL.md#cl02-b-progress-ownership-ordering-and-recovery-p01-2026-10-24)).

**P01 run rules (in addition to the Common setup):**
- **Configuration.** Every run names its configuration. **J01** is the launch, with or without the P01 delta (source commit named). A **BASE** run is a reference only.
  - Codex already has one BASE-equivalent observation: J01 launch, no progress delta, 7 entries merged without a joint event (Codex 2026-10-24, A01).
- **Snapshots.** For both copied saves, take before/after snapshots of:
  - the 57 listed flags (A-23..A-25);
  - the kind-1 groups of the areas visited;
  - the inventory goods of the 19 reward rows (A-29), plus their taken flags and get flags.
  - The tool is Codex's choice. A snapshot is taken with the game at the title screen or closed, never while loading.
- **Logs.** Capture `shared progress (…): merged into our own world - <n> boss flag(s) newly set (of <m> …), <b> world flag(s) …; saves backed up first: …` and every `BBSC boss drop: event …` line. These counts are cross-checks; the snapshots decide.
- **Cleanup.** After every row: both players save and quit, then restore both copied saves from the before-copy. Remove that row's `shared-progress/pending-*` and `own-world/own-*` files from both DLL folders, after copying them into the row's private evidence.

| ID | Precondition | Production boundary | Action / observation | Required assertions | Blocker / status |
|---|---|---|---|---|---|
| G2-01 (P01) | H has killed at least two listed bosses that G has not, and is later in the night (A-23, A-25). G has neither | A-17 → A-18 baseline → A-22 | G joins and waits until playable. Nobody fights. G departs, saves and reloads. H saves and reloads | G's listed flags and kind-1 groups after reload equal G's before-snapshot. The night follows the A-25 decision. H unchanged | NOT RUN. Needs the A-25 decision (G2-14) |
| G2-03 (P01) | H stands at a boss fog with the boss alive in both worlds | B-16 playable start; A-18 | G joins. H kills the boss **before** G is playable (during G's join load; Codex marks the playable time from the B-16 predicate) | That boss's listed flags are not admitted for G. No reward line for G. Source prediction for the existing reward path: a `reward queued` and an `item lot … given` line **can** appear, because enqueue is state-6 only and the tick has no playable gate (A-27); record it as a REPRODUCED-GAP if observed. A receipt-time baseline is also predicted to admit the kill when a pre-kill packet arrives after the playable start (C1) | NOT RUN. Timing needs a scripted host action |
| G2-02 (P01) | Neither player has boss X (one of the 19 rows with a taken flag, e.g. row 6) | A-27 reward; A-18 admission | G joins and is playable. They kill X together. G departs, saves and reloads. H reloads | G's save has X's listed flags only (no other H history). G got X's lot once (one `item lot … given` line). H's save has its own normal kill | NOT RUN |
| G2-04 (P01) | Like G2-02, with two more bosses Y and Z alive for both | B-18 death/loading; B-19 departure | (a) G dies (kept death) and H kills Y while G is dead. (b) H travels through a lamp, G follows, and they kill Z. (c) G leaves, then H kills a third boss W | (a) and (b) admitted, and kept after both reloads. (c) not admitted. If state 6 does not hold through (a) (Q8), record that as a REPRODUCED-GAP, not a pass | NOT RUN |
| G2-05 (P01) | G is ahead: boss V and a lamp that H lacks | A-22 merge + B-22 own world | G joins, plays, departs, reloads | G keeps V and its lamp. No listed flag of G goes 1→0 | NOT RUN |
| G2-06 (P01) | (a) H and G made different choices for one NPC quest before joining. (b) An NPC step H can take during the session that G has done differently | A-26 (kind-1 unclassified), kinds 6/7 excluded | G joins. In (b), H takes the conflicting step while G is playable. G departs and reloads | G's NPC state unchanged in (a) and (b), checked on the NPC in game and in the per-flag before/after diff of that NPC's flags. A P01 delta that still collects unclassified kind-1 bits is expected to fail (b) | NOT RUN. Codex picks the NPC; needs per-flag inspection |
| G2-07 (P01) | G already took boss X's lot in its own world | A-28, A-29 | (a) Row with a taken flag: a joint kill of X in H's world. (b) Row with taken flag 0 and a goods get flag (rows 3, 8, 10, 15, 18): a joint kill in a **new game run** | (a) Repeat lot or nothing, never the first lot again. (b) Baseline: the first lot is given again, a source-predicted REPRODUCED-GAP if observed. With the A-29 check: nothing given | NOT RUN |
| G2-11 | Like G2-02, but the session breaks before the kill completes. Variant: G restarts its game between attempts | B-20 rejoin; A-28 run memory | (a) G leaves and rejoins the same H in the same run; they kill X. (b) The same after G restarts its game | X's lot given once in total over (a) and once over (b). None of H's history from before the first session is admitted, and X's flags are admitted once. Whether the rejoin to the same H is a new epoch is open (C4, B-28); record whether the lock was released between the sessions | NOT RUN |
| G2-12 | G earned boss X's reward earlier, then consumed or used it (Codex picks a consumable row or a key used on a door) | A-30 | Joint kill of X again in another H world | Not re-granted. The inventory check alone does not count (A-30). Record which existing flag blocked it | NOT RUN. Needs a row with a consumable reward |
| G2-08 (P01, conditional on the P01 delta) | After G2-02's kill | B-21 pending file | Kill G's process 5 s and 15 s after the kill. Restart and load the same character | More than 10 s: X merges at the next home load and nothing else does. Less than 10 s: may be lost; report it. Own-world groups restored before the merge | NOT RUN |
| G2-13 | Conditional on a P01 delta that changes the file magic. G's DLL folder holds a baseline `pending-*.bin` (`BBSP`) for the test character, with H's history in it | B-23 | Start the P01 build, load the character at home, then join and depart once | The legacy file is not merged, either at home or at the first state-6 tick. It stays on disk, or is renamed as Codex decides. Its content is unchanged. G's flags equal the before-snapshot plus eligible events only | NOT RUN |
| G2-09 (P01, conditional) | G has characters in slots 0 and 1. In one run it saves slot 0, then loads slot 1 and joins before slot 1 is written | B-24 | Kill during the session. Restart and load slot 0, then slot 1 | Slot 0 gets nothing from slot 1's session. Slot 1's eligible entries arrive only on slot 1. A cross-slot write is a REPRODUCED-GAP | NOT RUN |
| G2-10 (P01, conditional) | Make the DLL's `save-backups/` unwritable before G's trip home | B-25 | Depart after an eligible kill | Record the merge behavior. A delta that changes persistence must not merge without a backup unless it shows a warning. Originals intact | NOT RUN |
| G2-14 | H is later in the night than G; no joint event | A-25 | G joins, plays, departs, reloads | Record G's night after reload (baseline: moved to H's). This row records the decision Codex/user take on A-25. It is not a fix by itself | NOT RUN. Product decision |
| G2-15 | H at a boss fog, boss K alive in both worlds. G about to finish its join load | C1; B-27; A-18, A-20 | H kills K **shortly before** G's playable start, so a flags packet or K's block snapshot produced before the kill can arrive after that start (Codex chooses the means; without delay control, repeat at the boundary and record arrival times from the existing `shared progress` / `world state` lines) | K is not admitted for G. Source prediction for a "first receipt after playable" baseline: K is admitted (C1), a REPRODUCED-GAP | NOT RUN. Needs boundary timing |
| G2-16 | G playable. Boss K alive in both worlds, in a block whose first post-playable snapshot has not arrived yet; flags variant: within 5 s of the playable start | C2; B-17 | G and H kill K together before the first post-playable observation of K's flag or block | K **is** admitted for G (outcome 9). Source prediction for a first-seen baseline: folded into the baseline and lost, a REPRODUCED-GAP. A documented loss is not a pass | NOT RUN |
| G2-17 | One block B of H's area; at least two completed snapshots N and N+1 of B with a bit that differs | B-26; C3; A-20 | Deliver N+1 complete, then a delayed N complete (fixture of `OnBbscWorldFlagsPacket`, or a captured run if Codex can reorder) | `bbsc_world_blocks[B]` is not replaced by the older N, and no bit is admitted through 1→0→1. Source prediction: N replaces N+1 (L16912), a REPRODUCED-GAP. A freshness check that passes this must also pass a host process restart (counter back at 0) | NOT RUN. NAT fixture level is enough for the receiver |
| G2-18 | Like G2-02, with boss X earned together early in the session | C4; B-28; Q8 | (a) G kept death and reload; (b) H dies; (c) a follow load to another area. After each, they kill one more boss together. (d) G leaves H1 and joins H2, who has older history | (a)-(c): no baseline reset; X stays admitted; each later joint kill is admitted. (d): H2's older history is not admitted; X stays admitted. Record the session state and lock lines across each transition | NOT RUN. Needs Q8 |
| G2-19 | Boss reward rows from the 19 (one with a goods lot, one with a native award) | A-27; A-32 | (a) H kills the boss during G's join load into the boss's area. (b) G has been playable in this party, then is dead or loading (kept death, or a follow load) when H kills the boss in that area. (c1) G and H kill the boss together while G is playable; the event is queued and G departs before the award (at once, or while the item manager is unreadable during the load). (c2) G departs first; then H kills the boss. (c3) As (c1), then G loads a different character, or joins another host H2, before the entry is settled. (c4) As (c1), then G departs, reloads and rejoins twice more. (d) A queue entry from session 1 exists when session 2 starts | (a) no reward. (b) admitted although G is not playable at that moment (the party's eligibility window is still open); given once after G is ready for delivery again, not rejected, not dropped and not early. (c1) the reward stays deliverable and is given exactly once to G's original character, before departure completes or afterward; not lost. (c2) rejected: no `reward queued` line and no reward for G. (c3) deferred: not given to the other character or as H2's party reward, and not discarded while they are active; settled once for the original character when it is loaded again. (c4) one given line in total and the goods count raised once. (d) never given as a session-2 event. A valid admitted session-1 entry is settled once as session 1's reward for its original owner: in session 2 if that owner is loaded, otherwise deferred until it is. Only invalid entries (never admitted, stale, missing or invalid owner record) are discarded. Every given line must be followed by the goods in the after-snapshot; a `given` mark without the item is a REPRODUCED-GAP. Source prediction: (a) can give; (b) can give, since the existing enqueue has no playable gate (A-27); (c1) lost, marked given without the award by the award-time area test (L10436-10441) or dropped while the manager is unreadable (L10426-10428); (c3) and (d) can give to whichever character is loaded; a failed native award is not detected | NOT RUN. Needs scripted host timing. (c1)/(c3) runtime feasibility and award confirmation stay open until Codex verifies the chosen delta; a crash or exit before settlement is outside this row (no persistence assigned) |

**Suggested P01 order:**
1. G2-14 (decision), then G2-01 and G2-03: the import gap.
2. G2-02 and G2-04: eligible joint kills.
3. G2-06 (NPC conflicts).
4. G2-15..G2-18: ordering, first-event and epoch constraints (C1-C4).
5. G2-19, G2-07, G2-11, G2-12: rewards.
6. The conditional rows, only for the delta actually proposed.

Each row ends with both players' save/reload checked (outcome 5/6/8 evidence = SAVE).

## CL03-C: discriminating native probes for P02 (2026-10-25)

CL03 section. **Execution status of every row: NOT RUN.** Claims: B-29..B-37 and M1-M4 ([IDENTITY-PROTOCOL.md § CL03-B](IDENTITY-PROTOCOL.md#cl03-b-earned-event-and-party-epoch-signal-matrix-p02-2026-10-25)), A-33..A-36 ([BBSC-002-MAP.md § CL03-A](BBSC-002-MAP.md#cl03-a-earned-event-admission-feasibility-p02-2026-10-25)). Common setup and P01 run rules apply.

**Observable fields (existing log lines only; no new hook is required):**
- `BBSC lua event: <name> (caller …)` (B-29);
- `BBSC boss clear: BlockClear2_1 (player type N)` (B-34), and any `ForceSummonSuccess` trace record (B-30);
- `boss drop: event E queued for user U slot S` (P, B-35);
- `relay: our host is player X` and `relay: no longer a guest … let go` (B-31);
- `join teleport: guest moved …` and `load cover: fading in … guest placed beside the host` (B-32);
- `life: player X says it is dead/alive` (B-33);
- session state where logged.

Evidence level: **NATIVE-LOG**, both clients, copied saves, time-aligned.

### New cases (only the distinctions G2-03/04/15..19 cannot express)

| ID | Source boundary | Paired input (positive / negative) | Required assertion | Discriminates | Blocker / status |
|---|---|---|---|---|---|
| G2-20 | B-35 reward wait vs. the join-load copy of host flags | **Negative:** H killed boss X (one of the 19 rows) **before** any party; G has not. G joins into X's area, nobody fights, G stays 60 s. **Positive:** G2-02 joint kill of X | Negative: **no** `queued` line for X. Positive: one line within seconds of the kill. A negative-side line means the wait also fires at load (M1 = "also at load") | M1. Decides whether K1 can stand at all | NOT RUN. Needs `SHADPS4_BBSC_DREAM` and guest items on, and H save with X dead, G save without |
| G2-21 | B-34 `BlockClear2_1` on the guest; B-30 label | H kills boss Y with G (a) alive in the arena, (b) dead (kept death), (c) in a follow load, (d) in another area of H's world. **Negative:** G loads into an area whose boss H killed earlier (as G2-20) | For each of (a)-(d): whether G logs `BlockClear2_1` and at what time relative to H's. Negative: no `BlockClear2_1` on G. Record whether a `ForceSummonSuccess` record appears on either side at each kill | M2 and B-30. Decides K2/K3 | NOT RUN. (b)/(c) need scripted host timing |
| G2-22 | B-31 lock, B-32 first placement, B-33 life | One session, in order: (a) G kept death and respawn; (b) H death; (c) a follow load; (d) G leaves and rejoins the same H with a gap under 5 s, then (e) over 5 s; (f) G joins H2; (g) H quits to title and hosts again **with a different character in the same process**, and G joins | For each transition: session state, whether `no longer a guest` appears, whether a new `guest placed beside the host` appears, and the locked host id. Required for K1: (a)-(c) keep state 6, no unlock, no second placement. **And** (d), (e), (f) and (g) each show a boundary that existing log fields can tell apart from (a)-(c). Source predicts (d) and (g) keep the same host id (B-31). If they are not separable, C4 stays open for every candidate | M3 (Q8) **and** C4. Decides whether the K1 window survives death and loading, and whether a new party can be told from a continuing one | NOT RUN |

### Reused cases with the CL03 discriminator

| Case | Behavior covered | What it must now separate |
|---|---|---|
| G2-03 | Kill before initial playable | Record the kill time against B-32's placement line, not state 6. Run only after G2-20 |
| G2-16 | First eligible kill before any new summary | Is the `queued` line (B-35) and/or `BlockClear2_1` (B-34) present for the first kill after placement? This separates "signal fires at kill" from "folded into the first summary" |
| G2-15, G2-17 | Delayed / reordered older data | **Also applies to K1/K2 (CL03-REV01).** Pair G2-17's delayed older snapshot (a block where boss X is alive in N+1 and dead in the older N, or the reverse) with the reward and boss-clear lines. Assert: no `queued` line and no `BlockClear2_1` caused by the older state. Until this passes or source proves it, C3 stays unresolved for K1/K2 |
| G2-04, G2-18 | New kill during same-party death/loading | Add the G2-22 fields. A kill during G's death must give a `queued` line, and P's enqueue area test must not reject it during a follow load (A-33) |
| G2-19(c2) | Post-departure kill | Expect no `queued` line: the gate needs state 6 (B-35) |
| G2-11, G2-18(d) | Same-host rejoin / new host | Use G2-22(d)-(f) to record whether the lock and placement change |
| G2-19(c3) | Original-owner deferred delivery | Unchanged (B02/B03 territory). Not an admission probe |

**Smallest order and stopping condition:**
1. **G2-20** first: it needs no joint kill, only the negative input.
2. **G2-21** (a) and the negative input, then (b)-(d).
3. **G2-22**.

**Stop** and report "no existing guest-side earn-time producer" if G2-20 shows a `queued` line on the negative side **and** G2-21 shows no `BlockClear2_1` on a dead or loading guest. Neither K1 nor K2 can then work, and a native producer has to be found first (Codex). **Also stop** (C4 open for every candidate) if G2-22 cannot separate (d) or (g) from a continuing party with existing fields. **Continue** to G2-17 (paired, for C3) and then G2-03/16/04/18/19 only for a candidate that G2-20..22 leave standing.
