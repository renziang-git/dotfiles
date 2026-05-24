-- 基础配置
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.termguicolors = true

vim.opt.modifiable = true

vim.opt.spelllang = { "en" }

vim.opt.undofile = true
vim.opt.undodir = vim.fn.stdpath("data") .. "/undo"

vim.opt.clipboard = "unnamedplus"

-- 启用智能缩进
vim.opt.smartindent = true
vim.opt.autoindent = true

-- tab 设置
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.expandtab = true

-- 动效
-- vim.o.lazyredraw = true
--

-- 进入命令行模式时启用大小写不敏感
vim.api.nvim_create_autocmd("CmdlineEnter", {
	pattern = "[:/>?]",
	command = "set ignorecase",
})

-- 离开命令行模式时恢复大小写敏感
vim.api.nvim_create_autocmd("CmdlineLeave", {
	pattern = "[:/>?]",
	command = "set noignorecase",
})
