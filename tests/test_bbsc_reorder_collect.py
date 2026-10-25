"""Actual receiver + actual shared-progress collector: delayed older host snapshots (CL03 C3 /
G2-17) must not be collected as party progress. Fixture evidence, not native gameplay proof."""
from paths import ROOT
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(os.environ.get('BBSC_FIXTURE_SOURCE') or
              ROOT / '.superpowers/reference/BBSC/emulator/src/core/bloodborne_re.cpp')


def run_reorder_fixture(source, directory):
    src = source.read_text(encoding='utf-8')

    def function(signature):
        start = src.index(signature + '(')
        brace = src.index('{', start)
        depth, end = 1, brace + 1
        while depth:
            depth += (src[end] == '{') - (src[end] == '}')
            end += 1
        return src[start:end]

    constants = src[src.index('constexpr std::array<u32, 4> BbscWorldFlagKinds'):
                    src.index('static_assert(BbscDreamGroupCount <=')]
    state = src[src.index('struct BbscWorldSnapshot {'):
                src.index('// Host side: one snapshot of `count` groups')]
    progress = src[src.index('constexpr std::array<u32, 49> BbscProgressFlags'):
                   src.index('// OR the collected host progress')]
    code = r'''
#include <algorithm>
#include <array>
#include <atomic>
#include <bit>
#include <cassert>
#include <chrono>
#include <cstring>
#include <filesystem>
#include <iostream>
#include <map>
#include <mutex>
#include <optional>
#include <string>
#include <string_view>
#include <utility>
#include <vector>
#include "core/libraries/np/np_signaling/np_signaling_bbsc.h"
#define PS4_SYSV_ABI
#define LOG_INFO(...)
#define LOG_WARNING(...)
#define BBSC_TIMELINE(...)
constexpr u32 BbscDreamStateMap = 0x15000000;
constexpr u64 EventFlagManPointerOffset = 0x0553B100;
constexpr s64 BbscProgressFileMs = 10000, BbscProgressRecoverMs = 15000;
constexpr u32 BbscMapArea(u32 map) { return (map >> 24) & 0xFF; }
struct BbscSaveSlot { std::string user; int slot = -1; };
struct { u64 held = 0; } bbsc_dream_own;
s64 now_ms = 10000;
u64 image_base = 1;
s64 SteadyNowMs() { return now_ms; }
bool EnvFlagEnabled(const char*) { return true; }
bool BbscWorldSyncEnabled() { return true; }
bool IsUsablePackedMap(u32 map) { return map == 0x18000000 || map == 0x18010000; }
bool BackupBbscSaves() { return true; }
bool BbscEventFlag(u32) { return false; }
u64 BbscFlagGroupStorage(u32) { return 0; }
s32 GetSessionState() { return 6; }
s32 GetLocalPlayerType() { return 1; }
u64 GetGlobalState() { return 9; }
u64 GetLocalPlayerCharacter() { return 7; }
int GetCharacterHp(u64) { return 100; }
bool ReadablePointer(u64 p, size_t) { return p != 0; }
template<class T> T ReadValue(u64, size_t) { return 0; }
std::optional<BbscSaveSlot> BbscActiveSaveSlot() { return BbscSaveSlot{"sd1", 3}; }
std::filesystem::file_time_type bbsc_active_slot_written{};
void RestoreBbscOwnWorld(const char*) {}
bool RecoverBbscOwnWorldFile(const BbscSaveSlot&) { return false; }
bool LoadBbscPendingProgress(const BbscSaveSlot&) { return false; }
void WriteBbscPendingProgress() {}
void FinishBbscPendingProgress() {}
void BbscAnnounce(const char16_t*, const char*) {}
bool bbsc_join_teleport_done = false;
u32 BbscRelayHostForPackets() { return 0x68a4be6d; }
bool BbscGuestInHostWorld() { return true; }
u32 GetCurrentPackedMap() { return 0x18000000; }
struct BbscBossReward { s64 event; u32 flag; s32 first_lot; s32 repeat_lot; };
constexpr std::array<BbscBossReward, 1> BbscBossRewards{{{12401800, 0, 50000001, 0}}};
''' + constants + state + function('u32 BbscWorldGroupKey') + '\n' + function('void OnBbscWorldFlagsPacket') + '\n' + progress
    code += 'std::pair<s64, size_t> MergeBbscSharedProgress(std::string_view) { return {-1, 0}; }\n'
    code += function('void TickBbscSharedProgress') + '\n'
    code += r'''
using Packet = Libraries::Np::NpSignaling::SignalingBbscWorldFlags;
// One complete snapshot of map 0x18000000 whose first group has `byte` in byte 0.
void snapshot(u32 sequence, u8 byte) {
    for (size_t i = 0; i < BbscWorldChunkCount; ++i) {
        Packet p{};
        p.version = 1; p.packed_map = 0x18000000; p.snapshot = sequence;
        p.chunk = i; p.chunk_count = BbscWorldChunkCount;
        p.group_count = std::min(BbscWorldChunkGroups, BbscWorldGroupCount - i * BbscWorldChunkGroups);
        p.present = (1u << p.group_count) - 1;
        if (i == 0) p.groups[0][0] = byte;
        OnBbscWorldFlagsPacket(&p, sizeof(p));
    }
}
void tick() { now_ms += 1500; TickBbscSharedProgress(); }
u8 collected() {
    const u32 key = BbscWorldGroupKey(0x18000000, 0);
    const auto it = bbsc_progress_groups.find(key);
    return it == bbsc_progress_groups.end() ? 0 : it->second[0];
}
int main() {
    // Before placement: snapshot 40 holds a transient host bit 0x01 (e.g. a fight in progress);
    // snapshot 41 has it cleared. Both are history.
    snapshot(40, 0x01);
    tick();
    snapshot(41, 0x00);
    tick();
    bbsc_join_teleport_done = true; // placed beside the host
    tick();
    // During the party the host sets 0x80: collected.
    snapshot(42, 0x80);
    tick();
    assert(collected() == 0x80);
    // A delayed older completed snapshot (39) carrying an old bit 0x40 arrives late: the receiver
    // keeps 42, so nothing old is collected.
    snapshot(39, 0x40);
    tick();
    assert(collected() == 0x80);
    // The same with a stale copy of 40 (its transient 0x01).
    snapshot(40, 0x01);
    tick();
    assert(collected() == 0x80);
    std::cout << "PASS delayed older snapshots are not collected as party progress\n";
}
'''
    fixture = directory / 'reorder-collect.cpp'
    fixture.write_text(code, encoding='utf-8')
    binary = directory / ('reorder-collect.exe' if os.name == 'nt' else 'reorder-collect')
    subprocess.run([shutil.which('clang++'), '-std=c++23', '-O0', '-I', str(source.parents[1]),
                    str(fixture), '-o', str(binary)], check=True)
    subprocess.run([str(binary)], check=True)


@unittest.skipUnless(shutil.which('clang++') and SOURCE.is_file(),
                     'prepared pinned BBSC reference and clang++ are required')
class ReorderCollectTests(unittest.TestCase):
    def test_delayed_older_snapshots_are_not_party_progress(self):
        with tempfile.TemporaryDirectory() as directory:
            run_reorder_fixture(SOURCE, Path(directory))


if __name__ == '__main__':
    unittest.main()
