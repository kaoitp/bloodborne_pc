"""Actual boss reward producer/consumer: a reward without a taken flag is given once per character,
also across runs (R03 B15, G2-07/12), and only becomes final once the owner's save is written after
the grant (PR #12 reviews: attempt line before the add, outcome right after it, held when an earlier
run left an attempt without its outcome; an experimental opt-in, SHADPS4_BBSC_REWARD_ONCE=1, while
a failed add with an unwritten removal cannot be told from a used-up delivery). A fresh process is simulated by clearing the in-memory lists and running
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
constexpr size_t BbscWorldGroupBytes = 125;
std::map<u32, std::array<u8, 125>> bbsc_own_world; // the own-world journal (B18)
std::optional<BbscSaveSlot> BbscActiveSaveSlot() { return current; }
u64 GetGlobalState() { return 9; }
u64 GetLocalPlayerCharacter() { return 7; }
int GetCharacterHp(u64) { return 100; }
bool ReadablePointer(u64 p, size_t) { return p != 0; }
u32 GetCurrentPackedMap() { return here; }
u32 BbscMapArea(u32 m) { return m >> 24; }
std::vector<u32> live_flags;            // the live flag table (own world when home)
bool BbscEventFlag(u32 f) { return std::ranges::find(live_flags, f) != live_flags.end(); }
bool home = false;                      // in our own world, not a guest
u64 GetGlobalState();
bool BbscOwnWorldNonGuest(u64) { return home; }
void BbscAnnounce(const char16_t*, const char*) {}
bool add_ok = true;
bool break_record_after_add = false; // the record breaks between the attempt and the outcome write
bool in_inventory = false;           // the lot's goods in the owner's carried items
bool fit_ok = true;                     // the add's fit check (the one-item capacity)
bool BbscBossGoodsFit(const BbscBossGoodsLot&) { return fit_ok; }
bool GiveBbscBossGoods(const BbscBossGoodsLot&) {
    if (break_record_after_add) {
        std::filesystem::create_directories(std::filesystem::path("user/boss-rewards") /
                                            ("given-" + current.user + "-" +
                                             std::to_string(current.slot) + ".txt.tmp"));
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
    bbsc_boss_reward_owed.clear();
    bbsc_boss_reward_durable.clear();
    bbsc_boss_reward_done.clear();
    bbsc_boss_reward_ledger_writes.clear();
    SettleBbscBossRewardsAtStart();
    QueueBbscBossRewardsOwedAtStart();
}
void kill() { // a joint Amelia kill, then the reward tick
    NoteBbscBossRewardEvent(12401800);
    TickBbscBossRewards();
}
void reward_once(const char* value) {
#ifdef _WIN32
    _putenv_s("SHADPS4_BBSC_REWARD_ONCE", value);
#else
    setenv("SHADPS4_BBSC_REWARD_ONCE", value, 1);
#endif
}
void dedup(const char* value) {
#ifdef _WIN32
    _putenv_s("SHADPS4_BBSC_REWARD_DEDUP", value);
#else
    setenv("SHADPS4_BBSC_REWARD_DEDUP", value, 1);
#endif
}
void dedup_unset() {
#ifdef _WIN32
    _putenv_s("SHADPS4_BBSC_REWARD_DEDUP", "");
#else
    unsetenv("SHADPS4_BBSC_REWARD_DEDUP");
#endif
}
std::filesystem::path owed_path(const BbscSaveSlot& s) {
    return "user/boss-rewards/owed-" + s.user + "-" + std::to_string(s.slot) + ".txt";
}
std::string owed_line(const BbscSaveSlot& s) {
    std::ifstream f("user/boss-rewards/owed-" + s.user + "-" + std::to_string(s.slot) + ".txt");
    return std::string((std::istreambuf_iterator<char>(f)), {});
}
size_t mine() { // queued for the current character (owed rewards of others wait in the queue too)
    return std::ranges::count_if(bbsc_boss_reward_queue, [](const auto& q) {
        return q.owner.user == current.user && q.owner.slot == current.slot;
    });
}
int main() {
    dedup("0");       // B18 is ON by default; its own section at the end
    reward_once("1"); // the experimental opt-in; default OFF is checked at the end
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
    assert(adds == 1 && (mine() == 0)); // no second Gold Pendant
    restart();
    NoteBbscBossRewardEvent(12401800);
    assert((mine() == 0)); // not even queued
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
    assert(mine() == 1);
    TickBbscBossRewards();
    assert(adds == 3 && mine() == 1);
    std::filesystem::remove("user/boss-rewards/given-sd1-5.txt");
    TickBbscBossRewards(); // readable again: given once
    assert(adds == 4 && (mine() == 0));
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
    assert(adds == 5 && (mine() == 0)); // not again

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
    assert(adds == 6 && mine() == 1); // waits, no second lot

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
    assert(adds == before_broken && mine() == 1); // no second lot
    in_inventory = true;                         // (the case where it was kept, not used)
    TickBbscBossRewards();
    in_inventory = false;
    assert(adds == before_broken && (mine() == 0) && record(fourteen) == "12401800\n");

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
    assert(adds == before_ten && mine() == 1);
    assert(record(ten).empty());                 // the failed add's attempt line went at once
    add_ok = true;
    TickBbscBossRewards();
    assert(adds == before_ten + 1 && record(ten).find("granted 12401800 ") == 0);
    // PR #12 review 4: the add FAILS and the removal of its attempt cannot be written, then a save,
    // an exit while unwritable, storage back. On disk this is the same as a delivery that worked
    // and was used up: held - no lot, no drop - however many kills and ticks follow. The log names
    // the line a person removes to release it; after that the reward is given once.
    restart();
    bbsc_boss_reward_queue.clear();
    const BbscSaveSlot fifteen{"sd1", 15};
    current = fifteen;
    add_ok = false;
    break_record_after_add = true;
    const int before_failed_outcome = adds;
    kill();
    break_record_after_add = false;
    assert(adds == before_failed_outcome && record(fifteen).find("attempt 12401800 ") == 0);
    game_saves(fifteen);
    restart();                                   // still unwritable
    std::filesystem::remove("user/boss-rewards/given-sd1-15.txt.tmp");
    restart();
    add_ok = true;
    kill();
    for (int i = 0; i < 50; ++i) TickBbscBossRewards();
    assert(adds == before_failed_outcome);       // held: neither given nor dropped
    assert(record(fifteen).find("attempt 12401800 ") == 0 && mine() == 1);
    std::filesystem::remove("user/boss-rewards/given-sd1-15.txt"); // the logged manual release
    TickBbscBossRewards();
    assert(adds == before_failed_outcome + 1);   // the debt is paid once
    game_saves(fifteen);
    TickBbscBossRewards();
    assert(record(fifteen) == "12401800\n");

    // Default OFF: without the variable nothing is written or read; once per process, as before.
    reward_once("0");
    restart();
    bbsc_boss_reward_queue.clear();
    const BbscSaveSlot sixteen{"sd1", 16};
    current = sixteen;
    const int before_off = adds;
    kill();
    kill();
    assert(adds == before_off + 1 && !std::filesystem::exists("user/boss-rewards/given-sd1-16.txt"));
    restart();
    kill();
    assert(adds == before_off + 2); // a new process may give it again (the existing behaviour)

    // ---- R03 B18: no second reward for a boss beaten in the own world, ON by default ----------
    const u32 amelia_flag = 12401800;
    const auto beaten_at_home = [] { bbsc_own_world[12401][800 / 8] |= 0x80u >> (800 % 8); };
    const auto fresh = [&](const BbscSaveSlot& slot) {
        current = slot;
        restart();                                      // the queue keeps other owners' owed rewards
        bbsc_own_world.clear();
        add_ok = fit_ok = true;
        home = false;
        live_flags.clear();
    };
    const auto held = [&](const BbscSaveSlot& slot) { // the bit the shared progress would save
        std::vector<u32> flags{amelia_flag};
        std::map<u32, std::array<u8, 125>> groups;
        groups[12401][800 / 8] = 0x80u >> (800 % 8);
        HoldBbscUndurableRewardBits(slot, flags, groups);
        return flags.empty() && groups[12401][800 / 8] == 0;
    };
    reward_once("0");

    // Default (variable unset) is ON: a guest that beat Amelia at home gets nothing, nothing owed.
    dedup_unset();
    {
        const BbscSaveSlot on{"sd1", 30};
        fresh(on);
        beaten_at_home();
        const int before = adds;
        kill();
        assert(adds == before && mine() == 0 && owed_line(on).empty());
    }
    // "0" turns it off: the existing behaviour, no ledger.
    dedup("0");
    {
        const BbscSaveSlot off{"sd1", 31};
        fresh(off);
        beaten_at_home();
        const int before = adds;
        kill();
        assert(adds == before + 1 && !std::filesystem::exists("user/boss-rewards/owed-sd1-31.txt"));
    }
    dedup_unset();

    for (const char* mode : {"0", "1"}) {
        reward_once(mode);
        const int base = mode[0] == '1' ? 60 : 40;
        const auto slot = [&](int i) { return BbscSaveSlot{"sd1", base + i}; };

        // Never beaten: given once; the owed line becomes a done line, claimed before the add.
        fresh(slot(0));
        bbsc_own_world[12401][801 / 8] |= 0x80u >> (801 % 8); // another bit of the group
        int before = adds;
        kill();
        assert(adds == before + 1 && owed_line(slot(0)).find("done 12401800 ") == 0);
        kill();
        restart();
        kill();                                               // done line: not again, even before
        assert(adds == before + 1 && mine() == 0);            // the boss flag reaches the save
        // Its flag in the own world and a save after it: the done line goes, the flag is the guard.
        bbsc_own_world.clear();                               // home: the journal is back
        home = true;
        live_flags = {amelia_flag};
        TickBbscBossRewards();
        game_saves(slot(0));
        TickBbscBossRewards();
        assert(owed_line(slot(0)).empty());
        beaten_at_home();
        restart();
        kill();
        assert(adds == before + 1);

        // No journal copy of the group: given (once).
        fresh(slot(1));
        before = adds;
        kill();
        assert(adds == before + 1);

        // Beaten at home: nothing, no record line, nothing owed.
        fresh(slot(2));
        beaten_at_home();
        before = adds;
        kill();
        assert(adds == before && mine() == 0 && owed_line(slot(2)).empty() && record(slot(2)).empty());

        // Gate 1 (owner requirement 1): the owed line cannot be written for the whole run. Nothing is
        // delivered and the shared progress leaves the boss flag out; the run ends; the next joint
        // kill earns it again: given once, nothing lost.
        fresh(slot(3));
        std::filesystem::create_directories(owed_path(slot(3)));  // unwritable ledger
        before = adds;
        kill();
        for (int i = 0; i < 3; ++i) TickBbscBossRewards();
        assert(adds == before && mine() == 1);
        assert(held(slot(3)));                                   // not in the progress
        std::filesystem::remove(owed_path(slot(3)));             // the game closes; storage back
        restart();                                               // journal bit stays OFF
        kill();
        assert(adds == before + 1 && owed_line(slot(3)).find("done ") == 0);
        assert(!held(slot(3)));                                  // durable now: in the progress

        // Owed on disk: the progress keeps the bit (review 1: refused delivery, bit saved, restart).
        fresh(slot(4));
        fit_ok = false;                                          // the one-item capacity is full
        before = adds;
        kill();
        assert(adds == before && owed_line(slot(4)) == "owed 12401800\n" && !held(slot(4)));
        game_saves(slot(4));
        beaten_at_home();                                        // the merge saved the boss bit
        restart();
        assert(mine() == 1);                                     // queued again from the owed line
        fit_ok = true;
        kill();
        assert(adds == before + 1 && mine() == 0 && owed_line(slot(4)).find("done ") == 0);
        restart();
        kill();
        assert(adds == before + 1);

        // Gate 2 (owner requirement 2): the line cannot be rewritten for the whole run after it was
        // owed. The claim fails, so nothing is delivered; after the restart it is delivered once,
        // then used up: never again.
        fresh(slot(5));
        before = adds;
        NoteBbscBossRewardEvent(12401800);                       // owed line written
        std::filesystem::create_directories(owed_path(slot(5)).string() + ".tmp"); // rewrites fail
        for (int i = 0; i < 3; ++i) TickBbscBossRewards();
        assert(adds == before && owed_line(slot(5)) == "owed 12401800\n");
        std::filesystem::remove(owed_path(slot(5)).string() + ".tmp");
        restart();
        TickBbscBossRewards();
        assert(adds == before + 1 && owed_line(slot(5)).find("done ") == 0);
        adds = before;                                           // used up
        restart();
        kill();
        for (int i = 0; i < 3; ++i) TickBbscBossRewards();
        assert(adds == before && mine() == 0);

        // An add refused right after its claim reopens the owed line; the next try gives it once.
        fresh(slot(6));
        add_ok = false;
        before = adds;
        kill();
        assert(adds == before && owed_line(slot(6)) == "owed 12401800\n" && mine() == 1);
        add_ok = true;
        TickBbscBossRewards();
        assert(adds == before + 1 && owed_line(slot(6)).find("done ") == 0);

        // Owner isolation: A's owed reward waits while B (beaten at home) plays, then goes to A.
        const BbscSaveSlot owner_a = slot(7), owner_b = slot(8);
        fresh(owner_a);
        fit_ok = false;
        before = adds;
        kill();
        fresh(owner_b);
        beaten_at_home();
        kill();
        for (int i = 0; i < 3; ++i) TickBbscBossRewards();
        assert(adds == before && owed_line(owner_b).empty() && owed_line(owner_a) == "owed 12401800\n");
        current = owner_a;
        bbsc_own_world.clear();
        TickBbscBossRewards();
        assert(adds == before + 1 && owed_line(owner_a).find("done ") == 0);
    }
    reward_once("0");
    dedup("0");
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

    def test_shared_progress_holds_undurable_reward_bits(self):
        """R03 B18: the boss bit of an obligation without its ledger line stays out of both the
        pending progress file and the merge (structural: those functions are fixture-stubbed)."""
        src = SOURCE.read_text(encoding='utf-8')
        for head in ('void WriteBbscPendingProgress() {', 'std::pair<s64, size_t> MergeBbscSharedProgress('):
            start = src.index(head)
            body = src[start:src.index('\n}\n', start)]
            hold = body.find('HoldBbscUndurableRewardBits(')
            self.assertGreater(hold, 0, head)
            self.assertLess(hold, body.find('put32(' if 'Pending' in head else 'set(0, flag, 1)'), head)


if __name__ == '__main__':
    unittest.main()
