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
				folder = "Inbox",
				date_format = "%Y-%m-%d",
			},
			new_notes_location = "Wiki",
			completion = {
				nvim_cmp = true,
				min_chars = 2,
			},
			mappings = {
				["gf"] = {
					action = function()
						return require("obsidian").util.gf_passthrough()
					end,
					opts = { noremap = false, expr = true, buffer = true },
				},
				["<cr>"] = {
					action = function()
						return require("obsidian").util.smart_action()
					end,
					opts = { buffer = true, expr = true },
				},
				["<leader>ch"] = {
					action = function()
						return require("obsidian").util.toggle_checkbox()
					end,
					opts = { buffer = true },
				},
				["<leader>os"] = {
					action = function() return require("obsidian").cmd.search() end,
					opts = { buffer = true },
				},
				["<leader>ot"] = {
					action = function() return require("obsidian").cmd.search_tags() end,
					opts = { buffer = true },
				},
				["<leader>on"] = {
					action = function() return require("obsidian").cmd.new() end,
					opts = { buffer = true },
				},
				["<leader>od"] = {
					action = function() return require("obsidian").cmd.dailies() end,
					opts = { buffer = true },
				},
				["<leader>op"] = {
					action = function() return require("obsidian").cmd.paste_img() end,
					opts = { buffer = true },
				},
				["<leader>ob"] = {
					action = function() return require("obsidian").cmd.backlinks() end,
					opts = { buffer = true },
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
