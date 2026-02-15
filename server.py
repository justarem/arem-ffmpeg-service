from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def process_video():
    video = request.files["video"]

    # Clean up old files if they exist
    if os.path.exists("input.mp4"):
        os.remove("input.mp4")

    if os.path.exists("output.mp4"):
        os.remove("output.mp4")

    # Save uploaded video
    video.save("input.mp4")

    # FFmpeg command: remove audio (mute video)
    command = [
        "ffmpeg",
        "-y",                # force overwrite
        "-i", "input.mp4",
        "-an",               # remove audio
        "-c:v", "copy",      # copy video without re-encoding
        "output.mp4"
    ]

    subprocess.run(command, check=True)

    return send_file("output.mp4", as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
