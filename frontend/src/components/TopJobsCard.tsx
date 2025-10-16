import * as React from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchTopJobs } from "../api/api";
import { Mosaic } from "react-loading-indicators";

export default function TopJobsCard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["top_jobs"],
    queryFn: fetchTopJobs,
    refetchInterval: 30000,
  });

  const LoadingOrError = (message: string) => (
    <div className="card flex flex-col items-center justify-center text-center p-6">
      <h3 className="text-2xl font-semibold mb-2">Top Jobs</h3>
      <p>{message}</p>
    </div>
  );

  if (isLoading)
    return (
      <div className="card flex flex-col items-center justify-center text-center p-6">
        <Mosaic color="var(--accent-primary)" size="large" />
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
    <div className="card p-6 max-h-[400px] overflow-y-auto">
      {/* Header */}
      <div className="flex flex-col items-center justify-center mb-6">
        <h3 className="text-2xl font-semibold text-center">Top Jobs</h3>
        <span
          className="text-sm font-medium px-3 py-1 rounded-full mt-2 text-center inline-block"
          style={{
            backgroundColor: "var(--accent-light)",
            color: "var(--text-secondary)",
          }}
        >
          {allKeywords.length > 0
            ? allKeywords.join(", ")
            : `${jobs.length} ${jobs.length === 1 ? "job" : "jobs"}`}
        </span>
      </div>

      {/* Job List */}
      {jobs.length === 0 ? (
        <p className="text-center">No matching jobs found</p>
      ) : (
        <div className="flex flex-col gap-4">
          {jobs.slice(0, 6).map((job: any, idx: number) => (
            <a
              key={idx}
              href={job.link}
              target="_blank"
              rel="noopener noreferrer"
              className="job-card flex flex-col justify-between p-4 transition-all duration-300 ease-out hover:border hover:border-[var(--accent-primary)] hover:bg-[var(--accent-light)] rounded-xl"
            >
              {job.logo && (
                <img
                  src={job.logo}
                  alt={`${job.company} logo`}
                  className="h-10 w-auto mb-3 object-contain self-start"
                />
              )}
              <div>
                <h3 className="font-semibold text-lg break-words">{job.title}</h3>
                {job.company && (
                  <p className="text-sm mt-1 break-words">{job.company}</p>
                )}
                {job.location && (
                  <p className="text-sm mt-1 break-words">{job.location}</p>
                )}
              </div>
            </a>
          ))}
        </div>
      )}
    </div>
  );
}

