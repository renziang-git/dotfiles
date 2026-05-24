return {
	{ "nvim-lua/plenary.nvim" },

	-- which-key
	{
		"folke/which-key.nvim",
		event = "VeryLazy",
		opts = {
			spec = {
				{ "<leader>a", group = "Avante AI" },
				{ "<leader>f", group = "Find/Search" },
				{ "<leader>t", group = "Theme" },
			},
		},
	},
	{
		"folke/snacks.nvim",
		priority = 1000,
		lazy = false,
		opts = {
			input = { enabled = true },
		},
	},
	{
		"folke/noice.nvim",
		event = "VeryLazy",
		dependencies = {
			"MunifTanjim/nui.nvim",
			-- 完全不要 nvim-notify
		},
		opts = {
			cmdline = {
				view = "cmdline_popup",
			},
			notify = {
				view = "mini", -- 使用 noice 内置的 mini 视图
				timeout = 3000,
			},
			presets = {
				lsp_doc_border = true,
			},
			-- ========== 新增：调整命令行弹窗位置到顶部 ==========
			views = {
				cmdline_popup = {
					position = {
						row = 1, -- 顶部（从1开始计数）
						col = "50%", -- 水平居中，也可以写 0（最左）或 "100%"
					},
					-- 可选：让弹窗宽度占满屏幕
					size = {
						width = "100%",
						height = "auto",
					},
				},
			},
		},
	},
	{
		"catppuccin/nvim",
		name = "catppuccin",
		lazy = false,
		priority = 1000,
		opts = {
			flavour = "mocha", -- 默认深色
			transparent_background = true,
			-- 关键：根据 flavor 覆盖颜色
			overrides = function(flavour)
				if flavour == "latte" then
					return {
						Normal = { fg = "#000000", bg = "none" }, -- 亮色模式下强制纯黑文字
						NormalNC = { fg = "#000000", bg = "none" }, -- 非活动窗口也黑色
					}
				else
					return {}
				end
			end,
		},
		config = function(_, opts)
			require("catppuccin").setup(opts)
			vim.cmd.colorscheme("catppuccin")
		end,
	},

	-- {
	-- 	"folke/tokyonight.nvim",
	-- 	lazy = false, -- ⭐ 关键：启动就加载
	-- 	priority = 1000, -- ⭐ 让它最先加载
	-- 	config = function()
	-- 		require("tokyonight").setup({
	-- 			style = "moon", -- storm / moon / night / day
	-- 		})
	-- 		vim.cmd.colorscheme("tokyonight")
	-- 	end,
	-- },
	{
		"RRethy/base16-nvim",
		lazy = false,
		priority = 1000,
	},
}
