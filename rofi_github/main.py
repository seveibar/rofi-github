#!/usr/bin/env python3

import sys
import requests
import os
import webbrowser
import rofi_menu
import sys
import shelve
import pathlib

log_file = "/tmp/rofi_github.log"
cwd = pathlib.Path(__file__).parent.absolute()


def debug_print(*args, **kwargs):
    with open(log_file, "a") as f:
        print(*args, **kwargs, file=f)


cache = shelve.open(f"{cwd}/github_rofi_settings")

usernames = cache.get("orgs") or []
TOKEN = cache.get("github_token") or os.environ["GITHUB_TOKEN"]


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
        return rofi_menu.Operation(rofi_menu.OP_EXIT)


# class SetGithubToken(rofi_menu.Item):
#     async def on_select(self, meta):
#         debug_print("setting token")

#         return rofi_menu.Operation(rofi_menu.OP_EXIT)


class SetGithubToken(rofi_menu.Menu):
    allow_user_input = True

    class CustomItem(rofi_menu.Item):
        async def render(self, meta):
            entered_text = meta.session.get("text", "[ no text ]")
            return f"You entered: {entered_text}"

    items = [CustomItem()]

    async def on_user_input(self, meta):
        meta.session["text"] = meta.user_input
        cache["github_token"] = meta.user_input
        return rofi_menu.Operation(rofi_menu.OP_EXIT)


class SetOrgs(rofi_menu.Menu):
    allow_user_input = True

    class CustomItem(rofi_menu.Item):
        async def render(self, meta):
            entered_text = meta.session.get("text", "[ no text ]")
            return f"You entered: {entered_text}"

    items = [CustomItem()]

    async def on_user_input(self, meta):
        meta.session["text"] = meta.user_input
        cache["orgs"] = meta.user_input.split(",")
        return rofi_menu.Operation(rofi_menu.OP_EXIT)


repo_items = [
    rofi_menu.ShellItem(repo["full_name"], f"echo {repo['name']}")
    for repo in get_cached_repos()
]

main_menu = rofi_menu.Menu(
    prompt="menu",
    items=[
        rofi_menu.NestedMenu("Set Github Token", SetGithubToken("Github Token")),
        rofi_menu.NestedMenu("Set Orgs", SetOrgs("Orgs (comma separated)")),
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
