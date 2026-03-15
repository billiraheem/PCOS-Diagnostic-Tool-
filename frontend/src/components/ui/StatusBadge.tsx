import { getRiskBadgeClass } from "@/utils/helpers";

interface StatusBadgeProps {
  riskLevel: string;
  isConfirmed?: boolean;
}

export default function StatusBadge({
  riskLevel,
  isConfirmed,
}: StatusBadgeProps) {
  return (
    <div className="flex gap-2">
      <span className={`badge ${getRiskBadgeClass(riskLevel)} badge-sm`}>
        {riskLevel}
      </span>
      {isConfirmed !== undefined && (
        <span
          className={`badge badge-sm ${isConfirmed ? "badge-info" : "badge-ghost"}`}
        >
          {isConfirmed ? "Confirmed" : "Presumptive"}
        </span>
      )}
    </div>
  );
}
