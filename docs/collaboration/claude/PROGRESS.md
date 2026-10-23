# CL01 progress

Status: VERIFIED for the audit documents (2026-10-23). No gameplay gate is affected; G1/G2/G3 stay with Codex. Parent: R03/R04. Owner: the user's external friend using Claude Code.

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

## Findings, ranked (all source-only; none reproduced)

1. **B-F1 / A-03.** A cross-map join needs the game-server TCP :20444 relay. The guest receives the host placement only through relay frame `0x31`. The P2P-channel fallback has no peers before the join. The emulator stores the broker's placement header in its own copy, which the DLL cannot read. R02 saw :20444 unreachable, so cross-map is expected to stall while same-map works. Fix is configuration only: make :20444 reachable. Cases SVC-03, G1-01.
2. **A-09 / A-10 / A-08.** Shared progress imports the host's older history:
   - It collects the host's full boss/time flags and whole kind-1 groups of every area (`WORLD_SYNC_ALL` default on).
   - It has no admission baseline.

   Smallest candidate: a first-seen baseline in `TickBbscSharedProgress` and `OnBbscProgressPacket`. Cases G2-01, G2-03.
3. **A-01 / B-09.** The broker's anywhere mode accepts a cross-map match when the host's password is empty. The client never checks the password. Candidates: a broker `MatchesSearch` change, or a client-side word check in the aimed frame. Case G1-04.
4. **A-C1 / A-C2.** BBSC cannot find saves in an absolute `BB_USER_DIR` without `BBSC_SAVE_DIR`, and two clients need two DLL folders. Configuration only. Applies to all cases.
5. **B-07.** In a split layout the UDP 3478 relay defaults to the shadNet address, but the server runs on the game server. R02's explicit `SHADPS4_P2P_RELAY=<G>:3478` is correct. Effect not tested (SVC-05).

Also recorded:
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
