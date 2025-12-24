#!/usr/bin/env bash

HIST_FILE="${XDG_CACHE_HOME:-$HOME/.cache}/fuzzel-url-history"

# 从历史中读取，交给 fuzzel
URL="$(
  cat "$HIST_FILE" 2>/dev/null \
  | fuzzel --dmenu --prompt="Chrome URL"
)"

# Esc / 空输入
[ -z "$URL" ] && exit 0

# 去空格
URL="$(echo "$URL" | xargs)"

# 自动补协议
if ! echo "$URL" | grep -qE '^[a-zA-Z]+://'; then
    URL="https://$URL"
fi

# 写回历史（去重）
{
    echo "$URL"
    cat "$HIST_FILE" 2>/dev/null
} | awk '!seen[$0]++' > "${HIST_FILE}.tmp"

mv "${HIST_FILE}.tmp" "$HIST_FILE"

# Chrome App 模式启动
setsid google-chrome-stable --app="$URL" >/dev/null 2>&1 &

