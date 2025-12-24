#!/usr/bin/env bash

# 自动检测显示器名称
monitor=$(xrandr | grep " connected" | cut -d ' ' -f1)

# 获取可用分辨率列表
resolutions=$(xrandr | grep -A1 "^$monitor" | tail -n +2 | awk '{print $1}' | grep -v '+')

# 使用 rofi 选择分辨率（也可以改成 dmenu）
choice=$(echo "$resolutions" | rofi -dmenu -p "选择分辨率:")

# 如果用户选择了某个分辨率
if [[ -n "$choice" ]]; then
    xrandr --output "$monitor" --mode "$choice"
    notify-send "分辨率已切换为 $choice"
else
    notify-send "取消切换分辨率"
fi

