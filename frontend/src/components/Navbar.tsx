import { useState, useEffect } from "react";

export default function Navbar() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    if (darkMode) document.documentElement.classList.add("dark");
    else document.documentElement.classList.remove("dark");
  }, [darkMode]);

  return (
    <nav className="flex justify-between items-center px-4 py-3 bg-gray-200 dark:bg-gray-800">
      <h1 className="font-bold text-lg">Job Scraper Dashboard</h1>
      <button
        onClick={() => setDarkMode(!darkMode)}
        className="px-3 py-1 rounded bg-gray-300 dark:bg-gray-700"
      >
        {darkMode ? "Light Mode" : "Dark Mode"}
      </button>
    </nav>
  );
}

