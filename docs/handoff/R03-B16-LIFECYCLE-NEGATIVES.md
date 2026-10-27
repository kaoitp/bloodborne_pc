# R03 B16: host loss and early guest crash, plus what Claude cannot run alone

2026-10-27, Claude (R03 takeover); revised after the PR #13 review. No source change.

**Tested composition (provenance).** These runs used the B15 v1 build from PR #12 head `7bed9e6`:
- DLL `e19397e80eebd0cd9dd2e8c4cc9de6599e94418ac2e953c4660814f4313aff82`.
- Patch `f4889473ad06b1322576ab7db8c3408bfb76cd270c7c7c16191c51cf73379f0c`.
- LF source `70ff36b4f4358635a8ed0e9761feaca1659fefff7ebb827463bee903687cbf8b`.

That head branches from `4426543`, **before PR #11 was integrated**, so its patch lacks PR #11's owner check, title continuity, progress-order and file-error guards. The results below are observations on that pre-PR #11 runtime composition. They are not attributed to the final integrated source. Lifecycle acceptance for the integrated source (seamless with PR #11, plus PR #12 revision 2 `854a26a`) stays **open** until it is run on a matching build.

Setup:
- mod defaults, spectate off, the experimental home recovery **off** (the default);
- the self-hosted server, two copied clients;
- host Kaori, guest U-I-AHH (sd1 slot 3, level 10, starting in Iosefka's Clinic);
- fresh copies of both protected saves.

**Snapshots.** I used `read-world.py`, which reads the 1250 flag groups, and `read-position.py`.
- S0 is the guest at home, before any join. It was taken about 35 s after the load, inside B07's 45 s window of early-load transients.
- S1 is the guest after case 1.
- S2 is the guest after case 2, taken about 90 s after its load.

## Case 1: host process killed during the visit (G3 host loss): bounded observation

**Timeline:**
- 00:00:09 the guest was placed in the host's world (Cathedral Ward).
- 00:00:30 the host process was killed. This is not a graceful Quit; B11 covered the graceful case.
- 00:00:31 `persistence suspended ... (guest sent home: session ended in the host's world)`.
- 00:00:46:
  - `return home: the trip home goes to our own spot 0x18010000 (-190.19, -50.63, 170.59), not 0x18000000 (the last warp's)`;
  - one second later, `own world (during the home load): 979 flag group(s) of our own world put back`;
  - then `shared progress: home again, nothing from the host to merge`.

**Result:**
- Position after the return: (-190.19, -50.63, 170.59), on the guest's own map 0x18010000. Before the join it stood at (-190.18, 166.48); the return uses the journal's own spot, about 4 m away.
- S0 → S1 differs only in 12705098, 12705301, 12705520, 12705521, 12705531 and 12705532, all cleared. These are exactly B07's six early-load transient bits, which were still set when S0 was taken.

**Limits of this result:**
- The return is to the journaled spot, about 4 m from the position read at S0. It is not an exact equality with S0's position.
- S0 itself was taken inside the early-load window.
- This is a bounded host-process-loss result (one run, pre-PR #11 composition). It does not show full settled or repeated save/reload integrity.

## Case 2: guest process killed 5.8 s after placement (G2-08 below 10 s): flags observation, origin GAP open

**Timeline:**
- 00:04:35.9 the guest was placed; the game saved at 00:04:36; the journal `own-sd1-3.bin` was on disk.
- 00:04:41.7 the guest process was killed.
- On restart: 00:06:07 `user sd1 slot 3 was left with another player's world in it ... putting our own back`, with 979 groups. The journal became `.restored`.

**Flags:** S1 → S2 has **0 differences** across 1250 groups. This is an observation between these two named snapshots (one run, pre-PR #11 composition), not a general flag-integrity proof.

**Position — gap:** the guest woke **in its own world at the host's spot in Cathedral Ward**: map 0x18000000, (19.77, -9.51, 101.51), own_world 1, character type 0. Its origin was the Clinic (0x18010000).
- The game's own save during the visit holds the summon placement.
- Only the experimental home recovery (`SHADPS4_BBSC_EXPERIMENTAL_HOME_RECOVERY=1`, off) would move the character back.
- For a low-level character this means landing in an area it has not reached. Here that was a level-10 Clinic character in Cathedral Ward, which is the locked-map situation of G1-07.

The flags are its own, so nothing is lost or imported. But the character is not "safely returned".

A02 described this gap ("R02 durable origin"), and the R02 prototype is contained behind the opt-in. This run confirms it on the default configuration, below the 10 s timing. The earlier B14 run checked the flags after a crash in the host's Dream (about 2 minutes, above 10 s); there the guest woke in its own Dream, which is unlocked for every character.

**Next step.** The R03 takeover already requires an interrupted guest to return safely to its original world and origin, or to a valid fallback, and leaves the method to Claude. So this needs no separate design approval. Claude is implementing a narrow, owner-safe durable-origin/fallback fix under the takeover, with copied profiles and focused RED/GREEN, then native proof. It does **not** flip the experimental home-recovery switch on without that switch's missing safety evidence. No packaging or deployment.

## What Claude cannot run alone (for the owner and the friend)

These rows stay open because the rig, the accounts or the timing are not in Claude's reach. Each lists what it needs.

The rows split into prerequisites and practical help. Help with steering or typing makes a run possible. It is **not** evidence that the row passes; each row passes only on its own run.

**Prerequisites (the row cannot be run without them):**

| Row | What is missing | What it needs |
|---|---|---|
| G1-05 stale/failed candidate isolation (H1/H2 race), G2-22 H1→H2 boundary | A third authorized identity and client. | **Conditional:** only while these rows stay in scope, a third test account on the self-hosted server. |
| G2-03/15/16 kill processed before placement, first eligible event | The host's kill must be processed during the guest's join load. On this rig the host processes it after the guest arrives. | **Conditional on timing:** a slower link, a second machine, or an agreed debug delay. Not a gameplay task. |
| G2-04/18/21(c) guest in a follow load at the kill | A supported in-party load. Deaths respawn in place and lamps are disabled in co-op. | **Conditional:** only if a supported in-party load exists. Otherwise the row is recorded as not applicable. |
| G3-06 unsupported area | Two different things: (a) co-op inside Chalice dungeons, which is unsupported and out of scope for feature work; (b) the safe unsupported-boundary behaviour (a guest or host entering an unsupported area ends the party safely), which is already requested. | (a) nothing; it stays unsupported. (b) a run that takes one side to an unsupported boundary. It may need help reaching it (below). |

**Practical help (makes a run possible; not evidence):**

| Row | Help needed |
|---|---|
| G2-05/06 progress outside the boss area: an NPC choice the two characters made differently, and a guest ahead of the host (boss or lamp) | A person steers the host (or both) to the NPC step or lamp, about 30–60 min. My pad steering cannot reach it reliably. Claude prepares the build, snapshots and comparison. |
| G1-04 empty / one-empty password cross-map controls | A person sets an empty password with the on-screen keyboard in the Network menu, about 5 min. Claude runs the join and the world comparison. |

**Also open, runnable without new prerequisites:** the B15 native rows (consumed and flagged rewards, and the save-confirmed cases; steps in [PR #12](https://github.com/kaoitp/bloodborne_pc/pull/12), `docs/handoff/R03-B15-REWARD-ONCE.md`), the final same-build lifecycle acceptance after the open PRs merge, and the native run of PR #11's final DLL.

All test processes are closed. The protected source saves are unchanged.
