# T2: own-world flags after save and independent reload

2026-10-29 (Asia/Bangkok), Codex. **PASS for the T1 recovered owner and matching-build no-party control.** Twelve settled snapshots across three fresh processes equal all1,250 prejoin groups; position and rotation remain exact. The six previously unclassified12705 bits reproduce during ordinary loading and clear without recovery or party activity. No product/source/default/server changes. T3/T4 and broad R03 remain open.

## Inputs and scope

User requests T2 after [T1](R03-T1-POINT-RECOVERY.md). Branch seamless at `8cebe51b566635ec294248f790c3c901b523d30e`. Reuse the unchanged T1 B19 build, mandatory notices and existing probe; hashes independently rechecked before preparation and after testing. No new build or fixture run was needed for this native-only continuation.

| Tested input | SHA256 |
|---|---|
| patch | `0d152637899ab4c0fbff97aa874da44d955b7e7090ff0a0b13ca0553de852608` |
| source | `464a21d71a212d5c64201c352571f2756b935f95aa7be59e87bf7d3c77ff7d39` |
| dll | `642a16933d7d821b301b3c4a9e373787800fadc7ba33023d972471972cfc5b5b` |
| probe | `6696d7d39c5d0c7e0bf16b29a1f624b5549ac9046f1886902da9564ba8940c14` |

Private evidence: `.superpowers/t2`. `reload-profile-b` is a fresh native01 profile copy with savedata and own-world directories replaced entirely from T1's protected after-t1-savedata/after-t1-own-world. Per-file hashes match those protected inputs. `control-profile-b` is a separate native01 profile copy, the savedata source used in the B17 preparation; its loaded state is independently compared against B17 prejoin. It has no new party in these control runs. Neither profile has an active `.bin` own-world journal; only retained restored/history files. No home recovery/own-world crash replay is logged in any T2 process. T1 originals and protected inputs are preserved.

Both profiles reuse T1's effective copied configuration: HOME_RECOVERY1, EXPERIMENTAL_HOME_RECOVERY0, SHARED_PROGRESS0, REWARD_ONCE0, GUEST_ITEMS1, DREAM1, SPECTATE0, no-death1,1280x720/30FPS and existing authorized online account/services. Play Online -> Continue with native BB_PAD_FILE controls. No bells, joining, movement or earned events. The three processes run sequentially; no second client needed. All report verified image/50 patch sites/160 hooks.

## Native results

Times below are Asia/Bangkok. Each range contains four snapshots about15s apart. All acceptance snapshots have own_world1, character_type0, loading0 and visible settled Clinic; loading0 alone was not used as settlement proof.

| Case | PID / mod log suffix | Early differences against prejoin | Repeated settled snapshots | Result |
|---|---|---|---|---|
| reload | 28488 / 193528-28488 | 12705301 at19:36:55 | 19:37:10–19:37:56: all1250 exact | PASS |
| control-before | 2968 / 193827-2968 | eleven bits at19:39:33–39; only12705301 by19:39:43 | 19:40:01–19:40:47: all1250 exact | PASS |
| control-after | 4276 / 194240-4276 | same eleven bits at19:44:01–08; only12705301 by19:44:11 | 19:44:30–19:45:16: all1250 exact | PASS |

Full log names: bbsc-mod-20261029-<suffix>.log under `.superpowers/t1/dll/logs`, because the same DLL directory is reused. Every settled snapshot also equals T1's immediate settled world and both control states. Map0x18010000, lamp2412950, position `(-190.1808319091797,-50.62248992919922,166.48239135742188,1)`, rotation `(0,0.06571602821350098,0,0)`; distance from journaled T1 origin **0.0m** in all twelve snapshots.

Control-before: after four exact settled snapshots, normal System -> Exit Game -> YES. userdata0003 saved19:42:04; title startup logo observed. Changed files are userdata0003, userdata0010 and their corresponding backups. Process closes exit0. `control-saved-manifest.json` verifies that control-after restarts from exactly this saved output; no save replacement between those runs. After sampling, reload and control-after windows close normally, runners exit0. No game remains running.

## Six-bit classification

The B17 differences `12705098,12705301,12705520,12705521,12705531,12705532` are all ON in the prejoin baseline, temporarily OFF during both ordinary no-party control loads, then ON again in every settled snapshot. Neither control process has an active recovery journal or logs a restoration. Thus these six observed differences are loading transients for this composition/Clinic state, not persistent personal-progress loss. The control also temporarily differs at12415461 and12415770–12415773; all eleven disappear by the first settled acceptance sample. No undocumented gameplay meaning is assigned to those flags.

The after-T1 process captures only12705301 in its first usable early position+world sample, then no differences. Its five other suspect bits already equal baseline when first sampled. Independently reproducing the full six-bit pattern in both no-party loads, and exact repeated after-T1 reload equality, resolves the T2 concern. This agrees with the older [B07 control](R03-B07-INDEPENDENT-RELOAD.md), but today's matching-build native evidence stands separately.

## Commands and checks

CLANG64 Python `C:/msys64/clang64/bin/python.exe`:

- `.superpowers/t2/prepare.py`: exit0; verifies T1 hashes, creates separate copies with assert-guarded paths, compares protected save manifests and captures original3171 hashes.
- `launch-reload.ps1 b`, `launch-control.ps1 b`, `launch-control-after.ps1 b`: existing T1 launch pattern adjusted only for copied profile/log paths. Run outside sandbox because T1 established address-space reservation failure inside it. Final runner exits0/0/0.
- `.superpowers/t2/capture.py <PID> <case>`: calls existing read-only read-position.py/read-world.py, retains raw snapshots and UTC sample times plus bit deltas. Reload samples at15s intervals; controls sample more densely during early load, then15s apart. First sample in each process cannot yet read the character position; it is excluded from acceptance. No memory writes.
- `.superpowers/t2/assert-result.py`: exit0. Asserts exact complete group dictionaries, role/loading/map/lamp/position/rotation for all12 settled snapshots; six-bit independent early reproduction; no active journals/recovery replay; all three module/hook confirmations; unchanged source/patch/DLL/probe and **3171 original paths/hashes exact**. Result in private assert-result.json; manifests and raw saves/logs remain ignored.

T2 native checks pass. This is bounded flag/position save persistence, not an inventory audit, new crash or multiplayer earning test. Recovery remains opt-in; no default/managed switch, packaging, deployment or PR17 reward-protocol change. Next: T3 actual pending-return cancellation, other-character before/after preservation and original-owner retry; then T4 forced-point failure and recorded-lamp persistence. Preserve protected B17 crash input for those cases.
