import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get('BBSC_FIXTURE_SOURCE') or
              ROOT / '.superpowers/reference/BBSC/emulator/src/core/bloodborne_re.cpp')


def run_party_fixture(source, directory):
    src = source.read_text(encoding='utf-8')

    def function(signature):
        start = src.index(signature + '(')
        brace = src.index('{', start)
        depth, end = 1, brace + 1
        while depth:
            if src[end] == '{':
                depth += 1
            elif src[end] == '}':
                depth -= 1
            end += 1
        return src[start:end]

    code = r'''
#include <algorithm>
#include <array>
#include <atomic>
#include <bit>
#include <cassert>
#include <cstdint>
#include <cstring>
#include <filesystem>
#include <iostream>
#include <map>
#include <mutex>
#include <optional>
#include <set>
#include <string>
#include <string_view>
#include <utility>
#include <vector>
using s64 = int64_t; using u64 = uint64_t; using s32 = int32_t;
using u32 = uint32_t; using u8 = uint8_t;
#define PS4_SYSV_ABI
#define LOG_INFO(...)
#define LOG_WARNING(...)
#define BBSC_TIMELINE(...)
struct BbscSaveSlot { std::string user; int slot = -1; };
struct BbscWorldSnapshot {
    s64 complete_ms = 0; u32 map = 0; u64 present = 0;
    std::array<std::array<u8, 125>, 10> groups{};
};
std::mutex bbsc_world_mutex;
std::map<u32, BbscWorldSnapshot> bbsc_world_blocks;
struct { u64 held = 0; } bbsc_dream_own;
constexpr u32 BbscDreamStateMap = 0x15000000;
constexpr size_t BbscWorldGroupBytes = 125;
constexpr u64 EventFlagManPointerOffset = 0x0553B100;
constexpr s64 BbscProgressFileMs = 10000, BbscProgressRecoverMs = 15000;
s64 now_ms = 10000;
u64 image_base = 1; // nonzero: the tick runs
bool EnvFlagEnabled(const char*) { return true; }
s64 SteadyNowMs() { return now_ms; }
bool BackupBbscSaves() { return true; }
bool BbscEventFlag(u32) { return false; }
u64 BbscFlagGroupStorage(u32) { return 0; }
u32 BbscWorldGroupKey(u32 map, size_t index) { return (map >> 16) * 10 + static_cast<u32>(index); }
s32 session_state = 6;
s32 GetSessionState() { return session_state; }
s32 GetLocalPlayerType() { return 1; }
u64 GetGlobalState() { return 9; }
u64 GetLocalPlayerCharacter() { return 7; }
int GetCharacterHp(u64) { return 100; }
bool ReadablePointer(u64 p, size_t) { return p != 0; }
template<class T> T ReadValue(u64 at, size_t off) { return 0; }
std::optional<BbscSaveSlot> BbscActiveSaveSlot() { return BbscSaveSlot{"sd1", 3}; }
void RestoreBbscOwnWorld(const char*) {}
bool RecoverBbscOwnWorldFile(const BbscSaveSlot&) { return false; }
bool LoadBbscPendingProgress(const BbscSaveSlot&) { return false; }
void WriteBbscPendingProgress() {}
void FinishBbscPendingProgress() {}
void BbscAnnounce(const char16_t*, const char*) {}
std::atomic<u32> bbsc_host_world_resets{0};
std::filesystem::file_time_type bbsc_active_slot_written{};
bool bbsc_join_teleport_done = false;
u32 relay_host = 0x68a4be6d;
u32 BbscRelayHostForPackets() { return relay_host; }
bool in_host_world = true;
bool BbscGuestInHostWorld() { return in_host_world; }
u32 current_map = 0x18000000;
u32 GetCurrentPackedMap() { return current_map; }
constexpr u32 BbscMapArea(u32 map) { return (map >> 24) & 0xFF; }
struct BbscBossReward { s64 event; u32 flag; s32 first_lot; s32 repeat_lot; };
constexpr std::array<BbscBossReward, 1> BbscBossRewards{{{12401800, 0, 50000001, 0}}};
std::atomic<s32> bbsc_relay_session_state{6};
std::atomic<s32> bbsc_host_time_bits{-1};
std::atomic<s64> bbsc_host_time_ms{0};
'''
    start = src.index('constexpr std::array<u32, 49> BbscProgressFlags')
    end = src.index('// OR the collected host progress', start)
    code += src[start:end]
    code += 'std::pair<s64, size_t> MergeBbscSharedProgress(std::string_view) { return {-1, 0}; }\n'
    for signature in ('void TickBbscSharedProgress', 'void OnBbscProgressPacket'):
        code += function(signature) + '\n'
    has_admit = 'void AdmitBbscRewardEvent(' in src
    code += ('void admit(s64 e) { AdmitBbscRewardEvent(e); }\n' if has_admit else
             'void admit(s64) {}\n')
    code += r'''
bool has(u32 flag) {
    return std::ranges::find(bbsc_progress_host_flags, flag) != bbsc_progress_host_flags.end();
}
bool bit(u32 key, u32 n) {
    const auto it = bbsc_progress_groups.find(key);
    return it != bbsc_progress_groups.end() && (it->second[n / 8] & (0x80u >> (n % 8))) != 0;
}
void packet(std::vector<u32> flags) { OnBbscProgressPacket(flags.data(), flags.size()); }
void snapshot(u32 map, u32 key_bit, bool on) {
    std::scoped_lock lock{bbsc_world_mutex};
    auto& s = bbsc_world_blocks[map];
    s.complete_ms = 1; s.map = map; s.present = 1;
    if (on) s.groups[0][key_bit / 8] |= static_cast<u8>(0x80u >> (key_bit % 8));
}
void tick() { now_ms += 1500; TickBbscSharedProgress(); }
int main() {
    // The host's older history: on in the first packet and snapshot, before we are placed.
    packet({2401, 2200});
    snapshot(0x18000000, 100, true);
    tick();
    packet({2401, 2200});
    bbsc_join_teleport_done = true; // placed beside the host
    tick();
    packet({2401, 2200});
    tick();
    assert(!has(2401) && !has(2200));
    assert(!bit(BbscWorldGroupKey(0x18000000, 0), 100));
    // Earned together: a boss flag and a world bit that turn on after placement.
    packet({2401, 2200, 2300});
    snapshot(0x18000000, 101, true);
    tick();
    assert(has(2300));
    assert(bit(BbscWorldGroupKey(0x18000000, 0), 101) && !bit(BbscWorldGroupKey(0x18000000, 0), 100));
    // A block first seen after placement is a baseline, not progress.
    snapshot(0x18010000, 5, true);
    tick();
    assert(!bit(BbscWorldGroupKey(0x18010000, 0), 5));
    // The reward event at the kill is collected; outside the boss's area it is not.
    current_map = 0x17000000; // another area (23)
    admit(12401800);
    assert(!bit(12401, 800));
    current_map = 0x18000000;
    admit(12401800);
    assert(bit(12401, 800));
    // Death or loading in the same party keeps the party open.
    bbsc_join_teleport_done = false;
    packet({2401, 2200, 2300, 2500});
    tick();
    assert(has(2500));
    // A new party (relay lock released) starts a new baseline: the host's progress made while we
    // were away is history, and nothing collected so far is dropped.
    ++bbsc_host_world_resets;
    packet({2401, 2200, 2300, 2500, 2600});
    tick();
    bbsc_join_teleport_done = true;
    tick();
    packet({2401, 2200, 2300, 2500, 2600});
    tick();
    assert(!has(2600) && has(2300) && has(2500) && bit(12401, 800));
    // A different host: also a new party.
    relay_host = 0x1234;
    bbsc_join_teleport_done = false;
    packet({2401, 2700});
    tick();
    bbsc_join_teleport_done = true;
    tick();
    packet({2401, 2700, 2800});
    tick();
    assert(!has(2700) && has(2800));
    std::cout << "PASS party baseline, earned flags/bits, first-sight blocks, reward event, "
                 "death/load continuity, new party and new host\n";
}
'''
    fixture = directory / 'party-progress.cpp'
    fixture.write_text(code, encoding='utf-8')
    binary = directory / ('party-progress.exe' if os.name == 'nt' else 'party-progress')
    subprocess.run([shutil.which('clang++'), '-std=c++23', '-O0', str(fixture), '-o', str(binary)],
                   check=True)
    subprocess.run([str(binary)], check=True)


@unittest.skipUnless(shutil.which('clang++') and SOURCE.is_file(),
                     'prepared pinned BBSC reference and clang++ are required')
class PartyProgressTests(unittest.TestCase):
    def test_only_progress_earned_in_the_party_is_collected(self):
        with tempfile.TemporaryDirectory() as directory:
            run_party_fixture(SOURCE, Path(directory))


if __name__ == '__main__':
    unittest.main()
