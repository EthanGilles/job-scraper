import { Link, useLocation } from "react-router-dom";
import { Home, Briefcase, FileText, Cctv, BriefcaseConveyorBelt, Sun, Moon } from "lucide-react";
import pkg from "../../package.json";
import "@fontsource/rubik";

interface NavbarProps {
  darkMode: boolean;
  setDarkMode: (val: boolean) => void;
}

export default function Navbar({ darkMode, setDarkMode }: NavbarProps) {
  const location = useLocation();
  const appVersion = pkg.version;

  return (
    <div
      className="fixed left-0 top-0 h-screen w-64 shadow-2xl rounded-r-2xl flex flex-col justify-between z-50"
      style={{
        fontFamily: "'Rubik', sans-serif",
        backgroundColor: "var(--navbar-bg)",
        color: "var(--navbar-text)",
      }}
    >
      <div>
        {/* Header */}
        <div
          className="flex items-center h-20 px-6 font-bold text-3xl rounded-tr-2xl"
          style={{ backgroundColor: "var(--accent-primary)", color: "white" }}
        >
          <div className="relative w-12 h-12 mr-4">
            <Cctv size={34} className="absolute -top-3 -left-3" />
            <BriefcaseConveyorBelt size={30} className="absolute top-2 left-6" />
          </div>
          JobWatch
        </div>

        {/* Nav Links */}
        <nav className="flex flex-col mt-4 space-y-2 px-2">
          <Link
            to="/"
            className={`flex items-center px-4 py-2 rounded-md font-medium transition ${
              location.pathname === "/" ? "bg-[var(--accent-primary)] text-white" : "text-[var(--navbar-text)] hover:bg-[var(--accent-primary)] hover:text-white"
            }`}
          >
            <Home className="mr-2" /> Home
          </Link>

          <Link
            to="/jobs"
            className={`flex items-center px-4 py-2 rounded-md font-medium transition ${
              location.pathname === "/jobs" ? "bg-[var(--accent-primary)] text-white" : "text-[var(--navbar-text)] hover:bg-[var(--accent-primary)] hover:text-white"
            }`}
          >
            <Briefcase className="mr-2" /> Jobs
          </Link>

          <Link
            to="/logs"
            className={`flex items-center px-4 py-2 rounded-md font-medium transition ${
              location.pathname === "/logs" ? "bg-[var(--accent-primary)] text-white" : "text-[var(--navbar-text)] hover:bg-[var(--accent-primary)] hover:text-white"
            }`}
          >
            <FileText className="mr-2" /> Logs
          </Link>
        </nav>
      </div>

      {/* Dark Mode Toggle flush above footer */}
      <div className="px-4 mb-2 mt-auto flex justify-center">
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="flex items-center px-3 py-1 rounded-full bg-gray-200 dark:bg-gray-800 text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600 transition"
        >
          {darkMode ? <Sun className="mr-2" size={16} /> : <Moon className="mr-2" size={16} />}
          {darkMode ? "Light Mode" : "Dark Mode"}
        </button>
      </div>

      {/* Footer */}
      <div
        className="px-4 py-4 text-center text-sm border-t"
        style={{
          backgroundColor: "var(--footer-bg)",
          color: "var(--footer-text)",
          borderColor: "var(--footer-border)",
        }}
      >
        <div>Ethan Gilles</div>
        <div>JobWatch</div>
        <div>Version: v{appVersion}</div>
      </div>
    </div>
  );
}
