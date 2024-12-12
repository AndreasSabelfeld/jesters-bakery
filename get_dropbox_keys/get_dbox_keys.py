import webbrowser
import base64
import requests
import json

APP_KEY = '<APP_KEY>'
APP_SECRET = '<APP_SECRET>'

url = f'https://www.dropbox.com/oauth2/authorize?client_id={APP_KEY}&' \
      f'response_type=code&token_access_type=offline'

webbrowser.open(url)

ACCESS_CODE_GENERATED = input("Enter the generated Access Token: ")

BASIC_AUTH = base64.b64encode(f'{APP_KEY}:{APP_SECRET}'.encode())

headers = {
    'Authorization': f"Basic {BASIC_AUTH}",
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = f'code={ACCESS_CODE_GENERATED}&grant_type=authorization_code'

response = requests.post('https://api.dropboxapi.com/oauth2/token',
                         data=data,
                         auth=(APP_KEY, APP_SECRET))
print(json.dumps(json.loads(response.text), indent=2))