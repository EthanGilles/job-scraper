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
  return (
    <div className="mb-8 p-4 card">
      {/* Company Header with large logo only */}
      <div className="flex items-center justify-between mb-6">
        {logo && (
          <img
            src={logo}
            alt={`${company} logo`}
            className="h-16 w-auto max-w-[200px] object-contain"
          />
        )}
        <span className="text-sm text-gray-500">{jobs.length} jobs</span>
      </div>

      {/* Jobs Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {jobs.map((job, idx) => (
          <a
            key={idx}
            href={job.link}
            target="_blank"
            rel="noopener noreferrer"
            className="card p-4 flex flex-col justify-between w-full relative overflow-hidden"
          >
            <div>
              <h3 className="font-semibold text-lg break-words">{job.title}</h3>
              {job.location && <p className="text-sm mt-1 break-words">{job.location}</p>}
              {job.category && <p className="text-sm mt-1 break-words">{job.category}</p>}
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}

