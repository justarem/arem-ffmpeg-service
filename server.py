from flask import Flask, request, send_file
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def process_video():
    video = request.files["video"]

    unique_id = str(uuid.uuid4())

    input_file = f"{unique_id}_input.mp4"
    output_file = f"{unique_id}_muted.mp4"

    video.save(input_file)

    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-an",
        "-c:v", "copy",
        output_file
    ]

    subprocess.run(command)

    response = send_file(output_file, as_attachment=True)

    # cleanup
    os.remove(input_file)
    os.remove(output_file)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
