import { Link, useLocation } from "react-router-dom";
import { Home, Briefcase, FileText, Grid } from "lucide-react";
import pkg from "../../package.json";

export default function Navbar() {
  const location = useLocation();
  const appVersion = pkg.version;

  return (
    <div className="flex flex-col h-screen w-64 shadow-md justify-between" style={{ fontFamily: "'Rubik', sans-serif" }}>
      {/* Top Nav */}
      <div>
        <div
          className="flex items-center h-16 px-4 text-white font-bold text-xl"
          style={{ backgroundColor: "#466f5e" }}
        >
          <Grid className="mr-2" size={28} />
          Job Scraper
        </div>

        <nav className="flex flex-col mt-4 space-y-2 px-2">
          <Link
            to="/"
            className={`flex items-center px-4 py-2 rounded-md font-medium transition ${
              location.pathname === "/"
                ? "bg-[#466f5e] text-white"
                : "text-[#0d0d0d] hover:bg-[#466f5e] hover:text-white"
            }`}
          >
            <Home className="mr-2" /> Home
          </Link>

          <Link
            to="/jobs"
            className={`flex items-center px-4 py-2 rounded-md font-medium transition ${
              location.pathname === "/jobs"
                ? "bg-[#466f5e] text-white"
                : "text-[#0d0d0d] hover:bg-[#466f5e] hover:text-white"
            }`}
          >
            <Briefcase className="mr-2" /> Jobs
          </Link>

          <Link
            to="/logs"
            className={`flex items-center px-4 py-2 rounded-md font-medium transition ${
              location.pathname === "/logs"
                ? "bg-[#466f5e] text-white"
                : "text-[#0d0d0d] hover:bg-[#466f5e] hover:text-white"
            }`}
          >
            <FileText className="mr-2" /> Logs
          </Link>
        </nav>
      </div>

      {/* Footer */}
      <div className="px-4 py-4 text-center text-gray-400 text-sm">
        <div>Ethan Gilles</div>
        <div>Job Scraper</div>
        <div>Version: v{appVersion}</div>
      </div>
    </div>
  );
}
