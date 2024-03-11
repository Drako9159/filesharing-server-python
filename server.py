from flask import Flask, send_from_directory, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.static_folder = "static"


def get_file_info():
    file_info = []
    for filename in os.listdir("."):
        filepath = os.path.join(".", filename)
        if os.path.isfile(filepath) and "server" not in filename.lower():
            size = os.path.getsize(filepath)
            size_str = f"{size / 1024:.2f} KB"
            file_info.append((filename, size_str))
    return file_info



@app.route("/")
def index():
    file_info = get_file_info()
    return render_template("index.html", file_info=file_info)




@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory('.', filename)


@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files["file"]
    if uploaded_file:
        filename = uploaded_file.filename
        uploaded_file.save(filename)
        message = f"The file {filename} is uploaded"
        return render_template("index.html", file_info=get_file_info(), message=message)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
