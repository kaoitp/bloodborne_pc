"""Actual summon-boundary and progress-byte helpers; no game process required."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get('BBSC_FIXTURE_SOURCE') or
              ROOT / '.superpowers/reference/BBSC/emulator/src/core/bloodborne_re.cpp')


def function(src, signature):
    start = src.index(signature + '(')
    brace = src.index('{', start)
    end, depth = brace + 1, 1
    while depth:
        depth += (src[end] == '{') - (src[end] == '}')
        end += 1
    return src[start:end]


@unittest.skipUnless(shutil.which('clang++') and SOURCE.is_file(),
                     'matching BBSC source and clang++ required')
class PlaytestFixTests(unittest.TestCase):
    def test_actual_role_boundary_and_combat_filter(self):
        src = SOURCE.read_text(encoding='utf-8')
        code = r'''
#include <array>
#include <cassert>
#include <cstdint>
#include <cstring>
#include <iostream>
using u64=uint64_t; using s32=int32_t; using u32=uint32_t; using u8=uint8_t;
constexpr u64 PlayerSlotManagerPointerOffset=16;
u64 image_base=1; s32 state=6, sign=-1, pending=0; bool readable=true, writable=true;
int writes=0;
namespace MemoryProt { constexpr int CpuWrite=1; }
s32 GetSessionState() { return state; }
u64 GetGlobalState() { return 100; }
bool ReadablePointer(u64,size_t) { return readable; }
bool HasMemoryAccess(u64,size_t,int) { return writable; }
template<class T> T ReadValue(u64 p,size_t off) {
    if(p==image_base+PlayerSlotManagerPointerOffset) return 200;
    return off==0x16F0 ? sign : pending;
}
template<class T> bool WriteValue(u64 p,size_t off,T v) {
    assert(p==200 && off==0x8C); pending=v; ++writes; return true;
}
#define LOG_INFO(...)
#define BBSC_TIMELINE(...)
'''
        code += function(src, 'void ClearBbscStaleHostSummonType') + '\n'
        code += function(src, 'u8 BbscDurableProgressByte') + '\n'
        code += r'''
int main() {
    ClearBbscStaleHostSummonType(); assert(pending==-1 && writes==1);
    ClearBbscStaleHostSummonType(); assert(writes==1);
    for(s32 v : {-1,1,2,12,13}) {
        pending=v; ClearBbscStaleHostSummonType(); assert(pending==v && writes==1);
    }
    for(s32 v : {0,3,4,7}) {
        state=v; pending=0; ClearBbscStaleHostSummonType(); assert(pending==0);
    }
    state=6;
    for(s32 v : {0,1,-2,-4,-12}) {
        sign=v; pending=0; ClearBbscStaleHostSummonType(); assert(pending==0);
    }
    sign=-1; readable=false; ClearBbscStaleHostSummonType(); assert(pending==0);
    readable=true; writable=false; ClearBbscStaleHostSummonType(); assert(pending==0);
    writable=true; image_base=0; ClearBbscStaleHostSummonType(); assert(pending==0);
    image_base=1; ClearBbscStaleHostSummonType(); assert(pending==-1 && writes==2);
    // Every bit in affected and adjacent groups: retain completion and unrelated progress.
    for(u32 key=12411;key<=12416;++key) for(size_t b=0;b<125;++b) {
        for(unsigned bit=0;bit<8;++bit) {
            u32 f=key*1000+b*8+bit;
            bool combat=f==12414700 || f==12414702 || f==12415400 ||
                        f==12414800 || f==12414802 || f==12414807;
            u8 value=0x80u>>bit;
            assert(BbscDurableProgressByte(key,b,value)==(combat?0:value));
        }
    }
    assert(BbscDurableProgressByte(12414,100,0xFF)==0x5E);
    std::cout<<"PASS role boundary, invalid pointers, invader/respawn preservation, 6000 progress bits\n";
}
'''
        with tempfile.TemporaryDirectory() as tmp:
            cpp = Path(tmp) / 'playtest.cpp'
            exe = Path(tmp) / 'playtest.exe'
            cpp.write_text(code, encoding='utf-8')
            subprocess.run([shutil.which('clang++'), '-std=c++23', '-O0', str(cpp),
                            '-o', str(exe)], check=True)
            subprocess.run([str(exe)], check=True)

    def test_compensation_removed_and_existing_paths_retained(self):
        src = SOURCE.read_text(encoding='utf-8')
        for removed in ('NoteBbscGuestEnemyDeath(', 'TickBbscGuestDrops(',
                        'GiveBbscGuestDrop(', 'bbsc_guest_drop_queue',
                        'An item was added to your items.'):
            self.assertTrue(removed not in src, removed)
        for retained in ('ApplyBbscGuestLootView(', 'TickBbscGuestItemsPickable(',
                         'NoteBbscBossRewardEvent(', 'TickBbscBossRewards('):
            self.assertIn(retained, src)
        reload_hook = src[src.index('if (site.offset == 0x0178D9C0) {'):]
        self.assertLess(reload_hook.index('ClearBbscStaleHostSummonType();'),
                        reload_hook.index('BbscConnectFirstReloadFinished();'))


if __name__ == '__main__':
    unittest.main()
