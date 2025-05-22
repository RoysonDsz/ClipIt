from flask import Blueprint, request, jsonify, send_file
import requests
from io import BytesIO

instagram_bp = Blueprint("instagram", __name__)

INSTAGRAM_API_URL = "https://instagram-scrapper-posts-reels-stories-downloader.p.rapidapi.com/reels"
HEADERS = {
    "x-rapidapi-key": "7e19915f0cmsh9fc5f9e100e6f05p1b7e32jsn0d920a5c1471",  # Replace with your actual API key
    "x-rapidapi-host": "instagram-scrapper-posts-reels-stories-downloader.p.rapidapi.com"
}

@instagram_bp.route('/get_reels', methods=['POST'])
def get_reels():
    data = request.get_json()
    user_id = data.get("user_id", "").strip()

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    querystring = {"user_id": user_id, "include_feed_video": "true"}

    try:
        response = requests.get(INSTAGRAM_API_URL, headers=HEADERS, params=querystring)
        response.raise_for_status()
        reels_data = response.json()

        # Extract important details
        reels = []
        if "data" in reels_data and "items" in reels_data["data"]:
            for item in reels_data["data"]["items"]:
                media = item.get("media", {})
                video_versions = media.get("video_versions", [])
                video_url = video_versions[0]["url"] if video_versions else None

                if video_url:
                    reels.append({
                        "video_url": video_url,
                        "caption": media.get("caption", ""),
                        "likes": media.get("like_count", 0),
                        "comments": media.get("comment_count", 0),
                        "thumbnail": media.get("image_versions2", {}).get("candidates", [{}])[0].get("url", ""),
                    })

        return jsonify({"reels": reels})

    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch reels", "details": str(e)}), 500


@instagram_bp.route('/get_profile', methods=['POST'])
def get_profile():
    data = request.json
    user_id = data.get("user_id")
    return jsonify({"user": {"name": "John Doe", "followers": 1200, "profile_pic": "URL_HERE"}})


@instagram_bp.route('/proxy', methods=['GET'])
def proxy():
    url = request.args.get("url")  
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return send_file(BytesIO(response.content), mimetype=response.headers['Content-Type'])
    
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch resource", "details": str(e)}), 500
