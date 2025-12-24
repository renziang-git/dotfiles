#!/usr/bin/env bash
# Polybar Nerd Font 测试脚本

BAR_NAME="font-test"
SYMBOLS="            "

# 杀掉旧实例
killall -q polybar
while pgrep -x polybar >/dev/null; do sleep 0.5; done

# 生成临时配置
CONFIG=$(mktemp)

cat > "$CONFIG" <<EOF
[bar/$BAR_NAME]
width = 100%
height = 30
background = #222222
foreground = #FFFFFF
font-0 = SFMono Nerd Font Mono:pixelsize=14;2
modules-center = test

[module/test]
type = custom/text
content = $SYMBOLS
content-foreground = #FFFFFF
EOF

# 启动测试 bar
polybar $BAR_NAME -c "$CONFIG" &
echo "✅ Polybar 字体测试已启动。"
echo "🔤 测试符号: $SYMBOLS"
echo "🧹 关闭测试栏请执行: killall polybar"

