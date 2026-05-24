return {
	{
		"nvim-treesitter/nvim-treesitter",
		build = ":TSUpdate",

		-- ⭐ 提前执行（安全）
		init = function()
			require("nvim-treesitter.install").compilers = { "gcc" }
		end,

		-- ⭐ 让 lazy 自动调用 setup（关键）
		opts = {
			ensure_installed = { "lua", "python", "markdown", "bash" },
			highlight = { enable = true },
			indent = { enable = true },
		},
	},
}
