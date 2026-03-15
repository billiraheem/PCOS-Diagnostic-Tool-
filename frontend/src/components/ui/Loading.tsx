import Skeleton from "react-loading-skeleton";
import "react-loading-skeleton/dist/skeleton.css";

interface LoadingProps {
  type?: "page" | "card" | "table" | "inline";
  count?: number;
}

export default function Loading({ type = "page", count = 3 }: LoadingProps) {
  if (type === "inline") {
    return <span className="loading loading-spinner loading-md"></span>;
  }

  if (type === "card") {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {Array.from({ length: count }).map((_, i) => (
          <div key={i} className="card bg-base-100 shadow-md p-6">
            <Skeleton height={20} width="60%" />
            <Skeleton height={40} className="mt-2" />
            <Skeleton height={14} width="40%" className="mt-2" />
          </div>
        ))}
      </div>
    );
  }

  if (type === "table") {
    return (
      <div className="space-y-3">
        <Skeleton height={40} /> {/* Header */}
        {Array.from({ length: count }).map((_, i) => (
          <Skeleton key={i} height={50} />
        ))}
      </div>
    );
  }

  // type === "page"
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <span className="loading loading-spinner loading-lg text-primary"></span>
    </div>
  );
}
