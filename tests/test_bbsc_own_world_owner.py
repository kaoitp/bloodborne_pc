"""Actual own-world journal keep/restore/file recovery with the owner check (R03 A02 blocker: a
pending journal of one character was put into another after Quit Game -> title -> Load; PR #11
review: a display name is not an identity and an unknown identity must wait). Fixture evidence with
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


def run_owner_fixture(source, directory):
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
#include <cstring>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <bit>
#include <map>
#include <mutex>
#define PS4_SYSV_ABI
#include <optional>
#include <string>
#include <string_view>
#include <vector>
using s32 = int32_t; using s64 = int64_t; using u8 = uint8_t; using u32 = uint32_t; using u64 = uint64_t;
#define LOG_INFO(...)
#define LOG_WARNING(...)
#define BBSC_TIMELINE(...)
struct BbscSaveSlot { std::string user; int slot = -1; };
namespace Bbsc { constexpr u32 HomeSpotKey = 0xFFFF9900; bool DecodeHomeSpot(const std::array<u8, 128>&) { return true; } }
constexpr size_t BbscWorldGroupBytes = 128;
constexpr u32 BbscTimeGroupKey = 9; constexpr size_t BbscTimeByte = 100; constexpr u8 BbscTimeMask = 0xE0;
constexpr u32 BbscOwnTimeKey = 0xFFFF9800;
constexpr u32 BbscOwnWorldMagic = 0x574F4242;
constexpr u64 PlayerSlotManagerPointerOffset = 0x0553B130;
std::map<u32, std::array<u8, BbscWorldGroupBytes>> bbsc_own_world;
std::optional<BbscSaveSlot> bbsc_own_world_slot;
bool bbsc_own_world_dirty = false;
std::optional<BbscSaveSlot> bbsc_home_recovery_slot;
struct { u64 held = 0; } bbsc_dream_own;
void RestoreBbscOwnDreamState(std::string_view) { bbsc_dream_own.held = 0; }
const char* BbscTimeName(int) { return ""; }
void RecoverBbscHomeSpot(const BbscSaveSlot&) {}
void BbscAnnounce(const char16_t*, const char*) {}
bool BbscHomeForOwnWorld() { return true; }
s64 SteadyNowMs() { static s64 now = 0; return now += 1000; }
std::optional<BbscSaveSlot> active_slot; // what the save folder would say (nullopt: not written yet)
std::optional<BbscSaveSlot> BbscActiveSaveSlot() { return active_slot; }
std::filesystem::path BbscOwnWorldPath(const BbscSaveSlot& slot) {
    return "own-" + slot.user + "-" + std::to_string(slot.slot) + ".bin";
}
alignas(16) u8 slot_manager[0x20] = {};
alignas(16) u8 game_data[0x100] = {};
alignas(16) u8 live_group[BbscWorldGroupBytes] = {};
u64 image_base = 0x100000;
u64 BbscFlagGroupStorage(u32 key) { return key == 1240 ? reinterpret_cast<u64>(live_group) : 0; }
bool ReadablePointer(u64 p, size_t) { return p >= 0x10000; }
template <class T> T ReadValue(u64 base, u64 off) {
    if (base == image_base + PlayerSlotManagerPointerOffset) return static_cast<T>(reinterpret_cast<u64>(slot_manager));
    T v; std::memcpy(&v, reinterpret_cast<void*>(base + off), sizeof(T)); return v;
}
template <class T> void WriteValue(u64 base, u64 off, T v) { std::memcpy(reinterpret_cast<void*>(base + off), &v, sizeof(T)); }
// Load a character: name in PlayerGameData; its save is written about 10 s later (active_slot).
void play(const char16_t* name, std::optional<BbscSaveSlot> saved) {
    std::memset(game_data + 0xA8, 0, 34);
    std::memcpy(game_data + 0xA8, name, std::char_traits<char16_t>::length(name) * 2);
    active_slot = saved;
}
void fill(u8 v) { std::memset(live_group, v, sizeof(live_group)); }
// Shared progress (the collected party progress of this character, merged at home).
std::mutex bbsc_progress_mutex;
std::vector<u32> bbsc_progress_host_flags;
std::map<u32, std::array<u8, BbscWorldGroupBytes>> bbsc_progress_groups;
std::optional<BbscSaveSlot> bbsc_progress_slot;
bool bbsc_progress_backed_up = false;
constexpr s64 BbscProgressMergeRetry = -2;
bool BackupBbscSaves() { return true; }
bool BbscEventFlag(u32) { return true; }
'''
    if 'bool BbscOwnWorldOwnerConfirmed(' not in src:
        raise AssertionError('source has no save-slot owner check (BbscOwnWorldOwnerConfirmed)')
    code += 'std::u16string bbsc_own_world_owner;\nbool bbsc_own_world_continuous = false;\n'
    if 'bool BbscOwnWorldReadyForProgress(' not in src:  # the source before the ordering fix
        code += 'size_t RestoreBbscOwnWorld(std::string_view);\n'
        code += 'bool BbscOwnWorldReadyForProgress() { return true; }\n'
    for head in ('std::u16string BbscLocalCharacterName(', 'std::string BbscNameForLog(',
                 'const u8* KeepBbscOwnWorldGroup(', 'void WriteBbscOwnWorldFile(',
                 'bool LoadBbscOwnWorldFile(', 'bool BbscOwnWorldOwnerConfirmed(',
                 'size_t RestoreBbscOwnWorld(', 'bool RecoverBbscOwnWorldFile(',
                 'void NoteBbscOwnWorldCharacterLoad(', 'bool BbscOwnWorldReadyForProgress(',
                 'std::pair<s64, size_t> MergeBbscSharedProgress('):
        if head == 'bool BbscOwnWorldReadyForProgress(' and head not in src:
            continue
        code += function(head) + '\n'
    code += r'''
int main() {
    u64 data = reinterpret_cast<u64>(game_data);
    std::memcpy(slot_manager + 0x08, &data, 8);
    const BbscSaveSlot eiei{"sd1", 1}, kaori{"sd1", 0}, twin{"sd1", 4};

    // 1. Normal trip home: EiEi keeps her group 1240 (0x11) as a guest, the host's 0x22 is written,
    //    she goes home without a title in between: put back at once (at the load hook).
    play(u"EiEi", eiei);
    fill(0x11);
    KeepBbscOwnWorldGroup(1240, live_group);
    fill(0x22);
    assert(RestoreBbscOwnWorld("during the home load") == 1 && live_group[0] == 0x11);

    // 2. A02: EiEi is a guest again, her journal is on disk, then Quit Game -> title -> Load Kaori.
    play(u"EiEi", eiei);
    fill(0x11);
    KeepBbscOwnWorldGroup(1240, live_group);
    WriteBbscOwnWorldFile();
    assert(std::filesystem::exists("own-sd1-1.bin"));
    fill(0x22);
    bbsc_dream_own.held = 1;
    play(u"", std::nullopt);              // the title screen
    NoteBbscOwnWorldCharacterLoad(); // Warp.StageDescriptor.Finalize, rdi 0
    play(u"Kaori", std::nullopt);         // Kaori loads; her save is not written yet
    fill(0x33);
    assert(RestoreBbscOwnWorld("during the home load") == 0);
    assert(live_group[0] == 0x33 && !bbsc_own_world.empty()); // not ready: nothing written, kept
    active_slot = kaori;                  // Kaori's save is written: another character
    assert(RestoreBbscOwnWorld("home") == 0);
    assert(live_group[0] == 0x33 && bbsc_own_world.empty() && bbsc_dream_own.held == 0);
    assert(std::filesystem::exists("own-sd1-1.bin")); // kept for its owner
    assert(!RecoverBbscOwnWorldFile(kaori)); // Kaori has no journal of her own

    // 3. Back to EiEi: her file is recovered for her slot and put back.
    play(u"", std::nullopt);
    NoteBbscOwnWorldCharacterLoad(); // Warp.StageDescriptor.Finalize, rdi 0
    play(u"EiEi", eiei);
    fill(0x44);
    assert(RecoverBbscOwnWorldFile(eiei));
    assert(live_group[0] == 0x11 && bbsc_own_world.empty());
    assert(std::filesystem::exists("own-sd1-1.bin.restored"));

    // 4. Same name, other character (PR #11 review): another "EiEi" in slot 4 after a title.
    play(u"EiEi", eiei);
    fill(0x11);
    KeepBbscOwnWorldGroup(1240, live_group);
    fill(0x22);
    play(u"", std::nullopt);
    NoteBbscOwnWorldCharacterLoad(); // Warp.StageDescriptor.Finalize, rdi 0
    play(u"EiEi", twin);
    fill(0x55);
    assert(RestoreBbscOwnWorld("during the home load") == 0 && live_group[0] == 0x55);
    assert(bbsc_own_world.empty());

    // 5. Name not readable while a journal waits (PR #11 review): nothing written, nothing dropped.
    play(u"EiEi", eiei);
    fill(0x11);
    KeepBbscOwnWorldGroup(1240, live_group);
    fill(0x22);
    play(u"", std::nullopt);
    fill(0x66);
    assert(RestoreBbscOwnWorld("during the home load") == 0 && live_group[0] == 0x66);
    assert(!bbsc_own_world.empty());
    play(u"EiEi", eiei); // the owner's save is written: put back
    assert(RestoreBbscOwnWorld("home") == 1 && live_group[0] == 0x11);

    // 6. The title signal missed, but another name is loaded: not put back.
    play(u"EiEi", eiei);
    fill(0x11);
    KeepBbscOwnWorldGroup(1240, live_group);
    play(u"Kaori", std::nullopt);
    fill(0x77);
    assert(RestoreBbscOwnWorld("during the home load") == 0 && live_group[0] == 0x77);
    assert(!bbsc_own_world.empty());
    active_slot = kaori;
    assert(RestoreBbscOwnWorld("home") == 0 && live_group[0] == 0x77 && bbsc_own_world.empty());

    // 7. PR #11 review: own world first, then the earned progress. EiEi's journal (0x11, from
    //    before the visit) is on disk and she earned bit 0x80 of group 1240 with the host (pending,
    //    in memory). Quit -> Kaori (another slot) -> quit -> EiEi again, inside the 15 s recovery
    //    throttle, so the merge path is the first to look.
    std::filesystem::remove("own-sd1-1.bin.restored");
    play(u"EiEi", eiei);
    fill(0x11);
    KeepBbscOwnWorldGroup(1240, live_group);
    WriteBbscOwnWorldFile();
    fill(0x22);
    {
        std::array<u8, BbscWorldGroupBytes> earned{};
        earned.fill(0x80);
        bbsc_progress_groups[1240] = earned;
        bbsc_progress_slot = eiei;
    }
    play(u"", std::nullopt);
    NoteBbscOwnWorldCharacterLoad(); // Warp.StageDescriptor.Finalize, rdi 0
    play(u"Kaori", kaori);
    fill(0x33);
    assert(!BbscOwnWorldReadyForProgress() || MergeBbscSharedProgress("t").first == BbscProgressMergeRetry);
    assert(live_group[0] == 0x33); // nothing of EiEi's in Kaori
    play(u"", std::nullopt);
    NoteBbscOwnWorldCharacterLoad();
    play(u"EiEi", eiei);
    fill(0x44); // the table as loaded
    assert(BbscOwnWorldReadyForProgress()); // her own world is back first
    assert(live_group[0] == 0x11);
    const auto merged = MergeBbscSharedProgress("after the home load");
    assert(merged.first == 0 && live_group[0] == 0x91); // the earned bit on top of her own world
    assert(!RecoverBbscOwnWorldFile(eiei)); // the throttled recovery later finds nothing to undo
    assert(live_group[0] == 0x91 && std::filesystem::exists("own-sd1-1.bin.restored"));
    std::cout << "PASS the journal is put back only for its owner's save slot\n";
}
'''
    fixture = directory / 'own-owner.cpp'
    fixture.write_text(code, encoding='utf-8')
    binary = directory / ('own-owner.exe' if os.name == 'nt' else 'own-owner')
    subprocess.run([shutil.which('clang++'), '-std=c++23', '-O0', '-g', '-fsanitize=address',
                    str(fixture), '-o', str(binary)], check=True)
    subprocess.run([str(binary)], check=True, cwd=directory)


@unittest.skipUnless(shutil.which('clang++') and SOURCE.is_file(),
                     'prepared pinned BBSC reference and clang++ are required')
class OwnWorldOwnerTests(unittest.TestCase):
    def test_journal_is_put_back_only_for_its_owner(self):
        with tempfile.TemporaryDirectory() as directory:
            run_owner_fixture(SOURCE, Path(directory))


if __name__ == '__main__':
    unittest.main()
