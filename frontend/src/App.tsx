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
        <div className="flex min-h-screen h-screen"> {/* ensure full height */}
          <Navbar />
          <main className="flex-1 p-6 bg-[var(--bg-main)] flex flex-col">
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

