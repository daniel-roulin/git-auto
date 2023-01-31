import requests
import webbrowser
import time

CLIENT_ID = "6cc55721e136b29c9d0f"
SCOPE = "repo"
GRANT_TYPE = "urn:ietf:params:oauth:grant-type:device_code"

def login():
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