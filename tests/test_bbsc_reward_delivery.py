"""Run the pinned DLL reward producer/consumer with controlled native dependencies.

Requires the locally prepared BBSC reference used by tools/build_bbsc_mod.py.
No game assets or saves are read. This fixture is not native gameplay proof.
"""
from paths import ROOT
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = ROOT / '.superpowers/reference/BBSC/emulator/src/core/bloodborne_re.cpp'


def run_delivery_fixture(source, directory):
    src = source.read_text(encoding='utf-8')
    p = directory
    def function(name, kind='void'):
        start = src.index(kind + ' ' + name + '(')
        brace = src.index('{', start)
        depth, end = 1, brace + 1
        while depth:
            if src[end] == '{':
                depth += 1
            elif src[end] == '}':
                depth -= 1
            end += 1
        return src[start:end]

    code=r'''

#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <mutex>
#include <optional>
#include <string>
#include <vector>
using s64 = int64_t;
using u64 = uint64_t;
using s32 = int32_t;
using u32 = uint32_t;
using u8 = uint8_t;
#define PS4_SYSV_ABI
#define LOG_INFO(...)
#define LOG_WARNING(...)
#define BBSC_TIMELINE(...)
struct BbscSaveSlot {
  std::string user;
  int slot = -1;
};
struct BbscBossReward {
  s64 event;
  u32 flag;
  s32 first_lot;
  s32 repeat_lot;
};
struct BbscBossGoodsLot {
  s32 lot;
  u32 goods;
  s32 count;
  u32 flag;
};
std::array<BbscBossReward, 1> BbscBossRewards{{{12411700, 6645, 50000010, 0}}};
std::array<BbscBossGoodsLot, 1> BbscBossGoodsLots{{{50000010, 4114, 1, 0}}};
std::mutex bbsc_boss_reward_mutex;
constexpr u64 ItemManPointerOffset = 0x553D6E0,
              EventFlagManPointerOffset = 0x553B100,
              AwardItemLotOffset = 0x17DDC50;
s64 SteadyNowMs() {
  static s64 now = 1000;
  return now += 1000;
}
bool item_ready = true, event_ready = true, loaded = true, alive = true,
     add_ok = true, taken = false, slot_ready = true;
int adds = 0, popups = 0;
u32 here = 0x18010000;
bool bbsc_join_teleport_done = false; // the join teleport's latch (spectate on only)
bool bbsc_party_placed = true;        // placed beside the host
bool spectate = false;
s32 session_state = 6, character_type = 1;
bool BbscSpectateEnabled() { return spectate; }
s32 GetSessionState() { return session_state; }
s32 GetLocalCharacterType() { return character_type; }
BbscSaveSlot current{"sd1", 1};
bool EnvFlagEnabled(const char *) { return true; }
std::optional<BbscSaveSlot> bbsc_own_world_slot;
std::optional<BbscSaveSlot> BbscActiveSaveSlot() {
  if (!slot_ready)
    return {};
  return current;
}
u64 GetGlobalState() { return 9; }
u64 GetLocalPlayerCharacter() { return 7; }
int GetCharacterHp(u64) { return alive ? 100 : 0; }
bool ReadablePointer(u64 p, size_t) { return p != 0; }
u32 GetCurrentPackedMap() { return here; }
u32 BbscMapArea(u32 m) { return m >> 24; }
bool BbscEventFlag(u32) { return taken; }
void BbscAnnounce(const char16_t *, const char *) {}
bool GiveBbscBossGoods(const BbscBossGoodsLot &) {
  ++adds;
  return add_ok;
}
void fake_award(u64, s32, u32) { ++popups; }
u64 image_base = reinterpret_cast<u64>(&fake_award) - AwardItemLotOffset;
template <class T> T ReadValue(u64 at, u64 off) {
  if (at == 9)
    return off == 8 ? static_cast<T>(!loaded) : 0;
  if (at == image_base + ItemManPointerOffset)
    return item_ready ? 1 : 0;
  if (at == image_base + EventFlagManPointerOffset ||
      at == image_base + 0x553B0D8)
    return event_ready ? 1 : 0;
  return 1;
}
    '''
    owner_bound = 'struct BbscBossRewardPending' in src
    if owner_bound:
        start = src.index('struct BbscBossRewardPending')
        end = src.index('void NoteBbscBossRewardEvent', start)
        code += src[start:end]
    else:
        code += 'std::vector<s64> bbsc_boss_reward_queue, bbsc_boss_reward_given;\n'
    code += function('NoteBbscBossRewardEvent') + '\n' + function('TickBbscBossRewards')
    if 'void TickBbscPartyPlacement(' in src:
        code += '\n' + function('BbscGuestInHostWorld', 'bool') + '\n' + function('TickBbscPartyPlacement')
        code += "\n#define PARTY_PLACEMENT\n"
    entry = '{12411700, current}' if owner_bound else '12411700'
    code += 'void enqueue_test_event() { bbsc_boss_reward_queue.push_back(' + entry + '); }\n'
    code += """
    void seed() {
        bbsc_boss_reward_queue.clear();
        bbsc_boss_reward_given.clear();
        adds = popups = 0;
        enqueue_test_event();
    }
    """
    code+=r'''

int main() {
  seed();
  item_ready = false;
  TickBbscBossRewards();
  assert(bbsc_boss_reward_queue.size() == 1 && bbsc_boss_reward_given.empty());
  item_ready = true;
  event_ready = false;
  TickBbscBossRewards();
  assert(bbsc_boss_reward_queue.size() == 1);
  event_ready = true;
  loaded = false;
  TickBbscBossRewards();
  assert(adds == 0 && bbsc_boss_reward_queue.size() == 1);
  loaded = true;
  alive = false;
  TickBbscBossRewards();
  assert(adds == 0 && bbsc_boss_reward_queue.size() == 1);
  alive = true;
  add_ok = false;
  TickBbscBossRewards();
  assert(adds == 1 && popups == 0 && bbsc_boss_reward_queue.size() == 1 &&
         bbsc_boss_reward_given.empty());
  slot_ready = false;
  TickBbscBossRewards();
  assert(adds == 1 && bbsc_boss_reward_queue.size() == 1);
  slot_ready = true;
  current.user = "other";
  TickBbscBossRewards();
  assert(adds == 1 && bbsc_boss_reward_queue.size() == 1);
  current.user = "sd1";
  current.slot = 0;
  TickBbscBossRewards();
  assert(adds == 1 && bbsc_boss_reward_queue.size() == 1);
  current.slot = 1;
  add_ok = true;
  TickBbscBossRewards();
  assert(adds == 2 && popups == 0 && bbsc_boss_reward_queue.empty() &&
         bbsc_boss_reward_given.size() == 1);
  TickBbscBossRewards();
  assert(adds == 2);
  seed();
  enqueue_test_event();
  TickBbscBossRewards();
  assert(adds == 1 && bbsc_boss_reward_given.size() == 1);
  seed();
  add_ok = false;
  taken = false;
  TickBbscBossRewards();
  taken = true;
  add_ok = true;
  TickBbscBossRewards();
  assert(adds == 2 && bbsc_boss_reward_queue.empty());
  seed();
  taken = true;
  TickBbscBossRewards();
  assert(adds == 0 && popups == 0 && bbsc_boss_reward_queue.empty() &&
         bbsc_boss_reward_given.size() == 1);
  taken = false;
  seed();
  bbsc_boss_reward_queue.clear();
  NoteBbscBossRewardEvent(999);
  assert(bbsc_boss_reward_queue.empty());
  here = 0x15000000;
  NoteBbscBossRewardEvent(12411700);
  assert(bbsc_boss_reward_queue.empty());
  here = 0x18010000;
  bbsc_party_placed = false; // the boss dies during our join load: the host's kill
  NoteBbscBossRewardEvent(12411700);
  assert(bbsc_boss_reward_queue.empty());
  bbsc_party_placed = true;
  NoteBbscBossRewardEvent(12411700);
  NoteBbscBossRewardEvent(12411700);
  assert(bbsc_boss_reward_queue.size() == 1);
  here = 0x15000000;
  TickBbscBossRewards();
  assert(adds == 1 && bbsc_boss_reward_given.size() == 1);
  NoteBbscBossRewardEvent(12411700);
  assert(bbsc_boss_reward_queue.empty());
  current.slot = 0;
  here = 0x18010000;
  NoteBbscBossRewardEvent(12411700);
  assert(bbsc_boss_reward_queue.size() == 1);
  TickBbscBossRewards();
  assert(adds == 2 && bbsc_boss_reward_given.size() == 2);
#ifdef PARTY_PLACEMENT
  // PR #7 review: spectate OFF ("Respawn in place" off), boss items ON. There is no join teleport,
  // so its latch stays false; the game's summon load places the guest.
  seed();
  bbsc_boss_reward_queue.clear();
  spectate = false;
  bbsc_join_teleport_done = false;
  session_state = 0;
  TickBbscPartyPlacement();
  assert(!bbsc_party_placed); // a new session starts unplaced
  session_state = 6;
  loaded = false;
  TickBbscPartyPlacement();
  assert(!bbsc_party_placed);
  NoteBbscBossRewardEvent(12411700); // the boss dies during our summon load: the host's kill
  assert(bbsc_boss_reward_queue.empty());
  loaded = true;
  alive = false;
  TickBbscPartyPlacement();
  assert(!bbsc_party_placed);
  alive = true;
  character_type = 0; // not a guest
  TickBbscPartyPlacement();
  assert(!bbsc_party_placed);
  character_type = 1;
  NoteBbscBossRewardEvent(12411700);
  assert(bbsc_boss_reward_queue.empty()); // not before the first placement tick
  TickBbscPartyPlacement();
  assert(bbsc_party_placed && !bbsc_join_teleport_done);
  alive = false; // a death and a load in the session keep it
  loaded = false;
  TickBbscPartyPlacement();
  assert(bbsc_party_placed);
  alive = true;
  loaded = true;
  NoteBbscBossRewardEvent(12411700);
  NoteBbscBossRewardEvent(12411700);
  assert(bbsc_boss_reward_queue.size() == 1);
  TickBbscBossRewards();
  TickBbscBossRewards();
  NoteBbscBossRewardEvent(12411700);
  assert(adds == 1 && bbsc_boss_reward_given.size() == 1 && bbsc_boss_reward_queue.empty());
  // Spectate ON: placement still waits for the join teleport.
  session_state = 0;
  TickBbscPartyPlacement();
  assert(!bbsc_party_placed);
  session_state = 6;
  spectate = true;
  TickBbscPartyPlacement();
  assert(!bbsc_party_placed);
  bbsc_join_teleport_done = true;
  TickBbscPartyPlacement();
  assert(bbsc_party_placed);
  std::cout << "PASS spectate off: no reward before the summon load places us, then exactly one\n";
#endif
  std::cout << "PASS unavailable item/event/loading/death; failed direct add "
               "retry without popup; owner isolation; once-only confirmed "
               "goods; completed lot\n";
}
    '''
    fixture = p / 'delivery-fixture.cpp'
    fixture.write_text(code, encoding='utf-8')
    binary = p / ('delivery-fixture.exe' if os.name == 'nt' else 'delivery-fixture')
    subprocess.run([shutil.which('clang++'), '-std=c++23', '-O0', str(fixture),
                    '-o', str(binary)], check=True)
    subprocess.run([str(binary)], check=True)


@unittest.skipUnless(shutil.which('clang++') and SOURCE.is_file(),
                     'prepared pinned BBSC reference and clang++ are required')
class BossRewardDeliveryTests(unittest.TestCase):
    def test_owner_bound_retry_and_once_only_delivery(self):
        with tempfile.TemporaryDirectory() as directory:
            run_delivery_fixture(SOURCE, Path(directory))


if __name__ == '__main__':
    unittest.main()
