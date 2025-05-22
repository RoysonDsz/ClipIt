import { useState } from "react";

export default function YouTubeDownloader() {
  const [videoUrl, setVideoUrl] = useState("");
  const [downloadLink, setDownloadLink] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleDownload = async () => {
    setError("");
    setDownloadLink("");
    setLoading(true);

    if (!videoUrl.trim()) {
      setError("Please enter a valid YouTube URL.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: videoUrl }),
      });

      const data = await response.json();

      if (response.ok) {
        setDownloadLink(`http://127.0.0.1:5000/download/${data.file_name}`);
      } else {
        setError(data.error || "Failed to download video.");
      }
    } catch (err) {
      setError("Server error. Please try again later.");
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-4">YouTube Video Downloader</h1>

      <div className="w-full max-w-md">
        <input
          type="text"
          placeholder="Enter YouTube Video URL"
          className="w-full p-3 text-white rounded-lg border border-gray-400 focus:ring-2 focus:ring-blue-500"
          value={videoUrl}
          onChange={(e) => setVideoUrl(e.target.value)}
        />
        <button
          onClick={handleDownload}
          className="w-full mt-4 bg-red-500 hover:bg-red-600 p-3 rounded-lg font-bold"
          disabled={loading}
        >
          {loading ? "Processing..." : "Download"}
        </button>
      </div>

      {loading && <div className="mt-4 animate-spin rounded-full h-8 w-8 border-t-4 border-blue-500"></div>}

      {error && <p className="text-red-500 mt-4">{error}</p>}

      {downloadLink && (
        <div className="mt-6">
          <p className="text-green-400">✅ Download Ready:</p>
          <a
            href={downloadLink}
            className="mt-2 inline-block bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
            download
          >
            Click here to Download
          </a>
        </div>
      )}
    </div>
  );
}