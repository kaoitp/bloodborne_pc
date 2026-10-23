# R02 pinned baseline composition

Date: 2026-10-23 (Asia/Bangkok). This records composition and native startup only; G1/G2/G3 gameplay remains unverified. See [progress](../WINDOWS-PROGRESS.md) and the [active plan](../superpowers/plans/2026-10-23-bbport172-bbsc002-alignment.md).

## Source and exact patch

- Work checkout: `C:/Projects/bloodborne_pc`, branch `seamless`, starting HEAD `01f4b7508bd87e1a0cced662db586142635f1a61`; clean before R02. The app checkout was detached at the same commit, so it was left untouched. No old worktree/source/build/test results were reused.
- BBport base: `e5d04e2ba4864ccf40de6c3cf6aa532855320b0d`; `git merge-base --is-ancestor e5d04e2 HEAD` exited 0.
- BBSC: `git clone --no-checkout https://github.com/CLSAMG22/BBSC.git .superpowers/reference/BBSC`, then `git -C .superpowers/reference/BBSC checkout --detach 4f11faf88b6ba658ebde6fe5fbefdadedba4fa41`; both exited 0, `rev-parse HEAD` matched the full pin.
- Git for Windows has system `core.autocrlf=true`. Checked-out patch SHA256 was `84edf6d382e34e2c1ede32737cc138519e4ec9feb66f5bc15a7757714b20e7d5`; application stopped until canonical bytes were obtained. `git -c core.autocrlf=false checkout-index --force` did not change that checked-out hash. `git archive --format=tar --output=../pinned-patch.tar HEAD bbport/bbport-1.7.2-bbsc.patch` in the reference clone, followed by `tar -xf`, preserved the upstream BOM/LF bytes and produced exact planned SHA256 `e34c79b388605998b430ec4eed556fc2cb8c8928f1d3e9f26bf5d2df29732aa3`.
- Reviewed all 15 destinations: registration/NP lookup, relay transport and its declarations, Matching2 member replay/static peer resolution, signaling activation/revalidation/packet layouts/helpers, and the two intentionally empty gameplay callbacks. The existing CMake recursive NP source glob already includes the added lookup source; no build-system change or replacement callbacks were added.
- `git apply --check .superpowers/reference/bbport/bbport-1.7.2-bbsc.patch`, `git apply` and `git apply --reverse --check` all exited 0. Only those 15 upstream source paths were staged. No custom runtime delta.
- Tested runtime diff: `git diff --cached --binary HEAD -- gpu`, SHA256 `27d2aa943f3ea7b43d7cc3bff0b8fececdbcdf072727207418d293fb666a8c4a`. Source-only staged tree before documentation: `f4575566f0cca45ba999c654dac689486183ca93`. This checkpoint commit identifies the complete tracked state.
- Independent source check: apply the canonical patch to the 12 original files obtained with binary-safe `git show HEAD:<path>` under ignored `postimages-v2/`; compare all 15 outputs against working files after CRLF normalization only. PASS 15/15. An initial helper omitted the first BOM-prefixed section and failed; a subsequent short Git-postimage-ID diagnostic did not match all upstream IDs and was not used as acceptance. The final content comparison passed. Private per-file working/canonical SHA256 evidence: `.superpowers/reference/r02-source-verification.json`.
- Plain `git diff --check` reports the baseline's existing CRLF lines as trailing whitespace. `git -c core.whitespace=cr-at-eol diff --check -- gpu` and staged equivalent passed; source line endings were preserved rather than reformatted.

## Dependency pins and build

`git submodule update --init --recursive` exited 0 in this checkout. All six Gitlinks remain unchanged:

| Path | Commit |
|---|---|
| gpu/third_party/fsr-vulkan | c64f093404125e960813f95f1996c14780f0dd69 |
| gpu/third_party/imgui | f1cc2ae15e53a861a874c3034aae6798fde194ab |
| gpu/third_party/magic_enum | e046b69a3736d314fad813e159b1c192eaef92cd |
| gpu/third_party/miniz | 2948eebafc5b9f1c69bebed80333e403a09bd62d |
| gpu/third_party/xbyak | cd6bad3cad2e07a3e277c23d2b1f065320024717 |
| third_party/LibAtrac9 | efca2e3af35562a09a9bb6deed90e45b4b824dc4 |

Used the installed MSYS2 CLANG64 environment, with `MSYSTEM=CLANG64`, `CHERE_INVOKING=1`, `C:/msys64/usr/bin/bash.exe -lc 'bash build.sh > .superpowers/reference/r02-build.log 2>&1'`. Waited exit 0; Ninja completed 336/336. No installs or dependency upgrades. Clang 23.1.3 (MSYS2 revision 067886dba977a6b4c97dfedfb25286b5eda55620), CMake 4.4.4, Ninja 1.13.2, Vulkan 1.4.363, SDL3 3.4.18. Installed package inventory from `pacman -Q`: private `.superpowers/reference/r02-installed-packages.txt`, SHA256 `77feb07774421cf44107e5cec489a031259c1ca0a07c57a8a8aa48b32136840b`. These are observed installed versions, not a claim to reproduce the release supplier's compiler environment.

`build.sh` applied the two already-versioned FSR-Vulkan patches to its submodule working tree, as documented in `gpu/patches/fsr-vulkan/README.md`; no Gitlink update. CMake policy/deprecation warnings were nonfatal. No new compatibility fix was needed. Linux-only `build.sh --test` programs were not run on Windows.

| Fresh source output | SHA256 |
|---|---|
| out/bb-probe.exe | a948f6948d934f024f6089d976edf97bd915f0e46381cdeaad45d9595b1a27ca |
| out/bb-gpu-capabilities.exe | 6088a8c9f98a7bf2496007a1d2d960f735cc10d9e7486739fa2c4dfd4f851a45 |
| out/bb-play.exe | 7e5d8ea54886ac8bd83de8b7cf5b49926552d5c9588166365f306271d63c91c8 |

`bb-play.exe` is an ordinary `build.sh` target; no release EXE/ZIP packaging was run.

## Gameplay DLL, existing loader and data

Fetched metadata from `https://api.github.com/repos/CLSAMG22/BBSC/releases/tags/v0.0.2`, then downloaded [BBSC-0.0.2-BBport.zip](https://github.com/CLSAMG22/BBSC/releases/download/v0.0.2/BBSC-0.0.2-BBport.zip) to ignored reference storage. Size 97,987,945 bytes; local SHA256 `001efc0a03b47bd6b2660c598fd6d172d2aaae3201a4982134d1f215918acd3c` matches GitHub's release asset digest. Saved metadata privately in `.superpowers/reference/release-v0.0.2.json`.

Extracted only `bbsc.dll`, `bbsc-launch.exe`, `mod.json`, LICENSE/NOTICE/SUPPORTERS/CREDITS, launch instructions/script and the supplied source patch into `.superpowers/baseline/`. Packaged BBport/emulator executables and runtime libraries were not extracted over source build outputs or executed. No artifact is tracked in Git.

| File under .superpowers/baseline/bbsc | SHA256 |
|---|---|
| bbsc.dll | 1df7d39e31c5d1acf034b5fd990b669e5e82944be477f26b0a46621a91610fdf |
| bbsc-launch.exe | c7fbaa406d972324645153bb8cc8bdad17fcd7db2f05026d67e3ba68f34750c1 |
| mod.json | ccea635caf411f56859070d971f5920fe60462da915f291b1f9720a285ae7321 |
| LICENSE.txt | 8177f97513213526df2cf6184d8ff986c675afb514d4e68a404010521b880643 |
| NOTICE.txt | 9919b68f5e5f4f80d2b316c7dae40c45d0d43ce6274670d67de655fb11f01f07 |
| SUPPORTERS.txt | 82c82f554ead1aef9639ee42596a34686baa508d4b9a63566c35f9b1f5dbd6a0 |
| CREDITS.txt | b8af9cabe589841374782ee4a6f6d399080c6a549b1e70bbbc53d536d87055ab |

PE inspection with `llvm-readobj --file-headers --coff-imports` confirms both mod and loader are x86-64; their imports are Windows system DLLs. The source manifest matches the release manifest after line-ending normalization: version 0.0.2, CUSA03173, bbsc.dll. All three mandatory notice markers in `emulator/mod/bbsc_mod.cpp::NoticesPresent` passed. The package's source patch hashes to `84edf6...` (CRLF); its content equals the canonical pinned patch after CRLF normalization.

Pinned mod sources/build recipe are under `emulator/mod/`; they compile `bloodborne_re.cpp`, hook/relay/channel/HTTP/Discord code and `bbsc_memscan.cpp`, with generated patch/message tables from `emulator/src/core/`. Runtime kit data comes from the user's game tables. There is no replacement loader or external game-data bundle to invent. The upstream `build-mod.cmd` requires MSVC 2022 Community/clang-cl and hardcodes `D:/BBSC/build/mod`; that compiler path is absent here. The exact official release DLL/loader above were used, not claimed as locally rebuilt or byte-reproducible from source.

## Copied-profile native evidence

The user supplied a compatible game dump, a source profile and separate self-hosted ShadNet/game-server addresses. Paths, addresses, secrets, assets, profile manifests, raw logs and captures remain private/ignored.

- SFO check using the repository's `scripts/prepare.py::sfo`: TITLE_ID CUSA03173, APP_VER 01.09. No forced patch/version override. `run.py` prepared the image, libc/modules/content and reported 30 FPS with zero extra community patch writes.
- Fresh test data: `.superpowers/r02-test/profile-a/`, user copy beneath `user/`. `robocopy /E /XJ` copied the user's profile, excluding caches/captures/logs/screenshots/shaders/save-backups/own-world and two raw log files; copy exit below 8. No old test profile or prior-repository result reused. A private pre/post manifest checks every original file and pathname: PASS 3,171/3,171 unchanged.
- Cleared inherited `BB_*`, `BBSC_*`, `SHADPS4_*` in the launch command's own environment, then set absolute `BB_GAME_DIR`, `BB_DATA_DIR`, `BB_USER_DIR`, `BB_GPU_USER_DIR`, `BB_CONFIG`, `BB_PROBE` (upstream injector), `BBSC_EMULATOR` (fresh out/bb-probe.exe), `BB_FPS=30`, `BB_ONLINE=0`. No online credentials/login or account creation. No custom managed admission/progress code was imported/enabled.
- Use existing `SHADPS4_HTTP_HOST_OVERRIDES_JSON` pointing at copied `host_overrides.custom.json`. `ss4.scej-network.jp:20443` routes to the game server; both summon-messenger prefixes route to ShadNet WebAPI :31315. The shipped launcher/source `HostOverridesFiles` define this arrangement. Set existing `BBSC_RELAY=<game-server>:20444` and `SHADPS4_P2P_RELAY=<game-server>:3478` for split-service configuration; UDP transport effectiveness is untested. Configuration SHA256: `d0bef3e27f19b3c42406a2f2422005a62ffb3ad229951fca812442020109b419`.
- First startup omitted the explicit override environment variable; with online disabled the DLL reported no override file. Closed that test normally, set the existing variable and repeated. The user then clarified the game server has a separate IP; corrected only copied configuration and repeated against the split-service layout. This is setup evidence, not a runtime change.
- Started `C:/msys64/clang64/bin/python.exe -u run.py` with hidden helper window and separate private stdout/stderr. Verified the probe process module path is exactly the pinned `.superpowers/baseline/bbsc/bbsc.dll`, not another installed DLL. Image validation, 52 patch writes, 159/159 hooks, mod-ready and kit-table-ready markers were observed. Native game process had a responsive Bloodborne window. This proves native load/startup, not visual or playable-session acceptance.
- Normal `CloseMainWindow()` was used only for the test probes started here. No original user process was running at the preflight. No save slot, login, summon or gameplay input was selected. Original-profile integrity was verified after the tests.
- Read-only TCP checks: ShadNet :31313/:31315 reachable, corrected game API :20443 reachable; game relay :20444 not reachable. The first check used the ShadNet address for game ports before the user clarified the split; that result is superseded. No service source/version inferred, no redeploy, no firewall/server change. Relay failure may have the existing P2P-channel fallback; neither fallback nor UDP :3478 was exercised with peers.

Private evidence: `.superpowers/reference/r02-build.log`, `out/gpu-build.log`, `.superpowers/reference/r02-runtime.diff`, `.superpowers/r02-test/startup*.stdout.log`/`startup*.stderr.log`, original-profile hash manifest, and `.superpowers/baseline/bbsc/logs/` plus `captures/`. Do not add these to Git.

## Acceptance boundary and next action

R02 composition/source/build/native-load acceptance is separate from gameplay. G1/G2/G3 remain WAIT_DEP. R03 build and narrow native-startup checks have evidence; self-hosted two-client routing/authentication, cross-map/Dream selected-host join, jointly earned progress/rewards, save/reload and safe return are NOT RUN. Observed Vulkan/cache/missing-optional-part warnings are recorded in private logs, not promoted to unrelated graphics fixes. No R04 change is justified by this smoke test.

Next: R03 with two distinct existing authorized accounts/copied profiles and verified required service routes; investigate actual relay/fallback availability without changing the deployed server. Do not duplicate one account to claim two clients. Keep custom admission/application OFF. No packaging or live-server redeployment.
