# CL01 progress

Status: VERIFIED for the audit documents (2026-10-23), corrected for review CL01-REV01 (2026-10-24, see the last checkpoint). No gameplay gate is affected; G1/G2/G3 stay with Codex. Parent: R03/R04. Owner: the user's external friend using Claude Code.

Read [the work package](../../handoff/CLAUDE-CODE-WINDOWS.md). The external audit was performed by Claude Code in a separate clone; findings are below. R02 evidence exists in [the primary record](../../handoff/BBSC-BASELINE.md); it does not count as a test executed by Claude. G1/G2/G3 remain open.

This file is the owned tracker: `docs/collaboration/claude/PROGRESS.md`.

## Inputs to record at external start

- Audit base SHA: `04c6e7b4b9a042c872e6ed815dacce6c7a7a0d8e` (clean clone of origin/seamless; `merge-base --is-ancestor f3734da HEAD` exit 0). Remote: origin = https://github.com/kaoitp/bloodborne_pc.git.
- Audit branch: `claude/bbsc002-reference-audit` in a separate clone.
- BBport base: `e5d04e2ba4864ccf40de6c3cf6aa532855320b0d`.
- BBSC source: `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`; `rev-parse HEAD` of `.superpowers/reference/BBSC` (autocrlf=false clone) matched.
- Canonical patch SHA256: `e34c79b388605998b430ec4eed556fc2cb8c8928f1d3e9f26bf5d2df29732aa3`; `sha256sum` of the reference checkout matched.
- Required R02 source ancestor: `f3734da56722f21dd2c25dcca89b85d1c93f2109`.
- Usage availability/remaining windows: not exposed to this Claude Code session (unavailable).

## Work sequence

| Slice | Status | Dependencies | Owned output / completion |
|---|---|---|---|
| CL01-A | VERIFIED | Frozen base and verified reference | `BBSC-002-MAP.md`: complete composition ownership summary; join/progress/return source rows with citations and candidate gaps separated from reproduction |
| CL01-B | VERIFIED | Same pins; independent of A | `IDENTITY-PROTOCOL.md`: all required service routes, split-host/relay fallback settings and relevant identity validation, with source/evidence/unknowns |
| CL01-C | VERIFIED | A/B for final citations | `ACCEPTANCE-CASES.md`: actionable G1/G2/G3/service cases and all-11-outcome coverage matrix, execution status NOT RUN |
| CL01 handback | VERIFIED | A/B/C and document checks | Four-path-only commit; full base/branch/commit, checks, findings, limitations and next action |

A/B may be investigated alongside Codex R03; the external single Claude session can do A then B. C may draft case IDs early but remains WAIT_DEP until A/B citations are ready. Codex owns implementation and test execution. Slice status above was set by the external Claude session.

## Checkpoint format

For each external checkpoint record:

- Slice/status, full audit base and pinned reference SHAs; current commit and dirty/staged paths.
- Changed deliverable paths (only the four allowed by the work package).
- Actual source/coverage/link/UTF-8/whitespace/scope commands, waited exits and counts; native/gameplay NOT RUN.
- Ranked findings by A/B claim ID and C case ID; candidate source mismatch versus actual reproduced gap; missing evidence.
- Usage or unavailable, limitations, next action, handback branch/full commit/transfer method when ready.

Keep private addresses, credentials, saves, game assets and raw logs out of these files. Source findings need immutable commit/path/symbol/line citations. VERIFIED for an audit slice means its source/document deliverable passed checks; gameplay gates are updated only by Codex from actual evidence. Shared plans/entry points are read-only for Claude.

## Checkpoint 2026-10-23: handback

- **Base and branch.** Audit base `04c6e7b4b9a042c872e6ed815dacce6c7a7a0d8e`, branch `claude/bbsc002-reference-audit`. The handback commit is the one that adds this section; the full SHA goes to the user with the handback.
- **References.**
  - BBSC `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`; patch blob SHA256 `e34c79b3…2aa3` matched.
  - Additional reference shadnet-p2p `5a849a192fd4450593c57b10697316ac324c856e`, cloned with autocrlf=false into the ignored `.superpowers/reference/`. It is named by the BBSC server README as the source of the release's `shadnet.exe`.
- **Deliverables.** [BBSC-002-MAP.md](BBSC-002-MAP.md) (A-C1..A-C4, A-01..A-16), [IDENTITY-PROTOCOL.md](IDENTITY-PROTOCOL.md) (B-01..B-14, B-F1, Q1..Q6) and [ACCEPTANCE-CASES.md](ACCEPTANCE-CASES.md) (29 cases, an 11-outcome matrix, execution NOT RUN).
- **Checks, each with exit 0 and the results stated:**
  - Inline Python:
    - **Pinned citations:** 79 checked. All 25 distinct files exist at their pinned commits, and every cited line falls inside its file.
    - **Coverage:** 11 of 11 outcome rows.
    - **IDs:** every referenced claim and case ID is defined (35 claims, 29 cases).
  - Local link/anchor check, UTF-8/LF/no-BOM, `git diff --check`, and a scope check (`git diff --name-only <base>` lists only the four allowlisted files): see the commit message.
- **Not run by Claude:** builds, the game, servers, accounts, native or gameplay tests. Native facts quoted are Codex's R02.
- **Usage:** not exposed to this session.

## Findings, ranked (all source-only; none reproduced; revised for CL01-REV01)

1. **A-09 / A-10 / A-08.** Shared progress imports the host's older history:
   - It collects the host's full boss/time flags and whole kind-1 groups of every area (`WORLD_SYNC_ALL` default on).
   - It has no admission baseline.

   Smallest candidate for the older-history part: a first-seen baseline in `TickBbscSharedProgress` and `OnBbscProgressPacket`. **It addresses older-history import only.** It still imports every kind-1 bit that changes during the session, including unclassified flags, so outcome 6 additionally needs a verified-event filter (allow only classified eligible boss/story flags) and a conflicting NPC change tested during the session (G2-06(b)). Cases G2-01, G2-03, G2-06.
2. **A-01 / B-09.** The broker's anywhere mode accepts a cross-map match when the host's password is empty. The client never checks the password. Candidates: a broker `MatchesSearch` change, or a client-side word check in the aimed frame. Case G1-04.
3. **A-C1 / A-C2.** BBSC cannot find saves in an absolute `BB_USER_DIR` without `BBSC_SAVE_DIR`, and two clients need two DLL folders. Configuration only. Applies to all cases.
4. **B-F1 / A-03 (conditional source hypothesis).** Without the TCP :20444 relay, a cross-map join may stall if the aimed placement frame `0x31` reaches no P2P-channel peer. The channel can learn the guest from an ACTIVE signaling connection before the join, so the outcome depends on the order of the claim send and signaling activation, and on any re-claim. Not decided by source; SVC-03(a) decides it. No unconditional :20444 prerequisite. Codex 2026-10-24 showed relay-backed cross-map success, not relay necessity.
5. **B-07.** In a split layout the UDP 3478 relay defaults to the shadNet address, but the server runs on the game server. R02's explicit `SHADPS4_P2P_RELAY=<G>:3478` is correct. Configuration and registration lines are preflight only; the route counts as proven only with rising bidirectional `… sent / … received through the relay` counters naming each other on both clients (SVC-05).

Also recorded:
- **A-03 / G1 configurations:** BASE (pinned defaults, `SHADPS4_BBSC_WARP_JOIN` on) and J01 (Codex `run.py` default `0`) are separate configurations; every G1 run names one.
- **A-13:** the pre-join spot is kept in memory only, with no lamp.
- **A-14:** no validity check on return.
- **A-16:** Chalice is unsupported, with no send-home.
- **A-02:** anywhere mode also relaxes the same-map level and distance filters.
- **A-C3:** loader race, Supermedo PR 125.
- **B-10:** game-API `UserId` collisions are possible.
- **B-11:** the aimed placement is bound to the delivered claim only by `UserId`.

## Unknowns and next action

**Unknowns:**
- The deployed shadNet and game-server builds.
- Whether the binaries equal their sources.
- Kind-1 group contents versus NPC phases.
- The load position after a crash.
- State during a kept death.

**Next (Codex):**
1. Integrate after the gate in the work package.
2. Answer Q1–Q6 in R03, in the suggested case order.
3. Base R04 only on reproduced failures.

**Transfer:** the user chooses a branch URL or a patch file. Claude does not push to `seamless` or `windows`.

## Checkpoint 2026-10-24: CL01-REV01 corrections

- **Review.** kaoitp CL01-REV01 (CHANGES_REQUESTED on PR #1) reviewed `eb493a40cfc2f2ad0e28f485e4208040b27d897f` against frozen base `04c6e7b4b9a042c872e6ed815dacce6c7a7a0d8e` and current `seamless` `bd24679c7655a97bd4d9fba2b11ee079e6033751`. The audit base stays frozen; no rebase.
- **Corrections, each re-checked against the pinned source:**
  1. **B-F1 is a conditional source hypothesis.** B `bbsc_channel.cpp` L161-170 calls `NotePeer` when `sceNpSignalingGetConnectionStatus` reports ACTIVE, so pre-join signaling can give the channel its peer. The aimed frame is sent once per claim request (B `bbsc_http.cpp` L507-524, `bbsc_relay.cpp` L491-496). The unconditional :20444 prerequisite is removed from A-03, B-05, §2, SVC-03, G1-01, G1-04, the coverage matrix and this tracker. The R02 outage is dated 2026-10-23; Codex's 2026-10-24 relay-backed success is cited separately.
  2. **BASE and J01 are separate configurations.** B `bbsc_persistence.h` L34 enables `SHADPS4_BBSC_WARP_JOIN` by default. The no-extra-reload assertion now applies to J01 (`run.py` from `af235b3`); the observed BASE second reload and failed return are attributed Codex evidence (G1-01, G1-03).
  3. **UDP route proof needs transferred frames.** Configuration and registration are preflight only; SVC-05 and B-07 now require rising bidirectional counters from K `p2p_sockets.cpp` L754-772 (receive counter L948) naming each other, or captured forwarded frames.
  4. **A first-seen delta is not the NPC/verified-event filter.** A-09 and A-10 now state that the baseline addresses older-history import only; outcome 6 keeps the verified-event requirement and the new G2-06(b) in-session NPC conflict.
- **Codex evidence cited (not Claude tests):** R03/R04 records at `bd24679` (`docs/WINDOWS-PROGRESS.md`, `docs/handoff/R04-JOIN-RELOAD.md`), linked by immutable URL because those files are not in the frozen base.
- **Not run by Claude:** builds, the game, servers, accounts, native or gameplay tests. No case status changed to PASS.
- **Checks:** see the correction commit message.

## CL02-P01: progress contract (2026-10-24)

Status: **VERIFIED for the source/documents, corrected for review CL02-REV01** (see the checkpoint below; set IN_PROGRESS before any CL02 deliverable edit; VERIFIED after the checks). This is not a runtime PASS; G2 stays with Codex. Work package: `docs/handoff/CLAUDE-CODE-WINDOWS.md` § CL02-P01 at `seamless` `b1391b0`.

| Slice | Status | Owned output |
|---|---|---|
| CL02-A | VERIFIED | `BBSC-002-MAP.md` § CL02: progress flags, the 19 boss-event reward rows, eligible vs unclassified, smallest seam |
| CL02-B | VERIFIED | `IDENTITY-PROTOCOL.md` § CL02: progress ownership, snapshot ordering, recovery and legacy pending data |
| CL02-C | VERIFIED (cases NOT RUN) | `ACCEPTANCE-CASES.md` § CL02: focused P01 G2 matrix, all NOT RUN |
| CL02 handback | VERIFIED | this file: pins, checks, unknowns, ranked P01 recommendations, full commit SHA |

- Comparison base: accepted CL01 head `108bf28f069d7017712fd71e24fb7fd6b2bbde36`; branch `claude/p01-progress-contract` in the same separate clone (clean before branching). CL01 audit base `04c6e7b` and pins K/B/N unchanged.
- Codex evidence read (public Git objects, no rebase): `6cff29d75c9f8dedf887bf6b52fefc8a02b9cc5d` `docs/handoff/R03-ACCEPTANCE.md`, `docs/handoff/R04-JOIN-RELOAD.md`, `docs/superpowers/specs/2026-10-18-bbsc-anywhere-coop-design.md`.
- Source pins for new claims: B `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41` (`emulator/src/core/bloodborne_re.cpp`, `bbsc_persistence.h`, `emulator/mod/bbsc_relay.cpp`, `bbsc_channel.cpp`), read from the existing ignored reference clone. K and N are unchanged.
- Deliverables: [BBSC-002-MAP.md § CL02-A](BBSC-002-MAP.md#cl02-a-progress-and-reward-contract-for-p01-2026-10-24) (A-17..A-31, the 19 reward rows), [IDENTITY-PROTOCOL.md § CL02-B](IDENTITY-PROTOCOL.md#cl02-b-progress-ownership-ordering-and-recovery-p01-2026-10-24) (B-15..B-25, Q7..Q10), [ACCEPTANCE-CASES.md § CL02-C](ACCEPTANCE-CASES.md#cl02-c-focused-p01-progress-matrix-2026-10-24) (G2 rows reused, plus G2-11..G2-14, all NOT RUN). CL01 sections, IDs and evidence dates are unchanged.
- Not run by Claude: builds, the game, servers, accounts, private saves or logs. Codex evidence (the 7 entries, the 15:32 timeline, backup false) is quoted from `6cff29d`; Claude did not reproduce it.

### CL02 ranked P01 recommendations (source only; nothing implemented)

1. **Filter at collection, not at merge** (A-18, A-21). A first-seen baseline in `OnBbscProgressPacket` and in the kind-1 loop of `TickBbscSharedProgress`, admitting only 0→1 transitions, is a candidate against the bulk import of older history (G2-01). It is **not implementation-ready for outcome 9**: constraints C1-C4 (delayed pre-playable baseline, swallowed first event, reorder, epoch boundary) are open, and the existing signals cannot close them (B-26..B-28). The reset point must be a genuine new party or host epoch, not every state-6 entry. The merge, the pending file and crash recovery need no change for whatever the filter admits.
2. **Restrict what can be admitted to the existing finite list** (A-23). Leave A-24 (9466-9471, unclassified) and kind-1 groups (A-26) out until they are classified. A first-seen delta over whole kind-1 groups is expected to fail G2-06(b).
3. **Decide the night flags** (A-25, G2-14). As written they import a host's later night at merge time without a joint event.
4. **Rewards use the same eligibility contract** (A-27, A-32). The existing enqueue is state-6 only and the award tick is ungated, so a pre-playable reward is possible. Eligibility is judged **when the event is earned**, as a window per party epoch: the first playable start opens it, it stays open through that party's death and loading, and genuine departure or a new epoch closes it (an event earned while it is not open is rejected). Delivery is a separate step with its own readiness gate: an earned, admitted reward is kept for its original owner and epoch through death, loading and departure and settled exactly once. While another character or a later party is active it is deferred, not given to them and not discarded. It is never dropped only because the guest departed. A confirmed award before "given" is also required. None is implemented; the existing award-time area test loses an earned reward when departure beats the award (A-32).
5. **Close the cross-run reward duplicate where an existing flag allows it** (A-29), as a separate concern from item 4. Before giving a first lot for a taken-flag-0 row, check the goods row's existing get flag. That covers rows 3, 8, 10, 15 and 18; the other 7 flag-0 rows have no existing record (unknown).
6. **Legacy pending data** (B-23). A filtered build writes a new file magic, so baseline `BBSP` files are not re-imported. The conditional cases G2-13, G2-08, G2-09 and G2-10 apply only to the delta actually proposed.

### CL02 unknowns

- Which A-23 flag belongs to which of the 19 events, and whether 9450-9465 are counters.
- Whether any kind-1 bit is an NPC quest phase.
- Names and progression roles of the unnamed reward goods.
- First-arrival timing per flag and block, and whether state 6 holds through death (Q7, Q8).
- Which of the 7 A01 entries are A-23, A-24 or A-25 members (Q9).
- Whether delayed or reordered snapshots occur in practice, and whether the lock holds through same-party transitions (Q11).
- Whether the existing reward path queues before playable or loses a queued event (Q12).
- How C1-C4 can be closed with existing signals at all. Source says they cannot as written (B-26..B-28).

**Next (Codex):** review this contract, answer Q7-Q10 from existing logs or snapshots where possible, then decide R04-P01. Claude does not implement it.

## Checkpoint 2026-10-24: CL02-REV01 corrections

- **Review.** kaoitp CL02-REV01 (changes requested, PR #1 comment 6382726381) on handback `b48d2b36c6e41cb66cfc474287fc5eaf6bec6863`, base `108bf28f069d7017712fd71e24fb7fd6b2bbde36`. Same branch `claude/p01-progress-contract`, one correction commit on top; no rebase. CL01 sections, pins K/B/N and all stable IDs unchanged.
- **Corrections, each re-checked against pinned B `4f11faf`:**
  1. **Snapshot counter is not an ordering guarantee.** `OnBbscWorldFlagsPacket` resets the single assembly buffer on any different map or ID (L16893) and a completed snapshot replaces the block (L16912); there is no high-water check. B-17's guarantee is revised; new B-26 records the N+1-then-N counterexample; any freshness check is an unimplemented candidate (with its restart/`u32` counterexamples). Case G2-17.
  2. **First receipt after playable is not event time.** New B-27 (no host time in either packet; `complete_ms` is local, L16906) and B-28 (the lock as the only epoch-like signal, 5 s unlock). The former "rules" are now open constraints C1-C4; the every-state-6 reset is replaced by a reset only at a genuine new party/host epoch, with eligibility kept through same-party death and loading. Cases G2-15, G2-16, G2-18; G2-11 revised.
  3. **Rewards need the eligibility contract.** A-27 now cites the `BbscGuestInHostWorld`-only enqueue gate and the ungated `TickBbscBossRewards` (L16051); G2-03's "no reward line" is predicted to fail on the existing path. New A-32: queue ownership and award confirmation (silent drop at L10426-10428, "given" before the award, unchecked native award). A-31 qualified. The A-29 get-flag check is kept as a separate concern. Case G2-19.
- **Also fixed:** the seam's pending-file reference now points at B-23 (was B-18).
- **Line note.** In the pinned file `complete_ms` is set at L16906 and the reset test is L16893; the review's L16909 / L16895-16918 refer to the same code.
- **Not run by Claude:** builds, the game, servers, accounts, native or gameplay tests, private data. All new cases are NOT RUN. Source-only suggestions stay candidates until Codex's reproduction and native gates pass.
- **Checks:** see the correction commit message.

## Checkpoint 2026-10-25: CL02-REV02 correction

- **Review.** kaoitp CL02-REV02 (PR #1 comment 6388357678) on `c6cb7b3d75b164bfbe2b6dc164241141918de615`: the three REV01 findings are closed; one P2 remains. Same branch `claude/p01-progress-contract`, one correction commit on top; no rebase. CL01 sections, pins K/B/N, stable IDs and the REV01 fixes unchanged. Further CL02 discussion moves to a separate PR into `seamless`, as requested.
- **Correction ([P2] earned reward vs departure), re-checked against pinned B `4f11faf`:** A-32 no longer drops every queued reward at departure or a new epoch. It separates **eligibility when earned** (at enqueue; events earned after eligibility ended are rejected) from **delivery and confirmation** (an admitted entry stays an obligation to its original owner and epoch, confirmed before departure completes or settled exactly once afterward, never given to a later party or another character). Only unearned, stale or wrong-owner entries are discarded. New source facts: an entry is a bare event ID with no owner or epoch (L10295, L10306-10308); the area test runs at award time and marks an earned event given without the award once the guest has left the area (L10436-10441); `given` is never cleared in a run (L10296). So the existing path loses an earned reward when departure beats the award. Remaining constraints: owner matching inherits the B-24 slot gap; the queue does not survive a crash or exit (no persistence assigned). The seam (i), ranked item 4 and G2-19 are revised: (c) is split into (c1) earned before departure, deliverable once to the original owner; (c2) first earned after departure, rejected; (c3) no delivery to another character or party; (c4) no duplicate across repeated departure/reload; (d) states how a session-1 entry is settled or discarded.
- **Not run by Claude:** builds, the game, servers, accounts, native or gameplay tests, private data. G2-19 stays NOT RUN; runtime feasibility and award confirmation stay open until Codex verifies the chosen delta.
- **Checks:** see the correction commit message.

## Checkpoint 2026-10-25: CL02-REV03 correction

- **Review.** kaoitp CL02-REV03 on PR #2 (changes requested, two P2) on `2386dfc6137d502d6464a21fcc16bfec4eb2a31f`. REV01 and REV02 corrections stay as accepted. One correction commit on the same branch; no rebase. CL01 sections, pins and stable IDs unchanged.
- **Corrections (contract wording; no new source claim):**
  1. **Eligibility through same-party death/loading.** A-32 and seam (i) no longer require playable readiness at every enqueue. Playable readiness opens the party's eligibility window once; the window stays open through that party's death and loading and closes only at genuine departure or a new epoch (C4). Events earned in the boss's area while it is open are admitted even while the guest is dead or loading. Delivery has its own readiness gate (owner loaded, alive, not loading, item manager readable). G2-19(b) now states this, with the source prediction that the existing ungated enqueue can give (A-27).
  2. **Inactive owner is deferred, not discarded.** The wrong-owner discard is narrowed to invalid admissions (never admitted, stale, missing or invalid owner record). A valid admitted obligation whose owner is not loaded, or which waits through a later party, is deferred under its original owner and epoch. G2-19(c3) and (d) now match: (d) settles a valid session-1 entry for its original owner when loaded and discards only invalid entries. In-process contract only; no persistence.
- **Not run by Claude:** builds, the game, servers, accounts, native or gameplay tests, private data. G2-19 stays NOT RUN.
- **Checks:** see the correction commit message.

## CL03-P02: earned-event and party-epoch source feasibility (2026-10-25)

Status: VERIFIED for the source/document deliverable (2026-10-25); set IN_PROGRESS in commit `e3fb202` before the deliverable edits. No gameplay gate is affected. Work package: [CL03-P02 at 80518ab](https://github.com/kaoitp/bloodborne_pc/blob/80518ab0713b8775248a2a2c63feb025e73d1ae7/docs/handoff/CLAUDE-CODE-WINDOWS.md#cl03-p02-earned-event-and-party-epoch-source-feasibility), assigned on merged PR #2. Branch `claude/p02-event-provenance` from frozen comparison base `7a5eca3fcdc662afcce1de7b6d57510311b710b2` (clean clone, no rebase). The CL01/CL02 sections above are historical and unchanged.

| Slice | Status | Owned output |
|---|---|---|
| CL03-B (signal matrix) | VERIFIED | `IDENTITY-PROTOCOL.md` § CL03-B |
| CL03-A (feasibility decision) | VERIFIED | `BBSC-002-MAP.md` § CL03-A |
| CL03-C (discriminating probes) | VERIFIED | `ACCEPTANCE-CASES.md` § CL03-C |
| CL03 handback | VERIFIED | This section: base, pins, checks, ranked conclusion, next native observation |

### CL03 handback

- **Inputs.** Base `7a5eca3fcdc662afcce1de7b6d57510311b710b2`. Pinned B `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`, read as Git blobs: `emulator/src/core/bloodborne_re.cpp`, `emulator/mod/bbsc_relay.cpp`, `emulator/src/core/libraries/np/np_signaling/np_signaling_helpers.cpp`, `bbport/bbport-1.7.2-bbsc.patch`. P is `gpu/patches/bbsc/0001-profile-storage-and-clang64.patch` at the base. Retained test read: `tests/test_bbsc_reward_delivery.py` at the base; it calls `NoteBbscBossRewardEvent` directly, so it does not exercise the hook gate or the wait timing. Codex handoffs read at the base: B02, B03, C01, B04, and the CL03 package at `80518ab`.
- **Deliverables.**
  - [IDENTITY-PROTOCOL.md § CL03-B](IDENTITY-PROTOCOL.md#cl03-b-earned-event-and-party-epoch-signal-matrix-p02-2026-10-25): B-29..B-37 and missing evidence M1-M4.
  - [BBSC-002-MAP.md § CL03-A](BBSC-002-MAP.md#cl03-a-earned-event-admission-feasibility-p02-2026-10-25): A-33..A-36 and the decision.
  - [ACCEPTANCE-CASES.md § CL03-C](ACCEPTANCE-CASES.md#cl03-c-discriminating-native-probes-for-p02-2026-10-25): G2-20..G2-22, the reused cases and the stopping rule.
- **Not run by Claude:** builds, the game, servers, accounts, native hooks or tests, private data. All CL03 cases are NOT RUN.

**Ranked conclusion (source only): NOT IMPLEMENTATION-READY, a bounded impossibility with existing signals.**
1. **No earn time on the only guest signal that carries an event ID** (B-35). The reward hook fires when the guest's copy of the event evaluates its player-type wait. The host's block flags are copied into the guest's world at the join and follow loads, before play. So a boss killed before the party may queue a reward at that load (M1).
2. **No event ID on the only guest kill-time signal** (B-34, `BlockClear2_1`). Whether it runs on a dead, loading or elsewhere guest is unknown (M2). Pairing by area is ambiguous for 11 of the 19 rows.
3. **No attempt or epoch anywhere.** The relay host id distinguishes host processes only (B-31). The first-placement flag `bbsc_join_teleport_done` (B-32) is the best existing "first playable" marker, but it resets on any state ≠ 6 poll and is stored nowhere. A host id plus a placement marker does not establish a new-party boundary (same-host rejoin, host character change in the same process): C4 is an independent blocker (REV01).
4. **Host flags carry no event or time** (B-36), and flag ↔ event is still unmapped (M4).
5. **Side findings.**
   - The `0x013849A0` label conflict (B-30).
   - P's enqueue area test rejects an earned event during a follow load into another area (A-33).
   - On BBport, `0x26` arrives only through the relay `from_our_host` path; the emulator build's raw receive has no sender check (B-36).

**Next native observation (Codex):** G2-20 first: a pre-party kill, then G joins into that area with no fight. Does `boss drop: event … queued` appear? Then G2-21: `BlockClear2_1` on a guest that is alive, dead, loading, or elsewhere, plus the `ForceSummonSuccess` label. Then G2-22: state, lock and placement through death, follow load and rejoin, including a host character change in the same process. Then G2-17 paired with the reward line (C3). Stop if the reward wait fires at load and the clear does not run for a dead or loading guest; also stop (C4 open) if G2-22 cannot separate a same-host rejoin or host character change from a continuing party.

**Unresolved risks:** the B-30 mislabel can make existing trace logs misleading; M3 (Q8) also affects CL02's eligibility window; delivery/merge safety (B02/B03) stays separate from admission.

- **Checks:** see the handback commit message.

### Checkpoint 2026-10-25: CL03-REV01 corrections

- **Review.** kaoitp CL03-REV01, recorded in the shared tracker at seamless `58d80bd` (not posted on PR #3), on head `08c205c08ed75513b02a445f1456fc4e3b349c99`: CHANGES REQUIRED, two Spec P2. One correction commit on the same branch; no rebase. Base prefixes, pins and IDs unchanged.
- **Corrections (wording/verdicts; no new source claim):**
  1. **Stale world-state input (C3).** A-33's C3 cell no longer says "not affected". The callback is local, but the world state driving it can be older host data (B-35 load copy, B-26 older snapshot replacing newer). This is unresolved: no guarantee either way. K2's C3 is marked the same way. The G2-15/G2-17 reused row now applies to K1/K2: G2-17 is paired with the reward and boss-clear lines.
  2. **C4 is an independent blocker.** A host id plus a placement marker does not show a new party. The CL03-A decision now says M1/M3 are necessary, not sufficient. G2-22 adds (g), a host character change in the same process, and requires (d)-(g) to be separable from a continuing party. A new stopping condition applies if they are not. Verdicts: A-33 blocked on M1, M3, C3 and C4; A-34 and A-35 also carry C4.
- **Not run by Claude:** builds, the game, servers, accounts, native tests, private data. All CL03 cases stay NOT RUN.
- **Checks:** see the correction commit message.
