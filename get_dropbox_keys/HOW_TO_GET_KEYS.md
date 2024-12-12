# How to Obtain and Use Keys for Dropbox API

This guide walks you through the process of generating a refresh token and using it to acquire short-lived access tokens for the Dropbox API, based on helpful explanations found on Stack Overflow.

---

## Steps to Generate a Refresh Token

### 1. Log in into your Dropbox Account and create an App:
1. Visit this URL: https://www.dropbox.com/developers/apps/create
2. Choose `Scoped Access`
3. Choose `App Folder - Access to a single folder created specifically for your app.`
4. Name the App: `valheim-sync`

### 2. Change the app permissions:
1. Visit your app: https://www.dropbox.com/developers/apps?_tk=pilot_lp&_ad=topbar4&_camp=myapps
2. Under `Permissions` tick: `files.metadata.write`, `files.metadata.read`, `files.content.write` and `files.content.read`

### 3. Generate an Authorization Code
1. Replace `<APP_KEY>` in the `get_dbox_keys.py` with the Key under `Settings`
2. Replace `<APP_SECRET>` in the `get_dbox_keys.py` with the Secret under `Settings`
3. Run the `get_dbox_keys.py` script
3. Input the generated access code to the input field

### 4. Enter the credentials to the `.env` file:
```env
WORLD_NAME = "[Enter Your World Name Here]"
ACCESS_TOKEN = "#####"
APP_KEY = "#####"
APP_SECRET = "#####"
REFRESH_TOKEN = "#####"
```