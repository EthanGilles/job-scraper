import { useQuery } from "@tanstack/react-query";
import { fetchJobs } from "../api/api";
import JobList from "../components/JobList";
import { Commet } from "react-loading-indicators";
import { getCompanyLogo } from "../utils/logos";

interface JobsPageProps {
  darkMode: boolean;
}

export default function JobsPage({ darkMode }: JobsPageProps) {
  const { data, isLoading, error } = useQuery({
    queryKey: ["jobs"],
    queryFn: fetchJobs,
    refetchInterval: 900_000,
  });

  if (isLoading)
    return (
      <div className="flex justify-center items-center h-full min-h-[60vh]">
        <Commet color="var(--accent-primary)" size="large" />
      </div>
    );

  if (error) return <div>Error loading jobs: {(error as Error).message}</div>;

  return (
    <div className="p-6">
      {data &&
        Object.entries(data).map(([company, jobs]) => (
          <JobList
            key={company}
            company={company}
            logo={getCompanyLogo(company, darkMode)}
            jobs={jobs as any[]}
          />
        ))}
    </div>
  );
}
