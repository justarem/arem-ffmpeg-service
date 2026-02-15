from flask import Flask, request, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route("/", methods=["POST"])
def process_video():
    video = request.files["video"]
    hook = request.form.get("hook", "Punjabi R&B hits different")

    input_filename = f"{uuid.uuid4()}.mp4"
    output_filename = f"{uuid.uuid4()}_edited.mp4"

    video.save(input_filename)

    command = [
        "ffmpeg",
        "-y",
        "-i", input_filename,
        "-vf", f"drawtext=text='{hook}':fontcolor=white:fontsize=60:box=1:boxcolor=black@0.6:boxborderw=20:x=(w-text_w)/2:y=150",
        "-an",
        "-c:v", "libx264",
        "-preset", "fast",
        output_filename
    ]

    subprocess.run(command)

    return send_file(output_filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
