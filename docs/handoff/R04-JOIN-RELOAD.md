# R04-J01: preserve the native cross-map guest load

2026-10-24, Asia/Bangkok. Status: VERIFIED for the bounded Cathedral Ward -> Hunter's Dream join/placement/normal-return case. R03 and the full G1/G2/G3 gates remain open. Review/test source base: `93ad51fd105f01e7d3fc74cf3a5806e1449b2bce` on `seamless` in `C:/Projects/bloodborne_pc`.

## Change justification

1. Goal: selected-host cross-map join, adjacent guest placement and safe own-world departure using existing BBSC mechanisms.
2. Pinned baseline gap: the guest joined from Cathedral Ward into the host's Dream, then a second full reload left it with Beckoner-style End co-op; confirming that option reported No resonance/feature unavailable. Earlier same-map guest return worked.
3. Existing default is insufficient: pinned BBSC `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`, `emulator/src/core/bbsc_persistence.h`, enables `SHADPS4_BBSC_WARP_JOIN` by default. In `bloodborne_re.cpp`, `BbscWarpJoinEnabled` and `TickBbscJoinTeleport` request the extra session reload after the native cross-map handoff has already loaded the map. The existing later position correction does not require this second reload. OLD `2685ff6751da30bfda61e37db28df831e23c65f1` removed that second StageTransition; this was a lead, not current acceptance evidence.
4. Smallest responsible change: `run.py` defaults the existing flag to `0` only when `BBSC_EMULATOR` identifies the DLL launch. Explicit nonempty overrides, including `1`, remain honored; stock launch is unchanged. No new option, DLL source import/rebuild, backend or protocol change.
5. Acceptance: launch-environment regression, then the same copied-character cross-map join, adjacent placement, correct guest return menu, original-map return and absence of the extra reload. No changes to identity/home-field validation or managed admission/progress application.

## Actual native RED / GREEN

Two distinct authorized accounts, isolated copied profiles, identical copied character identity, matching nonempty summon word. Private values stay outside Git. The equal CharaId did not prevent these successful joins; UserId and SessionId were distinct. This does not establish that all identity scenarios work.

| Observation | Baseline | Fixed launch |
|---|---|---|
| Same-map control | Claim 11:46:39; JoinSession_White 11:46:42; guest state 6, adjacent placement 11:47:05; normal return 11:50:39-52 | Not repeated after this launch-only change |
| Cross-map native handoff | 11:54:36, Cathedral Ward -> host's Dream | 12:19:11.684, same route |
| Dream loaded | 11:54:45 | 12:19:22 |
| Extra full reload | Requested 11:54:47.771 | No full-reload request in fixed guest log |
| Adjacent placement | 11:54:56.744 | 12:19:25.744, host X + 1; blue cooperator visually confirmed |
| Parting Blank | End co-op -> feature unavailable | Return to Your Own World |
| Departure | Failed own-world return | Confirmed 12:21:26; state 6 -> 7 -> 0; Cathedral Ward origin selected 12:21:32; visibly solo there 12:21:46 |

The native return reported 979 restored flag groups, 142 differing flags and zero missing groups. This is log evidence, not independent proof of eligible jointly earned progress, reward non-duplication or crash recovery.

Host PID 26224/HWND 393870; baseline guest PID 17956/HWND 985156; fixed guest PID 6596/HWND 329784. A first fixed guest process (16604) disappeared before character load without an identified cause; no gameplay result is attributed to that attempt. The retry captured stdout and stderr separately. No Windows Application event identified its cause.

## Verification and artifact identity

Commands used `C:/msys64/clang64/bin/python.exe` in the primary checkout:

- `-m unittest discover -s tests -p test_run_bbsc.py -v`: initial regression RED (`None != '0'`), then GREEN. Final four tests passed, including explicit 0/1 overrides, empty default and stock launch. The tests execute actual `run.main` and capture the environment at its mocked child-process boundary; they do not start a game or qualify native behavior.
- `-m py_compile run.py tests/test_run_bbsc.py`: PASS.
- `-m unittest discover -s tests`: run once, 154 tests, 1 failure, 8 errors, 48 skipped, exit 1. Errors concern Windows symlink privilege, missing shell/tool lookup, overlay launch and packaged Vulkan setup. The failure is the Linux/Nix external NVIDIA driver fixture. These paths were not changed; the full suite is not claimed passing.
- Inline Standards/Spec review against the recorded base, AGENTS and active scope contract: no blocking finding in this bounded change. Test isolation restores environment, argv, cwd and sys.path. No subagents, per AGENTS. All-map/general progress acceptance remains incomplete.
- `git diff --check`: PASS before publication. Only the pre-existing FSR-Vulkan working-tree dirt is excluded from the checkpoint.

| Tested input | SHA256 |
|---|---|
| Changed run.py | `59143bfbf7bea4d86b4e1b3667eeec2bb94bf42480dd3a5e44c965b56e0c7928` |
| Final fixture test | `92bccf60f8f43ddc24fc9d5218eb30deaa3994a576f8528e098f3d74c0128e07` |
| Unchanged source-built probe | `a948f6948d934f024f6089d976edf97bd915f0e46381cdeaad45d9595b1a27ca` |
| Official BBSC DLL | `1df7d39e31c5d1acf034b5fd990b669e5e82944be477f26b0a46621a91610fdf` |
| Official existing loader | `c7fbaa406d972324645153bb8cc8bdad17fcd7db2f05026d67e3ba68f34750c1` |

Private evidence: `.superpowers/r03-claim` contains pre/post manifests, artifact hashes, baseline screenshots and the initial RED fixture log; `.superpowers/r04-join-reload` contains the full-suite log and preserved failed-run copied saves; `.superpowers/r04-join-reload-retry` contains fixed Dream/return-menu/origin-return screenshots, separate process streams and cleanup.json. Corresponding baseline BBSC mod/timeline logs use stamps `20261024-114105-26224`, `20261024-114137-17956` and `20261024-121121-6596`. Native hook and HTTP captures remain in ignored test directories. Helpers contain secrets: never print or stage them.

Both active clients Quit Game before normal window closure; both verified test PIDs exited. CloseMainWindow returned true for each; no numeric exit code was available from those process objects, so no exit-code assertion is made. Original profile comparison: 3,171 paths/hashes before and after, zero differences. Only copies were restored for the retry. Existing DLL TCP service was reachable in this session; earlier unreachable observations are historical. No server redeployment or system-policy change.

## Limits and next action

The earlier guest-deactivation-before-claim failure did not reproduce in this loop; its cause remains unconfirmed. Do not add speculative fast claim requests or bypass identity checks. This fixes a demonstrated downstream cross-map reload/guest-role problem, not every join failure. The launcher default applies to DLL launches; direct emulator invocation must use the existing flag explicitly to reproduce it.

Next G1: other supported story-map routes, locked own-map visit, selected/wrong/stale candidates and failed join without world mutation; verify lighting because the disabled extra reload had a visual-refresh purpose. Then G2 eligible shared progress/rewards/save-reload and G3 disconnect/interrupted recovery with independent snapshots. Chalice remains unsupported. Custom managed admission/progress stays OFF; no packaging or live deployment. Latest pre-publication usage: 29%/73% remaining; continue periodic checks and honor the below-10% stop rule.
