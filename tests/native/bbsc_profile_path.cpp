#include <cstdlib>
#include <filesystem>
#include "common/path_util.h"
int main() {
    const std::filesystem::path expected(_wgetenv(L"BB_USER_DIR"));
    if (Common::FS::GetUserPath(Common::FS::PathType::UserDir) != expected) return 3;
    if (Common::FS::GetUserPath(Common::FS::PathType::CapturesDir) != expected / "captures") return 4;
}
