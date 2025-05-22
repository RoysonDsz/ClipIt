export default function Home() {
    return (
      <div className="text-white text-center mt-10 p-6">
        <h1 className="text-4xl font-bold">Welcome to the Media Downloader</h1>
        <p className="mt-4 text-lg text-gray-400">
          Download videos and music from Instagram, YouTube, and Spotify easily!
        </p>
  
        {/* Features Section */}
        <div className="mt-10 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-bold text-blue-400">Instagram Reels</h2>
            <p className="text-gray-400 mt-2">Download high-quality Instagram Reels instantly.</p>
          </div>
  
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-bold text-red-400">YouTube Videos</h2>
            <p className="text-gray-400 mt-2">Get YouTube videos in various resolutions and formats.</p>
          </div>
  
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-bold text-green-400">Spotify Music</h2>
            <p className="text-gray-400 mt-2">Download high-quality Spotify tracks for offline listening.</p>
          </div>
        </div>
  
        {/* Navigation Buttons */}
        <div className="mt-10 flex justify-center space-x-4">
          <a href="/instagram" className="bg-blue-500 px-6 py-3 rounded-md text-white font-bold hover:bg-blue-600">
            Instagram
          </a>
          <a href="/youtube" className="bg-red-500 px-6 py-3 rounded-md text-white font-bold hover:bg-red-600">
            YouTube
          </a>
          <a href="/spotify" className="bg-green-500 px-6 py-3 rounded-md text-white font-bold hover:bg-green-600">
            Spotify
          </a>
        </div>
      </div>
    );
  }
  