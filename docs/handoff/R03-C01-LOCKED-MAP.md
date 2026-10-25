# R03-C01 fresh-character locked-map join

2026-10-25, Codex inline. Source checkpoint ad7beca5078e33a385912dd84687a1d47d495efd on seamless; [B03 exact source/build hashes](R03-B03-PROGRESS-BACKUP.md), [plan](../superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md), [tracker](../WINDOWS-PROGRESS.md). No runtime change in C01. R03 stays IN_PROGRESS.

## Copied native case

The user identified a newly created character with no defeated boss. Actual copied list identifies U-I-AHH, slot3, level10, Clinic/Central Yharnam. Host is copied Kaori, slot0, Cathedral Ward. Distinct authorized accounts, separate copied profiles/ports, same source-built probe and B03 DLL96e398b23e0d48af4f220a7ca7534d529369e1f194bc65e60da55d884ca2303d. Actual Windows module checks confirm both A17308/HWND3147804 and B9104/HWND14354200 load that DLL, both160/160 hooks. Shared progress and guest boss items OFF; experimental home recovery ON only on copies. No boss/NPC interaction or newly earned reward is part of this visit.

Fresh original3171-file manifest and both copied save trees protected. Guest initial map0x18010000/lamp2412950; host0x18000000/lamp2402950. First host claim14:05:50 expires after34s without a join; existing stale cleanup/automatic retry then accepts the second claim14:06:51. JoinSession_White14:06:55, state4 at14:06:56, state6 at14:06:59. Actual host SummonSuccess_White and two hunters14:07:19; guest placed beside host and cover fades14:07:23. First-claim delay is observed, its cause unresolved; no claim that all pre-join delays vanished.

Settled blue guest own=0/type=1/loading=0 in Cathedral Ward at(20.690552,-9.504714,101.509285); host(19.869566,-9.506302,101.509285), about0.82m apart. This is actual representative locked-own-map visiting/placement, not an all-map sweep. The first snapshot was taken during setup; the journal's later accepted-summon origin is authoritative for return.

Normal observed Parting Blank -> Return to Your Own World -> YES restores Clinic/Central map0x18010000, lamp2412950, point(-190.180832,-50.622490,166.482391), heading0.065716. Every value equals decoded HomeSpotKey from the protected actual journal. Independent native all1250 flag groups equal prejoin exactly, including after actual Quit/title/Online/Continue. Same-PID guest prejoin/returned/reloaded JSON SHA2562cf351d1454d3cb163fc23b4566518d7354a34b04317c137f4836d754b17ae74. All979 ordinary journal groups equal prejoin; two extra groups are existing time/origin metadata. No pending shared-progress file is created. No older-host-history acceptance is inferred with progress OFF.

## Required-route observations and public logging

Completed C01 logs contain221 actual HTTP dispatches:218 to configured self-hosted services (A:36 WebAPI31315 +86 gameAPI20443; B:18 +78). The other3 are host public playlog PUTs to bb-playlog-test.s3.amazonaws.com; all return403 Forbidden. Actual join, normal return and independent reload continue despite these failures. Thus public playlog success is not required for this observed flow; this does not mean zero public requests or proof of every future route.

Established connection capture during the joined case shows each actual test PID connected to configured ShadNet31313 and gameplay DLLrelay20444, with no other established destinations in that capture. Authentication, accepted claim, member/peer exchange, native blue guest and received host-world/progress packets go beyond port reachability. Progress packets arrive before native playable completion, confirming they cannot serve as eligibility proof. UDP3478/P2P fallback isolation and every unobserved route are not claimed from this TCP snapshot.

## Host delta and solo control

Host independently saves/reloads, but host-full-flag equality is not established:16 changed bits after co-op across groups2/7/9/12415, and12 after reload (7620..7624,7630..7632,9182,9186,9190,9198). Group7 meaning remains unclassified; an initial unsupported starter-choice label was corrected before publication. Common9182/9186/9190/9198 are inspected local event bodies and include multiplayer checks; this alone does not classify every effect or prove lost quest choices.

Same-DLL solo control A18844/HWND2753694 restores only protected pre-C01 copied A savedata, no second client/bell/peer. Three independent1250-group snapshots, including more than5min settled, exactly equal the original host baseline. Therefore automatic solo warm-up did not reproduce the co-op differences. Exact field/writer and gameplay consequence remain unresolved; no speculative flag-restoration patch. Local finite EMEVD/ESD/PARAMDEF scans and actual SummonSuccess register trace are private leads, not native eligibility or first-writer proof.

## Checks, cleanup and next action

Commands: existing read-position.py/read-world.py PID OUTPUT, compare-world.py BEFORE AFTER DELTA; decode-origin.py, read-routes.py and assert-final.py in private .superpowers/r03-c01. Final assertion PASS: guest pre/return/reload1250 groups, exact journal origin/lamp/heading,979 journal groups, three solo controls, original3171 path/hash equality, all3 public playlog403 results, no bb-probe remaining. Both original C01 launcher sessions and solo control session64698 complete exit0. All3 test processes normally Quit to visually confirmed title; CloseMainWindow/WaitForExit true. Copied co-op/control after-saves protected; copied A baseline restored. Original profile never modified. Raw logs, signed URLs, addresses, credentials, game assets and saves remain ignored.

No build/test suite rerun is needed for documentation-only C01; B03 source/artifacts are unchanged. Fresh evidence checks do not establish G2 jointly-earned boss/story rewards, native reward failure/retry, history exclusion, in-memory wrong-character merge, or all remaining candidate/disconnect/recovery cases. Managed application remains OFF; no packaging/deployment or audit-owned edits. Latest usage68%/11%used=32%/89%remaining, above checkpoint threshold.

Next: locate the actual host flag writer and native event/admission producer before changing persistence. Preserve C01 successful locked-map evidence; do not repeat an all-map sweep or adopt a first-received-snapshot delta. R03 closure remains blocked by actual G2 gaps and explicitly unverified affected cases, not by lack of a successful representative join.
