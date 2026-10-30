"""Exercise the actual DLL snapshot receiver; this is not native gameplay proof."""
from paths import ROOT
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(os.environ.get('BBSC_FIXTURE_SOURCE') or
              ROOT / '.superpowers/reference/BBSC/emulator/src/core/bloodborne_re.cpp')


def run_ordering_fixture(source, directory):
    src = source.read_text(encoding='utf-8')
    start = src.index('static void ReceiveBbscWorldFlagsPacket(')
    brace = src.index('{', start)
    depth, end = 1, brace + 1
    while depth:
        depth += (src[end] == '{') - (src[end] == '}')
        end += 1
    receiver = src[start:end] + '''
void OnBbscWorldFlagsPacket(const void* data, std::uint32_t size) {
    ReceiveBbscWorldFlagsPacket(data, size);
}
'''
    constants = src[src.index('constexpr std::array<u32, 4> BbscWorldFlagKinds'):
                    src.index('static_assert(BbscDreamGroupCount <=')]
    state = src[src.index('struct BbscWorldSnapshot {'):
                src.index('// Host side: one snapshot of `count` groups')]
    code = r'''
#include <algorithm>
#include <array>
#include <atomic>
#include <cassert>
#include <cstring>
#include <iostream>
#include <map>
#include <mutex>
#include "core/libraries/np/np_signaling/np_signaling_bbsc.h"
#define LOG_INFO(...)
s64 now_ms = 100;
s64 SteadyNowMs() { return ++now_ms; }
bool BbscWorldSyncEnabled() { return true; }
bool IsUsablePackedMap(u32 map) { return map == 0x18000000 || map == 0x18010000 || map == 0x15000000; }
''' + constants + state + receiver + r'''
using Packet = Libraries::Np::NpSignaling::SignalingBbscWorldFlags;
void complete(u8 version, u32 map, u32 sequence, u8 value) {
    const auto total = version == 2 ? BbscDreamGroupCount : BbscWorldGroupCount;
    const auto chunks = version == 2 ? BbscDreamChunkCount : BbscWorldChunkCount;
    for (size_t i = 0; i < chunks; ++i) {
        Packet p{};
        p.version = version; p.packed_map = map; p.snapshot = sequence;
        p.chunk = i; p.chunk_count = chunks;
        p.group_count = std::min(BbscWorldChunkGroups, total - i * BbscWorldChunkGroups);
        p.present = (1u << p.group_count) - 1;
        std::memset(p.groups, value, sizeof(p.groups));
        OnBbscWorldFlagsPacket(&p, sizeof(p));
    }
}
int main() {
    complete(1, 0x18000000, 22, 0x22);
    assert(bbsc_world_blocks.at(0x18000000).groups[0][0] == 0x22);
    complete(1, 0x18000000, 21, 0x21);
    assert(bbsc_world_blocks.at(0x18000000).snapshot == 22);
    assert(bbsc_world_blocks.at(0x18000000).groups[0][0] == 0x22);
    Packet pending{};
    pending.version = 1; pending.packed_map = 0x18000000;
    pending.snapshot = 24; pending.chunk_count = BbscWorldChunkCount;
    pending.group_count = BbscWorldChunkGroups; pending.present = 0xff;
    OnBbscWorldFlagsPacket(&pending, sizeof(pending));
    complete(1, 0x18000000, 23, 0x23);
    assert(bbsc_world_assembling.snapshot == 24);
    assert(bbsc_world_blocks.at(0x18000000).snapshot == 22);
    complete(1, 0x18000000, 24, 0x24);
    assert(bbsc_world_blocks.at(0x18000000).snapshot == 24);

    const s64 completed = bbsc_world_blocks.at(0x18000000).complete_ms;
    now_ms += 10000;
    complete(1, 0x18000000, 24, 0xee);
    assert(bbsc_world_blocks.at(0x18000000).groups[0][0] == 0x24);
    assert(bbsc_world_blocks.at(0x18000000).complete_ms == completed);
    complete(1, 0x18010000, 3, 0x33);
    assert(bbsc_world_blocks.at(0x18010000).snapshot == 3);
    complete(1, 0x18000000, 23, 0xee);
    assert(bbsc_world_blocks.at(0x18000000).snapshot == 24);
    complete(2, 0x15000000, 8, 0x88);
    complete(2, 0x15000000, 7, 0xee);
    assert(bbsc_dream_ready.snapshot == 8 && bbsc_dream_ready.groups[0][0] == 0x88);
    assert(bbsc_world_blocks.at(0x18000000).snapshot == 24);
    Packet bad{};
    bad.version = 3; bad.packed_map = 0x18000000;
    bad.snapshot = 100; bad.chunk_count = BbscWorldChunkCount;
    OnBbscWorldFlagsPacket(&bad, sizeof(bad));
    bad.version = 1; bad.chunk_count = 0;
    OnBbscWorldFlagsPacket(&bad, sizeof(bad));
    bad.chunk_count = BbscWorldChunkCount; bad.chunk = BbscWorldChunkCount;
    OnBbscWorldFlagsPacket(&bad, sizeof(bad));
    bad.chunk = 0; bad.packed_map = 0;
    OnBbscWorldFlagsPacket(&bad, sizeof(bad));
    OnBbscWorldFlagsPacket(nullptr, sizeof(bad));
    OnBbscWorldFlagsPacket(&bad, sizeof(bad) - 1);
    assert(bbsc_world_blocks.size() == 2 && bbsc_world_blocks.at(0x18000000).snapshot == 24);
    ClearBbscHostWorldSnapshots();
    assert(bbsc_world_blocks.empty() && bbsc_dream_ready.map == 0);
    complete(1, 0x18000000, 0xfffffffeu, 0x44);
    complete(1, 0x18000000, 0xffffffffu, 0x55);
    complete(1, 0x18000000, 0, 0x66);
    complete(1, 0x18000000, 0xffffffffu, 0xee);
    complete(1, 0x18000000, 0x80000000u, 0xee);
    assert(bbsc_world_blocks.at(0x18000000).snapshot == 0);
    assert(bbsc_world_blocks.at(0x18000000).groups[0][0] == 0x66);
    ClearBbscHostWorldSnapshots();
    complete(1, 0x18000000, 1, 0x11);
    assert(bbsc_world_blocks.at(0x18000000).snapshot == 1);
    std::cout << "PASS world/Dream ordering, pending chunks, duplicates, maps, wrap/reset and invalid packets\n";

}
'''
    fixture = directory / 'world-ordering.cpp'
    fixture.write_text(code, encoding='utf-8')
    binary = directory / ('world-ordering.exe' if os.name == 'nt' else 'world-ordering')
    subprocess.run([shutil.which('clang++'), '-std=c++23', '-O0',
                    '-I', str(SOURCE.parents[1]), str(fixture), '-o', str(binary)], check=True)
    subprocess.run([str(binary)], check=True)


@unittest.skipUnless(shutil.which('clang++') and SOURCE.is_file(),
                     'prepared pinned BBSC reference and clang++ are required')
class WorldOrderingTests(unittest.TestCase):
    def test_older_completed_snapshot_does_not_replace_newer(self):
        with tempfile.TemporaryDirectory() as directory:
            run_ordering_fixture(SOURCE, Path(directory))


if __name__ == '__main__':
    unittest.main()
