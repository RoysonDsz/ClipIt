from flask import Flask
from routes.instagram import instagram_bp
from routes.youtube import youtube_bp
from routes.spotify import spotify_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin requests for frontend

# Register routes
app.register_blueprint(instagram_bp)
app.register_blueprint(youtube_bp)
app.register_blueprint(spotify_bp)

if __name__ == "__main__":
    app.run(debug=True)
