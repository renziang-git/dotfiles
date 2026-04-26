#!/bin/bash

# 获取当前焦点窗口的 XID
win_id=$(xprop -root _NET_ACTIVE_WINDOW | awk '{print $5}')

# 如果没有获取到，退出
[ -z "$win_id" ] && exit

# 获取该窗口对应的 PID
pid=$(xprop -id "$win_id" _NET_WM_PID | awk '{print $3}')

# 如果 PID 存在，就强制杀死
if [ -n "$pid" ]; then
    kill -9 "$pid"
fi

