# Valheim Save Sync

A Python-based tool that detects changes to your Valheim world save files and automatically synchronizes them via Dropbox. This ensures that all shared users always have the latest world saves on their computers, allowing anyone to host the server without the need for a dedicated or paid server.

## Features

- **Automatic Detection**: Monitors Valheim save files for changes.
- **Dropbox Integration**: Uploads updated save files to Dropbox seamlessly.
- **Shared Access**: Downloads the latest save files for all shared users.

## Requirements

- Python 3.10 or higher (recommended)
- Dropbox account and API keys (follow the [HOW_TO_GET_KEYS](get_dropbox_keys\HOW_TO_GET_KEYS.md) file under `*\get_dropbox_keys\`!)
- Have Valheim installed

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/valheim-save-sync.git
   cd valheim-save-sync
   ```
2. Run the installer file:
   ```bash
   installer.bat
   ```
3. A file will be created inside the working directory and a shortcut is being made to the desktop.

## Usage

1. Start the program:
   ```bash
   python __main__.py
   ```
   Or run the created executables:
   ```bash
   valheim-sync.exe
   ```
2. The tool will automatically detect changes to the local Valheim save files and synchronize them across all shared users via Dropbox.

## How It Works

1. The program monitors the directory where the lcoal Valheim save files are stored.
2. When a change is detected, the updated files are uploaded to a shared Dropbox folder.
3. Shared users automatically download the updated save files to their local computers on startup of Valheim.
4. This only works with the local world save files. So in order for the worlds to be uploaded, you need to save them locally

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.
