# BBSC product outcomes

Original approved design: 2026-10-18. Scope clarified: 2026-10-23. This migrated document retains approved behavior while omitting historical implementation proposals. The [active plan](../plans/2026-10-23-bbport172-bbsc002-alignment.md) selects BBport 1.7.2 + BBSC 0.0.2 and requires baseline reuse before demonstrated-gap fixes.

The delivery goals are seamless supported-map join, jointly earned progress sync and self-hosted services. Preserve all other baseline game systems; no new launcher, input/renderer work, general quest/storage/NG framework or replacement backend is implied.

## Required behavior

1. Support main-story maps and Hunter's Dream. Chalice Dungeons are excluded.
2. Cross-map matching requires the same nonempty co-op password. Preserve existing same-map matching rules and unrelated level/channel restrictions.
3. A map being locked in the guest's own world does not prevent visiting the host there.
4. Preserve the guest's pre-party map, position, heading and previously unlocked fallback lamp before entering the host's world, including recovery after process exit.
5. Show the host's world during the visit; permanently share only events earned together. Joining must not import the host's older progress.
6. Add verified boss/story progress while preserving the guest's existing progress and conflicting NPC quest choices. Do not copy whole flag groups.
7. Return to the original point only when valid in the restored own world; otherwise use the lamp recorded before joining.
8. Give missing progression items tied to shared events only from an explicitly verified list. Do not duplicate owned items or re-grant consumed event rewards.
9. Eligibility begins when the guest has finished joining and is playable, continues through death/loading in that party, and ends on departure.
10. If the host enters an unsupported area, end co-op, notify the guest and return them safely.
11. Use the user's self-hosted BBSC-compatible game/matchmaking/summon/relay services as required by the actual release. The required join/progress path must not depend on a public BBSC/THD service.

These are outcomes, not instructions to recreate old HMAC, journal, receipt, save-codec, inventory or recovery modules. Use the selected releases' existing mechanisms first. When a demonstrated gap requires persistent-state changes, test the affected crash/retry/wrong-character/save-failure boundaries. Preserve baseline authentication, validation and save protection.

## Acceptance

Two distinct copied-profile clients/accounts must exercise cross-map/Dream join and placement, jointly earned boss/story events, independent save/reload, no older-host-progress import or relevant reward duplication, normal departure/disconnect and interrupted-session return. Record self-hosted routing for required services. Separate source/fixture/native/gameplay evidence and state untested/unsupported areas explicitly.
