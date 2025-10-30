# main.py - YT-DLP Audio API - 100% FUNCȚIONAL
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
        cmd = [
            "yt-dlp",
            "-f", "140",  # m4a, 128kbps, direct
            "--get-url",
            "--no-playlist",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "--referer", "https://www.youtube.com/",
            "--add-header", "Accept-Language:en-US,en;q=0.9",
            f"https://www.youtube.com/watch?v={video_id}"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=20,
            check=False
        )
        
        url = result.stdout.strip()
        
        if result.returncode != 0:
            error = result.stderr.strip()
            if "Sign in" in error or "bot" in error:
                return "YouTube bot detection. Try again later.", 503
            return f"yt-dlp error: {error}", 500
            
        if not url or not url.startswith("http"):
            return "Failed to extract URL", 500
            
        return url, 200
        
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
