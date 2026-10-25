"""Exercise the actual shared-progress merge callers with controlled backup failure."""
from paths import ROOT
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest

SOURCE = ROOT / '.superpowers/reference/BBSC/emulator/src/core/bloodborne_re.cpp'


def run_backup_fixture(source, directory):
    src = source.read_text(encoding='utf-8')

    def function(signature):
        start = src.index(signature + '(')
        brace = src.index('{', start)
        end, depth = brace + 1, 1
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
#include <chrono>
#include <filesystem>
#include <iostream>
#include <map>
#include <mutex>
#include <optional>
#include <set>
#include <string>
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
constexpr s64 BbscProgressFileMs = 10000, BbscProgressRecoverMs = 15000;
constexpr u64 EventFlagManPointerOffset = 0x0553B100;
std::optional<BbscSaveSlot> bbsc_progress_slot;
BbscSaveSlot current{"sd1", 1};
std::array<u8, 125> live{};
std::set<u32> own_flags;
s64 now_ms = 10000;
bool backup_ok = false, pending_file = true, active_ready = true;
int backups = 0, sets = 0, finishes = 0, notices = 0;
void native_set(u64, u32 flag, u8) { own_flags.insert(flag); ++sets; }
u64 image_base = reinterpret_cast<u64>(&native_set) - 0x0132E5A0;
bool EnvFlagEnabled(const char*) { return true; }
s64 SteadyNowMs() { return now_ms; }
bool BackupBbscSaves() { ++backups; return backup_ok; }
bool BbscEventFlag(u32 flag) { return own_flags.contains(flag); }
u64 BbscFlagGroupStorage(u32) { return reinterpret_cast<u64>(live.data()); }
u32 BbscWorldGroupKey(u32, size_t) { return 12411; }
s32 GetSessionState() { return 0; }
s32 GetLocalPlayerType() { return 0; }
u64 GetGlobalState() { return 9; }
u64 GetLocalPlayerCharacter() { return 7; }
int GetCharacterHp(u64) { return 100; }
bool ReadablePointer(u64 p, size_t) { return p != 0; }
template<class T> T ReadValue(u64 at, size_t off) {
    if (at == 9) return off == 0x1592 ? 1 : 0;
    return 1;
}
std::optional<BbscSaveSlot> BbscActiveSaveSlot() { if (!active_ready) return {}; return current; }
void RestoreBbscOwnWorld(const char*) {}
void RestoreBbscOwnWorldAtLoad() {}
std::vector<int> recovered, loaded; // slots whose own journal / pending file was read
bool RecoverBbscOwnWorldFile(const BbscSaveSlot& slot) { recovered.push_back(slot.slot); return false; }
bool LoadBbscPendingProgress(const BbscSaveSlot& slot) { loaded.push_back(slot.slot); return false; }
void WriteBbscPendingProgress() {}
void FinishBbscPendingProgress() { ++finishes; pending_file = false; }
void BbscAnnounce(const char16_t*, const char*) { ++notices; }
std::atomic<u32> bbsc_host_world_resets{0};
std::filesystem::file_time_type bbsc_active_slot_written{};
bool bbsc_join_teleport_done = false;
u32 BbscRelayHostForPackets() { return 0; }
bool BbscGuestInHostWorld() { return false; }
u32 GetCurrentPackedMap() { return 0; }
constexpr u32 BbscMapArea(u32 map) { return (map >> 24) & 0xFF; }
struct BbscBossReward { s64 event; u32 flag; s32 first_lot; s32 repeat_lot; };
constexpr std::array<BbscBossReward, 1> BbscBossRewards{{{12401800, 0, 50000001, 0}}};
'''
    if src.index('std::optional<BbscSaveSlot> bbsc_progress_slot') < src.index('std::pair<s64, size_t> MergeBbscSharedProgress'):
        code = code.replace('std::optional<BbscSaveSlot> bbsc_progress_slot;', '')
    start = src.index('constexpr std::array<u32, 49> BbscProgressFlags')
    end = src.index('// OR the collected host progress', start)
    code += src[start:end]
    for signature in ('std::pair<s64, size_t> MergeBbscSharedProgress',
                      'void TickBbscSharedProgress', 'void ApplyBbscSharedProgressAtLoad'):
        code += function(signature) + '\n'
    code += r'''
void saved() {
    bbsc_active_slot_written = std::filesystem::file_time_type::clock::now() + std::chrono::seconds(1);
}
void seed() {
    now_ms += 10000; current = {"sd1", 1};
    own_flags.clear(); live.fill(0); sets = finishes = backups = notices = 0;
    backup_ok = false; pending_file = true; active_ready = true;
    bbsc_progress_host_flags = {2401};
    bbsc_progress_groups.clear(); bbsc_progress_groups[12411][0] = 0x80;
    bbsc_progress_was_guest = true; bbsc_progress_slot = BbscSaveSlot{"sd1", 1};
    bbsc_progress_left_ms = now_ms - 1000; bbsc_progress_home_ms = now_ms - 5000;
    bbsc_progress_merged_at_load = false; bbsc_progress_backed_up = false;
}
void unchanged() {
    assert(sets == 0 && own_flags.empty() && live[0] == 0);
    assert(bbsc_progress_was_guest && bbsc_progress_slot.has_value());
    assert(bbsc_progress_host_flags.size() == 1 && bbsc_progress_groups.size() == 1);
    assert(pending_file && finishes == 0);
}
int main() {
    seed(); TickBbscSharedProgress(); unchanged(); assert(backups == 1);
    ApplyBbscSharedProgressAtLoad(); unchanged();
    assert(backups == 2 && !bbsc_progress_merged_at_load && notices == 1);
    backup_ok = true; active_ready = false; now_ms += 1000; TickBbscSharedProgress(); unchanged();
    ApplyBbscSharedProgressAtLoad(); unchanged(); active_ready = true;
    current.user = "other"; now_ms += 1000; TickBbscSharedProgress(); unchanged();
    ApplyBbscSharedProgressAtLoad(); unchanged(); current.user = "sd1";
    current.slot = 0; now_ms += 1000; TickBbscSharedProgress(); unchanged();
    ApplyBbscSharedProgressAtLoad(); unchanged(); assert(backups == 2);
    current.slot = 1; ApplyBbscSharedProgressAtLoad();
    assert(sets == 1 && live[0] == 0x80 && bbsc_progress_merged_at_load);
    assert(pending_file && finishes == 0 && backups == 3);
    now_ms += 1000; TickBbscSharedProgress();
    // Merged into the live flags; the pending file stays until the game writes the save.
    assert(sets == 1 && finishes == 0 && pending_file && backups == 3);
    assert(bbsc_progress_host_flags.empty() && bbsc_progress_groups.empty());
    assert(!bbsc_progress_was_guest && !bbsc_progress_slot);
    now_ms += 1000; TickBbscSharedProgress();
    assert(finishes == 0 && pending_file); // no save written yet
    // Another character is loaded before the first one's save is confirmed: it recovers its own
    // journal and pending file, and the first one keeps waiting.
    current.slot = 2; recovered.clear(); loaded.clear();
    now_ms += 16000; TickBbscSharedProgress();
    assert(recovered == std::vector<int>{2} && loaded == std::vector<int>{2});
    assert(finishes == 0 && pending_file);
    current.slot = 1; recovered.clear(); loaded.clear();
    now_ms += 16000; TickBbscSharedProgress();
    assert(recovered.empty() && loaded.empty() && finishes == 0); // still live, not reloaded
    saved();
    now_ms += 1000; TickBbscSharedProgress();
    assert(finishes == 1 && !pending_file);
    now_ms += 1000; TickBbscSharedProgress(); ApplyBbscSharedProgressAtLoad();
    assert(finishes == 1 && sets == 1);
    seed(); TickBbscSharedProgress(); unchanged();
    backup_ok = true; now_ms += 1000; TickBbscSharedProgress();
    assert(sets == 1 && live[0] == 0x80 && finishes == 0 && pending_file);
    saved(); now_ms += 1000; TickBbscSharedProgress();
    assert(finishes == 1 && !pending_file);
    std::cout << "PASS no mutation/finalization after failed backup; load and settled retry; once-only merge\n";
}
'''
    fixture = directory / 'progress-backup.cpp'
    fixture.write_text(code, encoding='utf-8')
    binary = directory / ('progress-backup.exe' if os.name == 'nt' else 'progress-backup')
    subprocess.run([shutil.which('clang++'), '-std=c++23', '-O0', str(fixture),
                    '-o', str(binary)], check=True)
    subprocess.run([str(binary)], check=True)


@unittest.skipUnless(shutil.which('clang++') and SOURCE.is_file(),
                     'prepared pinned BBSC reference and clang++ are required')
class ProgressBackupTests(unittest.TestCase):
    def test_failed_backup_keeps_pending_progress_for_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            run_backup_fixture(SOURCE, Path(directory))


if __name__ == '__main__':
    unittest.main()