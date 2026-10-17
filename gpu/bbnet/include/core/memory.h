// bbport online module: shadPS4's memory manager as BBSC asks it (is this address mapped, with
// which protection), answered from the runtime's own map (runtime_memory_vma_info). Each thread
// remembers the last few mappings for a moment: BBSC checks every read it makes, and the map is
// behind a lock the game's own mappings take. Host-owned image and stack mappings are queried
// from Linux separately: they are not in the direct/flexible memory table.
#pragma once
#include <array>
#include <cerrno>
#include <chrono>
#include <cstdio>
#include <cstdint>
#ifdef __linux__
#include <linux/fs.h>
#include <sys/ioctl.h>
#endif

#include "common/singleton.h"
#include "common/types.h"

extern "C" int runtime_memory_vma_info(uintptr_t address, int* prot, int* type, uintptr_t* end);

namespace Core {

enum class MemoryProt : u32 {
    NoAccess = 0,
    CpuRead = 1,
    CpuWrite = 2,
    CpuReadWrite = 3,
    CpuExec = 4,
    GpuRead = 16,
    GpuWrite = 32,
    GpuReadWrite = 48,
};

class MemoryManager {
public:
    bool IsValidMapping(u64 address, u64 size) {
        u32 prot = 0;
        void* start = nullptr;
        void* end = nullptr;
        return size != 0 && QueryProtection(address, &start, &end, &prot) == 0 &&
               size <= reinterpret_cast<u64>(end) - address;
    }
    /// 0 and the mapping's range and protection (MemoryProt bits), or -1 when unmapped.
    int QueryProtection(u64 address, void** start, void** end, u32* prot) {
        struct Cached {
            u64 start = 0, end = 0;
            u32 prot = 0;
            std::chrono::steady_clock::time_point at{};
        };
        thread_local std::array<Cached, 8> cache{};
        thread_local unsigned next = 0;
        const auto now = std::chrono::steady_clock::now();
        for (const auto& c : cache) {
            if (address >= c.start && address < c.end &&
                now - c.at < std::chrono::milliseconds(250)) {
                *start = reinterpret_cast<void*>(c.start);
                *end = reinterpret_cast<void*>(c.end);
                *prot = c.prot;
                return 0;
            }
        }
        int p = 0, type = -1;
        uintptr_t mapping_end = 0;
        if (!runtime_memory_vma_info(address, &p, &type, &mapping_end)) {
#ifndef _WIN32
            // The loader maps the image and stacks itself. Do not cache their host permissions:
            // mprotect/munmap bypass the runtime's mapping table (and GPU traps use it too).
            if (FILE* maps = std::fopen("/proc/self/maps", "r")) {
#ifdef PROCMAP_QUERY
                // Linux 6.11+: query one VMA instead of scanning maps on every BBSC read.
                struct procmap_query query{};
                query.size = sizeof(query);
                query.query_addr = address;
                if (ioctl(fileno(maps), PROCMAP_QUERY, &query) == 0) {
                    *start = reinterpret_cast<void*>(query.vma_start);
                    *end = reinterpret_cast<void*>(query.vma_end);
                    *prot = u32(query.vma_flags) &
                            (u32(MemoryProt::CpuReadWrite) | u32(MemoryProt::CpuExec));
                    std::fclose(maps);
                    return 0;
                }
                if (errno == ENOENT) {
                    std::fclose(maps);
                    return -1;
                }
#endif
                char line[512];
                while (std::fgets(line, sizeof(line), maps)) {
                    unsigned long long first = 0, last = 0;
                    char perms[5] = {};
                    if (std::sscanf(line, "%llx-%llx %4s", &first, &last, perms) != 3 ||
                        address < first || address >= last) {
                        continue;
                    }
                    *start = reinterpret_cast<void*>(first);
                    *end = reinterpret_cast<void*>(last);
                    *prot = (perms[0] == 'r' ? u32(MemoryProt::CpuRead) : 0) |
                            (perms[1] == 'w' ? u32(MemoryProt::CpuWrite) : 0) |
                            (perms[2] == 'x' ? u32(MemoryProt::CpuExec) : 0);
                    std::fclose(maps);
                    return 0;
                }
                std::fclose(maps);
            }
#endif
            return -1;
        }
        // The runtime's map gives the end of the mapping, not its start: the address itself
        // stands for it (callers check address >= start).
        auto& slot = cache[next++ % cache.size()];
        slot = {address & ~u64(0xfff), mapping_end, u32(p), now};
        *start = reinterpret_cast<void*>(slot.start);
        *end = reinterpret_cast<void*>(slot.end);
        *prot = slot.prot;
        return 0;
    }
};

using Memory = Common::Singleton<MemoryManager>;

} // namespace Core
