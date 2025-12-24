#!/usr/bin/env bash
HOST=127.0.0.1
PORT=8765
TIMEOUT=2

# 检查端口是否开放
echo "Testing AnkiConnect at $HOST:$PORT …"
if command -v nc &>/dev/null; then
  nc -z -w${TIMEOUT} $HOST $PORT
  OK=$?
elif [ -e /dev/tcp/$HOST/$PORT ]; then
  OK=0
else
  OK=1
fi

if [ $OK -eq 0 ]; then
  echo "✅ Port $PORT open — service reachable"
  # 可选：测试 HTTP 响应
  curl -sSf "http://$HOST:$PORT" &>/dev/null
  if [ $? -eq 0 ]; then
    echo "✅ HTTP OK — AnkiConnect seems alive"
  else
    echo "⚠️ Port open, but HTTP request failed"
  fi
else
  echo "❌ Port $PORT closed or unreachable"
fi

