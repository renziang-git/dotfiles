
# ==============================================================================
# 基础
# ==============================================================================

import os

# 不加载 GUI 自动配置，所有行为只由 config.py 决定
config.load_autoconfig(False)

# ==============================================================================
# Esc 行为增强（Insert 模式）
# 作用：
# - 退出 insert → normal
# - 让输入框失去焦点
# - 切回英文输入法（fcitx5）
# ==============================================================================

cmd_escape_fcitx = (
    "mode-leave ;; "
    "jseval -q document.activeElement.blur() ;; "
    "spawn --detach sh -c 'command -v fcitx5-remote >/dev/null && fcitx5-remote -c'"
)


# ==============================================================================
# Userscript / GreasyFork 脚本管理（声明式）
# ==============================================================================

# 启用的油猴脚本（支持 GreasyFork 详情页 或 .user.js 直链）
enabled_scripts = [
    # CSDN 去广告
    "https://greasyfork.org/zh-CN/scripts/420352-csdn-focus",
    # 知乎免登录
    "https://greasyfork.org/zh-CN/scripts/396171-%E7%9F%A5%E4%B9%8E%E5%85%8D%E7%99%BB%E5%BD%95",
]

# 暂时禁用的脚本（不删除文件）
disabled_scripts = [
]

# 通过环境变量传给 userscript
os.environ["QB_GM_LIST"] = " ".join(enabled_scripts)
os.environ["QB_GM_DISABLED_LIST"] = " ".join(disabled_scripts)


#快捷键
SCRIPT_PREFIX = "gs"
config.bind("<Escape>", cmd_escape_fcitx, mode="insert")

# gr：
# 1. 重新加载 config.py
# 2. 执行 qb-update-gm userscript
#config.bind("gr", "config-source ;; spawn --userscript qb-update-gm")
config.bind(f"{SCRIPT_PREFIX}u", "spawn --userscript qb-update-gm")
config.bind(f"{SCRIPT_PREFIX}t", "spawn --userscript qb-translate")
config.bind(f"{SCRIPT_PREFIX}c", "spawn --userscript qb-translate-selection")


# 进入视频控制模式
config.bind("gv", "mode-enter passthrough")

c.bindings.commands["passthrough"] = {
    # 速度
    "a": "spawn --userscript qb-video-control down",
    "s": "spawn --userscript qb-video-control reset",
    "d": "spawn --userscript qb-video-control up",
    "r": "spawn --userscript qb-video-control 2.5",
    # 时间跳转
    "z": "spawn --userscript qb-video-control back",
    "x": "spawn --userscript qb-video-control forward",

    # 退出
    "<Escape>": "mode-leave",
}# 视频控制（userscript 测试）

# Alt 快捷键（normal 模式）
config.bind("<Alt-a>", "spawn --userscript qb-video-control down")
config.bind("<Alt-s>", "spawn --userscript qb-video-control reset")
config.bind("<Alt-d>", "spawn --userscript qb-video-control up")
config.bind("<Alt-z>", "spawn --userscript qb-video-control back")
config.bind("<Alt-x>", "spawn --userscript qb-video-control forward")
config.bind("<Alt-r>", "spawn --userscript qb-video-control 2.5")
