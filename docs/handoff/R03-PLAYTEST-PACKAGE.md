# Corrected playtest package — local ready

2026-10-31 (Asia/Bangkok). PK01 COMPLETE. User explicitly authorizes packaging the corrected version for later playtest, superseding the earlier no-packaging scope for this local artifact. No GitHub release uploaded, game/launcher launched, installed game or profile changed, or server deployed.

Output: `dist/bbsc-seamless-test-20261031-playtestfix.zip`, **79,462,366 bytes**, SHA256 **`b3142878caefd4699b5d29c295081780fed4af140b0f0d37ddfeb16e374dfd18`**. Adjacent `.zip.sha256` file records the same digest. ZIP files remain ignored/local rather than committed.

## Composition

Reused `dist/bbsc-seamless-test-httpfix.zip` after verifying its recorded SHA256 `401382180e01e8d3e612155445b5a7c58c3cb7504b35018cc35c616e0d36eaa1`. This is the existing experimental package, not a full clean rebuild of its launcher/emulator. Gameplay source checkpoint is `b3fa095a3513e00dff6ac638ac10b547f6401b26`.

Replaced `bbsc/bbsc.dll` with the [offline-checked correction](R03-PLAYTEST-SOURCE-FIX.md), SHA256 `fc4d851a321abf59c5a57d211e1154d9b9cbc39880e4fa5bc8082eca8249307c`, and supplied its matching LICENSE/NOTICE/SUPPORTERS files. Updated `READ-ME-TEST.txt` with fixes, limits, safe update instructions and the user playtest checklist. Added `PACKAGE-MANIFEST.json` containing runtime commit, base/DLL hashes and byte lengths/SHA256 for every original package file; the manifest excludes itself. EXEs, launcher, dependencies, account utility and mod configuration are byte-identical to the base.

## Validation

Inline Python `zipfile` assembly and validation exited0. Assertions check base/DLL hashes, unique relative member names with no traversal/drive paths, exclusion of personal runtime directories and sensitive extensions, and presence of all five replacement entries. The archive contains **1,186 entries**: 1,185 baseline entries plus the manifest. `ZipFile.testzip()` returns None; every file matches its manifest hash and either its exact base content or the explicitly supplied replacement. Existing certificate resources are retained from the verified base; no installed user directory, save, account credential, raw log or game asset was used as an input.

Private validation output/manifest is in `.superpowers/playtest-package/validation.json` and `manifest.json`. Existing runtime's 12 BBSC fixture and 2 native-header PASS/build evidence is reused because packaging does not change the DLL. No first-run, multiplayer or graphical-launcher success is inferred from ZIP checks.

## Use and next action

Both players should use the corrected DLL. Fresh installation: extract the full ZIP into a new folder and follow `READ-ME-TEST.txt`. Existing installation: close game/launcher, back up the previous `bbsc/bbsc.dll` outside the game folder and replace the DLL plus matching notices. Keep existing user folder, saves, account and server settings. No EXE replacement or switch change is required for these fixes.

User owns playtest; await both clients' mod logs, timelines and captures. Role/menu/gauge behavior, rare drops and broader R03 acceptance remain unverified on this corrected runtime. Boss replay filtering remains limited to the inspected Cleric Beast/Gascoigne bits and does not retroactively repair already-saved state. Archive is prepared locally; publishing/distribution is a separate action.
