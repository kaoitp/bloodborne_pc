"""Actual durable-origin return after a crash as a guest (R03 B17; B16 case 2: the guest woke in its
own world at the host's spot). The return is on by default and bound to its owner: a load from the
title drops it, every step checks the active save slot, the journal file stays until the return
settles, and a return with no way back gives up once (bounded fallback). Fixture evidence with
controlled memory and a real journal file in a temporary folder, not native gameplay proof."""
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
u64 image_base = 0;
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
bool warp_ok = true;
bool RequestBbscSessionWarp(u64, const SummonPlacementDescriptor& to, std::string_view, bool) {
    warps.push_back(to.packed_region);
    return warp_ok;
}
void SuspendBbscHomeRecovery();
'''
    for name in ('BbscHomeRecoveryOn', 'SettleBbscHomeRecovery', 'NoteBbscHomeRecoveryLoad'):
        if f' {name}(' not in src:
            raise AssertionError(f'source has no {name}: no owner-bound durable-origin return')
    start = src.index('struct BbscHomeSpot {')
    code += src[start:src.index('// Game tick: forget the spot', start)]
    code += function('void NoteBbscOwnWorldCharacterLoad(') + '\n'
    code += r'''
const BbscSaveSlot u_i_ahh{"sd1", 3}, kaori{"sd1", 0};
const u32 clinic = 0x18010000;
void journal(const BbscSaveSlot& s, s32 lamp = 1801000) { // a crash left this file; arm as RecoverBbscOwnWorldFile does
    std::ofstream(BbscOwnWorldPath(s)) << "journal";
    bbsc_own_world.clear();
    const auto bytes = Bbsc::EncodeHomeSpot({clinic, lamp, {-190.19f, -50.63f, 170.59f, 1.f}, {}});
    std::copy(bytes.begin(), bytes.end(), bbsc_own_world[Bbsc::HomeSpotKey].begin());
    bbsc_own_world_slot = s;
    RecoverBbscHomeSpot(s);
}
void tick(int n) { // as TickBbscHomeSpot calls it
    for (int i = 0; i < n; ++i) if (bbsc_home_recovery_slot) TickBbscHomeRecovery();
}
void arrive(u32 map, float x) { // the warp's load, then the game saves the slot
    NoteBbscHomeRecoveryLoad();
    active_slot.reset();
    current_map = map;
    here.position = {x, -50.63f, 170.59f, 1.f};
    tick(1);                  // slot unknown since the load: waits
}
bool kept(const BbscSaveSlot& s) { return std::filesystem::exists(BbscOwnWorldPath(s)); }
bool settled(const BbscSaveSlot& s) {
    return std::filesystem::exists(std::filesystem::path(BbscOwnWorldPath(s)).concat(".restored"));
}
void reset_world() { current_map = 0x18000000; here.position = {19.77f, -9.51f, 101.51f, 1.f}; warps.clear(); }
int main() {
    // 1. B16 case 2, default configuration: back to the Clinic spot, then settled.
    active_slot = u_i_ahh;
    journal(u_i_ahh);
    assert(bbsc_home_recovery_slot.has_value()); // on by default
    tick(3);
    assert(warps.size() == 1 && warps[0] == clinic);
    arrive(clinic, -190.19f);
    assert(bbsc_home_recovery_slot.has_value() && !settled(u_i_ahh));
    active_slot = u_i_ahh;
    tick(3);
    assert(!bbsc_home_recovery_slot && settled(u_i_ahh) && !kept(u_i_ahh));

    // 2. A02: Quit Game -> title -> another character before the return arrived. Nothing of the
    // return reaches Kaori; the file stays for U-I-AHH.
    reset_world();
    std::filesystem::remove(std::filesystem::path(BbscOwnWorldPath(u_i_ahh)).concat(".restored"));
    active_slot = u_i_ahh;
    journal(u_i_ahh);
    tick(3);
    assert(warps.size() == 1);                    // asked, not yet loaded
    NoteBbscOwnWorldCharacterLoad();              // Warp.StageDescriptor.Finalize rdi 0: the title
    NoteBbscHomeRecoveryLoad();                   // that load's RespawnPoint.Resolve
    active_slot = kaori;
    current_map = clinic;                         // even on the same map
    tick(5);
    assert(!bbsc_home_recovery_slot && warps.size() == 1 && kept(u_i_ahh) && !settled(u_i_ahh));

    // 3. Same, but the title load is missed: the owner check alone drops it at Kaori's first step.
    reset_world();
    active_slot = u_i_ahh;
    journal(u_i_ahh);
    tick(3);
    assert(warps.size() == 1);
    NoteBbscHomeRecoveryLoad();                   // accepted as "the return's load" (A02's hole)
    active_slot = kaori;
    here.position = {500.f, 0.f, 0.f, 1.f};      // far from the spot: would ask for the lamp
    current_map = clinic;
    tick(5);
    assert(!bbsc_home_recovery_slot && warps.size() == 1 && kept(u_i_ahh) && !settled(u_i_ahh));

    // 4. Another load before the return (a death): dropped, the file stays; its owner takes it up again.
    reset_world();
    active_slot = u_i_ahh;
    journal(u_i_ahh);
    NoteBbscHomeRecoveryLoad();                   // not asked for: suspends
    assert(!bbsc_home_recovery_slot && kept(u_i_ahh));
    journal(u_i_ahh);                             // RecoverBbscOwnWorldFile again, 15 s later
    tick(3);
    assert(warps.size() == 1 && warps[0] == clinic);

    // 5. No way back: the point is refused every time and no lamp is recorded -> gives up once,
    // own world kept, the journal settled, the player told.
    reset_world();
    bbsc_home_recovery_slot.reset();
    std::filesystem::remove(BbscOwnWorldPath(u_i_ahh));
    active_slot = u_i_ahh;
    warp_ok = false;
    journal(u_i_ahh, -1);
    tick(40);
    assert(!bbsc_home_recovery_slot && settled(u_i_ahh) && announced == 1);
    assert(warps.size() == 5);                    // BbscHomeRecoveryMaxTries, then no more
    warp_ok = true;

    // 6. Opt-out: SHADPS4_BBSC_HOME_RECOVERY=0 arms nothing.
    reset_world();
    std::filesystem::remove(std::filesystem::path(BbscOwnWorldPath(u_i_ahh)).concat(".restored"));
#ifdef _WIN32
    _putenv_s("SHADPS4_BBSC_HOME_RECOVERY", "0");
#else
    setenv("SHADPS4_BBSC_HOME_RECOVERY", "0", 1);
#endif
    journal(u_i_ahh);
    assert(!bbsc_home_recovery_slot);
    std::cout << "PASS durable origin: back to the spot by default, owner-bound (title load, active "
                 "slot), dropped returns kept for the owner, bounded fallback, opt-out\n";
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
