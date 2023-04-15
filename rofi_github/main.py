#!/usr/bin/env python3

import sys
import requests
import os
import webbrowser
import rofi_menu
import sys

log_file = "/tmp/rofi_github.log"


def debug_print(*args, **kwargs):
    with open(log_file, "a") as f:
        print(*args, **kwargs, file=f)


# Replace with your GitHub username and personal access token
usernames = ["seveibar", "seamapi"]
TOKEN = os.environ["GITHUB_TOKEN"]


def list_repos():
    all_repos = []
    for username in usernames:
        page = 1
        while True:
            url = f"https://api.github.com/users/{username}/repos"
            headers = {"Authorization": f"Bearer {TOKEN}"}
            params = {"per_page": 100, "page": page}
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                repos = response.json()
                if not repos:
                    break  # No more repos to fetch
                all_repos.extend(repos)
                page += 1  # Move to the next page
            else:
                raise Exception(
                    f"Failed to fetch repos for {username}: {response.status_code} - {response.text}"
                )

    return all_repos


debug_print(list_repos())

repo_items = [
    rofi_menu.ShellItem(repo["full_name"], f"echo {repo['name']}")
    for repo in list_repos()
]

main_menu = rofi_menu.Menu(
    prompt="menu",
    items=[
        rofi_menu.ShellItem("Set Github Token", "echo 'project 1'"),
        rofi_menu.ShellItem("Refresh Repos", "echo 'project 1'")
        # OutputSomeTextItem("Output anything"),
        # DoAndExitItem("Do something and exit"),
        # CurrentDatetimeItem(),
        # CounterItem(),
        # CounterItem(),
        # rofi_menu.NestedMenu("User input", HandleUserInputMenu()),
    ]
    + repo_items,
)


if __name__ == "__main__":
    rofi_menu.run(main_menu)
# if __name__ == "__main__":
#     menu = GitHubRepoSearchMenu()
#     rofi_menu.run(menu, rofi_version="1.7")
