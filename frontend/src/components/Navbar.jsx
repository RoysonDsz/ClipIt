import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-gray-800 text-white p-4 flex justify-around">
        <Link to="/" className="text-2xl font-bold">Home</Link>
      <Link to="/instagram" className="hover:text-blue-400">Instagram</Link>
      <Link to="/youtube" className="hover:text-red-400">YouTube</Link>
      <Link to="/spotify" className="hover:text-green-400">Spotify</Link>
      <Link to="/insta" className="hover:text-yellow-400">Insta</Link>
    </nav>
  );
}
