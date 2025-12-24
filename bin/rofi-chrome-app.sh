#!/usr/bin/env bash

# 历史记录文件，用来在 rofi 里回显以前输入过的网址
HIST_FILE="${XDG_CACHE_HOME:-$HOME/.cache}/rofi-url-history"

# 让 rofi 作为 dmenu 用，支持历史记录
URL="$(cat "$HIST_FILE" 2>/dev/null | rofi -dmenu -p 'Chrome URL' -l 10)"

# 用户按 Esc 或没输入
[ -z "$URL" ] && exit 0

# 去掉两端空格
URL="$(echo "$URL" | xargs)"

# 如果没有协议，就自动补上 https://
if ! echo "$URL" | grep -qE '^[a-zA-Z]+://'; then
    URL="https://$URL"
fi

# 把这次输入的 URL 写回历史，去重
{
    echo "$URL"
    cat "$HIST_FILE" 2>/dev/null
} | awk '!seen[$0]++' > "${HIST_FILE}.tmp"

mv "${HIST_FILE}.tmp" "$HIST_FILE"

# 启动 chrome app 模式窗口
setsid google-chrome-stable --app="$URL" >/dev/null 2>&1 &

