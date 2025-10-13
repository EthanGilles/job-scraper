import * as React from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchJobs, fetchLogs, fetchStats } from "../api/api";
import { PieChart } from "@mui/x-charts/PieChart";
import { Briefcase, Building2, Clock, Activity, AlertTriangle, CheckCircle } from "lucide-react";

interface Stats {
  total_jobs: number;
  companies: number;
  total_scrapes: number;
  scrape_durations_seconds: number;
  last_scrape: string;
}

export default function HomePage() {
  const { data: stats } = useQuery<Stats>({
    queryKey: ["stats"],
    queryFn: async () => {
      await fetchJobs(); // trigger scrape
      return fetchStats();
    },
    refetchInterval: 10000,
  });

  const { data: logs } = useQuery({
    queryKey: ["logs", 500],
    queryFn: ({ queryKey }) => fetchLogs(queryKey[1] as number),
    refetchInterval: 10000,
  });

  const { data: jobsData } = useQuery<Record<string, any[]>>({
    queryKey: ["jobsData"],
    queryFn: fetchJobs,
  });

  const totalJobs = stats?.total_jobs ?? 0;
  const totalCompanies = stats?.companies ?? 0;
  const totalScrapes = stats?.total_scrapes ?? 0;
  const avgDuration = stats?.scrape_durations_seconds?.toFixed(2) ?? "0.00";
  const lastScrape = stats?.last_scrape ?? "N/A";

  const formattedLastScrape =
  lastScrape !== "N/A"
    ? (() => {
        const d = new Date(lastScrape);
        const datePart = d.toLocaleDateString("en-US", { month: "long", day: "numeric" }); // October 12
        const timePart = d.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit", hour12: true }); // 10:44 PM
        return `${datePart}\n\n${timePart}`; // newline between date and time
      })()
    : "N/A";

  const logText = logs ?? "";
  const warnings = logText.match(/WARNING/g)?.length ?? 0;
  const errors = logText.match(/ERROR/g)?.length ?? 0;

  const pieData =
    jobsData && Object.keys(jobsData).length > 0
      ? Object.entries(jobsData).map(([company, jobs]) => ({
          id: company,       // used internally
          label: company,    // shows in tooltip
          value: jobs.length // number of jobs
        }))
      : [];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {/* Pie Chart for Job Distribution */}
      <div className="card flex flex-col items-center p-6">
        <h3 className="text-2xl font-semibold mb-2">Jobs Per Company</h3>
        {pieData.length > 0 ? (
          <PieChart
            series={[
              {
                data: pieData,
                valueFormatter: (d) => `${d.value} jobs`,
                highlightScope: { fade: 'global', highlight: 'item' },
                faded: { innerRadius: 30, additionalRadius: -30, color: 'gray' },
              },
            ]}
            height={200}
            width={200}
          />

        ) : (
          <p>No job data yet</p>
        )}
      </div>

      {/* Jobs Found */}
      <div className="card flex flex-col items-center p-6 space-y-6">
        <Briefcase size={60} className="text-[#466f5e]" />
        <h3 className="text-3xl font-semibold">Jobs Found</h3>
        <p className="text-6xl font-bold text-[#466f5e]">{totalJobs}</p>
      </div>

      {/* Companies Scraped */}
      <div className="card flex flex-col items-center p-6 space-y-6">
        <Building2 size={60} className="text-[#6f732f]" />
        <h3 className="text-3xl font-semibold">Companies Scraped</h3>
        <p className="text-6xl font-bold text-[#6f732f]">{totalCompanies}</p>
      </div>

      {/* Last Scrape */}
      <div className="card flex flex-col items-center p-6">
        <Clock size={48} className="mb-4 text-[#6f732f]" />
        <h3 className="text-2xl font-semibold">Last Scrape</h3>
        {lastScrape !== "N/A" ? (
          <p className="text-3xl font-bold text-[#6f732f] text-center">
            {new Date(lastScrape).toLocaleDateString("en-US", { month: "long", day: "numeric" })}{" at "}
            {new Date(lastScrape).toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit", hour12: true })}
          </p>
        ) : (
          <p className="text-3xl font-bold text-[#6f732f]">N/A</p>
        )}
      </div>

      {/* Average Duration */}
      <div className="card flex flex-col items-center p-6">
        <Clock size={48} className="mb-4 text-[#466f5e]" />
        <h3 className="text-2xl font-semibold">Avg. Scrape Duration</h3>
        <p className="text-3xl font-bold text-[#466f5e]">{`${avgDuration}s`}</p>
      </div>

      {/* Placeholder Metric */}
      <div className="card flex flex-col items-center p-6">
        <Activity size={48} className="mb-4 text-[#b38a58]" />
        <h3 className="text-2xl font-semibold">Your Metric</h3>
        <p className="text-3xl font-bold text-[#b38a58]">--</p>
      </div>

      {/* Total Scrapes */}
      <div className="card flex flex-col items-center p-6">
        <Activity size={48} className="mb-4 text-[#b38a58]" />
        <h3 className="text-2xl font-semibold">Total Scrapes</h3>
        <p className="text-3xl font-bold text-[#b38a58]">{totalScrapes}</p>
      </div>


      {/* Warnings */}
      <div className="card flex flex-col items-center p-6">
        <AlertTriangle size={48} className="mb-4 text-yellow-400" />
        <h3 className="text-2xl font-semibold">Warnings</h3>
        <p className="text-3xl font-bold text-yellow-400">{warnings}</p>
      </div>

      {/* Errors */}
      <div className="card flex flex-col items-center p-6">
        <CheckCircle size={48} className="mb-4 text-red-400" />
        <h3 className="text-2xl font-semibold">Errors</h3>
        <p className="text-3xl font-bold text-red-400">{errors}</p>
      </div>



    </div>
  );
}
