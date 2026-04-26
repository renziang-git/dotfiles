#!/usr/bin/env bash
# 自動根據窗口寬高切換 split 方向

# 獲取當前聚焦窗口寬高
get_window_size() {
    # 輸出格式：Window 12345678 geometry 800x600+0+0
    OUTPUT=$(xdotool getwindowfocus getwindowgeometry)
    if [[ $OUTPUT =~ ([0-9]+)x([0-9]+) ]]; then
        WIDTH="${BASH_REMATCH[1]}"
        HEIGHT="${BASH_REMATCH[2]}"
        echo "$WIDTH $HEIGHT"
    fi
}

update_split() {
    read WIDTH HEIGHT < <(get_window_size)
    if (( WIDTH > HEIGHT )); then
        i3-msg split h
    else
        i3-msg split v
    fi
}

# 監聽 i3 窗口事件（通過 i3-msg subscribe）比 while read 更穩
i3-msg -t subscribe '[ "window" ]' | while read -r line; do
    # 判斷是新建窗口事件
    if echo "$line" | grep -q '"change":"new"'; then
        update_split
    fi
done

