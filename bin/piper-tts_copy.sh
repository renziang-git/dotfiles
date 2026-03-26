#!/bin/bash

# 确保安装了 wl-clipboard (Wayland) 或 xclip (X11)
# 该脚本从剪贴板读取文本，并通过 piper-tts 调整语速后播放

# 1. 获取剪贴板内容
# Wayland 用户使用: wl-paste
# X11 用户使用: xclip -selection clipboard -o
CONTENT=$(wl-paste 2>/dev/null || xclip -selection clipboard -o 2>/dev/null)

if [ -z "$CONTENT" ]; then
  echo "剪贴板为空或未找到剪贴板工具。"
  exit 1
fi

# 2. 设置模型路径和参数
MODEL_PATH="$HOME/models/tts/en_US-lessac-low.onnx"
# length_scale 越小语速越快，1.0 为正常，1.5-2.0 较慢
SPEED=1

# 3. 管道传输并播放
echo "$CONTENT" |
  piper-tts \
    --model "$MODEL_PATH" \
    --length_scale "$SPEED" \
    --output_file - |
  mpv - --no-video
