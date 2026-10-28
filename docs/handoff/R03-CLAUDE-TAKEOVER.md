# R03: Claude takes over implementation and validation

2026-10-25 (Asia/Bangkok). Active assignment from the project owner: finish R03. Claude now owns implementation, builds, native/gameplay testing, documentation and publication across this repository. The previous CL01-CL04 four-document audit assignment is historical, not the current write allowlist. Codex is handing over, not running a competing implementation session.

## Goal and freedom of approach

Keep the [product outcomes](../superpowers/specs/2026-10-18-bbsc-anywhere-coop-design.md) and three goals unchanged:

1. Supported story-map/Hunter's Dream co-op: guest can join the selected host from the supported routes, including an own world that has not unlocked the host map, and appears beside the host. Representative maps are sufficient; the owner does not require every-map repetition. Chalice remains outside the existing product scope.
2. Progress and relevant rewards earned together belong to both players and survive each player's own save/reload. Older host history and guest-specific earlier progress/NPC choices remain distinct. A real eligible obligation must remain with its original character when delivery is delayed; it must not be lost or delivered to another character/party.
3. The required self-hosted flow works and departure/disconnect/interruption returns the guest to their own world, progress and valid origin/fallback.

The owner clarified: keep our goals and general approach; Claude can choose methods freely where they do not substantially conflict with that approach. Use the complete pinned BBport1.7.2 + BBSC0.0.2 composition as the starting point, reuse existing mechanisms and preserve unrelated upstream behavior. Claude can choose investigation order, tools, delegation, experiments, implementation and tests without a Codex approval round. There is no four-file limit and no requirement to wait for Codex. Codex's account-usage stop is not a stop for Claude's separate account. Historical audit-only, inline-only, frozen-package and Codex-only implementation procedures do not govern this takeover. The earlier packaging/deployment exclusions describe the previous assignment; this handoff adds no new method restrictions. Judge proposed work against the R03 goals and the owner's clarification rather than copying old process prohibitions.

Protect the user's original data and private credentials as part of a correct implementation. Existing copied profiles/after-saves are available. Report what actually passed; source hypotheses, fixtures and native gameplay answer different questions. Current default-OFF switches below are facts about the tested configuration; Claude owns the decision and evidence for subsequent changes.

## Start here

Latest native update (2026-10-28): read the [current progress summary](../WINDOWS-PROGRESS.md#latest-handoff-for-the-active-implementer) and [native04 evidence](R03-FINAL-NATIVE-04.md) first. Published checkpoint `38f8ab3` proves a bounded command-assisted Amelia party kill, pendant x1 on both, exact automatic guest origin return and both fresh-process save+journal reloads. Runtime artifacts unchanged; broader R03 gates remain open. The older B06 starting point below is historical context, not the latest native status. Copied native04 saves/journal/logs remain private on the original machine; both games are closed.

Read root AGENTS.md/CLAUDE.md, this handoff, [latest B06](R03-B06-WORLD-ORDERING.md), [B05 event probes](R03-B05-EVENT-PROBES.md), the latest entries in [progress](../WINDOWS-PROGRESS.md), [plan](../superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md), then CL03/CL04 additions in [acceptance cases](../collaboration/claude/ACCEPTANCE-CASES.md) and [identity/protocol](../collaboration/claude/IDENTITY-PROTOCOL.md). Read older checkpoints when the affected behavior needs them. The old [Claude audit package](CLAUDE-CODE-WINDOWS.md) is reference history.

Repository https://github.com/kaoitp/bloodborne_pc.git, branch seamless. Runtime checkpoint a43e26fcddfc5f5759ef30c9c53f35df214acb12; published quota checkpoint ea69b94f085fdf47aa5fd73b3ed192e2c6322373. Newer documentation commits containing this handoff are expected. Original machine's authoritative checkout is C:/Projects/bloodborne_pc; the app-created C:/Users/numbe/.codex/worktrees/5e56/bloodborne_pc is stale and detached. Existing local dirt is the documented FSR-Vulkan build patch state, not a new Gitlink change. No game remains running; one-time18:11 automation was deleted.

On another machine:

```powershell
git clone --single-branch --branch seamless https://github.com/kaoitp/bloodborne_pc.git bloodborne-r03
cd bloodborne-r03
git status --short --branch
git log -4 --oneline
git merge-base --is-ancestor a43e26fcddfc5f5759ef30c9c53f35df214acb12 HEAD
```

An existing friend clone can fetch origin, inspect its uncommitted work and integrate origin/seamless without overwriting it. The old audit branch is not the runtime state. Choose an implementation branch/worktree or continue seamless according to the working setup; coordinate publication so another actor's work is retained. Publish source/checkpoints to origin/seamless with normal history-preserving Git integration. The owner already requested this handoff to be pushed; no Codex review dependency is being introduced.

## What is already proved, and what is not

| Area | Actual evidence | Still open |
|---|---|---|
| Join | Same-map/Dream and fresh locked Clinic character to Cathedral; B06 candidate guest placed0.849996m from B03 host; normal return correct | Remaining candidate/party-boundary cases; not every map required |
| Own-world state | B01/B03/C01 bounded preservation/recovery; B06 immediate return all1250 groups exact, origin exact to accepted journal | B06 independent settled reload of protected co-op after-saves; six early reload bits unclassified |
| Older host history | B05 host Amelia already dead12401800ON, guestOFF; visited-worldON but no reward/clear logs >60s without fight | Negative alone lacks positive producer sensitivity; not full history-exclusion proof |
| Reward delivery | B02 actual-function tests for owner-bound retry/dedup/frozen lot/direct-goods confirmation; B03 backup/owner retry | No actual joint boss kill yet; alive/dead/loading/elsewhere producer and relevant reward persistence |
| Snapshot ordering | B06 actual receiver RED/GREEN rejects delayed completed/partial old input, duplicates, wrap/reset; normal native join works | No injected live reorder/callback paired G2-17; not earned-event or epoch admission proof |
| Services | C01 required self-hosted multiplayer flow observed | Three public playlogPUT403 did not block that run; do not claim every future route independent from that one run |

B06 same-process Quit/Continue retained own map/lamp/point but an early native snapshot differed at12705098,12705301,12705520,12705521,12705531,12705532. The no-party fresh baseline control initially had12705301 only, then all1250 groups exactly matched after visible load settled. So native loading0 alone was too early to imply settled state. Do not label all six either corruption or harmless without the pending independent co-op replay. Current working profile-b was restored to BEFORE-B baseline; the relevant AFTER-B save is protected separately.

B05 same-process host character change twice hit unrelated GPU PM4 unimplemented errors, runner23 (type0/base87 then base17). No third trial completed; G2-22(g) remains graphics-blocked, not a proven party-epoch failure. Existing1280x720 options reduced load but did not establish a renderer fix. Do not infer character identity from relay/member counts.

## First useful continuation

A suggested next sequence, not a fixed method:

1. Preserve current copied data and replay .superpowers/r03-b06/native/after-b-savedata in a copied B profile with the frozen B06 DLL. Fresh process, PlayOnline/Continue, wait until the visible world and subsequent flag snapshots settle. Compare all1250 groups to native/guest-before-world.json and position to journal-origin.json. Keep early and settled snapshots distinct. The no-party baseline control and exact origin are already available.
2. Actual jointly earned event: copied host Kaori slot0 has Amelia12401800OFF; guest U-I-AHH slot3 is the fresh Clinic/Central character actually used. Verify those actual preconditions, rather than relying on character-name spelling in earlier chat. Stage a live boss, join then earn the event together, and inspect real native event/queue/inventory/own-save outcomes. The user had been asked for manual Kaori staging but paused before responding; nobody killed Amelia in this session. Claude may stage/play itself or request only the gameplay help it needs.
3. Discriminate old host history versus actual kill; first playable, party lifetime/new party/same-host rejoin/host-character change; delivery readiness while dead/loading versus eligibility. CL03 C1-C4 and CL04 cases explain the known ambiguity. Pick the smallest supported fix, then verify affected boundaries and the product outcomes.

CL04 observability facts: full160/160 hooks, Dream/boss-clear and required switches must actually be active before interpreting absence; TraceEntry/LuaSessionEvent are throttled after hit64, and ForceSummonSuccess label overlaps BlockClear2_1 at0x013849A0. B05 maxima hit2, so its bounded absence was below that throttle. Use a fresh guest per paired run because reward queue/given state is memory-local. A local receipt time, first received snapshot, membership count or boss-name gauge is not proof an event was earned together. Valid pending delivery belongs to its original owner/party context even after eligibility closes; don't discard it merely because a new party starts.

Current configuration: shared progress/custom managed application OFF; experimental own-world recovery defaultOFF but explicitly ON on copied probes; extra WarpJoin0 via existing runner fix. Automatic party epoch/earned-event admission is not implemented/proved. B06 cache reset does not establish that every real lifecycle boundary is correct. Claude can evolve configuration/implementation using its own evidence.

## Code, build and checks

The gameplay implementation is the pinned BBSC reference under .superpowers/reference/BBSC/emulator/src/core/bloodborne_re.cpp, represented in this repository by gpu/patches/bbsc/0001-profile-storage-and-clang64.patch. BBport shim callbacks intentionally delegate to the external DLL. Runtime changes must reach the tracked patch, not remain only in the ignored reference checkout. The complete patch contains four destinations; retain earlier fixes when regenerating it. tools/build_bbsc_mod.py applies tracked patches when missing and verifies the pinned source. Root BBport source already includes the baseline patch.

```powershell
$env:PATH='C:/msys64/clang64/bin;'+$env:PATH
# If missing: reconstruct the pinned BBSC checkout and its fmt/xbyak dependencies.
git -c core.autocrlf=false clone https://github.com/CLSAMG22/BBSC.git .superpowers/reference/BBSC
git -C .superpowers/reference/BBSC checkout --detach 4f11faf88b6ba658ebde6fe5fbefdadedba4fa41
git -C .superpowers/reference/BBSC submodule update --init --recursive
C:/msys64/clang64/bin/python.exe tools/build_bbsc_mod.py .superpowers/reference/BBSC .superpowers/claude-r03/dll
C:/msys64/clang64/bin/python.exe -m unittest discover -s tests -p 'test_bbsc_*.py'
C:/msys64/clang64/bin/python.exe -m unittest discover -s tests -p 'test_native_bbsc.py'
```

These Windows paths describe the original machine; adapt to the recipient environment. Fresh reference is needed before actual-function fixtures can run; a skip from missing ignored inputs is not their PASS. For the emulator/toolchain/native composition use [R02 recipe](BBSC-BASELINE.md) and build.sh; reuse verified composition on the original machine rather than repeating R02. Game CUSA03173 APP_VER01.09; copied savedata is under user/savedata/1/CUSA00207/SPRJ0005 despite the game's title ID. Do not set BBSC_SAVE_DIR when reproducing the old sd1 journal namespace accidentally as save; that changes ownership keys. Native save-slot detection is a newest-written-file heuristic, not a durable character identity guarantee.

Frozen B06 source SHA25676287a320bec6ba63c959b38a9764331cd89a27eb4d17798fa463d1c81a87494; patch6dec09c7497fe7f85efa8cc299412d6320e754baef265d53afd601e33e1c7f4c; DLLfaf8227f64137b50bbc54e076ad1f309bab7c20940370e1a277e9e2a8fdbac83; source-built probe6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14. B06 native host was B03 DLL96e398b23e0d48af4f220a7ca7534d529369e1f194bc65e60da55d884ca2303d, guest B06; do not relabel that as same-build paired earning proof.

Last checks:3 actual-function fixtures PASS,2 native-header tests PASS, local DLL build exit0. Full suite160 tests/1failure/8errors/48skips exit1, known Windows shell/symlink/Vulkan-Nix categories; full suite is not green. B06 final4-destination reverse-check,5 hashes,91 document links and originals3171 exact. See checkpoint for actual commands/results, not just this summary.

## Local inputs and portable support

Git supplies source/docs/tests, not game assets, accounts, full profiles, raw logs or binaries. On the original PC:

- .superpowers/r03-resume.json points to supplied private inputs; .superpowers/r03-retry/launch-test.ps1 and newer r03-b06/native/launch-test.ps1 contain existing authorized accounts/configuration. Read privately, never print them into logs/commits.
- Profiles .superpowers/r03-retry/profile-a and profile-b; original user's D:/Games/Bloodborne/bbport-windows/user was never launched/modified and all3171 files remain exact. Assets D:/Games/Bloodborne/CUSA03173/dvdroot_ps4. Native prepared ELF profile-a/out/eboot.elf. Existing source probe out/bb-probe.exe and its runtime DLL dependencies need the build/output directory, not just one EXE copied in isolation.
- Latest co-op save copies native/after-a-savedata (Kaori host) and native/after-b-savedata (guest after co-op/normal save); native/before-b-savedata is the protected guest baseline. Private B05/B06 evidence remains on disk; raw logs are not published.
- Native read-only helpers .superpowers/r03-close/read-position.py and read-world.py; .superpowers/r03-a03/compare-world.py compares groups ignoring PID. Group format125bytes, MSB-first. Existing BB_PAD_FILE with110ms directional/500ms action pulses then clear/gap worked. User's keyboard i/j/k/l plusSpace also works; OS synthetic keys were unreliable. Observe selection before item use; a cleanup mistake once selected Duel Bell instead of Blank, no combat. Quit to title then close the verified test process before copying savedata.

Optional private archive, prepared and CRC/SHA256-checked: .superpowers/r03-claude-transfer/r03-claude-local-support.zip,87 files,19,018,684 bytes, SHA2560cc68e440ce0a38d72a9c851ff906b9d8310bf367092e79ca16347a081b1efe0. Extract at the recipient repository root. It contains selected copied BEFORE/AFTER saves, state/journal snapshots, diagnostic helpers, B03/B06 DLLs, original injector/manifest/notices and per-file manifest. It excludes credentials/launch helpers, game assets, original profiles and raw logs. This is a private save-bearing file for direct handoff by the user, not a Git artifact. If the friend uses another PC, also supply authorized game/profile/account/service inputs separately or recreate equivalent copied tests; the archive is not a complete runnable installation. Claude can work from source before those runtime inputs arrive and label the missing validation accurately.

## R03 completion

Close the existing plan/tracker gates with matching current source/artifact/configuration and actual evidence for the product goals. Preserve useful historical records, clearly supersede failed hypotheses and record any remaining unsupported behavior. Then publish the implementation and handoff. Claude is the decision-maker for how to get there; this suggested sequence is not an approval barrier.

## Prompt to give Claude

> รับช่วงเป็นเจ้าของ R03 ทั้ง implementation และ native/gameplay validation ใน repo bloodborne_pc branch seamless อ่าน AGENTS.md, CLAUDE.md และ docs/handoff/R03-CLAUDE-TAKEOVER.md แล้วทำต่อจาก checkpoint ล่าสุด เป้าหมายและแนวทางหลักคงเดิม: supported-map join แล้ว guest อยู่ข้าง host, progress/รางวัลที่ได้ร่วมกันโดยไม่รับประวัติเก่า host หรือทำลาย progress ส่วนตัว, self-hosted flow และกลับโลกเดิมได้ คุณเลือกวิธีวิเคราะห์ แก้ source/build/config ทดสอบ ใช้เครื่องมือหรือ subagents และอัปเดตเอกสารได้เอง ไม่จำกัดสี่ไฟล์ audit และไม่ต้องรอ Codex อนุมัติ วิธีที่ไม่ขัดแนวทางหลักมากให้ตัดสินใจเอง กฎ usage-stop ของบัญชี Codex ไม่ใช่ข้อจำกัดบัญชีคุณ เริ่มจาก pending independent settled reload ของ protected co-op after-b save แล้ว actual jointly earned boss event/party boundary หรือเลือก discriminator ที่เหมาะกว่าจากหลักฐาน บันทึกผลที่ทำจริงและ push งานกลับ seamless จนปิด R03 ได้
