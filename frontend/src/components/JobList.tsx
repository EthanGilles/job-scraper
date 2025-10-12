import { useState } from "react";

interface Job {
  title: string;
  link: string;
  location?: string;
  category?: string;
  department?: string;
}

interface JobListProps {
  company: string;
  jobs: Job[];
}

export default function JobList({ company, jobs }: JobListProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className="border rounded-md mb-4 shadow-sm">
      <button
        className="w-full text-left px-4 py-2 font-semibold bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600"
        onClick={() => setOpen(!open)}
      >
        {company} ({jobs.length})
      </button>
      {open && (
        <ul className="px-4 py-2 bg-gray-50 dark:bg-gray-800">
          {jobs.map((job, idx) => (
            <li key={idx} className="py-1">
              <a
                href={job.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 dark:text-blue-400 hover:underline"
              >
                {job.title} {job.location ? `- ${job.location}` : ""}
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

