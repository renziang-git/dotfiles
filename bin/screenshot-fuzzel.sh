#!/usr/bin/env bash
set -e

MENU=$(printf "󰆟 区域 → 剪贴板\n󰆟 区域 → 文件\n󰆟 区域 → 标注\n———\n󰍹 全屏 → 剪贴板\n󰍹 全屏 → 文件\n" \
  | fuzzel --dmenu \
           --prompt="Screenshot" \
           --lines=6 \
           --width=32 \
           --anchor=center \
           --layer=overlay \
           --no-sort \
           --match-mode=exact)

[ -z "$MENU" ] && exit 0

DIR="$HOME/Pictures/Screenshots"
mkdir -p "$DIR"
FILE="$DIR/$(date +%F-%H%M%S).png"

case "$MENU" in
  *"区域 → 剪贴板")
    grim -g "$(slurp)" - | wl-copy ;;
  *"区域 → 文件")
    grim -g "$(slurp)" "$FILE" ;;
  *"全屏 → 剪贴板")
    grim - | wl-copy ;;
  *"全屏 → 文件")
    grim "$FILE" ;;
  *"区域 → 标注")
    grim -g "$(slurp)" - | swappy -f - ;;
esac

