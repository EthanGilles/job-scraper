import { Link, useLocation } from "react-router-dom";
import { Home, Briefcase, FileText, Cctv, BriefcaseConveyorBelt} from "lucide-react";
import pkg from "../../package.json";
import "@fontsource/rubik";

export default function Navbar() {
  const location = useLocation();
  const appVersion = pkg.version;

  return (
    <div className="flex flex-col h-screen w-64 shadow-md justify-between" style={{ fontFamily: "'Rubik', sans-serif" }}>
      {/* Top Nav */}
      <div>
        <div
          className="flex items-center h-20 px-6 text-white font-bold text-3xl" 
          style={{ backgroundColor: "#466f5e" }}
        >
          <div className="relative w-12 h-12 mr-4"> {}
            <Cctv size={34} className="absolute -top-3 -left-3" /> {}
            <BriefcaseConveyorBelt size={28} className="absolute top-3 left-5" /> {}
          </div>
          JobWatch
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
        <div>JobWatch</div>
        <div>Version: v{appVersion}</div>
      </div>
    </div>
  );
}
