from installer import install_if_missing
install_if_missing("requests", "GitPython")

import os
from auth import auth_url
from git import Repo


while True:
    answer = input("Your command: git ")
    words = answer.split()
    command = words[0]
    args = words[1:]

    if command == "init":
        if len(args) >= 1:
            repo_dir = args[0] 
        else:
            repo_dir = os.getcwd()
        Repo.init(repo_dir)
    elif command == "clone":
        if len(args) < 2:
            print("Missing parameters!")
            exit()
        git_url = auth_url(args[0])
        repo_dir = args[1]
        Repo.clone_from(git_url, repo_dir)
