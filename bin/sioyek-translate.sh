#!/usr/bin/env bash

PID_FILE="$HOME/.cache/sioyek-translate.pid"

# ---------- 1) 读取剪贴板 ----------
text="$(wl-paste 2>/dev/null)"
[ -z "$text" ] && exit 0

# ---------- 2) 语言识别（strip ANSI） ----------
code="$(
  trans -id "$text" 2>/dev/null |
    sed -r 's/\x1B\[[0-9;]*[mK]//g' |
    awk -F'  +' '/^Code/ {print $2; exit}' |
    xargs
)"
[ -z "$code" ] && exit 1

# ---------- 3) 判断翻译方向 ----------
if [[ "$code" == zh* ]]; then
  dir="zh:en"
elif [[ "$code" == en ]]; then
  dir="en:zh"
else
  exit 1
fi

# ---------- 4) 杀掉上一个窗口（PID 精确） ----------
if [ -f "$PID_FILE" ]; then
  old_pid="$(cat "$PID_FILE")"
  kill "$old_pid" 2>/dev/null
fi

# ---------- 5) 立刻打开 foot，在里面做翻译 ----------
foot \
  --app-id "sioyek-translate" \
  --title "Translation" \
  sh -c "
echo '[ Original ]'
echo \"$text\"
echo
echo '------------------------------'
echo '[ Translation ]'
echo

trans \"$dir\" \"$text\" \
| sed -r 's/\\x1B\\[[0-9;]*[mK]//g' \
| awk '
    /^Translations of / {flag=1; next}
    flag && /^[[:space:]]{4}/ {
      sub(/^[[:space:]]{4}/, \"\")
      print \"    \" \$0
      exit
    }
  '

echo
read -n 1
" &

PID=$!
echo "$PID" >"$PID_FILE"

# 关键新增部分 ↓↓↓
sleep 0.15

#转移焦点到translate窗口
niri msg focus-window --app-id sioyek-translate
niri-sidebar toggle-window
