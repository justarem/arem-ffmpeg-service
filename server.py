from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def process_video():
    video = request.files["video"]
    hook_text = request.form.get("hook", "You know exactly who this reminds you of.")

    video.save("input.mp4")

    output_name = hook_text.replace(" ", "_")[:50] + ".mp4"

    command = [
        "ffmpeg",
        "-i", "input.mp4",
        "-vf", f"drawtext=text='{hook_text}':fontcolor=white:fontsize=70:box=1:boxcolor=black@0.6:boxborderw=20:x=(w-text_w)/2:y=150",
        "-an",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        output_name
    ]

    subprocess.run(command)

    return send_file(output_name, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
