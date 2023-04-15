#!/bin/sh

script_path="$(dirname "$(readlink -f "$0")")"

rm -f /tmp/rofi_github.log
touch /tmp/rofi_github.log
tail -f /tmp/rofi_github.log &

rofi -modi "github-repo-search:$script_path/rofi_github/main.py" -show "github-repo-search"
