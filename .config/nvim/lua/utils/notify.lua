local M = {}

local function is_running(cmd)
	return vim.fn.system("pgrep -x " .. cmd) ~= ""
end

function M.detect()
	if is_running("mako") then
		return "mako"
	elseif is_running("dunst") then
		return "dunst"
	else
		return "none"
	end
end

return M
