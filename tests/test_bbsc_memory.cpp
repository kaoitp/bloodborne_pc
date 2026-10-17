// SPDX-License-Identifier: GPL-2.0-or-later
#include <cassert>
#include <cstdio>
#include <cstdint>
#include <limits>
#include <cerrno>
#include <cstdarg>
#include <linux/fs.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <unistd.h>

#include "core/memory.h"

extern "C" void* runtime_low_map(std::size_t size, int prot);

#ifdef PROCMAP_QUERY
static bool unsupported = false;
static unsigned queries = 0;
static unsigned successful_queries = 0;
extern "C" int ioctl(int fd, unsigned long request, ...) noexcept {
    va_list args;
    va_start(args, request);
    void* arg = va_arg(args, void*);
    va_end(args);
    if (request == PROCMAP_QUERY) {
        ++queries;
        if (unsupported) {
            errno = ENOTTY;
            return -1;
        }
    }
    const int result = int(syscall(SYS_ioctl, fd, request, arg));
    if (request == PROCMAP_QUERY && result == 0) {
        ++successful_queries;
    }
    return result;
}
#endif

static void CheckMappings() {
    const auto page = static_cast<std::size_t>(sysconf(_SC_PAGESIZE));
    auto* image = static_cast<std::uint8_t*>(runtime_low_map(0x8000, PROT_READ | PROT_WRITE));
    assert(image);
    const auto base = reinterpret_cast<u64>(image);
    auto* memory = Core::Memory::Instance();
    void* start = nullptr;
    void* end = nullptr;
    u32 prot = 0;

    // The image's global pointers gate BBSC's player and inventory lookups.
    *reinterpret_cast<u64*>(image) = 0x1100001000ULL;
    assert(memory->IsValidMapping(base, sizeof(u64)));
    assert(memory->QueryProtection(base, &start, &end, &prot) == 0);
    assert(prot == u32(Core::MemoryProt::CpuReadWrite));
    assert(*reinterpret_cast<u64*>(image) == 0x1100001000ULL);

    assert(mprotect(image + page, page, PROT_READ) == 0);
    assert(memory->QueryProtection(base + page, &start, &end, &prot) == 0);
    assert(prot == u32(Core::MemoryProt::CpuRead));
    assert(!memory->IsValidMapping(base + page - 1, 2));

    assert(mprotect(image + page, page, PROT_NONE) == 0);
    assert(memory->QueryProtection(base + page, &start, &end, &prot) == 0);
    assert(prot == u32(Core::MemoryProt::NoAccess));
    assert(mprotect(image + page, page, PROT_READ | PROT_EXEC) == 0);
    assert(memory->QueryProtection(base + page, &start, &end, &prot) == 0);
    assert(prot == (u32(Core::MemoryProt::CpuRead) | u32(Core::MemoryProt::CpuExec)));

    assert(!memory->IsValidMapping(base, std::numeric_limits<u64>::max()));
    assert(!memory->IsValidMapping(base, 0));
    assert(munmap(image, 0x8000) == 0);
    assert(!memory->IsValidMapping(base, sizeof(u64)));
    assert(!memory->IsValidMapping(0, sizeof(u64)));
}

int main() {
#ifdef PROCMAP_QUERY
    FILE* maps = std::fopen("/proc/self/maps", "r");
    assert(maps);
    struct procmap_query probe{};
    probe.size = sizeof(probe);
    probe.query_addr = reinterpret_cast<uintptr_t>(&queries);
    const bool supported = syscall(SYS_ioctl, fileno(maps), PROCMAP_QUERY, &probe) == 0;
    std::fclose(maps);
#endif
    CheckMappings();
#ifdef PROCMAP_QUERY
    assert(queries > 0); // No full maps scan for every BBSC read on current kernels.
    assert(!supported || successful_queries > 0);
    unsupported = true;
    queries = 0;
    successful_queries = 0;
    CheckMappings();
    assert(queries > 0);
    assert(successful_queries == 0);
#endif
    std::puts("PASS: BBSC host mapping bounds and permissions, including legacy kernel fallback");
}
