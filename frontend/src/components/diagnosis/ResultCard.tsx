import { formatProbability } from "@/utils/helpers";
import {
  AlertTriangle,
  CheckCircle,
  ShieldAlert,
  HelpCircle,
} from "lucide-react";

interface ResultCardProps {
  probability: number;
  riskLevel: string;
  isConfirmed: boolean;
  recommendation: string;
}

export default function ResultCard({
  probability,
  riskLevel,
  isConfirmed,
  recommendation,
}: ResultCardProps) {
  const getConfig = () => {
    switch (riskLevel?.toUpperCase()) {
      case "HIGH":
        return {
          icon: <ShieldAlert size={32} />,
          bgClass: "bg-error/10 border-error",
          textClass: "text-error",
          label: isConfirmed
            ? "CONFIRMED PCOS POSITIVE"
            : "High Risk — Presumptive Positive",
        };
      case "MODERATE":
        return {
          icon: <HelpCircle size={32} />,
          bgClass: "bg-warning/10 border-warning",
          textClass: "text-warning",
          label: "Ambiguous / Inconclusive",
        };
      case "LOW":
        return {
          icon: <CheckCircle size={32} />,
          bgClass: "bg-success/10 border-success",
          textClass: "text-success",
          label: "Low Risk",
        };
      default:
        return {
          icon: <AlertTriangle size={32} />,
          bgClass: "bg-base-200 border-base-300",
          textClass: "text-base-content",
          label: "Unknown",
        };
    }
  };

  const config = getConfig();

  return (
    <div className={`card border-2 ${config.bgClass}`}>
      <div className="card-body">
        {/* Status Header */}
        <div className="flex items-center gap-4">
          <div className={config.textClass}>{config.icon}</div>
          <div>
            <h2 className={`text-xl font-bold ${config.textClass}`}>
              {config.label}
            </h2>
            <p className="text-sm text-base-content/60">
              {isConfirmed ? "Confirmed Diagnosis" : "Presumptive Screening"}
            </p>
          </div>
        </div>

        {/* Probability */}
        <div className="mt-4 flex items-center gap-3">
          <div className={`text-3xl font-bold ${config.textClass}`}>
            {formatProbability(probability)}
          </div>
          <span className="text-sm text-base-content/60">Likelihood</span>
        </div>

        {/* Recommendation */}
        <div className="mt-4 p-4 bg-base-200 rounded-lg">
          <h4 className="text-sm font-semibold mb-2">Recommendation</h4>
          <p className="text-sm text-base-content/80 whitespace-pre-line">
            {recommendation}
          </p>
        </div>
      </div>
    </div>
  );
}
