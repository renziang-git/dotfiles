return {
	{
		"karb94/neoscroll.nvim",
		event = "VeryLazy",
		opts = {
			easing_function = "quadratic", -- ✔ 顺滑但不晕
		},
	},
	{
		"petertriho/nvim-scrollbar",
		event = "VeryLazy",
		opts = {
			show = true,
			handle = {
				color = "#5c5c5c",
			},
		},
	},
	{
		"stevearc/conform.nvim",
		event = "BufWritePre",
		opts = {
			formatters_by_ft = {
				lua = { "stylua" },
				python = { "black" },
				markdown = { "prettier" },
			},
		},
		config = function(_, opts)
			require("conform").setup(opts)

			-- ⭐ 保存自动格式化
			vim.api.nvim_create_autocmd("BufWritePre", {
				pattern = "*",
				callback = function(args)
					require("conform").format({
						bufnr = args.buf,
						lsp_fallback = true,
					})
				end,
			})
		end,
	},
}
