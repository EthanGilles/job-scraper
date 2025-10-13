import { useEffect, useRef } from "react";

interface LogViewerProps {
  logs: string[];
}

export default function LogViewer({ logs }: LogViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = 0; // newest logs at top
    }
  }, [logs]);

  const getKeywordColor = (keyword: string) => {
    switch (keyword) {
      case "ERROR":
        return "text-red-600 font-semibold";
      case "WARNING":
        return "text-yellow-500 font-semibold";
      case "INFO":
        return "text-green-500 font-semibold";
      default:
        return "";
    }
  };

  const getRestTextColor = (keyword: string) => {
    switch (keyword) {
      case "ERROR":
      case "WARNING":
        return "text-black";
      case "INFO":
        return "text-gray-500";
      default:
        return "text-gray-800";
    }
  };

  const renderLine = (line: string) => {
    const match = line.match(/(ERROR|WARNING|INFO)/);
    if (!match) return <span className="text-gray-800">{line}</span>;

    const keyword = match[0];
    const parts = line.split(keyword);

    return (
      <>
        <span className={getRestTextColor(keyword)}>{parts[0]}</span>
        <span className={getKeywordColor(keyword)}>{keyword}</span>
        <span className={getRestTextColor(keyword)}>{parts[1]}</span>
      </>
    );
  };

  return (
    <div
      ref={containerRef}
      className="flex-1 overflow-auto p-4 bg-white text-sm rounded-md font-mono"
    >
      {logs.map((line, idx) => (
        <div key={idx}>{renderLine(line)}</div>
      ))}
    </div>
  );
}

