from flask import Flask, request, jsonify, send_file
import subprocess
import os
import threading
import time
from urllib.parse import quote

app = Flask(__name__)
DOWNLOAD_DIR = os.path.expanduser("~/yt-downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def delete_file_later(path, delay=30):
    def delete():
        time.sleep(delay)
        if os.path.exists(path):
            os.remove(path)
            print(f"[INFO] File deleted: {path}")
    threading.Thread(target=delete, daemon=True).start()

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")
    format_type = data.get("format", "Video").lower()

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    print(f"[DEBUG] Received JSON: {data}")

    output_template = os.path.join(DOWNLOAD_DIR, "%(title).100s.%(ext)s")

    if format_type == "audio":
        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--output", output_template,
            "--print", "after_move:filepath",
            url
        ]
    else:
        cmd = [
            "yt-dlp",
            "-f", "best[ext=mp4][vcodec^=avc1][acodec^=mp4a]/best",
            "--output", output_template,
            "--print", "after_move:filepath",
            url
        ]
        if os.path.exists("cookies.txt"):
            cmd.insert(1, "--cookies")
            cmd.insert(2, "cookies.txt")

    print(f"[DEBUG] Running command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        filepath = result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        print("[ERROR] yt-dlp failed:")
        print(e.stderr.decode())
        return jsonify({"error": "yt-dlp failed", "details": e.stderr.decode()[:500]}), 500

    if not os.path.exists(filepath):
        print(f"[ERROR] File not found after download: {filepath}")
        return jsonify({"error": "Download failed: file not found"}), 500

    filename = os.path.basename(filepath)
    download_url = f"http://{request.host}/files/{quote(filename)}"
    print(f"[SUCCESS] File downloaded to: {filepath}")

    delete_file_later(filepath, delay=30)

    return jsonify({"download_url": download_url}), 200

@app.route("/files/<path:filename>")
def serve_file(filename):
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File no longer available"}), 404
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    print("Server starting on http://0.0.0.0:5000 ...")
    app.run(host="0.0.0.0", port=5000)