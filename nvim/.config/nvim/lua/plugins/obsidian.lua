return {
	{
		"epwalsh/obsidian.nvim",
		version = "*",
		lazy = true,
		ft = "markdown",
		dependencies = { "nvim-lua/plenary.nvim" },
		opts = {
			workspaces = {
				{ name = "obsidian", path = "~/obsidian" },
			},
			daily_notes = {
				folder = "00-Daily",
				date_format = "%Y-%m-%d",
			},
			completion = {
				nvim_cmp = true, -- 关键：禁用 nvim-cmp
				min_chars = 2,
			},
			-- Optional, configure key mappings. These are the defaults. If you don't want to set any keymappings this
			-- way then set 'mappings = {}'.
			mappings = {
				-- Overrides the 'gf' mapping to work on markdown/wiki links within your vault.
				["gf"] = {
					action = function()
						return require("obsidian").util.gf_passthrough()
					end,
					opts = { noremap = false, expr = true, buffer = true },
				},
				-- Toggle check-boxes.
				["<leader>ch"] = {
					action = function()
						return require("obsidian").util.toggle_checkbox()
					end,
					opts = { buffer = true },
				},
				-- Smart action depending on context, either follow link or toggle checkbox.
				["<cr>"] = {
					action = function()
						return require("obsidian").util.smart_action()
					end,
					opts = { buffer = true, expr = true },
				},
			},

			ui = {
				enable = true, -- 保留 UI 增强，但需配合 conceallevel
			},
		},
		-- 追加一个 config 函数来强制设置 conceallevel
		config = function(_, opts)
			require("obsidian").setup(opts)
			-- 针对 markdown 文件设置 conceallevel = 2
			vim.api.nvim_create_autocmd("FileType", {
				pattern = "markdown",
				callback = function()
					vim.opt_local.conceallevel = 2
				end,
			})
		end,
	},
}
