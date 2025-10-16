import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Navbar from "./components/Navbar";
import JobsPage from "./pages/JobsPage";
import LogsPage from "./pages/LogsPage";
import HomePage from "./pages/HomePage";
import "./theme.css";

const queryClient = new QueryClient();

function App() {
  const [darkMode, setDarkMode] = useState(() => {
    const stored = localStorage.getItem("darkMode");
    return stored ? JSON.parse(stored) : false;
  });

  useEffect(() => {
    if (darkMode) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }
    localStorage.setItem("darkMode", JSON.stringify(darkMode));
  }, [darkMode]);

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="flex h-screen overflow-hidden bg-[var(--bg-main)]">
          <Navbar darkMode={darkMode} setDarkMode={setDarkMode} />

          <main className="flex-1 overflow-y-auto p-6 ml-64">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/jobs" element={<JobsPage />} />
              <Route path="/logs" element={<LogsPage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
