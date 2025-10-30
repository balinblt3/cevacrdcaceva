# main.py - VERSIUNE FINALĂ – FĂRĂ FFMPEG
from flask import Flask, request
import subprocess
import re

app = Flask(__name__)

@app.route('/')
def get_audio_url():
    video_id = request.args.get('id', '').strip()
    
    if not re.match(r'^[a-zA-Z0-9_-]{11}$', video_id):
        return "Invalid YouTube ID", 400

    try:
        # FORMAT AUDIO SIMPLU – NU ARE NEVOIE DE FFMPEG
        cmd = [
            "yt-dlp",
            "-f", "140",  # m4a, 128kbps, direct URL
            "--get-url",
            "--no-playlist",
            f"https://www.youtube.com/watch?v={video_id}"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=15,
            check=False
        )
        
        url = result.stdout.strip()
        
        if result.returncode != 0:
            return f"yt-dlp error: {result.stderr}", 500
            
        if not url or not url.startswith("http"):
            return "Failed to extract URL", 500
            
        return url, 200
        
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
