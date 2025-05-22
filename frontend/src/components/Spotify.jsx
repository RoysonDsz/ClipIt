import { useState } from "react";

export default function SpotifyDownloader() {
  const [songId, setSongId] = useState("");
  const [songData, setSongData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchSpotifyData = async () => {
    setError("");
    setSongData(null);
    setLoading(true);

    if (!songId.trim()) {
      setError("Please enter a valid Song ID.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:5000/spotify?songId=${songId}`);
      const data = await response.json();

      if (response.ok) {
        setSongData(data);
      } else {
        setError(data.error || "Failed to fetch song data.");
      }
    } catch (err) {
      setError("Server error. Please try again later.");
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white p-6">
      <h2 className="text-3xl font-bold mb-6">Spotify Song Downloader 🎵</h2>

      <div className="w-full max-w-md">
        <input
          type="text"
          placeholder="Enter Spotify Song ID"
          value={songId}
          onChange={(e) => setSongId(e.target.value)}
          className="w-full p-3 text-white bg-gray-800 rounded-lg border border-gray-600 focus:ring-2 focus:ring-green-500"
        />
        <button
          onClick={fetchSpotifyData}
          className="w-full mt-4 bg-green-500 hover:bg-green-600 p-3 rounded-lg font-bold disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Fetching..." : "Get Song Info"}
        </button>
      </div>

      {loading && <div className="mt-4 animate-spin rounded-full h-8 w-8 border-t-4 border-green-500"></div>}

      {error && <p className="text-red-500 mt-4">{error}</p>}

      {songData && (
        <div className="bg-gray-800 p-6 mt-6 rounded-lg w-full max-w-md text-center">
          <h3 className="text-xl font-semibold">{songData.track_name}</h3>
          <p className="text-gray-400">Artist: {songData.artist}</p>
          <img src={songData.album_cover} alt="Album Cover" className="mt-4 w-32 mx-auto rounded-lg" />
          <a
            href={songData.download_url}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-4 inline-block bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg"
            download
          >
            🎧 Download Song
          </a>
        </div>
      )}
    </div>
  );
}
