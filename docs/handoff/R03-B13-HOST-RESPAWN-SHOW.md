# R03 B13: the guest is invisible on the host after the host's death

2026-10-26, Claude (R03 takeover). Base: seamless `cc4858d` (PR #7 and #8 merged). Source change in the tracked patch (`bloodborne_re.cpp` only).

Native setup:
- two online copied clients on the owner's self-hosted server;
- fresh copies of the protected Kaori host and U-I-AHH guest saves;
- spectate off on both clients;
- the disclosed debug aids (the host's own HP 0, a position read, the pad file).

## Finding

After the host died and respawned in the party, the host's screen showed only the guest's name tag and HP bar, not its body. The guest's own view was normal.

**Reproduction:** one host death (own HP 0) with the guest standing 0.6 m away.
- Before the death the guest's body was visible.
- After the respawn only the name tag showed.
- A Parting Blank and a rejoin brought the body back.

The mod's side looked healthy:
- the v8 reinsert restarted the guest's insert task (`v8 restarted 1 remote player insert task(s)`);
- the task returned to CreateWait;
- `hunters: 2` was logged;
- self-heal never fired, because the character exists.

## Cause

The guest's `PlayerIns` was dumped from the host's WorldChrMan in both states.

| State | `+0x1E0` |
|---|---|
| Recreated after the host death (invisible) | `0x9800`, later `0x8800` |
| After a fresh join (visible) | `0x109800` |
| The host's own character | `0x109800` |

**Test:** setting bit `0x100000` on the invisible guest character in the running host game made its body appear at once.

**Corroboration:** this bit is byte `+0x1E2` bit `0x10`. It is the same bit that BBSC's earlier phantom-flags experiment cleared (`+0x1E1` u32 `0x1001098 -> 0x1004098`, TickBbscReinsertV8 comment), and that experiment is documented as having made the guest invisible.

## Change

- `FindRemotePlayerOf(task)`: the existing WorldChrMan member lookup, now returning the `PlayerIns`. `RemotePlayerExists` uses it.
- `ArmBbscRemoteShow()` opens a 30 s window. It is called when the v8 reinsert restarts at least one task, and when self-heal restarts one.
- `TickBbscRemoteShow()` runs after self-heal in the rejoin block.
  - During the window and outside a load, it looks at each remote member (task mode 1/2) that has a character. If that character lacks the bit, the tick sets it, once, and logs `member character recreated without its shown bit … - set`.
  - It never touches the local player.

## Fixture

`test_bbsc_remote_show.py` compiles the actual `FindRemotePlayerOf`/`RemotePlayerExists` and the new show block with controlled memory. It covers:
- not armed;
- armed while loading;
- armed, which sets the remote guest's bit and leaves the self-host character and an already shown member alone;
- the window over;
- re-armed.

It is built with ASan.
- **RED** on the merged seamless source (`flags(guest_chr) == 0x109800` fails).
- **GREEN** now.
- `test_bbsc_*` 7 OK, `test_native_bbsc` 2 OK, `git diff --check` clean.
- DLL build `8dc083de…`, exit 0.

## Native evidence

Run with the new DLL, fresh saves:
- the guest joined and was placed (spectate off);
- host HP 0;
- 14:59:26.618 `v8 restarted`;
- 14:59:26.651 `member character recreated without its shown bit (+0x1E0 0x0, mode 1) - set`. The character was brand new, so its flags read 0, and the game filled in the rest later: it read `0x108800` afterwards.

**Screenshots:**
- the host sees the guest's body beside its name tag after the respawn;
- the guest sees the host normally.

## Limits

- Only the host-death path was tested natively. Self-heal re-arming the window has fixture coverage only.
- The meaning of the bit beyond "drawn" is not known. It is set only on remote member characters, only for 30 s after a restart, and only when missing.
- A guest's own death respawn was not looked at here: the guest's view of the host after a guest death.

## Also from this session: host stops were the rig

The host process stopped twice during a load earlier today. There was no crash line and no Windows error record, and the rig's PowerShell launcher ended with exit 1 at the same moment.

- **Cause:** the launcher used `$ErrorActionPreference='Stop'` with `*>` redirection. PowerShell 5.1 turns the first stderr line into a terminating error. This was reproduced without the game.
- **Fix:** the rig now launches through `cmd` and keeps one log per launch with the exit code.
- No mod change.

All protected source saves are unchanged. Test processes were closed.
