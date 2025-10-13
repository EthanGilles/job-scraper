import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Navbar from "./components/Navbar";
import JobsPage from "./pages/JobsPage";
import LogsPage from "./pages/LogsPage";
import HomePage from "./pages/HomePage";
import "./theme.css";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        {/* Outer container */}
        <div className="flex h-screen overflow-hidden bg-[var(--bg-main)]">
          {/* Fixed navbar */}
          <Navbar />

          {/* Scrollable main content with margin to the right of the navbar */}
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

