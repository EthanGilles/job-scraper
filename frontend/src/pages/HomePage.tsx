import { useQuery } from "@tanstack/react-query";
import { fetchJobs, fetchLogs, fetchStats } from "../api/api";
import { Briefcase, Building2, Clock, Activity, AlertTriangle, CheckCircle } from "lucide-react";

interface Stats {
  total_jobs: number;
  companies: number;
  total_scrapes: number;
  scrape_durations_seconds: number;
}

export default function HomePage() {
  const { data: stats, isLoading: statsLoading } = useQuery<Stats>({
  queryKey: ["stats"],
  queryFn: async () => {
    // trigger a scrape first
    await fetchJobs();  
    return fetchStats();
  },
  refetchInterval: 10000,
  });

  const { data: logs, isLoading: logsLoading } = useQuery({
    queryKey: ["logs", 500],
    queryFn: ({ queryKey }) => fetchLogs(queryKey[1] as number),
    refetchInterval: 10000,
  });

  // Stats from API (default to 0 while loading)
  const totalJobs = stats?.total_jobs ?? 0;
  const totalCompanies = stats?.companies ?? 0;
  const totalScrapes = stats?.total_scrapes ?? 0;
  const avgDuration = stats?.scrape_durations_seconds
    ? stats.scrape_durations_seconds.toFixed(2)
    : "0.00";

  // Log-based counts
  const logText = logs ?? "";
  const warnings = logText.match(/WARNING/g)?.length ?? 0;
  const errors = logText.match(/ERROR/g)?.length ?? 0;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
    {/* Jobs Found */}
    <div className="card flex flex-col items-center p-6">
      <Briefcase size={48} className="mb-4 text-[#466f5e]" />
      <h3 className="text-lg font-semibold">Jobs Found</h3>
      <p className="text-2xl font-bold text-[#466f5e]">{totalJobs}</p>
    </div>

    {/* Companies Scraped */}
    <div className="card flex flex-col items-center p-6">
      <Building2 size={48} className="mb-4 text-[#6f732f]" />
      <h3 className="text-lg font-semibold">Companies Scraped</h3>
      <p className="text-2xl font-bold text-[#6f732f]">{totalCompanies}</p>
    </div>

    {/* Total Scrapes */}
    <div className="card flex flex-col items-center p-6">
      <Activity size={48} className="mb-4 text-[#b38a58]" />
      <h3 className="text-lg font-semibold">Total Scrapes</h3>
      <p className="text-2xl font-bold text-[#b38a58]">{totalScrapes}</p>
    </div>

    {/* Average Duration */}
    <div className="card flex flex-col items-center p-6">
      <Clock size={48} className="mb-4 text-[#466f5e]" />
      <h3 className="text-lg font-semibold">Avg. Scrape Duration</h3>
      <p className="text-2xl font-bold text-[#466f5e]">{`${avgDuration}s`}</p>
    </div>

    {/* Warnings */}
    <div className="card flex flex-col items-center p-6">
      <AlertTriangle size={48} className="mb-4 text-yellow-400" />
      <h3 className="text-lg font-semibold">Warnings</h3>
      <p className="text-2xl font-bold text-yellow-400">{warnings}</p>
    </div>

    {/* Errors */}
    <div className="card flex flex-col items-center p-6">
      <CheckCircle size={48} className="mb-4 text-red-400" />
      <h3 className="text-lg font-semibold">Errors</h3>
      <p className="text-2xl font-bold text-red-400">{errors}</p>
    </div>
  </div>
  );
}

