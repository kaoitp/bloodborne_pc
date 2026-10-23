# CL01-C: executable acceptance cases

Owner: external Claude Code. These are specifications for Codex's R03/R04 runs. **Execution status of every case: NOT RUN.** Claims refer to A-xx in [BBSC-002-MAP.md](BBSC-002-MAP.md) and B-xx in [IDENTITY-PROTOCOL.md](IDENTITY-PROTOCOL.md). Symbols are from the pins listed there. No offsets, APIs or results are invented: wherever a value must be observed, the case says which log line or save to capture.

## Common setup (applies to every case unless stated)

- **Clients.** H (host) and G (guest) use two distinct existing authorized accounts. Each has its own copied `BB_USER_DIR`, its own DLL folder copy (A-C2), and `BBSC_SAVE_DIR=<its BB_USER_DIR>\savedata\<id>\CUSA00207\SPRJ0005` (A-C1). Use separate P2P ports if both run on one PC. Some cases need a third account H2 for a second host; mark them WAIT_DEP when none is available.
- **Builds.** R02 baseline: K `f3734da` source build plus the official `bbsc.dll` / `bbsc-launch.exe` (hashes in R02). Delta runs name their source commit. Do not mix baseline and delta evidence.
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
| SVC-03 | Cross-map join needs :20444 (B-F1, A-03) | (a) G:20444 unreachable, as R02 observed: try same-map, then cross-map, with the same non-empty password. (b) Same again with :20444 reachable (configuration only, no redeploy; skip if the user cannot open it) | host `RelaySendAimedPlacement` → relay → guest `OnAimedHostPlacement` → `RewriteAreaId` → broker `Advertise` | Prediction from source: (a) same-map joins, cross-map stalls (no `host … rang our sign` and no `connect-first - sign AreaId` on G). (b) Cross-map joins. Record the actual result. A REPRODUCED-GAP is only what is observed | G stays in its own world after a stall. G's save is unchanged | NAT + GP | NOT RUN; (b) needs the user to make :20444 reachable |
| SVC-04 | P2P-channel fallback after a join (B-06, B-12) | Same-map join with :20444 unreachable. Then: H walks into the next area; H lights a lamp | `SendFrame` → `P2PChannelSend` → guest `Dispatch` `from_our_host()` | Record whether G logs channel peers, follows H, and receives world flags or progress (`shared progress: the host has … boss flag(s)`) | — | NAT + GP | NOT RUN |
| SVC-05 | UDP transport relay on the split host (B-07, B-13) | Any session with `SHADPS4_P2P_RELAY=<G>:3478` | `RelaySetServer` → `Relay._shad` | Client: `P2P relay fallback: server … (forced for every peer)`. Server: `shadPS4 relay: <npid> registered` for both | — | NAT (client + server) | NOT RUN; server log access |
| SVC-06 | Game-server outage mid-session (outcome 11 robustness) | Stop only the user's game server for 2 minutes during a joined session, then start it. Only with the user's permission and without a redeploy | relay reconnect loop (B-05) | Record the behavior. Required: G's saves are intact, and a later departure still returns G home | Saves intact | NAT + GP + SAVE | NOT RUN; needs the user's OK, otherwise WAIT_DEP |

## G1: join

| ID | Required outcome / claims | Setup and action | Boundary | Expected allowed / rejected | No-side-effect assertions | Evidence | Status / blocker |
|---|---|---|---|---|---|---|---|
| G1-01 | Cross-map join beside the selected host (1, 2; A-03, A-05) | Same non-empty password "P". H in Cathedral Ward, G in Central Yharnam (both lamps lit). H rings the Hunt Bell, G rings the Kin Bell. Precondition: SVC-03(b) | as SVC-03, then `ApplyCrossMapSummonGuestPlacement` (native reload) and the join teleport | One native load into H's map. G ends within a few meters of H. Logs: `connect-first: placement written`, `summoned reload finished in host map` | No second forced `StageTransition` during the join. H's world flags are unchanged | NAT + GP | NOT RUN; WAIT_DEP on :20444 reachability |
| G1-02 | The same in the opposite direction, across areas (1) | H in Old Yharnam or Forbidden Woods, G in Cathedral Ward | same | same | same | NAT + GP | NOT RUN |
| G1-03 | Dream as source and target (1; A-04) | (a) H in the Dream, G in a story map. (b) G in the Dream, H in a story map. Password "P" | same, plus the Dream present/restore | Join succeeds both ways. After G goes home, G's Dream state (Doll, workshop, messengers' items) is G's own | G gets no Dream progress or starter items from H (B bloodborne_re.cpp L11081-11087 rule) | NAT + GP + SAVE | NOT RUN |
| G1-04 | Same **non-empty** password required cross-map (2; A-01, B-09) | Different maps: (a) H none, G "P". (b) H "P", G "Q". (c) both none | broker `MatchesSearch` → `Search` (Preparing) | **Required:** no cross-map join and no warp in (a), (b) and (c). Source prediction for the baseline: (b) refused, (a) and (c) **joined**. A candidate gap becomes REPRODUCED-GAP only when observed | G never loads H's map, and its position and world are unchanged | NAT (shadNet `preparing cross-map` if the user provides it) + GP | NOT RUN; WAIT_DEP on :20444 |
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
| G2-06 | Conflicting NPC choices are kept (6; A-10) | H and G made different choices for one NPC quest (e.g. a survivor sent to a different refuge). G joins, they play, G goes home | kind-1 merge (kinds 6/7 excluded) | G's NPC quest state is unchanged | No quest-phase flag is copied from H | SAVE + GP | NOT RUN; needs per-flag inspection |
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
| 1 | Story maps and Dream; Chalice excluded | G1-01, G1-02, G1-03, G3-06 | NAT + GP | :20444 reachability (SVC-03) |
| 2 | Same non-empty password cross-map; same-map rules kept | G1-04, G1-06, SVC-03 | NAT + GP | candidate gap A-01/A-02. Deployed broker UNKNOWN |
| 3 | Locked own-world map does not block the visit | G1-07 | GP + SAVE | — |
| 4 | Pre-party map, position, heading and lamp kept, incl. after process exit | G3-01, G3-02, G3-03 | GP + SAVE + NAT | candidate gap A-13 (memory-only spot, no lamp) |
| 5 | Show host world; share only jointly earned events; no older-history import | G2-01, G2-02, G1-03 | SAVE + NAT | candidate gap A-09 |
| 6 | Add verified progress, keep own progress and NPC choices, no whole-group copy | G2-05, G2-06, G2-02 | SAVE + GP | candidate gap A-10 (whole kind-1 OR) |
| 7 | Original point if valid, else the pre-join lamp | G3-01, G3-03, G3-05 | GP + SAVE | candidate gap A-14 (no validation) |
| 8 | Verified rewards, no duplicate or re-grant | G2-02, G2-07 | SAVE + GP | — |
| 9 | Eligibility from playable, through death and loading, until departure | G2-03, G2-04 | SAVE + NAT | Codex defines the "playable" observation point |
| 10 | Unsupported area: end, notify, safe return | G3-06 | NAT + GP + SAVE | UNSUPPORTED in the baseline (A-16) |
| 11 | Self-hosted services; no required public endpoint | SVC-01..SVC-06 | NAT (client + server) | :20444 reachability; server log access; SVC-06 needs the user's OK |

Persistence-failure cases G2-09 and G2-10 are conditional on an actual R04 persistence change.

**Suggested R03 order:**
1. SVC-01, SVC-02, SVC-05: identity and routes.
2. SVC-03(a) and SVC-04: the relay question.
3. G1-01, G1-03 after :20444 is reachable.
4. G1-04, G2-01: the two main candidate gaps.
5. G2-02, G2-05, G3-01..03, G2-08.
6. The rest.

Only observed failures feed R04, under the plan's five-part change rule.
