from flask import Flask, request, send_file
import subprocess
import uuid
import random

app = Flask(__name__)

HOOKS = [
    "POV: You just found an underrated Punjabi RnB singer",
    "Punjabi love songs always hit different",
    "This is what late night Punjabi feels like",
    "If you miss someone, this one’s for you",
    "Punjabi RnB > everything else",
    "You weren’t ready for this Punjabi vibe",
    "This singer deserves way more attention",
    "That toxic love but make it Punjabi",
    "This is not mainstream. This is special.",
    "Underrated Punjabi music hits harder",
    "POV: Your playlist just got better",
    "When Punjabi meets RnB perfectly",
    "This one is for the hopeless romantics",
    "You didn’t know you needed this song",
    "Real Punjabi emotions only",
    "This belongs in your late night drive playlist",
    "Warning: You might replay this",
    "If this hits, you have taste",
    "Punjabi heartbreak never sounded this good",
    "You found this before it blew up"
]

@app.route("/", methods=["POST"])
def process_video():
    video = request.files["video"]

    unique_id = str(uuid.uuid4())
    input_file = f"{unique_id}_input.mp4"
    output_file = f"{unique_id}_edited.mp4"

    video.save(input_file)

    # 🎲 Pick random hook
    hook_text = random.choice(HOOKS)

    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-an",
        "-vf",
        f"drawtext=text='{hook_text}':fontcolor=white:fontsize=60:"
        "box=1:boxcolor=black@0.6:boxborderw=20:"
        "x=(w-text_w)/2:y=100",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        output_file
    ]

    subprocess.run(command)

    return send_file(output_file, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
