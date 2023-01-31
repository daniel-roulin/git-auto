from installer import install_if_missing
install_if_missing("requests", "GitPython")

import os
from auth import login
from git import Repo

TOKEN_PATH = os.path.join(os.path.dirname(__file__), "token.txt")

if os.path.exists(TOKEN_PATH):
    with open(TOKEN_PATH, "r") as f:
        token = f.read()
else:
    token = login()
    with open(TOKEN_PATH, "w") as f:
        f.write(token)
    
print(f"git clone https://{token}@github.com/DanielRoulin/Trusk.git")

repo = Repo(os.getcwd())
git = repo.git
while True:
    print()
    answer = input("Your command: git ")
    words = answer.split()
    command = words[0]
    args = words[1:]
    try:
        command = getattr(git, command)
        command(*args)
    except Exception as e:
        print(e)
