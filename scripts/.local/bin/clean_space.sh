#!/bin/bash

# 定义需要清理的目录（这些目录删了不影响登录，不影响程序运行）
# 格式：描述|路径
TARGETS=(
  "Chrome 缓存|/home/r.za/.cache/google-chrome"
  "Qutebrowser 缓存|/home/r.za/.cache/qutebrowser"
  "Neovim 缓存|/home/r.za/.cache/nvim"
  "Pip 下载缓存|/home/r.za/.cache/pip"
  "Go 编译缓存|/home/r.za/.cache/go-build"
  "Mesa GPU 着色器缓存|/home/r.za/.cache/mesa_shader_cache"
  "Steam 残留数据|/home/r.za/.local/share/umu"
  "已删除软件的 Anki 残留|/home/r.za/.local/share/Anki2"
)

echo "--- 开始清理安全缓存 ---"

for item in "${TARGETS[@]}"; do
  desc="${item%%|*}"
  path="${item#*|}"

  if [ -d "$path" ]; then
    echo "[找到] $desc: $path"
    # 使用 -rf 删除目录下所有内容，但保留目录本身（可选，这里直接删除目录也行，程序会自动创建）
    rm -rf "$path"/* 2>/dev/null
    echo "      已清空。"
  else
    echo "[跳过] $desc: 路径不存在"
  fi
done

# 清理 Flatpak 无用运行时 (需要 sudo 或当前用户权限)
if command -v flatpak &>/dev/null; then
  echo "[正在清理] 未使用的 Flatpak 运行时..."
  flatpak uninstall --unused -y
fi

# 清理 Pacman 孤立依赖 (需要 sudo)
if command -v pacman &>/dev/null; then
  echo "[正在清理] Pacman 孤立依赖..."
  sudo pacman -Rs $(pacman -Qtdq) --noconfirm 2>/dev/null || echo "      没有可清理的孤立依赖。"
fi

echo "--- 清理完成！ ---"
