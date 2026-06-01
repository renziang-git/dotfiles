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
					opts = { buffer = true, desc = "切换复选框" },
				},
				["<leader>os"] = {
					action = function() vim.cmd("ObsidianSearch") end,
					opts = { buffer = true, desc = "搜索笔记" },
				},
				["<leader>ot"] = {
					action = function() vim.cmd("ObsidianTags") end,
					opts = { buffer = true, desc = "搜索标签" },
				},
				["<leader>on"] = {
					action = function() vim.cmd("ObsidianNew") end,
					opts = { buffer = true, desc = "新建笔记" },
				},
				["<leader>od"] = {
					action = function() vim.cmd("ObsidianDailies") end,
					opts = { buffer = true, desc = "今日日记" },
				},
				["<leader>op"] = {
					action = function() vim.cmd("ObsidianPasteImg") end,
					opts = { buffer = true, desc = "粘贴图片" },
				},
				["<leader>ob"] = {
					action = function() vim.cmd("ObsidianBacklinks") end,
					opts = { buffer = true, desc = "反向链接" },
				},
			},
			ui = {
				enable = true,
			},
		},
		config = function(_, opts)
			require("obsidian").setup(opts)
			vim.api.nvim_create_autocmd("FileType", {
				pattern = "markdown",
				callback = function()
					vim.opt_local.conceallevel = 2
					-- 注册 which-key 标签
					local wk_ok, wk = pcall(require, "which-key")
					if wk_ok then
						wk.add({
							{ "<leader>o",  group = "+obsidian" },
							{ "<leader>on", desc = "新建笔记" },
							{ "<leader>os", desc = "搜索笔记" },
							{ "<leader>ot", desc = "搜索标签" },
							{ "<leader>od", desc = "今日日记" },
							{ "<leader>ob", desc = "反向链接" },
							{ "<leader>op", desc = "粘贴图片" },
						})
					end
				end,
			})
		end,
	},
}
