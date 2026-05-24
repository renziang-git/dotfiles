#!/usr/bin/env bash
set -euo pipefail

format_gib() {
  local bytes=$1
  awk -v value="$bytes" 'BEGIN { printf "%.1fG", value / 1024 / 1024 / 1024 }'
}

cpu_usage() {
  local user nice system idle iowait irq softirq steal
  read -r _ user nice system idle iowait irq softirq steal _ _ < /proc/stat
  local idle1=$((idle + iowait))
  local total1=$((user + nice + system + idle + iowait + irq + softirq + steal))

  sleep 0.1

  read -r _ user nice system idle iowait irq softirq steal _ _ < /proc/stat
  local idle2=$((idle + iowait))
  local total2=$((user + nice + system + idle + iowait + irq + softirq + steal))

  local totald=$((total2 - total1))
  local idled=$((idle2 - idle1))
  if ((totald == 0)); then
    echo 0
    return
  fi

  echo $(((100 * (totald - idled) + totald / 2) / totald))
}

memory_usage() {
  local used total
  used=$(free -b | awk '/Mem:/ {print $3}')
  total=$(free -b | awk '/Mem:/ {print $2}')
  printf '%s %s' "$(format_gib "$used")" "$(format_gib "$total")"
}

disk_usage() {
  df -P / | awk 'NR==2 {gsub(/%/, "", $5); print $5}'
}

pango_block() {
  local text=$1
  local fg=$2
  local bg=$3
  printf '<span foreground="%s" background="%s"> %s </span>' "$fg" "$bg" "$text"
}

polybar_prefix_fg="#2E3440"
polybar_prefix_bg="#FFFFFF"
polybar_value_bg="#3B4252"
polybar_green="#A3BE8C"
polybar_yellow="#EBCB8B"
polybar_orange="#D08770"
polybar_red="#BF616A"

cpu_color() {
  local usage=$1
  if ((usage >= 80)); then
    echo "$polybar_red"
  elif ((usage >= 50)); then
    echo "$polybar_orange"
  else
    echo "$polybar_green"
  fi
}

case "${1:-}" in
  cpu)
    usage=$(cpu_usage)
    value_color=$(cpu_color "$usage")
    text="$(pango_block "C" "$polybar_prefix_fg" "$polybar_prefix_bg")$(pango_block "${usage}%" "$value_color" "$polybar_value_bg")"
    printf '{"text":"%s","tooltip":"CPU: %s%%"}\n' "$text" "$usage"
    ;;
  mem)
    read -r used total <<< "$(memory_usage)"
}
    text="$(pango_block "R" "$polybar_prefix_fg" "$polybar_prefix_bg")$(pango_block "${used}" "$polybar_green" "$polybar_value_bg")"
    printf '{"text":"%s","tooltip":"Mem: %s / %s"}\n' "$text" "$used" "$total"
    ;;
  disk)
    usage=$(disk_usage)
    text="$(pango_block "D" "$polybar_prefix_fg" "$polybar_prefix_bg")$(pango_block "${usage}%" "$polybar_yellow" "$polybar_value_bg")"
    printf '{"text":"%s","tooltip":"Disk: %s%% used"}\n' "$text" "$usage"
    ;;
  *)
    printf '{"text":"N/A","tooltip":"Unknown stat"}\n'
    ;;
esac
