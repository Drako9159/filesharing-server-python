from flask import Flask, send_from_directory, render_template, request, redirect, url_for
from flask_compress import Compress
import os
import sys
import socket
import logging
from waitress import serve


def get_file_info():

    """
    Retrieves information about files in the current directory.

    Returns:
        list: A list of tuples containing the filename and size in KB.
    """
    # Old code
    """
    file_info = []
    for filename in os.listdir("."):
        filepath = os.path.join(".", filename)
        if os.path.isfile(filepath) and "server" not in filename.lower():
            size = os.path.getsize(filepath)
            size_str = f"{size / 1024:.2f} KB"
            file_info.append((filename, size_str))
    return file_info
    """
    # New code
    file_info = [
        (f, f"{os.path.getsize(f) / 1024:.2f} KB")
        for f in os.listdir(".")
        if os.path.isfile(f) and "server" not in f.lower()
    ]
    return file_info

def get_base_dir():
    
    """
    Retrieves the base directory of the current application.

    Returns:
        str: The absolute path of the base directory.
    """

    base_path = os.path.abspath(sys.argv[0] if getattr(
        sys, 'frozen', False) else __file__)
    return os.path.dirname(base_path)

# Get local IP address
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Conectar a un servidor externo para determinar la IP local
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"  # Si falla, usa localhost como fallback

# Ajuste para PyInstaller: Manejar rutas correctamente
def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS  # Carpeta temporal donde PyInstaller descomprime archivos
    return os.path.abspath(os.path.dirname(__file__))

BASE_DIR = get_base_path()


# app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"), static_folder=os.path.join(BASE_DIR, "static"))
# app.static_folder = "static"
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"), static_folder=os.path.join(BASE_DIR, "static"))

# Habilira compresión para reducir el tamaño de las respuestas
Compress(app)

@app.route("/")
def index():

    """
    Defines the route for the root URL ("/") of the application.

    Retrieves file information using the get_file_info function and 
    renders the index.html template, passing the file information as a parameter.

    Returns:
        The rendered index.html template with file information.
    """

    file_info = get_file_info()
    return render_template("index.html", file_info=file_info)


# @app.route("/download/<filename>")
# def download_file(filename):
#     return send_from_directory('.', filename)

@app.route('/download/<filename>')
def download_file(filename):

    """
    Defines the route for downloading a file.

    Args:
        filename (str): The name of the file to be downloaded.

    Returns:
        send_from_directory: The file to be downloaded if it exists.
        tuple: A message indicating that the file was not found, along with a 404 status code.
    """

    # Old code
    """
    base_dir = get_base_dir()
    file_path = os.path.join(base_dir, filename)
    if os.path.isfile(file_path):
        return send_from_directory(base_dir, filename)
    else:
        return f'File {filename} not found.', 404
    """
    # New code
    base_dir = get_base_dir()
    file_path = os.path.join(base_dir, filename)
    
    if os.path.isfile(file_path):
        return send_from_directory(base_dir, filename, as_attachment=False)  # Permite ver archivos en navegador si es posible
    return f'File {filename} not found.', 404

@app.route("/upload", methods=["POST"])
def upload_file():

    """
    Defines the route for uploading a file.

    This function is decorated with the `@app.route` decorator, which specifies
    that the function should be called when a POST request is made to the "/upload"
    URL.

    Parameters:
        None

    Returns:
        render_template: If the uploaded file is successfully saved, the function
        returns the rendered "index.html" template with the file information and
        a success message.

        redirect: If the uploaded file is not provided, the function returns a
        redirect to the "index" route.

    """

    uploaded_file = request.files["file"]
    if uploaded_file:
        filename = uploaded_file.filename
        uploaded_file.save(filename)
        message = f"The file {filename} is uploaded"
        return render_template("index.html", file_info=get_file_info(), message=message)
    return redirect(url_for("index"))



if __name__ == "__main__":
    # Old code
    """
    app.run(host="0.0.0.0", port=8080)
    """
    # New code
    host = get_local_ip()
    port = 8080

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("waitress")

    logger.info(f"Running on http://{host}:{8080} (Press CTRL+C to quit)")
    serve(app, host=host, port=port)