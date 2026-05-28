#!/usr/bin/env bash
set -e

echo "=== xrandr 自动显示管理脚本 ==="

# 1. 检测已连接显示器
mapfile -t CONNECTED < <(xrandr | awk '/ connected/ {print $1}')

if [ "${#CONNECTED[@]}" -lt 1 ]; then
  echo "未检测到显示器"
  exit 1
fi

echo
echo "已检测到的显示器："
for i in "${!CONNECTED[@]}"; do
  echo "[$i] ${CONNECTED[$i]}"
done

# 2. 选择显示模式
echo
echo "选择显示模式："
echo "1) 扩展显示（双屏）"
echo "2) 仅使用某一个屏幕（独显）"
read -rp "输入 1 或 2: " MODE

# =========================
# 模式 2：独显
# =========================
if [ "$MODE" = "2" ]; then
  echo
  read -rp "选择要独显的屏幕编号: " SOLO_IDX
  SOLO="${CONNECTED[$SOLO_IDX]}"

  echo
  echo "即将执行："
  echo "只启用 $SOLO，其余屏幕关闭"
  echo
  read -rp "确认执行？(y/N): " CONFIRM

  if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
    CMD="xrandr"
    for m in "${CONNECTED[@]}"; do
      if [ "$m" = "$SOLO" ]; then
        CMD+=" --output $m --auto --primary"
      else
        CMD+=" --output $m --off"
      fi
    done
    eval "$CMD"
    echo "完成（独显模式）"
  else
    echo "已取消"
  fi
  exit 0
fi

# =========================
# 模式 1：扩展显示
# =========================

if [ "${#CONNECTED[@]}" -lt 2 ]; then
  echo "扩展显示需要至少 2 个显示器"
  exit 1
fi

echo
read -rp "选择主显示器编号（通常是内屏）: " MAIN_IDX
MAIN="${CONNECTED[$MAIN_IDX]}"

echo
read -rp "选择外接显示器编号: " EXT_IDX
EXT="${CONNECTED[$EXT_IDX]}"

if [ "$MAIN" = "$EXT" ]; then
  echo "主显示器和外接显示器不能相同"
  exit 1
fi

# 位置选择
echo
echo "选择外接显示器相对位置："
echo "1) 左边"
echo "2) 右边"
echo "3) 上面"
echo "4) 下面"
read -rp "输入 1-4: " POS

case "$POS" in
  1) REL="--left-of" ;;
  2) REL="--right-of" ;;
  3) REL="--above" ;;
  4) REL="--below" ;;
  *) echo "无效选择"; exit 1 ;;
esac

# 分辨率选择
echo
echo "可用分辨率（$EXT）："
mapfile -t MODES < <(
  xrandr | awk -v mon="$EXT" '
    $1==mon {f=1; next}
    f && $1 ~ /^[0-9]/ {print $1}
    f && $0=="" {exit}
  '
)

for i in "${!MODES[@]}"; do
  echo "[$i] ${MODES[$i]}"
done

read -rp "选择分辨率编号: " MODE_IDX
RES="${MODES[$MODE_IDX]}"

echo
echo "即将执行："
echo "xrandr --output $MAIN --auto --primary \\"
echo "       --output $EXT --mode $RES $REL $MAIN"
echo
read -rp "确认执行？(y/N): " CONFIRM

if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
  xrandr \
    --output "$MAIN" --auto --primary \
    --output "$EXT" --mode "$RES" $REL "$MAIN"
  echo "完成（扩展模式）"
else
  echo "已取消"
fi

