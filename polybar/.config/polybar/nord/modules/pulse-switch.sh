#!/bin/bash

# 获取当前默认输出设备
current_sink=$(pactl info | grep "Default Sink" | awk '{print $3}')

# 获取所有输出设备列表
sinks=$(pactl list short sinks | awk '{print $2}')

# 使用 rofi 弹出选择菜单
chosen=$(echo "$sinks" | rofi -dmenu -p "Select audio output:" -format "{input}")

# 切换默认输出
if [ -n "$chosen" ]; then
    pactl set-default-sink "$chosen"
fi

