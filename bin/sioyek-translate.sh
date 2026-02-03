#!/usr/bin/env bash

text="$(wl-paste)"
[ -z "$text" ] && exit 0

kitty \
  --config ~/.config/kitty/kitty.conf \
  --title "Translation" \
  sh -c "
echo '[ Original ]'
echo
echo \"$text\"
echo
echo '------------------------------'
echo
echo '[ Translation ]'
echo
trans -brief -no-ansi :zh \"$text\"
echo
echo '[ press q to close ]'
read -n 1
"
