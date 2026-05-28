#!/bin/sh

fuzzel \
  --dmenu \
  --prompt "Vim Hotkeys > " \
  < /home/r.za/bin/show_vim_config/vim_hotkey.txt \
  > /dev/null

