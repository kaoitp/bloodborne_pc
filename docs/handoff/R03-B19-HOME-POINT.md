# R03 B19: home recovery's point request landed at the lamp

2026-10-28. Claude (R03 takeover). Static diagnosis of [B17 native01](R03-B17-NATIVE-01.md) N1, source fix, fixture RED/GREEN, DLL built. **Native not run here.**

## Observation (B17 native01, N1)

- The fresh owner process requested the original point: `requested original point into 0x18010000 ... accepted true (try 1)`.
- About 9 s later it logged `arrived elsewhere`. The recorded-lamp fallback then settled at the Clinic lamp, **16.09 m** from the journaled spot.

## Cause (static reading)

`TickBbscHomeRecovery` asks for the point with `RequestBbscSessionWarp(global, to, "home recovery", false)`, and only then sets `bbsc_home_recovery_requested`. Inside that call:

1. `SetForcedSummonWarp` raises the forced-warp byte `global+0x1520`. With that byte set, the selector `0x01332BC0` takes the map and point from the forced block.
2. The selector runs at once, and its map choice (`0x01332C1B`) calls `GuardBbscStrayForcedWarp`.
3. The guard skips a home recovery only when `bbsc_home_recovery_slot && bbsc_home_recovery_requested`. The flag was still false. The guard saw a non-guest in its own world (`BbscOwnWorldNonGuest`), took `+0x1520` off and logged "taken off, the last lamp is used".
4. The selector used the last lamp, `+0x1528`, which `TickBbscHomeRecovery` had just set to the recorded lamp. The lamp is on the same map (0x18010000), so `RequestBbscSessionWarp`'s map check passed and the request was reported as accepted.
5. The load arrived at the lamp. That is 16 m from the point, outside the 5 m check, so the result was "arrived elsewhere" and then the lamp fallback.

**Check in the existing native01 log** (guest PID 19752, around 21:00:50.70): this predicts a line `BBSC forced warp at a map choice (session state 0, own world 1, forced map 0x18010000, ...): we are not a guest - taken off, the last lamp is used` right before `requested original point`. If it is there, the cause is confirmed without a new run.

## Fix

`bbsc_home_recovery_requested = true` is set **before** the point request, so the request's own map choice keeps the forced warp. A refused request still clears it, because the line after the call sets `requested`. The lamp path is unchanged: `RequestBbscLampReturn` takes the byte off itself, on purpose.

## Evidence

- `tests/test_bbsc_home_recovery.py`. Its `RequestBbscSessionWarp` stub now does what the real request does around the selector: it raises `+0x1520` and runs the actual `GuardBbscStrayForcedWarp` and `BbscOwnWorldNonGuest`, extracted from the source. The fixture's `image_base` is now non-zero, because the guard does nothing at 0. Case 1 asserts that the forced warp survives the point request's map choice.
- RED: `.superpowers/claude-r03/b19/before.cpp` (the fix removed) fails `forced_kept[0]`. GREEN with the fix.
- The full Python suite gives the same result as on `seamless` before the change: 181 ran, 48 skipped, 5 failures and 11 errors, all in the Linux-only tests, identical to the baseline.
- Patch regenerated from the reference tree. DLL `bbsc.dll` SHA256 `8b51860a1d0e12db31c346a8a10a16c9238189a7e1a17bd57739df6cb99da962`, local build, not packaged.

## Not done here, and native steps

This session does not run two instances (the user's session limit: token cost and RAM). Steps on your side:

1. Grep the native01 log for the guard line above. That is the cheap confirmation.
2. Repeat B17 N1 with this DLL, on the protected crash input, unchanged: `HOME_RECOVERY=1` on the copied guest only.
3. Expect the following:
   - `requested original point ... accepted true (try 1)`;
   - no "taken off" guard line at that time;
   - `own world and return point settled` without `arrived elsewhere`;
   - the position within 5 m of `(-190.18083,-50.62249,166.48239)`.
4. `tools/check_r03_native.py b17-n1 ...` should report MANUAL with one request. The position check stays manual.

N3's natural fallback path no longer happens on a valid point. N3 then needs the prepared synthetic unreachable-point copy. The six `12705` reload bits are a separate question: see the commit comment on 0066d0c.
