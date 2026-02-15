from flask import Flask, request, send_file
import subprocess

app = Flask(__name__)

@app.route("/", methods=["POST"])
def process_video():
    video = request.files["video"]

    video.save("input.mp4")

    command = [
        "ffmpeg",
        "-i", "input.mp4",
        "-an",
        "output.mp4"
    ]

    subprocess.run(command)

    return send_file("output.mp4", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
