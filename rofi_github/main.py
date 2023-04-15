#!/usr/bin/env python3

import sys
import requests
import os
import webbrowser
import rofi_menu
import sys
import shelve

log_file = "/tmp/rofi_github.log"


def debug_print(*args, **kwargs):
    with open(log_file, "a") as f:
        print(*args, **kwargs, file=f)


usernames = ["seveibar", "seamapi"]
TOKEN = os.environ["GITHUB_TOKEN"]

cache = shelve.open("github_rofi_settings")


def get_cached_repos():
    repos = cache.get("repos")
    if repos is None:
        return []
    return repos


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
    cache["repos"] = all_repos

    return all_repos


class UpdateRepoItem(rofi_menu.Item):
    async def on_select(self, meta):
        debug_print("updating repos")
        list_repos()


repo_items = [
    rofi_menu.ShellItem(repo["full_name"], f"echo {repo['name']}")
    for repo in get_cached_repos()
]

main_menu = rofi_menu.Menu(
    prompt="menu",
    items=[
        UpdateRepoItem("Set Github Token"),
        UpdateRepoItem("Refresh Repos"),
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
    cache.close()
