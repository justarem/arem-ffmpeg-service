from flask import Flask, request, send_file
import subprocess
import uuid
import random
import os

app = Flask(__name__)

HOOKS = [
    "POV: You just discovered an underrated Punjabi R&B singer",
    "Punjabi love songs hit different at night",
    "This is your sign to update your Punjabi playlist",
    "Underrated Punjabi R&B is a different vibe",
    "Why does Punjabi R&B sound this addictive?",
    "Late night drives need Punjabi R&B",
    "This deserves way more streams",
    "Punjabi heartbreak songs >>> everything",
    "You weren’t supposed to find this",
    "This artist is next up",
    "Punjabi R&B but it actually hits",
    "Don’t gatekeep this one",
    "If you get it, you get it",
    "This belongs on your repeat",
    "Why is this not viral yet?",
    "Found this and never recovered",
    "Punjabi R&B is evolving",
    "This song feels illegal to know",
    "You’ll replay this. Watch.",
    "This is your new obsession"
]

@app.route("/", methods=["POST"])
def process_video():
    if "video" not in request.files:
        return "No video file provided", 400

    video = request.files["video"]

    input_filename = f"{uuid.uuid4()}.mp4"
    output_filename = f"{uuid.uuid4()}_edited.mp4"

    video.save(input_filename)

    hook_text = request.form.get("hook")

    # If no hook passed → randomly pick one
    if not hook_text or hook_text.strip() == "":
        hook_text = random.choice(HOOKS)

    drawtext = (
        "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        f"text='{hook_text}':"
        "fontcolor=white:"
        "fontsize=60:"
        "box=1:"
        "boxcolor=black@0.6:"
        "boxborderw=20:"
        "x=(w-text_w)/2:"
        "y=150"
    )

    command = [
        "ffmpeg",
        "-y",
        "-i", input_filename,
        "-an",
        "-vf", drawtext,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        output_filename
    ]

    subprocess.run(command, check=True)

    if not os.path.exists(output_filename):
        return "Video processing failed", 500

    return send_file(output_filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
