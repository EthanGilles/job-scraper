import { useState } from "react";
import { ChevronRight, ChevronDown } from "lucide-react";

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
    <div className="mb-6">
      <button
        className="w-full flex justify-between items-center px-4 py-2 font-semibold rounded-md text-white transition uppercase"
        style={{ backgroundColor: "#466f5e" }}
        onClick={() => setOpen(!open)}
      >
        {company} ({jobs.length})
        {open ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
      </button>

      {open && (
        <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {jobs.map((job, idx) => (
            <a
              key={idx}
              href={job.link}
              target="_blank"
              rel="noopener noreferrer"
              className="card flex flex-col p-4 hover:bg-[#466f5e] hover:text-white transition"
            >
              <h3 className="font-semibold text-lg">{job.title}</h3>
              {job.location && <p className="text-sm mt-1">{job.location}</p>}
              {job.category && <p className="text-sm mt-1">{job.category}</p>}
            </a>
          ))}
        </div>
      )}
    </div>
  );
}
