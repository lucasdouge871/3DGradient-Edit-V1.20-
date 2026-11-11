#pragma once

#include <Geode/Geode.hpp>
#include <algorithm>

// Numbers shared by the popup, the setting listener and the preview.
namespace g3dui::limits {
    constexpr int kMinParts = 1;        // "Render parts" setting range ...
    constexpr int kMaxParts = 512;      // ... 1 x 1 up to 512 x 512
    constexpr int kLagWarnParts = 128;  // above this the user gets the "may lag" warning
    constexpr int kPreviewParts = 16;   // the live preview never draws more than this per side
    // Every point object gets its own group ID, and GD 2.2 has group IDs 1..9999.
    constexpr int kMaxGroupID = 9999;

    // The current "Render parts" setting (1 if mod.json doesn't have it).
    inline int renderParts() {
        auto* mod = geode::Mod::get();
        if (!mod->hasSetting("render-parts")) return kMinParts;
        auto value = mod->getSettingValue<int64_t>("render-parts");
        return std::max(kMinParts, std::min(kMaxParts, static_cast<int>(value)));
    }
}
