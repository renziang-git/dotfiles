return {
	{ "williamboman/mason.nvim", opts = {} },

	{
		"neovim/nvim-lspconfig",
		config = function()
			local servers = { "pyright", "lua_ls", "marksman" }
			for _, server in ipairs(servers) do
				vim.lsp.config(server, {})
				vim.lsp.enable(server)
			end
			vim.lsp.config("lua_ls", {
				settings = {
					Lua = {
						diagnostics = { globals = { "vim" } },
					},
				},
			})
		end,
	},

	-- nvim-cmp 补全引擎
	{
		"hrsh7th/nvim-cmp",
		dependencies = {
			"hrsh7th/cmp-nvim-lsp", -- LSP 补全源
			"hrsh7th/cmp-buffer", -- 缓冲区补全源
			"hrsh7th/cmp-path", -- 路径补全源
			"L3MON4D3/LuaSnip", -- 代码片段引擎
			"saadparwaiz1/cmp_luasnip", -- 片段补全源
			"onsails/lspkind.nvim", -- 图标美化
		},
		config = function()
			local cmp = require("cmp")
			local luasnip = require("luasnip")

			cmp.setup({
				-- 代码片段支持
				snippet = {
					expand = function(args)
						luasnip.lsp_expand(args.body)
					end,
				},

				-- 补全来源
				sources = cmp.config.sources({
					{ name = "nvim_lsp" }, -- LSP 补全
					{ name = "luasnip" }, -- 代码片段
				}, {
					{ name = "buffer" }, -- 当前缓冲区
					{ name = "path" }, -- 文件路径
				}),

				-- 快捷键映射
				mapping = cmp.mapping.preset.insert({
					-- 确认补全
					["<CR>"] = cmp.mapping.confirm({ select = true }),
					-- 上下选择
					["<C-j>"] = cmp.mapping.select_next_item(),
					["<C-k>"] = cmp.mapping.select_prev_item(),
					-- 滚动文档
					["<C-d>"] = cmp.mapping.scroll_docs(-4),
					["<C-f>"] = cmp.mapping.scroll_docs(4),
					-- 取消补全
					["<C-e>"] = cmp.mapping.abort(),
					-- 手动触发补全
					["<C-Space>"] = cmp.mapping.complete(),
				}),

				-- 补全窗口样式
				window = {
					completion = cmp.config.window.bordered(),
					documentation = cmp.config.window.bordered(),
				},

				-- 补全行为
				formatting = {
					format = require("lspkind").cmp_format({
						mode = "symbol",
						maxwidth = 50,
					}),
				},

				-- 实验性功能
				experimental = {
					ghost_text = true, -- 幽灵文本提示
				},
			})
		end,
	},

	-- 可选：提供图标（需要安装 lspkind-nvim）
	-- {
	--   "onsails/lspkind.nvim",
	--   event = "VeryLazy",
	-- },

	-- Copilot（如果需要）
	-- {
	-- 	"zbirenbaum/copilot.lua",
	-- 	cmd = "Copilot",
	-- 	event = "InsertEnter",
	-- 	opts = {
	-- 		suggestion = { enabled = true, auto_trigger = true, keymap = { accept = "<Tab>" } },
	-- 		panel = { enabled = false },
	-- 	},
	-- },
}
