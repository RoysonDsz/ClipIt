import { useState } from "react";

export default function Instagram() {
  const [userId, setUserId] = useState("");
  const [reels, setReels] = useState([]);
  const [error, setError] = useState("");

  const fetchReels = async () => {
    setError("");
    setReels([]);

    if (!userId.trim()) {
      setError("User ID cannot be empty");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/get_reels", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId.trim() }),
      });

      const data = await response.json();
      console.log("Response:", data);

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
      }

      setReels(data.reels || []);
    } catch (err) {
      console.error("Fetch error:", err);
      setError(err.message || "Failed to fetch data");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-6">Instagram Reels Downloader</h1>
      
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Enter User ID"
          className="p-2 text-white rounded-md border border-gray-300 focus:ring-2 focus:ring-blue-500"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        />
        <button
          onClick={fetchReels}
          className="bg-blue-500 px-4 py-2 rounded-md hover:bg-blue-600 transition"
        >
          Get Reels
        </button>
      </div>

      {error && <p className="text-red-500 mt-4">{error}</p>}

      {reels.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
          {reels.map((reel, index) => (
            <div key={index} className="bg-gray-800 p-4 rounded-md shadow-lg">
              
              <video className="w-full mt-2 rounded-md" controls>
                <source src={reel.video_url} type="video/mp4" />
              </video>
              <p className="text-gray-400 text-sm">❤️ {reel.likes} | 💬 {reel.comments}</p>
<button
  className="block text-center bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 mt-3 rounded-md"
  onClick={async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch(reel.video_url);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = `reel-${index}.mp4`; // File name
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url); // Clean up
    } catch (err) {
      console.error("Download failed", err);
    }
  }}
>
  Download Reel
</button>

            </div>
          ))}
        </div>
      )}
    </div>
  );
}
