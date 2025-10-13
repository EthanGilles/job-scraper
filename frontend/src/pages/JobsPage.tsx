import { useQuery, QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { fetchJobs } from "../api/api";
import JobList from "../components/JobList";

export default function JobsPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["jobs"],
    queryFn: fetchJobs,
    refetchInterval: 300_000,
  });

  if (isLoading) return <div>Loading jobs...</div>;
  if (error) return <div>Error loading jobs: {(error as Error).message}</div>;

  return (
    <div className="p-6">
      {data &&
        Object.entries(data).map(([company, jobs]) => (
          <JobList key={company} company={company} jobs={jobs as any[]} />
        ))}
    </div>
  );
}
