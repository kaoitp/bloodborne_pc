"""Actual boss reward producer/consumer: a reward without a taken flag is given once per character,
also across runs (R03 B15, G2-07/12), and only becomes final once the owner's save is written after
the grant (PR #12 reviews: attempt line before the add, outcome right after it, held when an earlier
run left an attempt without its outcome). A fresh process is simulated by clearing the in-memory lists and running
the start settle; the per-character record is a real file in a temporary folder, the save file's
write time is controlled. Not native gameplay proof."""
from paths import ROOT
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(os.environ.get('BBSC_FIXTURE_SOURCE') or
              ROOT / '.superpowers/reference/BBSC/emulator/src/core/bloodborne_re.cpp')


def run_once_fixture(source, directory):
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
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <filesystem>
#include <format>
#include <fstream>
#include <iostream>
#include <map>
#include <utility>
#include <mutex>
#include <optional>
#include <string>
#include <system_error>
#include <vector>
using s64 = int64_t; using u64 = uint64_t; using s32 = int32_t; using u32 = uint32_t; using u8 = uint8_t;
#define PS4_SYSV_ABI
#define LOG_INFO(...)
#define LOG_WARNING(...)
#define BBSC_TIMELINE(...)
namespace fmt {
template <class... A> std::string format(std::format_string<A...> f, A&&... a) {
    return std::format(f, std::forward<A>(a)...);
}
}
namespace Common::FS {
enum class PathType { CapturesDir };
std::filesystem::path GetUserPath(PathType) { return "user/captures"; }
}
struct BbscSaveSlot { std::string user; int slot = -1; };
struct BbscBossReward { s64 event; u32 flag; s32 first_lot; s32 repeat_lot; };
struct BbscBossGoodsLot { s32 lot; u32 goods; s32 count; u32 flag; };
// Amelia (no taken flag) and the Cleric Beast (flag 6645), as in the source table.
std::array<BbscBossReward, 2> BbscBossRewards{{{12401800, 0, 50000001, 0}, {12411700, 6645, 50000010, 0}}};
std::array<BbscBossGoodsLot, 2> BbscBossGoodsLots{{{50000001, 4001, 1, 0}, {50000010, 4114, 1, 0}}};
std::mutex bbsc_boss_reward_mutex;
constexpr u64 ItemManPointerOffset = 0x553D6E0, EventFlagManPointerOffset = 0x553B100,
              AwardItemLotOffset = 0x17DDC50;
s64 SteadyNowMs() { static s64 now = 1000; return now += 1000; }
int adds = 0;
u32 here = 0x18000000;                   // Cathedral Ward: Amelia's area
bool bbsc_party_placed = true;
BbscSaveSlot current{"sd1", 3};
bool EnvFlagEnabled(const char*) { return true; }
std::optional<BbscSaveSlot> bbsc_own_world_slot;
std::optional<BbscSaveSlot> BbscActiveSaveSlot() { return current; }
u64 GetGlobalState() { return 9; }
u64 GetLocalPlayerCharacter() { return 7; }
int GetCharacterHp(u64) { return 100; }
bool ReadablePointer(u64 p, size_t) { return p != 0; }
u32 GetCurrentPackedMap() { return here; }
u32 BbscMapArea(u32 m) { return m >> 24; }
bool BbscEventFlag(u32) { return false; }
void BbscAnnounce(const char16_t*, const char*) {}
bool add_ok = true;
bool break_record_after_add = false; // the record breaks between the attempt and the outcome write
bool in_inventory = false;           // the lot's goods in the owner's carried items
bool GiveBbscBossGoods(const BbscBossGoodsLot&) {
    if (break_record_after_add) {
        std::filesystem::create_directories(std::filesystem::path("user/boss-rewards") /
                                            ("given-" + std::string("sd1-") + "14.txt.tmp"));
    }
    if (!add_ok) return false;
    ++adds;
    return true;
}
u64 BbscCarriedInventory() { return 1; }
bool BbscInventoryHas(u64, u32) { return in_inventory; }
// The owner's save file write time; nullopt = not readable.
std::map<std::string, std::optional<std::filesystem::file_time_type>> save_written;
std::string key(const BbscSaveSlot& s) { return s.user + "-" + std::to_string(s.slot); }
std::optional<std::filesystem::file_time_type> BbscSaveSlotWritten(const BbscSaveSlot& slot) {
    const auto it = save_written.find(key(slot));
    return it == save_written.end() ? std::filesystem::file_time_type{} : it->second;
}
void game_saves(const BbscSaveSlot& s) { // the game writes this slot now
    save_written[key(s)] = std::filesystem::file_time_type::clock::now() + std::chrono::seconds(1);
}
void fake_award(u64, s32, u32) {}
u64 image_base = reinterpret_cast<u64>(&fake_award) - AwardItemLotOffset;
template <class T> T ReadValue(u64 at, u64 off) {
    if (at == 9) return off == 8 ? 0 : 0;
    return 1;
}
'''
    if 'bool BbscBossRewardOnce(' not in src:
        raise AssertionError('source has no once-per-character boss reward record')
    start = src.index('struct BbscBossRewardPending')
    code += src[start:src.index('void NoteBbscBossRewardEvent', start)]
    code += function('void NoteBbscBossRewardEvent(') + '\n' + function('void TickBbscBossRewards(')
    code += r'''
std::string record(const BbscSaveSlot& s) {
    std::ifstream f("user/boss-rewards/given-" + s.user + "-" + std::to_string(s.slot) + ".txt");
    return std::string((std::istreambuf_iterator<char>(f)), {});
}
void restart() { // a fresh process: nothing in memory, the start settle runs before any save
    bbsc_boss_reward_queue.clear();
    bbsc_boss_reward_given.clear();
    bbsc_boss_reward_unsaved.clear();
    bbsc_boss_reward_unclaimed.clear();
    SettleBbscBossRewardsAtStart();
}
void kill() { // a joint Amelia kill, then the reward tick
    NoteBbscBossRewardEvent(12401800);
    TickBbscBossRewards();
}
int main() {
    const BbscSaveSlot u_i_ahh{"sd1", 3}, six{"sd1", 2}, other{"sd1", 5}, seven{"sd1", 7},
        eight{"sd1", 8};
    // Run 1: U-I-AHH helps kill Amelia and gets the Gold Pendant; pending until the game saves.
    kill();
    assert(adds == 1);
    assert(record(u_i_ahh).find("granted 12401800 ") == 0);
    TickBbscBossRewards(); // no save yet: still pending
    assert(record(u_i_ahh).find("granted 12401800 ") == 0);
    game_saves(u_i_ahh);
    TickBbscBossRewards();
    assert(record(u_i_ahh) == "12401800\n"); // in the save: final
    // Run 2 (fresh process), another host's Amelia: not queued, and an older queued entry is skipped.
    restart();
    NoteBbscBossRewardEvent(12401800);
    bbsc_boss_reward_queue.clear();
    bbsc_boss_reward_queue.push_back({12401800, u_i_ahh});
    TickBbscBossRewards();
    assert(adds == 1 && bbsc_boss_reward_queue.empty()); // no second Gold Pendant
    restart();
    NoteBbscBossRewardEvent(12401800);
    assert(bbsc_boss_reward_queue.empty()); // not even queued
    // A second kill in the same process before the save: no second lot either.
    current = six;
    kill();
    assert(adds == 2);
    kill();
    assert(adds == 2);
    game_saves(six);
    TickBbscBossRewards();
    // A flagged row is unchanged: no file line, the game's taken flag decides.
    restart();
    NoteBbscBossRewardEvent(12411700);
    TickBbscBossRewards();
    assert(adds == 3);
    assert(record(six) == "12401800\n");
    // The record cannot be read (here: a folder in its place): no lot, the entry waits.
    restart();
    current = other;
    std::filesystem::create_directories("user/boss-rewards/given-sd1-5.txt");
    NoteBbscBossRewardEvent(12401800);
    assert(bbsc_boss_reward_queue.size() == 1);
    TickBbscBossRewards();
    assert(adds == 3 && bbsc_boss_reward_queue.size() == 1);
    std::filesystem::remove("user/boss-rewards/given-sd1-5.txt");
    TickBbscBossRewards(); // readable again: given once
    assert(adds == 4 && bbsc_boss_reward_queue.empty());
    game_saves(other);
    TickBbscBossRewards();

    // P1 (review): exit after the grant but BEFORE the save. The save on disk has no item, so the
    // record must not block a later legitimate kill.
    restart();
    current = seven;
    save_written[key(seven)] = std::filesystem::file_time_type::clock::now() -
                               std::chrono::seconds(10); // an older save, before the grant
    kill();
    assert(adds == 5);
    adds = 4;         // the process ends: the unsaved item is gone with it
    restart();        // start settle: save not written after the grant -> line dropped
    assert(record(seven).empty());
    kill();
    assert(adds == 5); // recovered: given again
    game_saves(seven);
    TickBbscBossRewards();
    assert(record(seven) == "12401800\n");

    // Converse: the save holds the item but making the line final fails (record not writable),
    // then the process ends. The item may even be used up since. No second lot.
    restart();
    current = eight;
    kill();
    assert(adds == 6);
    std::filesystem::create_directories("user/boss-rewards/given-sd1-8.txt.tmp"); // write fails
    game_saves(eight);
    TickBbscBossRewards();
    assert(record(eight).find("granted 12401800 ") == 0); // not final yet
    adds = 5;                  // used up (One Third of Umbilical Cord): nothing to check in items
    std::filesystem::remove("user/boss-rewards/given-sd1-8.txt.tmp");
    restart();                 // start settle: saved after the grant -> final
    assert(record(eight) == "12401800\n");
    kill();
    assert(adds == 5 && bbsc_boss_reward_queue.empty()); // not again

    // The same with the write still failing at the next start: the line stays pending and the
    // event waits (no second lot); a save that cannot be read is the same.
    restart();
    const BbscSaveSlot nine{"sd1", 9};
    current = nine;
    kill();
    assert(adds == 6);
    save_written[key(nine)] = std::nullopt; // save not readable at the next start
    restart();
    assert(record(nine).find("granted 12401800 ") == 0);
    kill();
    assert(adds == 6 && bbsc_boss_reward_queue.size() == 1); // waits, no second lot

    // PR #12 review 2: a failed grant, then a save WITHOUT the item, then an exit. Nothing may be
    // recorded for it: the next healthy kill gives it once.
    restart();
    bbsc_boss_reward_queue.clear();
    const BbscSaveSlot eleven{"sd1", 11};
    current = eleven;
    add_ok = false;
    const int before_failed = adds;
    kill();
    assert(adds == before_failed && record(eleven).empty()); // the failure is written at once
    game_saves(eleven);
    restart();                                   // no tick in between
    add_ok = true;
    kill();
    assert(adds == before_failed + 1);
    game_saves(eleven);
    TickBbscBossRewards();
    assert(record(eleven) == "12401800\n");

    // PR #12 review 3: the record is unwritable at the kill, then a save, the counter rolled back
    // (used up), an exit while still unwritable, the record writable again, another kill. The first
    // kill must not give an item it cannot record ("no line, no item"); the reward then arrives
    // exactly once, after the restart.
    restart();
    bbsc_boss_reward_queue.clear();
    const BbscSaveSlot thirteen{"sd1", 13};
    current = thirteen;
    std::filesystem::create_directories("user/boss-rewards/given-sd1-13.txt.tmp");
    const int before_unrecorded = adds;
    kill();
    assert(adds == before_unrecorded && record(thirteen).empty()); // deferred, not given
    game_saves(thirteen);
    restart();                                   // still unwritable at the restart
    std::filesystem::remove("user/boss-rewards/given-sd1-13.txt.tmp");
    kill();
    assert(adds == before_unrecorded + 1);       // given once, now that it can be recorded
    game_saves(thirteen);
    TickBbscBossRewards();
    assert(record(thirteen) == "12401800\n");
    restart();
    kill();
    assert(adds == before_unrecorded + 1);       // and never again

    // The record breaks between the attempt and the outcome write (the add worked): the attempt line
    // stays. Same process: no second lot. Saved, used up, exit: held at the restart (outcome unknown),
    // no second lot; once its goods are seen in the inventory it is final.
    restart();
    bbsc_boss_reward_queue.clear();
    const BbscSaveSlot fourteen{"sd1", 14};
    current = fourteen;
    break_record_after_add = true;
    const int before_broken = adds;
    kill();
    break_record_after_add = false;
    assert(adds == before_broken + 1 && record(fourteen).find("attempt 12401800 ") == 0);
    kill();
    assert(adds == before_broken + 1);
    game_saves(fourteen);
    adds = before_broken;                        // used up
    restart();                                   // unwritable still: nothing settles
    std::filesystem::remove("user/boss-rewards/given-sd1-14.txt.tmp");
    restart();                                   // attempt + save after it: held
    assert(record(fourteen).find("attempt 12401800 ") == 0);
    kill();
    assert(adds == before_broken && bbsc_boss_reward_queue.size() == 1); // no second lot
    in_inventory = true;                         // (the case where it was kept, not used)
    TickBbscBossRewards();
    in_inventory = false;
    assert(adds == before_broken && bbsc_boss_reward_queue.empty() && record(fourteen) == "12401800\n");

    // The same break with no save before the exit: nothing reached a save, the line goes, given again.
    restart();
    bbsc_boss_reward_queue.clear();
    std::filesystem::remove("user/boss-rewards/given-sd1-14.txt");
    save_written[key(fourteen)] = std::filesystem::file_time_type::clock::now() -
                                  std::chrono::seconds(10); // its last save is older
    break_record_after_add = true;
    const int before_unsaved_break = adds;
    kill();
    break_record_after_add = false;
    assert(adds == before_unsaved_break + 1);
    adds = before_unsaved_break;                 // the process ends without a save
    std::filesystem::remove("user/boss-rewards/given-sd1-14.txt.tmp");
    restart();
    assert(record(fourteen).empty());
    kill();
    assert(adds == before_unsaved_break + 1);

    // A failed grant leaves no line behind.
    restart();
    bbsc_boss_reward_queue.clear();
    const BbscSaveSlot ten{"sd1", 10};
    current = ten;
    add_ok = false;
    const int before_ten = adds;
    kill();
    assert(adds == before_ten && bbsc_boss_reward_queue.size() == 1);
    assert(record(ten).empty());                 // the failed add's attempt line went at once
    add_ok = true;
    TickBbscBossRewards();
    assert(adds == before_ten + 1 && record(ten).find("granted 12401800 ") == 0);
    std::cout << "PASS a boss reward without a taken flag is given once per character across runs, "
                 "final only once saved\n";
}
'''
    fixture = directory / 'reward-once.cpp'
    fixture.write_text(code, encoding='utf-8')
    binary = directory / ('reward-once.exe' if os.name == 'nt' else 'reward-once')
    subprocess.run([shutil.which('clang++'), '-std=c++23', '-O0', '-g', '-fsanitize=address',
                    str(fixture), '-o', str(binary)], check=True)
    subprocess.run([str(binary)], check=True, cwd=directory)


@unittest.skipUnless(shutil.which('clang++') and SOURCE.is_file(),
                     'prepared pinned BBSC reference and clang++ are required')
class RewardOnceTests(unittest.TestCase):
    def test_flagless_reward_once_per_character(self):
        with tempfile.TemporaryDirectory() as directory:
            run_once_fixture(SOURCE, Path(directory))


if __name__ == '__main__':
    unittest.main()
