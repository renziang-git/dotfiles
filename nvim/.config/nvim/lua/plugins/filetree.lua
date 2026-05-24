return {
	{
		"nvim-neo-tree/neo-tree.nvim",
		branch = "v3.x",
		dependencies = {
			"nvim-lua/plenary.nvim",
			"nvim-tree/nvim-web-devicons",
			"MunifTanjim/nui.nvim",
		},
		keys = {
			{ "<leader>e", ":Neotree toggle<CR>", desc = "Toggle file tree" },
		},
		opts = {
			filesystem = {
				filtered_items = {
					visible = false,
					hide_dotfiles = false,
					hide_gitignored = true,
					hide_by_name = {
						".git",
						"node_modules",
						"__pycache__",
					},
				},
			},
		},
	},
}
