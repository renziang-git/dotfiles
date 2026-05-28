#!/bin/bash

# 壁纸文件夹路径（改成你的）
WALLPAPER_DIR="$HOME/Pictures/wallpaper/"

# 随机选一张图片
IMG=$(find "$WALLPAPER_DIR" -type f \( -name '*.jpg' -o -name '*.png' -o -name '*.jpeg' \) | shuf -n 1)

# 如果没找到图片，用默认锁屏
if [ -z "$IMG" ]; then
  echo "No images found in $WALLPAPER_DIR"
  swaylock
else
  swaylock -i "$IMG" -c 000000 -s fill
fi
