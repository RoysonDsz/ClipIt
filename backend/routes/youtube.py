from flask import Blueprint, request, jsonify, send_file
import yt_dlp
import os

youtube_bp = Blueprint("youtube", __name__)

# Set the Downloads folder dynamically
if os.name == "nt":  # Windows
    DOWNLOAD_FOLDER = os.path.join(os.environ["USERPROFILE"], "Downloads")
else:  # macOS/Linux
    DOWNLOAD_FOLDER = os.path.join(os.environ["HOME"], "Downloads")

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

@youtube_bp.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing video URL"}), 400

    ydl_opts = {
        'format': 'best',
        'outtmpl': f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info_dict)
            return jsonify({"file_name": os.path.basename(file_name)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@youtube_bp.route("/download/<filename>")
def get_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)
