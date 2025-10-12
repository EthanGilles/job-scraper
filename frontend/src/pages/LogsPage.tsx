import { useQuery } from "@tanstack/react-query";
import { fetchLogs } from "../api/api";
import LogViewer from "../components/LogViewer";

export default function LogsPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["logs", 500],
    queryFn: ({ queryKey }) => fetchLogs(queryKey[1] as number),
    refetchInterval: 10000,
  });

  if (isLoading) return <div>Loading logs...</div>;
  if (error) return <div>Error loading logs: {(error as Error).message}</div>;

  // split string into lines and reverse for newest first
  const lines = data?.split("\n").reverse() ?? [];

  return (
    <div className="text-white">
      <LogViewer logs={lines} />
    </div>
  );
}

