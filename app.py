from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os
import subprocess

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
socketio = SocketIO(app)

def download_playlist_with_ytdlp(playlist_url, save_path):
    os.makedirs(save_path, exist_ok=True)
    command = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio[ext=mp4]/mp4",
        "--yes-playlist",
        "--output", os.path.join(save_path, "%(playlist_index)s - %(title)s.%(ext)s"),
        playlist_url,
    ]

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
    )

    for line in process.stdout:
        socketio.emit("progress", {"message": line.strip()})
    
    process.wait()
    if process.returncode == 0:
        socketio.emit("progress", {"message": "Download complete!"})
    else:
        socketio.emit("progress", {"message": "An error occurred during the download."})

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        playlist_url = request.form.get("playlist_url").strip()
        save_path = request.form.get("save_path").strip() or "Downloads"

        socketio.start_background_task(download_playlist_with_ytdlp, playlist_url, save_path)
        return render_template("index.html", playlist_url=playlist_url)

    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)
