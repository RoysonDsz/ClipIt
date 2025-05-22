from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)
# Enable CORS for ALL origins in development mode
# In production, you should restrict this to your frontend domain
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    """Simple route to test if API is working"""
    return jsonify({"status": "API is running", "version": "1.0.0"})

# 🎵 Spotify Download Route
@app.route('/spotify', methods=['GET'])
def spotify_download():
    song_url = request.args.get("songId")
    if not song_url:
        return jsonify({"error": "Missing songId parameter"}), 400
    
    try:
        url = "https://spotify-downloader9.p.rapidapi.com/downloadSong"
        querystring = {"songId": song_url}
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
            # Not JSON, return the error
            return jsonify({"error": "API returned invalid data", "content": response.text[:200]}), 500
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# 📺 YouTube Channel Info Route
@app.route('/youtube', methods=['GET'])
def youtube_info():
    channel_id = request.args.get("id")
    if not channel_id:
        return jsonify({"error": "Missing id parameter"}), 400
    
    try:
        url = "https://youtube-media-downloader.p.rapidapi.com/v2/misc/channel-details"
        querystring = {"channel_id": channel_id}
        headers = {
            "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
            "x-rapidapi-host": "youtube-media-downloader.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch YouTube channel info (Status: {response.status_code})"}), response.status_code
        
        try:
            data = response.json()
            return jsonify(data)
        except ValueError:
            return jsonify({"error": "API returned invalid data", "content": response.text[:200]}), 500
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# 📸 Instagram Scraper Route
@app.route('/instagram', methods=['GET'])
def instagram():
    user_id = request.args.get("userId")
    content_type = request.args.get("type", "reels")  # Default to reels if not specified
    
    if not user_id:
        return jsonify({"error": "Missing userId parameter"}), 400
    
    # Validate content type
    if content_type not in ["reels", "posts", "stories"]:
        return jsonify({"error": "Invalid content type. Must be reels, posts, or stories"}), 400
    
    try:
        url = f"https://instagram-scrapper-posts-reels-stories-downloader.p.rapidapi.com/{content_type}"
        querystring = {"user_id": user_id, "include_feed_video": "true"}
        headers = {
            "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
            "x-rapidapi-host": "instagram-scrapper-posts-reels-stories-downloader.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch Instagram data (Status: {response.status_code})"}), response.status_code
        
        try:
            data = response.json()
            
            # Extract relevant media URLs
            media_links = []
            for item in data.get("items", []):
                media_info = {
                    "id": item.get("id", ""),
                    "caption": item.get("caption", {}).get("text", "") if item.get("caption") else "",
                    "like_count": item.get("like_count", 0),
                    "comment_count": item.get("comment_count", 0),
                    "timestamp": item.get("taken_at", "")
                }
                
                # Handle different media types
                if "video_url" in item:
                    media_info["type"] = "video"
                    media_info["url"] = item["video_url"]
                    media_info["thumbnail"] = item.get("image_url", "")
                elif "image_url" in item:
                    media_info["type"] = "image"
                    media_info["url"] = item["image_url"]
                
                # Only add items that have media
                if "url" in media_info:
                    media_links.append(media_info)
            
            return jsonify({"media": media_links, "count": len(media_links)})
        
        except ValueError:
            return jsonify({"error": "API returned invalid data", "content": response.text[:200]}), 500
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == "__main__":
    # Use 0.0.0.0 to make sure the server is accessible from any IP
    app.run(host='0.0.0.0', debug=True, port=5000)