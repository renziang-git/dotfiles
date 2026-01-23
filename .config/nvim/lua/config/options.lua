-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here

-- 设置 Neovim 网络代理 (适配 v2raya)
vim.env.http_proxy = "http://127.0.0.1:20171"
vim.env.https_proxy = "http://127.0.0.1:20171"

-- 关键修正：变量名是 no_proxy，且值里不要带 http://
-- 这一行能救命，防止 Codeium 的本地心跳包被代理拦截
vim.env.no_proxy = "localhost,127.0.0.1"
