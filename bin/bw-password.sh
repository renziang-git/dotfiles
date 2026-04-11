#!/bin/bash

# 屏蔽 Node 警告
export NODE_OPTIONS="--no-deprecation"

# --- 环境检查与解锁 ---
check_auth() {
  STATUS=$(bw status | jq -r '.status')
  if [ "$STATUS" == "locked" ]; then
    echo "🔒 请输入主密码解锁："
    BW_SESSION=$(bw unlock --raw)
    [ $? -ne 0 ] && exit 1
    export BW_SESSION
  elif [ "$STATUS" == "unauthenticated" ]; then
    echo "❌ 请先执行 bw login"
    exit 1
  fi
}

# --- 功能 1：查询并复制密码 (fzf) ---
search_pass() {
  check_auth
  echo "🔍 正在读取列表..."
  # 获取列表，展示 [用户名] 名称 | ID
  SELECTED=$(bw list items --session "$BW_SESSION" |
    jq -r '.[] | "[\(.login.username // "N/A")] \(.name) | \(.id)"' |
    fzf --height 40% --reverse --header "回车(Enter)复制密码 | ESC 退出")

  UUID=$(echo "$SELECTED" | awk -F'| ' '{print $NF}')

  if [ -n "$UUID" ]; then
    COPY_CMD="pbcopy"
    command -v xclip >/dev/null && COPY_CMD="xclip -selection clipboard"
    command -v wl-copy >/dev/null && COPY_CMD="wl-copy"

    bw get password "$UUID" --session "$BW_SESSION" | tr -d '\n' | $COPY_CMD
    echo "✅ 密码已存入剪贴板！"
  fi
}

# --- 功能 2：存入新密码 (带自动生成) ---
add_pass() {
  check_auth
  read -p "📌 条目名称: " ITEM_NAME
  read -p "👤 用户名: " ITEM_USER

  # 询问是否生成随机密码
  read -p "🎲 是否生成随机密码? (y/n, 默认y): " GEN_RAND
  if [[ "$GEN_RAND" != "n" ]]; then
    # 生成 20 位包含数字和特殊符号的密码
    ITEM_PASS=$(bw generate -ulns --length 20)
    echo "✨ 已生成随机密码: $ITEM_PASS"
  else
    read -s -p "🔑 请手动输入密码: " ITEM_PASS
    echo ""
  fi

  echo "🚀 正在存入并同步..."
  TEMPLATE=$(bw get template item)
  NEW_ITEM=$(echo "$TEMPLATE" | jq \
    --arg name "$ITEM_NAME" \
    --arg user "$ITEM_USER" \
    --arg pass "$ITEM_PASS" \
    '.name=$name | .login.username=$user | .login.password=$pass')

  echo "$NEW_ITEM" | bw encode | bw create item --session "$BW_SESSION" >/dev/null
  bw sync --session "$BW_SESSION" >/dev/null
  echo "✅ 存入完成！"
}

# --- 逻辑分发 ---
case "$1" in
add)
  add_pass
  ;;
*)
  search_pass
  ;;
esac
