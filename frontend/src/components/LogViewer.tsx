import { useEffect, useRef } from "react";

interface LogViewerProps {
  logs: string[]; // now an array of lines
}

export default function LogViewer({ logs }: LogViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = 0; // scroll to top (newest logs)
    }
  }, [logs]);

  return (
    <div
      ref={containerRef}
      className="overflow-auto p-4 bg-gray-900 text-white text-sm rounded-md max-h-96 font-mono"
    >
      {logs.map((line, idx) => (
        <div key={idx}>{line}</div>
      ))}
    </div>
  );
}

