from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def process_video():
    video = request.files["video"]
    audio = request.files["audio"]

    video.save("input.mp4")
    audio.save("music.mp3")

    command = [
    "ffmpeg",
    "-i", "input.mp4",
    "-i", "music.mp3",
    "-map", "0:v:0",
    "-map", "1:a:0",
    "-c:v", "copy",
    "-c:a", "aac",
    "-shortest",
    "output.mp4"
]
    subprocess.run(command)

    return send_file("output.mp4", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
