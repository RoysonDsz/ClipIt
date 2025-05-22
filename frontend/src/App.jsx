import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Instagram from "./components/instagram";
import YouTube from "./components/Youtube";
import Spotify from "./components/Spotify";
import Home from "./components/Home";
import Insta from "./components/insta";


export default function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/instagram" element={<Instagram />} />
        <Route path="/youtube" element={<YouTube />} />
        <Route path="/spotify" element={<Spotify />} />
        <Route path="/insta" element={<Insta />} />
      </Routes>
    </Router>
  );
}
