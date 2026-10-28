"""Actual durable-origin return after a crash as a guest (R03 B17; B16 case 2: the guest woke in its
own world at the host's spot). An opt-in candidate until its native gate; bound to its owner (a load
from the title drops it, every step checks the active save slot, the journal file stays until the
return settles) and bounded per target (accepted request without a load times out, a failed point
goes to the recorded lamp, the arrival counts before the budget, an exhausted lamp ends once with the
journal kept as .unreturned). Fixture evidence with controlled memory, a real journal file and stubbed
warp/lamp requests in a temporary folder, not native gameplay proof."""
from paths import ROOT
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(os.environ.get('BBSC_FIXTURE_SOURCE') or
              ROOT / '.superpowers/reference/BBSC/emulator/src/core/bloodborne_re.cpp')
HEADER_DIR = ROOT / 'gpu/bbnet'


def run_home_fixture(source, directory):
    src = source.read_text(encoding='utf-8')

    def function(head):
        start = src.index(head)
        while src.index(';', start) < src.index('{', start):  # a declaration: skip to the definition
            start = src.index(head, start + 1)
        brace = src.index('{', start)
        depth, end = 1, brace + 1
        while depth:
            depth += {'{': 1, '}': -1}.get(src[end], 0)
            end += 1
        return src[start:end]

    code = r'''
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <optional>
#include <string>
#include <string_view>
#include <vector>
#include "bbsc_home_spot.h"
using s32 = int32_t; using s64 = int64_t; using u8 = uint8_t; using u32 = uint32_t; using u64 = uint64_t;
#define PS4_SYSV_ABI
#define LOG_INFO(...)
#define LOG_WARNING(...)
#define BBSC_TIMELINE(...)
namespace Bbsc = Core::Bbsc;
struct BbscSaveSlot { std::string user; int slot = -1; };
constexpr size_t BbscWorldGroupBytes = 128;
std::map<u32, std::array<u8, BbscWorldGroupBytes>> bbsc_own_world;
std::optional<BbscSaveSlot> bbsc_own_world_slot;
bool bbsc_own_world_dirty = false;
std::u16string bbsc_own_world_owner;
bool bbsc_own_world_continuous = false;
std::optional<BbscSaveSlot> bbsc_home_recovery_slot;
struct BbscTransform { std::array<float, 4> position{}; std::array<float, 4> rotation{}; };
struct SummonPlacementDescriptor { u32 packed_region{}; float x{}, y{}, z{}, heading{}; s32 area{}; };
constexpr u64 SelectSummonedPlacementOffset = 0x01332BC0, StageTransitionOffset = 0x013CDE30;
alignas(16) u8 global_block[0x1600] = {};
u64 image_base = 0x1000;                         // loaded (the guard does nothing before)
u64 GetGlobalState() { return reinterpret_cast<u64>(global_block); }
bool ReadablePointer(u64 p, size_t) { return p != 0; }
template <class T> T ReadValue(u64 base, u64 off) { T v{}; std::memcpy(&v, reinterpret_cast<const void*>(base + off), sizeof(T)); return v; }
template <class T> bool WriteValue(u64 base, size_t off, const T& v) { std::memcpy(reinterpret_cast<void*>(base + off), &v, sizeof(T)); return true; }
s64 SteadyNowMs() { static s64 now = 0; return now += 1000; }
u32 current_map = 0x18000000;                     // Cathedral Ward: the host's spot
BbscTransform here{{19.77f, -9.51f, 101.51f, 1.f}, {}};
int hp = 100;
u32 GetCurrentPackedMap() { return current_map; }
bool IsUsablePackedMap(u32 m) { return m != 0; }
u64 GetLocalPlayerCharacter() { return 7; }
int GetCharacterHp(u64) { return hp; }
std::optional<BbscTransform> ReadCharacterTransform(u64) { return here; }
bool home = true;
bool BbscHomeForOwnWorld() { return home; }
std::optional<BbscSaveSlot> active_slot;          // nullopt: not written since the load
std::optional<BbscSaveSlot> BbscActiveSaveSlot() { return active_slot; }
std::filesystem::path BbscOwnWorldPath(const BbscSaveSlot& s) {
    return "own-" + s.user + "-" + std::to_string(s.slot) + ".bin";
}
std::string BbscAreaName(u32) { return "area"; }
std::u16string BbscLocalCharacterName() { return u"x"; }
int announced = 0;
void BbscAnnounce(const char16_t*, const char*) { ++announced; }
bool LoadBbscOwnWorldFile(const BbscSaveSlot& s) { bbsc_own_world_slot = s; return true; }
u32 BbscLampPointMap(s32 lamp) {
    return lamp < 1000000 ? 0u : (static_cast<u32>(lamp / 100000) << 24) | (static_cast<u32>((lamp / 10000) % 10) << 16);
}
std::vector<u32> warps;                           // maps the return asked for
std::vector<bool> forced_kept;                    // the forced warp survived the request's map choice
bool warp_ok = true;
struct GuestRegisterSnapshot { u64 rcx{}, rsi{}, rbp{}; };
s32 GetSessionState() { return 0; }                // own world, no session
bool PutBbscHomeSpot(u64) { return false; }
void GuardBbscStrayForcedWarp(const GuestRegisterSnapshot& registers);
bool RequestBbscSessionWarp(u64 global, const SummonPlacementDescriptor& to, std::string_view, bool) {
    warps.push_back(to.packed_region);
    // As the real request: SetForcedSummonWarp raises +0x1520, then the selector 0x01332BC0 runs and
    // its map choice (0x01332C1B) calls the guard. With +0x1520 off the selector takes the last lamp.
    WriteValue<u8>(global, 0x1520, 1);
    GuardBbscStrayForcedWarp({global, 0xFFFFFFFF, 0});
    forced_kept.push_back(ReadValue<u8>(global, 0x1520) != 0);
    return warp_ok;
}
std::vector<u32> lamp_targets;                    // lamp loads the return asked for
bool lamp_ok = true;
bool RequestBbscLampReturn(u64, u32 target) {
    lamp_targets.push_back(target);
    return lamp_ok;
}
void SuspendBbscHomeRecovery();
'''
    for name in ('BbscHomeRecoveryOn', 'SettleBbscHomeRecovery', 'NoteBbscHomeRecoveryLoad',
                 'FailBbscHomeRecoveryTarget', 'RequestBbscLampReturn'):
        if f' {name}(' not in src:
            raise AssertionError(f'source has no {name}: no owner-bound durable-origin return')
    start = src.index('struct BbscHomeSpot {')
    code += src[start:src.index('// Game tick: forget the spot', start)]
    code += function('void NoteBbscOwnWorldCharacterLoad(') + '\n'
    code += function('bool BbscOwnWorldNonGuest(') + '\n' + function('void GuardBbscStrayForcedWarp(') + '\n'
    code += r'''
const BbscSaveSlot u_i_ahh{"sd1", 3}, kaori{"sd1", 0};
const u32 clinic = 0x18010000;
const s32 lamp = 2401000;                         // its recorded lamp: area 24 (0x18), map 0x18000000
const u32 lamp_map = 0x18000000;
void env(const char* value) {
#ifdef _WIN32
    _putenv_s("SHADPS4_BBSC_HOME_RECOVERY", value);
#else
    setenv("SHADPS4_BBSC_HOME_RECOVERY", value, 1);
#endif
}
std::filesystem::path with(const BbscSaveSlot& s, const char* ext) {
    return std::filesystem::path(BbscOwnWorldPath(s)).concat(ext);
}
void clean(const BbscSaveSlot& s) {
    std::filesystem::remove(BbscOwnWorldPath(s));
    std::filesystem::remove(with(s, ".restored"));
    std::filesystem::remove(with(s, ".unreturned"));
}
void journal(const BbscSaveSlot& s, s32 rec_lamp = lamp) { // a crash left this file; armed as RecoverBbscOwnWorldFile does
    std::ofstream(BbscOwnWorldPath(s)) << "journal";
    bbsc_own_world.clear();
    const auto bytes = Bbsc::EncodeHomeSpot({clinic, rec_lamp, {-190.19f, -50.63f, 170.59f, 1.f}, {}});
    std::copy(bytes.begin(), bytes.end(), bbsc_own_world[Bbsc::HomeSpotKey].begin());
    bbsc_own_world_slot = s;
    RecoverBbscHomeSpot(s);
}
void tick(int n) { // as TickBbscHomeSpot calls it
    for (int i = 0; i < n; ++i) if (bbsc_home_recovery_slot) TickBbscHomeRecovery();
}
void arrive(u32 map, float x) { // the requested load, then the game saves the slot
    NoteBbscHomeRecoveryLoad();
    active_slot.reset();
    current_map = map;
    here.position = {x, -50.63f, 170.59f, 1.f};
    tick(2);                  // slot unknown since the load: waits
    assert(bbsc_home_recovery_slot.has_value());
    active_slot = u_i_ahh;
}
bool kept(const BbscSaveSlot& s) { return std::filesystem::exists(BbscOwnWorldPath(s)); }
bool settled(const BbscSaveSlot& s) { return std::filesystem::exists(with(s, ".restored")); }
bool unreturned(const BbscSaveSlot& s) { return std::filesystem::exists(with(s, ".unreturned")); }
void fresh() {
    clean(u_i_ahh);
    bbsc_home_recovery_slot.reset();
    current_map = 0x18000000;
    here.position = {19.77f, -9.51f, 101.51f, 1.f};
    warps.clear();
    forced_kept.clear();
    global_block[0x1592] = 1;                     // in our own world
    lamp_targets.clear();
    warp_ok = lamp_ok = true;
    announced = 0;
    active_slot = u_i_ahh;
}
int main() {
    // 0. An opt-in candidate until the native gate: not armed by default.
    fresh();
    journal(u_i_ahh);
    assert(!bbsc_home_recovery_slot);
    env("1");

    // 1. B16 case 2 (opt-in): back to the Clinic spot, then settled.
    fresh();
    journal(u_i_ahh);
    assert(bbsc_home_recovery_slot.has_value());
    tick(3);
    assert(warps.size() == 1 && warps[0] == clinic);
    // B17 native01: the guard must keep the forced warp for the point, or the load goes to the lamp.
    assert(forced_kept.size() == 1 && forced_kept[0]);
    arrive(clinic, -190.19f);
    tick(3);
    assert(!bbsc_home_recovery_slot && settled(u_i_ahh) && !kept(u_i_ahh));

    // 2. A02: Quit Game -> title -> another character before the arrival. Nothing reaches Kaori; the
    // file stays for U-I-AHH.
    fresh();
    journal(u_i_ahh);
    tick(3);
    assert(warps.size() == 1);
    NoteBbscOwnWorldCharacterLoad();              // Warp.StageDescriptor.Finalize rdi 0: the title
    NoteBbscHomeRecoveryLoad();                   // that load's RespawnPoint.Resolve
    active_slot = kaori;
    current_map = clinic;
    tick(40);
    assert(!bbsc_home_recovery_slot && warps.size() == 1 && lamp_targets.empty());
    assert(kept(u_i_ahh) && !settled(u_i_ahh) && !unreturned(u_i_ahh));
    //    ... and its owner takes it up again (RecoverBbscOwnWorldFile when it is home).
    active_slot = u_i_ahh;
    current_map = 0x18000000;
    journal(u_i_ahh);
    tick(3);
    assert(warps.size() == 2 && warps[1] == clinic);

    // 3. A02 with the title load missed: Kaori's load is taken for the return's; the slot check drops
    // it at Kaori's first step - no lamp, nothing settled.
    fresh();
    journal(u_i_ahh);
    tick(3);
    NoteBbscHomeRecoveryLoad();
    active_slot = kaori;
    here.position = {500.f, 0.f, 0.f, 1.f};
    current_map = clinic;
    tick(40);
    assert(!bbsc_home_recovery_slot && warps.size() == 1 && lamp_targets.empty() && kept(u_i_ahh));

    // 4. Another load before the return (a death): dropped, the file stays; asked again on re-arming.
    fresh();
    journal(u_i_ahh);
    NoteBbscHomeRecoveryLoad();
    assert(!bbsc_home_recovery_slot && kept(u_i_ahh));
    journal(u_i_ahh);
    tick(3);
    assert(warps.size() == 1);

    // 5. Accepted but no load ever comes: times out (not before 30 s), then the recorded lamp.
    fresh();
    journal(u_i_ahh);
    tick(3);
    assert(warps.size() == 1);
    tick(20);                                     // ~20 s: still waiting for the load
    assert(bbsc_home_recovery_slot.has_value() && lamp_targets.empty());
    tick(15);                                     // past 30 s: point failed -> lamp asked
    assert(lamp_targets.size() == 1 && lamp_targets[0] == lamp_map && warps.size() == 1);
    arrive(lamp_map, 300.f);                      // at the lamp (any spot on its map)
    tick(3);
    assert(!bbsc_home_recovery_slot && settled(u_i_ahh));

    // 6. Point refused while a valid lamp is recorded: the lamp is used, not the point five times.
    fresh();
    warp_ok = false;
    journal(u_i_ahh);
    tick(5);
    assert(warps.size() == 1 && lamp_targets.size() == 1);
    arrive(lamp_map, 300.f);
    tick(3);
    assert(!bbsc_home_recovery_slot && settled(u_i_ahh) && announced == 0);

    // 7. The last try works (no lamp recorded): a success, not a spent budget.
    fresh();
    warp_ok = false;
    journal(u_i_ahh, -1);
    tick(4);                                      // two refused point requests
    assert(warps.size() == 2 && bbsc_home_recovery_slot.has_value());
    warp_ok = true;
    tick(3);                                      // the third and last: accepted
    assert(warps.size() == 3);
    arrive(clinic, -190.19f);
    tick(3);
    assert(!bbsc_home_recovery_slot && settled(u_i_ahh) && announced == 0);

    // 8. Point refused, lamp exhausted: ends once, journal kept as .unreturned, the player told.
    fresh();
    warp_ok = false;
    lamp_ok = false;
    journal(u_i_ahh);
    tick(40);
    assert(!bbsc_home_recovery_slot && unreturned(u_i_ahh) && !settled(u_i_ahh) && announced == 1);
    assert(warps.size() == 1 && lamp_targets.size() == 3);

    // 9. No lamp, the point never works: 3 point tries, then the same single end.
    fresh();
    warp_ok = false;
    journal(u_i_ahh, -1);
    tick(40);
    assert(!bbsc_home_recovery_slot && unreturned(u_i_ahh) && announced == 1);
    assert(warps.size() == 3 && lamp_targets.empty());

    // 10. Arrived on the right map but far from the spot: the lamp, then settled.
    fresh();
    journal(u_i_ahh);
    tick(3);
    arrive(clinic, 400.f);
    tick(3);
    assert(lamp_targets.size() == 1);
    arrive(lamp_map, 0.f);
    tick(3);
    assert(!bbsc_home_recovery_slot && settled(u_i_ahh));

    // 11. Off again with =0.
    fresh();
    env("0");
    journal(u_i_ahh);
    assert(!bbsc_home_recovery_slot);
    std::cout << "PASS durable origin: opt-in candidate, owner-bound (title load, active slot), "
                 "load timeout, point->lamp fallback, arrival before budget, single bounded end\n";
}
'''
    fixture = directory / 'home-recovery.cpp'
    fixture.write_text(code, encoding='utf-8')
    binary = directory / ('home-recovery.exe' if os.name == 'nt' else 'home-recovery')
    subprocess.run([shutil.which('clang++'), '-std=c++23', '-O0', '-g', '-fsanitize=address',
                    '-I', str(HEADER_DIR), str(fixture), '-o', str(binary)], check=True)
    subprocess.run([str(binary)], check=True, cwd=directory)


@unittest.skipUnless(shutil.which('clang++') and SOURCE.is_file(),
                     'prepared pinned BBSC reference and clang++ are required')
class HomeRecoveryTests(unittest.TestCase):
    def test_durable_origin_is_owner_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            run_home_fixture(SOURCE, Path(directory))


if __name__ == '__main__':
    unittest.main()
