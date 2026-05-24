return {
	{
		"xiyaowong/transparent.nvim",
		lazy = false, -- ⚠️ 重要：禁止懒加载，确保清理逻辑总是执行
		config = function()
			require("transparent").setup({
				-- 调整需要清除背景的组
				groups = {
					"Normal",
					"NormalNC",
					"Comment",
					"Constant",
					"Special",
					"Identifier",
					"Statement",
					"PreProc",
					"Type",
					"Underlined",
					"Todo",
					"String",
					"Function",
					"Conditional",
					"Repeat",
					"Operator",
					"Structure",
					"LineNr",
					"NonText",
					"SignColumn",
					"CursorLine",
					"CursorLineNr",
					"StatusLine",
					"StatusLineNC",
					"EndOfBuffer",
					"TelescopeBorder", -- 解决边框颜色
					"TelescopeNormal", -- 确保窗口主体透明
					"TelescopePreviewBorder",
					"TelescopePromptBorder",
					"TelescopeResultsBorder",
				},
				-- 清除特定插件（例如Telescope、Neo-tree、LazyGit）的额外背景组
				extra_groups = {
					"NormalFloat", -- 通用的浮动窗口
					"NeoTreeNormal", -- Neo-tree 文件树
					"NeoTreeNormalNC", -- Neo-tree 非活动窗口
					"TelescopeNormal", -- Telescope 查找窗口
					"LazyNormal", -- Lazy.nvim 插件管理界面
				},
			})
		end,
	},
}
