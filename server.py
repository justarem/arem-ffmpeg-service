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
        "-filter_complex",
        "[0:a]volume=0[a0];[1:a]volume=0.01[a1];[a0][a1]amix=inputs=2[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "output.mp4"
    ]

    subprocess.run(command)

    return send_file("output.mp4", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
