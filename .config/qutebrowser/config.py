#关闭download open_dispatcher
c.downloads.open_dispatcher = None
config.source('colors.py')
#外部编辑器
# c.editor.command = [
#     'kitty',
#     '--class', 'QuteEditor',
#     'vim',
#     '{file}'
# ]
#c.content.javascript.log = {
#    'error': False,
#    'warning': False,
#    'info': False,
#    'debug': False,
#}
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

#v2raya
config.bind(',k', 'spawn --userscript v2raya_fix')

# 使用快捷键（例如 'td'，代表 Toggle Darkmode）在暗黑模式间切换
config.bind('td', 'config-cycle colors.webpage.darkmode.enabled true false')


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
#-----------------------------------------------------------------------------
#启用chrome扩展
#config.set("content.extensions", True)
#-----------------------------------------------------------------------------
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

# 选中 tab（奇 / 偶）
# c.colors.tabs.selected.odd.bg = '#eeeeee'
# c.colors.tabs.selected.odd.fg = '#000000'
# c.colors.tabs.selected.even.bg = '#eeeeee'
# c.colors.tabs.selected.even.fg = '#000000'
#
# 启用或禁用 Chromium 的低端设备模式，以减小内存占用。
# 可选值："always"（总是启用）、"auto"（根据可用内存自动选择）、"never"（从不启用）。
c.qt.chromium.low_end_device_mode = 'auto'

# 强制软件渲染设置。有助于解决某些图形驱动的兼容性问题。
# 可选值："software-opengl"（LibGL 使用软件实现）、"qt-quick"（Qt Quick 使用软件渲染）、
# "chromium"（禁用 GPU，使用 Skia 软件渲染）、"none"（不强制软件渲染）。
c.qt.force_software_rendering = 'none'

# 处理 2D canvas 加速相关问题。禁用加速的 2D canvas 可以避免部分显卡的图形故障。
# 可选值："always"、"auto"、"never"。
c.qt.workarounds.disable_accelerated_2d_canvas = 'auto'

# 启用网页的平滑滚动。设置为 True 时，将启用平滑滚动动画（不影响 :scroll-px 命令）。
c.scrolling.smooth = True

# 会话惰性恢复：仅在标签获得焦点时加载恢复的页面，可减少启动时资源占用。
c.session.lazy_restore = False

# 窗口透明背景。启用后，可以拥有透明的标签栏/状态栏，但可能降低性能。
c.window.transparent = False
