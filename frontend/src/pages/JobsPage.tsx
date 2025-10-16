import { useQuery } from "@tanstack/react-query";
import { fetchJobs } from "../api/api";
import JobList from "../components/JobList";
import { Commet } from "react-loading-indicators";

const companyLogos: Record<string, string> = {
  digitalocean: "/logos/digitalocean.svg",
  atlassian: "/logos/atlassian.svg",
  plaid: "/logos/plaid.svg",
  stripe: "/logos/stripe.svg",
  datadog: "/logos/datadog.svg"
};

export default function JobsPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["jobs"],
    queryFn: fetchJobs,
    refetchInterval: 900_000, // refresh every 5 min
  });

  if (isLoading)
    return (
      <div className="flex justify-center items-center h-full min-h-[60vh]">
        <Commet color="#466f5e" size="large" />
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
            logo={companyLogos[company.toLowerCase()]} // step 3: pass logo dynamically
            jobs={jobs as any[]}
          />
        ))}
    </div>
  );
}
