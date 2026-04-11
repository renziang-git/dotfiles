#!/bin/bash

# 1. 配置路径（请确认 .onnx 和 .json 文件都在此目录下）
MODEL_PATH="$HOME/Downloads/zh_CN-huayan-medium.onnx"
SPEED=1.1

# 2. 获取 Wayland 下鼠标选中的文本 (--primary)
# 如果选区为空，则尝试获取剪贴板内容
CONTENT=$(wl-paste --primary 2>/dev/null || wl-paste 2>/dev/null)

# 3. 检查内容是否为空
if [ -z "$CONTENT" ]; then
  notify-send "Piper TTS" "未检测到选中文本 (Wayland)"
  exit 1
fi

# 4. 朗读并播放
# 注意：有些发行版命令是 piper，有些是 piper-tts，请根据你安装的情况调整
echo "$CONTENT" |
  piper-tts \
    --model "$MODEL_PATH" \
    --length_scale "$SPEED" \
    --output_file - |
  mpv - --no-video
