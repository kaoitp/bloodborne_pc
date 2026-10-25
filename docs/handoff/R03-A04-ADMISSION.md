# R03-A04 native admission checkpoint

Status: IN_PROGRESS, 2026-10-25 (Asia/Bangkok). The bounded initial-write cancellation/retry case passes on the experimental guest build. R03 and the broad G1/G2/G3 gates remain open. New recovery/admission stays OFF by default.

## Demonstrated gap and retained change

A03 admitted a guest while the own-world journal could not be written. Its rejected Lua-dispatcher skip was too late: the enclosing native function continued after the notification. Actual JoinSession_White caller `0x0131A7B2` belongs to function `0x0131A760`; executable disassembly confirms that function continues event/matching-state work after calling the dispatcher. The retained patch guards that enclosing entry with its verified six-byte R14 prologue.

Only under `SHADPS4_BBSC_EXPERIMENTAL_HOME_RECOVERY=1`, a still-own-world non-host captures the existing home/world journal before that transition. If the existing write has not completed, the guard suspends existing persistence, calls existing CSMultiPlayMan.StopRequest, and skips the enclosing transition. It does not hold a stale insertion. Existing native retry/search handles later attempts. No new protocol, loader, journal codec, progress catalogue or server change. Unknown/non-own/host contexts retain the existing bypass conditions; this checkpoint is the observed readable-own-world fault case, not blanket enablement approval.

Task/dependency/five-part justification preceded edits in [the tracker](../WINDOWS-PROGRESS.md). Base `ef2d774` on primary `C:/Projects/bloodborne_pc`, branch `seamless`; pinned BBSC reference `4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`. Existing FSR-Vulkan dirt and the four external audit-owned documents are untouched.

## Rejected native wait

The first A04 candidate held existing CSMultiPlayerIns.StartNotifyWait (`0x01E4FD50`). It was downstream: Lua join at 07:02:37.992 and summoned-reload placement at 07:02:41.797 preceded the hold. B 18364/HWND 133150 stayed at the original Cathedral coordinates while .bin.tmp was blocked, but after release around 07:03:35 it fell below Dream (Y -70, then -857), later changed load state. No healthy-placement PASS. The candidate was fully reverted; ignored rejected source/patch/DLL/suspect copied saves remain under `.superpowers/r03-a04`. Do not reuse it.

An earlier setup B 3208 separately exited 23 with GPU assertion `Unimplemented PM4 type 0` during character selection, before admission testing; excluded from the join verdict. One restart succeeded. No renderer change was made.

## Actual retained guest test

Guest B 408/HWND 854100 used cancellation DLL below, 160/160 hooks; test host A 19980/HWND 67340 used the rejected wait DLL, 159/159 hooks. The wait's changed guest-only path does not run while hosting, but this mixed pair is explicitly attributed; it is not a final release-pair gate. Distinct existing authorized accounts, separate copied profiles/ports, matching nonempty co-op words independently verified. Shared progress and Discord are disabled only in the private test harness; experimental recovery is opted in there. Production defaults are unchanged.

1. Fresh copied B was reset from protected pre-join saves and deliberately selected EiEi slot 1. Independent baseline: 1250 flag groups, Cathedral `0x18000000`, own world 1/type 0, lamp 2402950, position `(15.770329, -9.511212, 103.839012)`, heading -0.868897.
2. Occupied only its exact journal `.bin.tmp` with a nonempty test directory. At 07:14:10.584 actual native guard logged cancellation, Stop -> 1. Own-state restoration at 07:14:11.228 changed zero flags. Another automatic attempt at 07:14:51.696 was also canceled while storage remained blocked. No active journal existed.
3. Independent settled refusal comparison: all 1250 groups exactly equal the pre-join baseline; map/position/heading/lamp/own/type/loading fields also equal. `.superpowers/r03-a04/assert-refusal.py` exit 0. This tests actual captured native state, not a helper imitation.
4. Removed only the exact sentinel and empty directory. Renewed search on the copied clients. Healthy transition at 07:15:33.564 entered Dream as a blue guest beside the selected host; independently observed own 0/type 1, correct map and nearby coordinates, with visible co-op scene. Actual 126561-byte journal matches all 53 present members of the existing 57 Dream keys against the independent own baseline (four absent from the native table).
5. Normal Parting Blank return at 07:22:02.987 restored original Cathedral map, point, heading and lamp. Independent returned state differs from pre-join only in group 9: 29 flags, retained separately as the unresolved reward/state issue. No whole-world integrity or G2 PASS claim.
6. Actual Quit Game/YES -> title observed, then Online/Continue. Independent reload preserves all 1250 settled returned groups exactly, and the original point/map/heading/lamp. `.superpowers/r03-a04/assert-final.py` exit 0 also checks the 53 Dream keys and fresh original-profile manifest.

Private evidence: `.superpowers/r03-a04/native-cancel`, cancellation mod log `bbsc-mod-20261025-070931-408.log`, source/artifact manifest `cancel-hashes.json`. Saves, raw logs, account configuration and executable inputs remain ignored. Original profile: fresh 3171-file before/after path/hash manifests, zero differences. At this checkpoint A 19980 and B 408 are still active copied test processes for continued work; no original game profile was launched.

## Source, build and fixture evidence

| Item | SHA256 |
|---|---|
| Retained reference bloodborne_re.cpp | `26e6dc9c1c125664fe312febc9bf2285eac873993b6360033ac79795f18751ae` |
| Complete tracked four-file BBSC patch | `bb9a963d7393096f983c1028480c862f36aa8750a0458eed5e294a64a597f270` |
| Retained cancellation guest DLL | `02e3879b0a2329a2b26696eb65025c646b774ede5cdbc7d8d8dc1a0eac516c31` |
| Rejected wait DLL / actual test host | `fe255e63e83453893c5df7022be4417395004f5cd25b97900dedd3b77e2f31a2` |
| Source probe, unchanged A02 | `6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14` |

- `python tools/build_bbsc_mod.py .superpowers/reference/BBSC .superpowers/r03-a04/cancel-dll`: exit 0 with existing CLANG64 toolchain, original loader and mandatory notices. Initial wait preparation had declaration-order/UTF-8 setup failures; corrected before the final attributed build. No failed build is native evidence.
- `python -m unittest discover -s tests -p test_native_bbsc.py -v`: 2 PASS. `... -p test_run_bbsc.py -v`: 5 PASS. These do not prove the new native transition; the actual fault/retry above does.
- `python -m unittest discover -s tests`: 157 tests, 1 failure, 8 errors, 48 skips, exit 1. Same Windows symlink/shell/tool and packaged Vulkan/Nix fixture categories as A03; no full-suite PASS.
- Complete patch reverse apply-check and diff whitespace checks: PASS. All four prior reference destinations retained. No release EXE/ZIP or live-server deployment.
- Inline review against base ef2d774: Standards checks the single entry/skip registration, existing StopRequest ABI/callers, game-thread journal ownership, unchanged defaults and scope. Spec remains partial: the readable-own-world initial storage fault now cancels and retries, but unknown-state/pending-recovery enablement and remaining broad gates are not passed by this test.

## Remaining work and useful source leads

- [x] Bounded actual initial-write cancellation, clean own-state refusal, healthy later join/placement, normal return and independent save/reload.
- [ ] G2 jointly earned events/rewards, older-host-history exclusion, personal choice/item integrity and death/loading eligibility. Existing production progress/reward policy is unchanged.
- [ ] Remaining locked-own-map and stale/failed-candidate controls, final required self-hosted route correlation and affected recovery enablement checks. Keep experimental recovery OFF until the relevant gates pass.

Actual self-hosted summon HTTP captures for this pair: WebAPI port 31315, host get/request and guest create/delete/get, status 200/request_error 0; nonempty co-op word agreement verified without recording it. Earlier established TCP 31313/20444 connections are only connection evidence, not complete authentication/peer/progress route proof. Full route gate remains open.

Group 9 lead advanced without a runtime change: actual common event 9040 parameter bindings are `(instruction,target-byte,source-byte,count) = (0,4,0,4), (3,4,0,4), (4,0,4,4)`. They bind the same initializer flag to the early flag check and flag wait, and the second initializer argument to AwardItemLot. This strengthens the reward-related lead; it does not classify the 29 flags as harmless or justify restoring the entire group. Raw primary-script evidence is ignored `.superpowers/r03-a04/common9040-bindings.json`. Next inspect the actual flag producers/reward get flags and eligibility before changing G2.
