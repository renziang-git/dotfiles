# Esc 逻辑
cmd_escape_fcitx = (
    "mode-leave ;; "
    "jseval -q document.activeElement.blur() ;; "
    "spawn --detach sh -c 'command -v fcitx5-remote >/dev/null && fcitx5-remote -c'"
)
config.bind("<Escape>", cmd_escape_fcitx, mode="insert")


config.bind(',k', 'spawn --userscript v2raya_fix')
config.bind('td', 'config-cycle colors.webpage.darkmode.enabled true false')

#更新config以及同步gs脚本状态
config.bind("gr", "config-source ;; spawn --userscript qb-update-gm")

# 脚本类前缀 gs
SCRIPT_PREFIX = "gs"
config.bind(f"{SCRIPT_PREFIX}t", "spawn --userscript qb-translate")
config.bind(f"{SCRIPT_PREFIX}c", "spawn --userscript qb-translate-selection")

#yt-dlp 下载控制，bv-video ba-audio bv+ba 合并
config.bind(f"{SCRIPT_PREFIX}b", 'spawn yt-dlp -f "bv*+ba/b" {url}')
config.bind(f"{SCRIPT_PREFIX}v", 'spawn yt-dlp -f bv {url}')
config.bind(f"{SCRIPT_PREFIX}a", 'spawn yt-dlp -f ba {url}')

# 进入视频控制模式
config.bind("gv", "mode-enter passthrough")

c.bindings.commands["passthrough"] = {
    # 速度
    "a": "spawn --userscript qb-video-control down",
    "r": "spawn --userscript qb-video-control reset",
    "s": "spawn --userscript qb-video-control up",
    "e": "spawn --userscript qb-video-control 2.5",
    # 时间跳转
    "z": "spawn --userscript qb-video-control back",
    "x": "spawn --userscript qb-video-control forward",

    # 退出
    "<Escape>": "mode-leave",
}# 视频控制（userscript 测试）

# Alt 快捷键（normal 模式）
config.bind("<Alt-a>", "spawn --userscript qb-video-control down")
config.bind("<Alt-r>", "spawn --userscript qb-video-control reset")
config.bind("<Alt-s>", "spawn --userscript qb-video-control up")
config.bind("<Alt-z>", "spawn --userscript qb-video-control back")
config.bind("<Alt-x>", "spawn --userscript qb-video-control forward")
config.bind("<Alt-e>", "spawn --userscript qb-video-control 2.5")

