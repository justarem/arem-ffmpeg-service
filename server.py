from flask import Flask, request, send_file, jsonify
import subprocess
import uuid
import random
import os

app = Flask(__name__)

HOOKS = [
    "POV: You just discovered an underrated Punjabi RnB singer",
    "Punjabi love songs always hit different",
    "This Punjabi vibe is dangerous",
    "Late night Punjabi RnB feels",
    "You weren’t ready for this Punjabi drop",
    "This song deserves 10M streams",
    "Punjabi heartbreak hits different",
    "Your new favourite Punjabi song",
    "Underrated Punjabi artist alert",
    "Punjabi RnB season has started",
    "This one is going on repeat",
    "Don’t sleep on Punjabi RnB",
    "This vibe is illegal",
    "Punjabi songs for late drives",
    "If you love Punjabi music, wait for this",
    "You’ll replay this part",
    "Hidden Punjabi gem",
    "Punjabi + RnB = undefeated",
    "This deserves more hype",
    "Your playlist needs this"
]

@app.route("/", methods=["POST"])
def process_video():
    try:
        video = request.files["video"]

        input_filename = f"{uuid.uuid4()}.mp4"
        output_filename = f"{uuid.uuid4()}_edited.mp4"

        video.save(input_filename)

        hook = random.choice(HOOKS)
        hook = hook.replace(":", "\\:").replace("'", "\\'")

        command = [
            "ffmpeg",
            "-y",
            "-i", input_filename,
            "-vf",
            f"drawtext=text='{hook}':"
            f"fontsize=70:"
            f"fontcolor=white:"
            f"box=1:"
            f"boxcolor=black@0.6:"
            f"boxborderw=25:"
            f"x=(w-text_w)/2:"
            f"y=100",
            "-an",
            "-c:v", "libx264",
            "-preset", "veryfast",
            output_filename
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode != 0:
            print("FFMPEG ERROR:")
            print(result.stderr.decode())
            return jsonify({"error": "FFmpeg failed"}), 500

        return send_file(output_filename, as_attachment=True)

    except Exception as e:
        print("SERVER ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
