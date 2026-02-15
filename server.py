from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def process_video():
    video = request.files["video"]
    hook = request.form["hook"]

    video.save("input.mp4")

    command = [
        "ffmpeg",
        "-y",
        "-i", "input.mp4",
        "-vf",
        f"drawtext=text='{hook}':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=100:box=1:boxcolor=black@0.5",
        "-an",
        "-c:v", "libx264",
        "output.mp4"
    ]

    subprocess.run(command)

    return send_file("output.mp4", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
