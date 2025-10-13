import { useState } from "react";
import { ChevronDown } from "lucide-react";

interface Job {
  title: string;
  link: string;
  location?: string;
  category?: string;
}

interface JobListProps {
  company: string;
  logo?: string;
  jobs: Job[];
}

export default function JobList({ company, logo, jobs }: JobListProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="mb-8 card rounded-2xl border border-gray-100 bg-white">
      {/* Company Header */}
      <div
        className="flex items-center justify-between mb-4 cursor-pointer p-4"
        onClick={() => setIsOpen(!isOpen)}
      >
        {/* Logo and company name area */}
        <div className="flex items-center space-x-4">
          {logo && (
            <img
              src={logo}
              alt={`${company} logo`}
              className="h-16 w-auto max-w-[200px] object-contain"
            />
          )}
        </div>

        {/* Jobs count and arrow */}
        <div className="flex items-center space-x-2">
          <span
            className="text-sm font-medium px-3 py-1 rounded-full"
            style={{ backgroundColor: "#e7f0ec", color: "#466f5e" }}
          >
            {jobs.length} {jobs.length === 1 ? "job" : "jobs"}
          </span>
          <ChevronDown
            className={`transition-transform duration-300 ${
              isOpen ? "rotate-180" : "rotate-0"
            }`}
            size={24}
          />
        </div>
      </div>

      {/* Divider Bar */}
      <div className="h-[2px] bg-gray-200 mb-6"></div>

      {/* Jobs Grid */}
      <div
        className={`grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 transition-all duration-300 ${
          isOpen ? "max-h-[2000px] opacity-100" : "max-h-0 opacity-0 overflow-hidden"
        }`}
      >
        {jobs.map((job, idx) => (
          <a
            key={idx}
            href={job.link}
            target="_blank"
            rel="noopener noreferrer"
            className="card flex flex-col justify-between p-4 border border-gray-200
                       bg-white transition-all duration-300 ease-out
                       hover:bg-[#e7f0ec] hover:border-[#466f5e]"
          >
            <div>
              <h3 className="font-semibold text-lg text-gray-800 break-words">
                {job.title}
              </h3>
              {job.location && (
                <p className="text-sm mt-1 text-gray-600 break-words">{job.location}</p>
              )}
              {job.category && (
                <p className="text-sm mt-1 text-gray-500 break-words">{job.category}</p>
              )}
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}

