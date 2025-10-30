# main.py - YT-DLP Audio API
from flask import Flask, request, jsonify
import subprocess
import re

app = Flask(__name__)

@app.route('/')
def get_audio_url():
    video_id = request.args.get('id', '').strip()
    
    # Validare YouTube ID
    if not re.match(r'^[a-zA-Z0-9_-]{11}$', video_id):
        return "Invalid YouTube ID", 400

    try:
        # yt-dlp command
        cmd = [
            "yt-dlp",
            "-f", "bestaudio/best",
            "--get-url",
            f"https://www.youtube.com/watch?v={video_id}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        url = result.stdout.strip()
        
        if result.returncode != 0 or not url.startswith("http"):
            return "Failed to extract URL", 500
            
        return url, 200
        
    except Exception as e:
        return "Server error", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
