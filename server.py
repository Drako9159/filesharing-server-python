from flask import Flask, send_from_directory, render_template, request, redirect, url_for
import os
import sys

app = Flask(__name__)
app.static_folder = "static"


def get_file_info():

    """
    Retrieves information about files in the current directory.

    Returns:
        list: A list of tuples containing the filename and size in KB.
    """

    file_info = []
    for filename in os.listdir("."):
        filepath = os.path.join(".", filename)
        if os.path.isfile(filepath) and "server" not in filename.lower():
            size = os.path.getsize(filepath)
            size_str = f"{size / 1024:.2f} KB"
            file_info.append((filename, size_str))
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

    base_dir = get_base_dir()
    file_path = os.path.join(base_dir, filename)
    if os.path.isfile(file_path):
        return send_from_directory(base_dir, filename)
    else:
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
    app.run(host="0.0.0.0", port=8080)
