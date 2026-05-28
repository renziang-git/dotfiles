#!/bin/bash

# 标记位，防止重复报警
warned_50=false
warned_20=false

while true; do
  # 获取电量和状态
  LEVEL=$(cat /sys/class/power_supply/BAT0/capacity)
  STATUS=$(cat /sys/class/power_supply/BAT0/status)

  if [ "$STATUS" = "Discharging" ]; then
    # 20% 严重警告
    if [ "$LEVEL" -le 20 ] && [ "$warned_20" = false ]; then
      notify-send -u critical -i battery-empty "电池电量极低" "仅剩 ${LEVEL}%，请尽快插电！"
      warned_20=true
      warned_50=true # 触发了20%肯定不需要再报50%了
    # 50% 普通提醒
    elif [ "$LEVEL" -le 50 ] && [ "$LEVEL" -gt 20 ] && [ "$warned_50" = false ]; then
      notify-send -u normal -i battery-caution "电池电量过半" "当前电量 ${LEVEL}%，注意续航。"
      warned_50=true
    fi
  else
    # 如果正在充电，重置所有标记位，以便下次放电时再次报警
    warned_50=false
    warned_20=false
  fi

  sleep 60
done
