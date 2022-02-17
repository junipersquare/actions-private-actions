import argparse
import dataclasses
import json
import os
import re
import subprocess
import sys
import typing


# REQUIRED_ORGANIZATION = "junipersquare"


@dataclasses.dataclass
class Repo:
    owner: str
    name: str
    ref: str


@dataclasses.dataclass
class Config:
    repos: typing.List[Repo]
    checkout_path: str
    token: str


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("repos")
    parser.add_argument("checkout_path")
    parser.add_argument("token")

    parsed = parser.parse_args()

    try:
        repos_list = [parse_repo(x) for x in json.loads(parsed.repos)]
        # This isn't necessarily a list of strings at this point but it's not
        # really worth pulling in more validation.  Just fail.
    except json.JSONDecodeError:
        raise Exception("Invalid value for repo-list")

    return Config(
        repos=repos_list, checkout_path=parsed.checkout_path, token=parsed.token
    )


def parse_repo(repo_name: str) -> Repo:
    match = re.match(f"^(?P<org>.+)\\/(?P<repo>.+)@(?P<ref>.+)$", repo_name)

    if not match:
        raise Exception(f"Invalid repo '{repo_name}'.  Is the @ref included?")

    organization = match.group("org")

    if False:
        if organization != REQUIRED_ORGANIZATION:
            raise Exception(
                f"Invalid organization for '{repo_name}': Only actions from the {REQUIRED_ORGANIZATION} org are allowed."
            )

    return Repo(match.group("org"), match.group("repo"), match.group("ref"))


def checkout_repo(repo: Repo, path: str, token: str):
    clone_url = f"https://{token}@github.com/{repo.owner}/{repo.name}.git"
    clone_dir = os.path.join(path, repo.name)
    subprocess.check_call(
        [
            "git",
            "clone",
            "--depth=1",
            "--single-branch",
            "--branch",
            repo.ref,
            clone_url,
            clone_dir,
        ],
        shell=False,
        stdout=subprocess.DEVNULL,
    )


def main():
    try:
        config = parse_arguments()

        for repo in config.repos:
            checkout_repo(repo, config.checkout_path, config.token)
    except Exception as exc:
        print(f"::error::{exc}")
        sys.exit(1)
