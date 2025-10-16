import * as React from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchTopJobs } from "../api/api";
import { BriefcaseBusiness } from "lucide-react";
import { Mosaic } from "react-loading-indicators";

export default function TopJobsCard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["top_jobs"],
    queryFn: fetchTopJobs,
    refetchInterval: 30000,
  });

  const LoadingOrError = (message: string) => (
    <div className="card flex flex-col items-center justify-center text-center p-6">
      <h3 className="text-2xl font-semibold text-[var(--text-dark)] mb-2">Top Jobs</h3>
      <p className="text-[var(--text-light)]">{message}</p>
    </div>
  );

  if (isLoading)
    return (
      <div className="flex justify-center items-center h-full min-h-[60vh]">
        <Mosaic color="#466f5e" size="large" />
      </div>
    );
  if (error || !data) return LoadingOrError("Error loading jobs");

  const jobs = data.jobs ?? [];
  const allKeywords = (data.keywords ?? []).map((kw: string) =>
    kw
      .split(" ")
      .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
      .join(" ")
  );

  return (
    <div className="card p-6 bg-white border border-gray-100 rounded-2xl max-h-[400px] overflow-y-auto">
      {/* Header */}
      <div className="flex flex-col items-center justify-center mb-6">
        <h3 className="text-2xl font-semibold text-center text-[var(--text-dark)]">
          Top Jobs
        </h3>
        <span
          className="text-sm font-medium px-3 py-1 rounded-full mt-2 text-center"
          style={{
            backgroundColor: "#e7f0ec",
            color: "#466f5e",
            display: "inline-block",
            maxWidth: "100%",
            overflowX: "auto",
          }}
        >
          {allKeywords.length > 0
            ? allKeywords.join(", ")
            : `${jobs.length} ${jobs.length === 1 ? "job" : "jobs"}`}
        </span>
      </div>

      {/* Stacked Jobs List */}
      {jobs.length === 0 ? (
        <p className="text-center text-gray-600">No matching jobs found</p>
      ) : (
        <div className="flex flex-col gap-4">
          {jobs.slice(0, 6).map((job: any, idx: number) => (
            <a
              key={idx}
              href={job.link}
              target="_blank"
              rel="noopener noreferrer"
              className="card flex flex-col justify-between p-4 border border-gray-200 bg-white transition-all duration-300 ease-out hover:bg-[#e7f0ec] hover:border-[#466f5e]"
            >
              {/* Logo aligned left */}
              {job.logo && (
                <img
                  src={job.logo}
                  alt={`${job.company} logo`}
                  className="h-10 w-auto mb-3 object-contain self-start"
                />
              )}
              {/* Job Info */}
              <div>
                <h3 className="font-semibold text-lg text-gray-800 break-words">
                  {job.title}
                </h3>
                {job.company && (
                  <p className="text-sm mt-1 text-gray-600 break-words">{job.company}</p>
                )}
                {job.location && (
                  <p className="text-sm mt-1 text-gray-500 break-words">{job.location}</p>
                )}
              </div>
            </a>
          ))}
        </div>
      )}
    </div>
  );
}

