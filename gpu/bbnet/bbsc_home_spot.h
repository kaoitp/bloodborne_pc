// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include <array>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <optional>
#include <span>

namespace Core::Bbsc {
inline bool HomeRecoveryEnabled(const char* value) {
    return value && value[0] == '1' && value[1] == '\0';
}
inline bool AcceptHomeRecoveryLoad(bool requested, bool& loaded) {
    if (!requested || loaded) return false;
    loaded = true;
    return true;
}
inline constexpr std::uint32_t HomeSpotKey = 0xffff484d;
struct HomeSpot {
    std::uint32_t map{};
    std::int32_t lamp{-1};
    std::array<float, 4> position{};
    std::array<float, 4> rotation{};
};
inline bool SupportedHomeMap(std::uint32_t map) {
    const auto area = map >> 24;
    return (map & 0xffff) == 0 && ((map >> 16) & 0xff) <= 9 &&
           ((area >= 21 && area <= 28) || (area >= 32 && area <= 36));
}
inline bool FiniteHomePosition(const HomeSpot& spot) {
    if (spot.position[0] == 0.f && spot.position[1] == 0.f && spot.position[2] == 0.f) return false;
    for (float value : spot.position) {
        if (!std::isfinite(value) || std::abs(value) > 20000.f) return false;
    }
    for (float value : spot.rotation) {
        if (!std::isfinite(value)) return false;
    }
    return true;
}
inline std::array<std::uint8_t, 44> EncodeHomeSpot(const HomeSpot& spot) {
    std::array<std::uint8_t, 44> bytes{};
    const std::uint32_t version = 1;
    std::memcpy(bytes.data(), &version, 4);
    std::memcpy(bytes.data() + 4, &spot.map, 4);
    std::memcpy(bytes.data() + 8, &spot.lamp, 4);
    std::memcpy(bytes.data() + 12, spot.position.data(), 16);
    std::memcpy(bytes.data() + 28, spot.rotation.data(), 16);
    return bytes;
}
inline std::optional<HomeSpot> DecodeHomeSpot(std::span<const std::uint8_t> bytes) {
    if (bytes.size() < 44) return std::nullopt;
    std::uint32_t version{};
    HomeSpot spot;
    std::memcpy(&version, bytes.data(), 4);
    std::memcpy(&spot.map, bytes.data() + 4, 4);
    std::memcpy(&spot.lamp, bytes.data() + 8, 4);
    std::memcpy(spot.position.data(), bytes.data() + 12, 16);
    std::memcpy(spot.rotation.data(), bytes.data() + 28, 16);
    if (version != 1 || !SupportedHomeMap(spot.map)) return std::nullopt;
    const auto lamp = spot.lamp;
    const auto lamp_map = lamp < 1000000 ? 0u :
        (static_cast<std::uint32_t>(lamp / 100000) << 24) |
        (static_cast<std::uint32_t>((lamp / 10000) % 10) << 16);
    if (!FiniteHomePosition(spot) && !SupportedHomeMap(lamp_map)) return std::nullopt;
    return spot;
}
} // namespace Core::Bbsc
