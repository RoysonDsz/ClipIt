from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

spotify_bp = Blueprint("spotify", __name__)

@spotify_bp.route('/spotify', methods=['GET'])
def spotify_download():
    song_id = request.args.get("songId")  # Ensure parameter is correctly passed
    if not song_id:
        return jsonify({"error": "Missing songId parameter"}), 400

    try:
        url = "https://spotify-downloader9.p.rapidapi.com/downloadSong"
        querystring = {"songId": song_id}
        headers = {
            "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
            "x-rapidapi-host": "spotify-downloader9.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 429:
            return jsonify({"error": "Rate limit exceeded. Try again later."}), 429
        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch song data (Status: {response.status_code})"}), response.status_code

        # Ensure we're getting JSON back
        try:
            data = response.json()
            return jsonify(data)
        except ValueError:
            return jsonify({"error": "API returned invalid data", "content": response.text[:200]}), 500

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500
