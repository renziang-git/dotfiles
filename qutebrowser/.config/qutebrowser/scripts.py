import os
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

