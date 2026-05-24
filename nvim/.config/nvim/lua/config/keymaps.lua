vim.keymap.set("n", "<leader>td", function()
	vim.o.background = "dark"
end, { desc = "Dark mode (moon)" })

vim.keymap.set("n", "<leader>tl", function()
	vim.o.background = "light"
end, { desc = "Light mode (day)" })

vim.keymap.set("n", "<leader>fm", function()
	require("conform").format()
end, { desc = "Format code" })

vim.keymap.set("n", "<leader>bd", "<cmd>bd<CR>", {
	desc = "Delete Buffer",
})

-- 搜索后取消高亮
vim.keymap.set("n", "<Esc>", "<cmd>nohlsearch<CR>", {
	desc = "Clear Search Highlight",
})

vim.keymap.set("n", "<leader>us", function()
	vim.opt.spell = not vim.opt.spell:get()
end, {
	desc = "Toggle Spell",
})

-- Insert 模式快捷鍵
-- ===================
-- 单词跳转（Alt + f/b）
vim.keymap.set("i", "<A-f>", "<S-Right>", { desc = "Word →" })
vim.keymap.set("i", "<A-b>", "<S-Left>", { desc = "Word ←" })

-- 行操作（Ctrl + Shift 组合，避免与默认冲突）
vim.keymap.set("i", "<C-A-d>", "<C-o>dd", { desc = "Delete line" }) -- Ctrl+Shift+d
vim.keymap.set("i", "<C-A-x>", "<C-o>cc", { desc = "Change line" }) -- Ctrl+Shift+x

-- ========== Alt 方向键：移动光标 ==========
-- Alt+h/j/k/l 对应 左/下/上/右
vim.keymap.set("i", "<A-h>", "<Left>", { desc = "←" })
vim.keymap.set("i", "<A-j>", "<Down>", { desc = "↓" })
vim.keymap.set("i", "<A-k>", "<Up>", { desc = "↑" })
vim.keymap.set("i", "<A-l>", "<Right>", { desc = "→" })

-- ========== Ctrl+Alt+hl：行首行尾 ==========
-- vim.keymap.set("i", "<C-A-h>", "<Home>", { desc = "行首" })
-- vim.keymap.set("i", "<C-A-l>", "<End>", { desc = "行尾" })

-- ========== Ctrl+Alt+jk：上下翻页 ==========
vim.keymap.set("i", "<C-A-f>", "<C-o><C-f>", { desc = "Page ↓" }) -- Ctrl+F 向下翻页
vim.keymap.set("i", "<C-A-b>", "<C-o><C-b>", { desc = "Page ↑" }) -- Ctrl+B 向上翻页

-- ========== Ctrl+Alt+u：撤销 ==========
vim.keymap.set("i", "<C-A-u>", "<C-o>u", { desc = "Undo" })

-- 额外：快速选择整行（类似 VSCode）
vim.keymap.set("i", "<C-l>", "<C-o>V", { desc = "Select line" }) -- Ctrl+l

-- Alt + h/j/k/l 控制方向（与普通模式一致）
vim.api.nvim_set_keymap("i", "<A-h>", "<Left>", { noremap = true, silent = true })
vim.api.nvim_set_keymap("i", "<A-j>", "<Down>", { noremap = true, silent = true })
vim.api.nvim_set_keymap("i", "<A-k>", "<Up>", { noremap = true, silent = true })
vim.api.nvim_set_keymap("i", "<A-l>", "<Right>", { noremap = true, silent = true })

-- Alt + f/b 前进/后退一个单词
vim.api.nvim_set_keymap("i", "<A-f>", "<S-Right>", { noremap = true, silent = true })
vim.api.nvim_set_keymap("i", "<A-b>", "<S-Left>", { noremap = true, silent = true })

-- Ctrl + d 删除整行（在 insert 模式下）
vim.api.nvim_set_keymap("i", "<C-d>", "<Esc>ddi", { noremap = true, silent = true })
-- 或者更精确的版本（先删除当前行再进入插入模式）
vim.api.nvim_set_keymap("i", "<C-d>", "<C-o>dd", { noremap = true, silent = true })

-- Alt + d/u 翻页（向后/向前）
vim.api.nvim_set_keymap("i", "<A-d>", "<C-d>", { noremap = true, silent = true })
vim.api.nvim_set_keymap("i", "<A-u>", "<C-u>", { noremap = true, silent = true })
