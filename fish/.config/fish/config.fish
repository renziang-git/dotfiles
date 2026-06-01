if status is-interactive
    # Commands to run in interactive sessions can go here
end


# Created by `pipx` on 2026-02-02 04:44:25

# npm 全局包的路径（注意是连字符 -，不是下划线 _）
set -gx PATH ~/.npm_global/bin $PATH

# 用户本地 bin
set -gx PATH ~/.local/bin $PATH

# DeepSeek API — 密钥在 conf.d/secrets.fish 中设置
# 端点与模型
set -x ANTHROPIC_BASE_URL https://api.deepseek.com/anthropic
set -x ANTHROPIC_MODEL deepseek-v4-pro

# Claude Code CLI 专用（可选保留）
set -x ANTHROPIC_DEFAULT_OPUS_MODEL deepseek-v4-pro
set -x ANTHROPIC_DEFAULT_SONNET_MODEL deepseek-v4-pro
set -x ANTHROPIC_DEFAULT_HAIKU_MODEL deepseek-v4-flash
set -x CLAUDE_CODE_SUBAGENT_MODEL deepseek-v4-flash
set -x CLAUDE_CODE_EFFORT_LEVEL max

# theme.sh configuration
if type -q theme.sh
	if test -e ~/.theme_history
	theme.sh (theme.sh -l|tail -n1)
	end
	# Optional
	# Bind C-o to the last theme.
	function last_theme
		theme.sh (theme.sh -l|tail -n2|head -n1)
	end
	bind \co last_theme
	alias th='theme.sh -i'
	# Interactively load a light theme
	alias thl='theme.sh --light -i'
	# Interactively load a dark theme
	alias thd='theme.sh --dark -i'
end

# 启用 Fish 的 vi 模式
fish_vi_key_bindings

# （可选）让你的提示符显示当前是 Normal 还是 Insert 模式
function fish_mode_prompt
  switch $fish_bind_mode
    case default
      echo -n 'N'
    case insert
      echo -n 'I'
    case visual
      echo -n 'V'
  end
end
