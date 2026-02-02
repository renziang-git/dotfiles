-- bootstrap lazy.nvim, LazyVim and your plugins
require("config.lazy")

local notifier = require("utils.notify").detect()

if notifier ~= "none" then
  vim.notify("Hello from nvim")
end

vim.opt.wrap = true
