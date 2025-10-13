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

  const lines = data?.split("\n").reverse() ?? [];

  return (
    <div className="flex flex-col flex-1 h-full"> {/* take all available space */}
      <div className="card flex flex-col flex-1 overflow-hidden p-6">
        <h2 className="text-xl font-semibold mb-4">Logs</h2>
        <LogViewer logs={lines} />
      </div>
    </div>
  );
}

