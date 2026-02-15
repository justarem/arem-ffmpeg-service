import os
import uuid
import random
import subprocess
from flask import Flask, request, send_file

app = Flask(__name__)

HOOKS = [
    "POV - you just found an underrated Punjabi RnB singer",
    "Punjabi love songs hit different at night",
    "This Punjabi RnB voice deserves 1M views",
    "Do not gatekeep this Punjabi singer",
    "Why is nobody talking about Punjabi RnB like this",
    "Late night Punjabi RnB just hits",
    "This song belongs in your 2AM playlist",
    "Underrated Punjabi RnB energy",
    "You were not ready for this Punjabi vibe",
    "This one is for the hopeless romantics",
    "Punjabi RnB is evolving",
    "Play this when you miss her",
    "Not your typical Punjabi song",
    "This is what Punjabi RnB should sound like",
    "This deserves to go viral",
    "If you know you know",
    "For the real Punjabi RnB fans",
    "This voice is different",
    "One listen will not be enough",
    "Add this to your heartbreak playlist"
]


def escape_text(text):
    return (
        text.replace("\\", "\\\\")
            .replace(":", "\\:")
            .replace("'", "\\'")
            .replace(",", "\\,")
            .replace("%", "\\%")
    )


@app.route("/", methods=["POST"])
def process_video():
    if "video" not in request.files:
        return "No video file provided", 400

    file = request.files["video"]

    input_filename = f"{uuid.uuid4()}.mp4"
    output_filename = f"{uuid.uuid4()}_edited.mp4"

    file.save(input_filename)

    hook = escape_text(random.choice(HOOKS))

    # IMPORTANT: specify Linux font path
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    command = [
        "ffmpeg",
        "-y",
        "-i", input_filename,
        "-an",
        "-vf",
        f"drawtext=fontfile={font_path}:"
        f"text='{hook}':"
        f"fontsize=70:"
        f"fontcolor=white:"
        f"box=1:"
        f"boxcolor=black@0.6:"
        f"boxborderw=25:"
        f"x=(w-text_w)/2:"
        f"y=100",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        "-movflags", "+faststart",
        output_filename
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        return "FFmpeg processing failed", 500

    os.remove(input_filename)

    return send_file(
        output_filename,
        as_attachment=True,
        download_name="edited_video.mp4",
        mimetype="video/mp4"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
