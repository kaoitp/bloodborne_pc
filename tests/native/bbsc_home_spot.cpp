#include "bbsc_home_spot.h"
#include <cassert>
#include <limits>
int main() {
    assert(!Core::Bbsc::HomeRecoveryEnabled(nullptr));
    assert(!Core::Bbsc::HomeRecoveryEnabled("0"));
    assert(!Core::Bbsc::HomeRecoveryEnabled("10"));
    assert(Core::Bbsc::HomeRecoveryEnabled("1"));
    Core::Bbsc::HomeSpot spot{0x18000000, 2402950, {1.f, 2.f, 3.f, 1.f}, {0.f, .5f, 0.f, 0.f}};
    auto bytes = Core::Bbsc::EncodeHomeSpot(spot);
    const auto decoded = Core::Bbsc::DecodeHomeSpot(bytes);
    assert(decoded && decoded->map == 0x18000000 && decoded->lamp == 2402950);
    assert(decoded->position[2] == 3.f && decoded->rotation[1] == .5f);
    assert(!Core::Bbsc::DecodeHomeSpot(std::span(bytes).first(43)));
    bytes[0] = 2;
    assert(!Core::Bbsc::DecodeHomeSpot(bytes));
    spot.map = 0x28000000;
    assert(!Core::Bbsc::DecodeHomeSpot(Core::Bbsc::EncodeHomeSpot(spot)));
    spot.map = 0x18000000;
    spot.position[0] = std::numeric_limits<float>::quiet_NaN();
    const auto fallback = Core::Bbsc::DecodeHomeSpot(Core::Bbsc::EncodeHomeSpot(spot));
    assert(fallback && !Core::Bbsc::FiniteHomePosition(*fallback) && fallback->lamp == 2402950);
    spot.position = {30000.f, 2.f, 3.f, 1.f};
    assert(!Core::Bbsc::FiniteHomePosition(spot));
    spot.position = {0.f, 0.f, 0.f, 1.f};
    assert(!Core::Bbsc::FiniteHomePosition(spot));
    spot.position[0] = std::numeric_limits<float>::quiet_NaN();
    spot.lamp = -1;
    assert(!Core::Bbsc::DecodeHomeSpot(Core::Bbsc::EncodeHomeSpot(spot)));
}
