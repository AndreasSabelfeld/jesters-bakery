# Valheim Save Sync

A Python-based tool that detects changes to your Valheim world save files and automatically synchronizes them via Dropbox. This ensures that all shared users always have the latest world saves on their computers, allowing anyone to host the server without the need for a dedicated or paid server.

## Features

- **Automatic Detection**: Monitors Valheim save files for changes.
- **Dropbox Integration**: Uploads updated save files to Dropbox seamlessly.
- **Shared Access**: Downloads the latest save files for all shared users.

## Requirements

- Python 3.10 or higher (recommended)
- Dropbox account and API keys
- Valheim installed

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/valheim-save-sync.git
   cd valheim-save-sync
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the program:
   ```bash
   python __main__.py
   ```
2. The tool will automatically detect changes to Valheim save files and synchronize them across all shared users via Dropbox.

## How It Works

1. The program monitors the directory where Valheim save files are stored.
2. When a change is detected, the updated files are uploaded to a shared Dropbox folder.
3. Shared users automatically download the updated save files to their local computers on startup of Valheim.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.
