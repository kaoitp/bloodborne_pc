"""Actual member-character lookup + the shown-bit repair after an insert-task restart (R03,
host death: the guest recreated without +0x1E0 bit 0x100000 showed only its name tag).
Fixture evidence with controlled memory; the native finding is in R03-B13-HOST-RESPAWN-SHOW.md."""
from paths import ROOT
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(os.environ.get('BBSC_FIXTURE_SOURCE') or
              ROOT / '.superpowers/reference/BBSC/emulator/src/core/bloodborne_re.cpp')


def run_show_fixture(source, directory):
    src = source.read_text(encoding='utf-8')

    def function(head):
        start = src.index(head)
        brace = src.index('{', start)
        depth, end = 1, brace + 1
        while depth:
            depth += {'{': 1, '}': -1}.get(src[end], 0)
            end += 1
        return src[start:end]

    code = r'''
#include <cassert>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <vector>
using s32 = int32_t; using s64 = int64_t; using u8 = uint8_t; using u32 = uint32_t; using u64 = uint64_t;
#define PS4_SYSV_ABI
#define LOG_INFO(...)
#define BBSC_TIMELINE(...)
enum class MemoryProt { CpuRead, CpuWrite };
constexpr u64 CandidateLocalStatePointerOffset = 0x0553E878, MemberIdEqualsOffset = 0x00CA1C70;
bool fake_equals(u64 a, u64 b) { return *reinterpret_cast<u64*>(a) == *reinterpret_cast<u64*>(b); }
u64 image_base = reinterpret_cast<u64>(&fake_equals) - MemberIdEqualsOffset;
s64 now_ms = 1000;
s64 SteadyNowMs() { return now_ms; }
struct World { u8 pad[0x30]; s32 count; u8 pad2[4]; u64 entries; };
alignas(16) u8 global_state[0x1600] = {};
World world{};
u64 entries[4 * 7] = {}; // 0x38 bytes per entry, PlayerIns* at +0
alignas(16) u8 host_chr[0x800] = {}, guest_chr[0x800] = {}, other_chr[0x800] = {};
alignas(16) u8 guest_task[0x100] = {}, host_task[0x100] = {}, other_task[0x100] = {};
std::vector<u64> tasks;
u64 GetGlobalState() { return reinterpret_cast<u64>(global_state); }
std::vector<u64> GetMultiPlayerInsTasks() { return tasks; }
bool ReadablePointer(u64 p, size_t) { return p != 0; }
bool HasMemoryAccess(u64, size_t, MemoryProt) { return true; }
bool IsValidMemberId(u64 p) { return *reinterpret_cast<u64*>(p) != 0; }
template <class T> T ReadValue(u64 base, u64 off) {
    if (base == image_base + CandidateLocalStatePointerOffset) return static_cast<T>(reinterpret_cast<u64>(&world));
    T v; std::memcpy(&v, reinterpret_cast<void*>(base + off), sizeof(T)); return v;
}
template <class T> void WriteValue(u64 base, u64 off, T v) { std::memcpy(reinterpret_cast<void*>(base + off), &v, sizeof(T)); }
template <class T> void put(u8* p, size_t off, T v) { std::memcpy(p + off, &v, sizeof(T)); }
u32 flags(const u8* chr) { u32 v; std::memcpy(&v, chr + 0x1E0, 4); return v; }
'''
    if 'u64 FindRemotePlayerOf(' in src:
        code += function('u64 FindRemotePlayerOf(') + '\n'
    code += function('bool RemotePlayerExists(') + '\n'
    if 'void TickBbscRemoteShow(' in src:
        start = src.index('constexpr u32 BbscPlayerShownBit')
        code += src[start:src.index('void TickBbscRemoteShow(')] + function('void TickBbscRemoteShow(')
    else:  # the source before the repair: nothing sets the bit
        code += 'void ArmBbscRemoteShow() {}\nvoid TickBbscRemoteShow() {}\n'
    code += r'''
int main() {
    world.count = 3; world.entries = reinterpret_cast<u64>(entries);
    entries[0] = reinterpret_cast<u64>(host_chr);
    entries[7] = reinterpret_cast<u64>(guest_chr);
    entries[14] = reinterpret_cast<u64>(other_chr);
    put<u64>(host_chr, 0x3D8, 11); put<u64>(guest_chr, 0x3D8, 22); put<u64>(other_chr, 0x3D8, 33);
    put<u64>(host_task, 0xC8, 11); put<s32>(host_task, 0xE8, 3);   // self-host
    put<u64>(guest_task, 0xC8, 22); put<s32>(guest_task, 0xE8, 1); // remote guest
    put<u64>(other_task, 0xC8, 33); put<s32>(other_task, 0xE8, 1);
    put<u32>(host_chr, 0x1E0, 0x9800);   // must never be touched: not a remote member
    put<u32>(guest_chr, 0x1E0, 0x9800);  // recreated after the host's death: hidden
    put<u32>(other_chr, 0x1E0, 0x109800);
    tasks = {reinterpret_cast<u64>(host_task), reinterpret_cast<u64>(guest_task),
             reinterpret_cast<u64>(other_task)};
    assert(RemotePlayerExists(reinterpret_cast<u64>(guest_task)));
    TickBbscRemoteShow(); // not armed: no restart happened
    assert(flags(guest_chr) == 0x9800);
    ArmBbscRemoteShow();
    global_state[0x08] = 1; // loading
    TickBbscRemoteShow();
    assert(flags(guest_chr) == 0x9800);
    global_state[0x08] = 0;
    TickBbscRemoteShow();
    assert(flags(guest_chr) == 0x109800);
    assert(flags(host_chr) == 0x9800 && flags(other_chr) == 0x109800);
    now_ms += 31'000; // the window after the restart is over
    put<u32>(guest_chr, 0x1E0, 0x8800);
    TickBbscRemoteShow();
    assert(flags(guest_chr) == 0x8800);
    ArmBbscRemoteShow(); // a later restart arms it again
    TickBbscRemoteShow();
    assert(flags(guest_chr) == 0x108800);
    std::cout << "PASS a member character recreated without its shown bit gets it after a restart\n";
}
'''
    fixture = directory / 'remote-show.cpp'
    fixture.write_text(code, encoding='utf-8')
    binary = directory / ('remote-show.exe' if os.name == 'nt' else 'remote-show')
    subprocess.run([shutil.which('clang++'), '-std=c++23', '-O0', '-g', '-fsanitize=address',
                    str(fixture), '-o', str(binary)], check=True)
    subprocess.run([str(binary)], check=True)


@unittest.skipUnless(shutil.which('clang++') and SOURCE.is_file(),
                     'prepared pinned BBSC reference and clang++ are required')
class RemoteShowTests(unittest.TestCase):
    def test_recreated_member_character_is_shown(self):
        with tempfile.TemporaryDirectory() as directory:
            run_show_fixture(SOURCE, Path(directory))


if __name__ == '__main__':
    unittest.main()
