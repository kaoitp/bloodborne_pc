#include "shader_recompiler/info.h"
#include <array>
#include <cassert>
#include <cstring>

struct Pair { u32 first; u32 second; };

int main() {
    Shader::Info info;
    std::array<u32, 16> user{};
    info.user_data = user;
    const auto empty = info.ReadUdReg<AmdGpu::Buffer>(0, 0);
    assert(empty.base_address == 0);
    const auto absent_offset = info.ReadUdReg<Pair>(0, 4);
    assert(absent_offset.first == 0 && absent_offset.second == 0);

    std::array<u32, 4> table{11, 22, 33, 44};
    const auto tagged = reinterpret_cast<u64>(table.data()) | 0xabcd000000000000ULL;
    std::memcpy(user.data(), &tagged, sizeof(tagged));
    const auto indirect = info.ReadUdReg<Pair>(0, 2);
    assert(indirect.first == 33 && indirect.second == 44);

    user[3] = 7;
    user[4] = 13;
    const auto direct = info.ReadUdReg<Pair>(Shader::IR::NumScalarRegs, 3);
    assert(direct.first == 7 && direct.second == 13);

    std::array<u32, 16> snapshot{};
    std::memcpy(snapshot.data(), &tagged, sizeof(tagged));
    Shader::Info::ud_snapshots[0] = {&info, snapshot.data(), snapshot.size(), nullptr, 0, 0};
    Shader::Info::num_ud_snapshots = 1;
    const auto captured = info.ReadUdReg<Pair>(0, 0);
    assert(captured.first == 11 && captured.second == 22);
    snapshot[0] = 0;
    snapshot[1] = 0xffff0000;
    const auto tagged_null = info.ReadUdReg<Pair>(0, 2);
    assert(tagged_null.first == 0 && tagged_null.second == 0);
    Shader::Info::num_ud_snapshots = 0;
}
