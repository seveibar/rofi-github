# Search Github Repos with Rofi

This is a simple script to search Github repos using Rofi. It uses the Github
API to search for repos and then opens the repo in your browser.

## Installation

## Development

Run `./test.sh` to automatically start rofi with `main.py`

## Adding to i3

1.Install `rofi_menu` globally with `pip install rofi_menu`

2. Add the following line to your i3 config

```
bindsym $mod+g exec --no-startup-id rofi -modi "github-repo-search:/path/to/rofi-github/rofi_github/main.py" -show "github-repo-search"
```
