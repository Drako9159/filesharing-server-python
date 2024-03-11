# Simple File Sharing Server

This project is a lightweight file-sharing server designed to share files from a local folder over a network. It also provides the functionality to upload files, making it a quick and easy solution for transferring files between devices.

## Features

- Share files from a local folder over the network.
- Upload files to the server for quick file transfers.

## Getting Started

### Prerequisites

Make sure you have [Flask](https://flask.palletsprojects.com/) installed. You can install it using:

```bash
pip install flask

```
### Running the Server

1. CLone the repository

```bash
git clone https://github.com/Drako9159/filesharing-server-python.git
```
2. Run the server

```bash
python server.py
```
4. Open your web browser and go to http://localhost:8080/ to access the file-sharing server

## Packaging the Application
If you want to package your application into a single executable, you can use PyInstaller.

1. Install pypinstaller

```bash
pip install pyinstaller
```

2. Package your application

```bash
pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" server.py
```

For a complete list of dependencies, refer to the requirements.txt file.

#### Additional Notes
- Make sure to customize the application to suit your specific needs.
Security considerations: This application is intended for local network use. If used in a public environment, consider implementing security measures such as authentication and encryption.
- Feel free to explore the code, modify it, and adapt it to your requirements! If you have any questions or suggestions, feel free to open an issue or contribute to the project.