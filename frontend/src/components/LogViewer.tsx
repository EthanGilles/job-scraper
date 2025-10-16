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
        return "var(--log-text-alert)";
      case "INFO":
        return "var(--log-text)";
      default:
        return "var(--log-text)";
    }
  };

  const renderLine = (line: string) => {
    const match = line.match(/(ERROR|WARNING|INFO)/);
    if (!match) return <span style={{color: "var(--log-text-alert)"}}>{line}</span>;

    const keyword = match[0];
    const parts = line.split(keyword);

    return (
      <>
        <span style={{color: getRestTextColor(keyword)}}>{parts[0]}</span>
        <span className={getKeywordColor(keyword)}>{keyword}</span>
        <span style={{color: getRestTextColor(keyword)}}>{parts[1]}</span>
      </>
    );
  };

  return (
    <div
      ref={containerRef}
      className="flex-1 overflow-auto p-4 text-sm rounded-md font-mono transition-colors"
      style={{
        backgroundColor: "var(--log-bg)",
        color: "var(--log-text)",
      }}
    >
      {logs.map((line, idx) => (
        <div key={idx}>{renderLine(line)}</div>
      ))}
    </div>
  );
}

