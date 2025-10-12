import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { useQuery, QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Navbar from "./components/Navbar";
import JobsPage from "./pages/JobsPage";
import LogsPage from "./pages/LogsPage";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Navbar />
        <div className="p-4">
          <nav className="mb-4 space-x-4">
            <Link className="text-blue-600 dark:text-blue-400" to="/">Jobs</Link>
            <Link className="text-blue-600 dark:text-blue-400" to="/logs">Logs</Link>
          </nav>
          <Routes>
            <Route path="/" element={<JobsPage />} />
            <Route path="/logs" element={<LogsPage />} />
          </Routes>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;

