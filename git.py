import sys
from io import BytesIO
import zipfile
import os
from urllib.parse import urlparse
import webbrowser
import time
import subprocess

DATA_PATH = "J:\git-data"
MODULES_PATH = os.path.join(DATA_PATH, "pymodules")
TOKEN_PATH = os.path.join(DATA_PATH, "token.txt")
GIT_EXE_PATH = os.path.join(DATA_PATH, "git-exe\cmd\git.exe")
def main():
    # Install modules + download git + auth
    if not os.path.exists(DATA_PATH):
        os.mkdir(DATA_PATH)
        install_modules("requests")
        
        global requests
        import requests
        download_git()
        
        with open(TOKEN_PATH, "w") as f:
            f.write(get_token())
            
    with open(TOKEN_PATH, "r") as f:
        token = f.read()
            
    command = sys.argv[0]
    if command == "sync":
        message = input("Commit message: ")
        git(["add", "."])
        git(["commit", "-m", message])
        git(["push"])
    elif command == "publish":
        git(["init"])
        git(["branch" "-M" "main"])
        repo_name = input("Repository name: ")
        is_private = input("Public repo? [y/n] ") != "y"
        create_repo(repo_name, is_private)
        git(["remote", "add", "origin", https://github.com/DanielRoulin/Test-of-the-API.git])
        git(["push", "-u", "origin", "main"])
    
    
def create_repo(name, private):
    # set the authentication header
    headers = {
        "Authorization": f"token {token}"
    }

    # set the request body
    data = {
        "name": name,
        "private": private,
    }

    # make the POST request to create the new repository
    response = requests.post("https://api.github.com/user/repos", headers=headers, json=data)

    # check the response status code
    if response.status_code == 201:
        print("Repository created successfully")
    else:
        print("Error creating repository:", response.json()["message"])
        exit()
        
    return response.json()["clone_url"]

def git(args):
    # Auth + Execute command
    args_quoted = []
    for arg in args:
        if arg.startswith("https:") or arg.startswith("http:"):
            arg = auth_url(arg)
        if " " in arg:
            arg = '"' + arg + '"'
        args_quoted.append(word)
    full_command = f"{GIT_EXE_PATH} {' '.join(args_quoted)}"
    print(f"Executing command: {full_command}")
    os.system(full_command)
    
def get_token():
    CLIENT_ID = "6cc55721e136b29c9d0f"
    SCOPE = "repo"
    GRANT_TYPE = "urn:ietf:params:oauth:grant-type:device_code"
    params = {
        "client_id": CLIENT_ID,
        "scope": SCOPE,
    }
    headers = {
        "Accept": "application/json",
    }
    r = requests.post("https://github.com/login/device/code", data=params, headers=headers)
    data = r.json()
    print(f'Your verification code: {data["user_code"]}')
    webbrowser.open(data["verification_uri"])
    params = {
        "client_id": CLIENT_ID,
        "device_code": data["device_code"],
        "grant_type": GRANT_TYPE
    }
    headers = {
        "Accept": "application/json",
    }
    while True:
        r = requests.post("https://github.com/login/oauth/access_token", data=params, headers=headers)
        data_token = r.json()
        if "error" in data_token:
            if data_token["error"] == "authorization_pending":  
                time.sleep(data["interval"])
                continue
            else:
                print(f"Error: {data_token}")
        else:
            return data_token["access_token"] 

def auth_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{token}@{parsed.netloc}/{parsed.path}"
        
def install_modules(*modules):
    sys.path.append(MODULES_PATH)
    print("Installing modules: " +  ", ".join(modules))
    subprocess.check_call(['pip', 'install', '--target=' + MODULES_PATH, *modules])
    print("Installed modules: " +  ", ".join(modules))

def progress(completion):
    sys.stdout.write(f"\r[{round(50*completion) * '='}>{round(50*(1-completion)) * '.'}] {round(completion * 100)}% ")
    sys.stdout.flush()

def download_git():
    url = 'https://github.com/DanielRoulin/git-auto/releases/download/latest/git-exe.zip'   
    print("Downloading file...")
    with requests.get(url, stream=True) as r:
        with BytesIO() as f:
            total_size = int(r.headers.get('Content-Length'))
            chunk_size = 10_000_000 # 10MB 
            for i, chunk in enumerate(r.iter_content(chunk_size=chunk_size)):
                c = i * chunk_size / total_size
                progress(c)
                f.write(chunk)
            progress(1)
            print('Download completed')
            
            print("Extracting file...")
            with zipfile.ZipFile(f) as zf:
                filesList = zf.namelist()
                for idx, file in enumerate(filesList):
                    c = idx / len(filesList)
                    progress(c)
                    zf.extract(file, DATA_PATH)
                zf.close()
            progress(1)
            print("Extraction completed")

if __name__ == "__main__":
    main()
