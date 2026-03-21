import { Users, Activity, AlertTriangle, CheckCircle } from "lucide-react";
import { DashboardPatient } from "@/services/diagnosisService";

interface StatsCardsProps {
  patients: DashboardPatient[];
  totalPatients: number;
}

export default function StatsCards({
  patients,
  totalPatients,
}: StatsCardsProps) {
  const totalDiagnoses = patients.filter((p) => p.has_diagnosis).length;
  const highRisk = patients.filter((p) => p.risk_level === "HIGH").length;
  const confirmed = patients.filter((p) => p.is_confirmed).length;

  const stats = [
    {
      title: "Total Patients",
      value: totalPatients,
      icon: <Users size={24} />,
      color: "text-primary",
      bg: "bg-primary/10",
    },
    {
      title: "Diagnoses Run",
      value: totalDiagnoses,
      icon: <Activity size={24} />,
      color: "text-info",
      bg: "bg-info/10",
    },
    {
      title: "High Risk",
      value: highRisk,
      icon: <AlertTriangle size={24} />,
      color: "text-error",
      bg: "bg-error/10",
    },
    {
      title: "Confirmed",
      value: confirmed,
      icon: <CheckCircle size={24} />,
      color: "text-success",
      bg: "bg-success/10",
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat) => (
        <div
          key={stat.title}
          className="card bg-base-100 shadow-sm border border-base-300"
        >
          <div className="card-body p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-base-content/60">{stat.title}</p>
                <p className="text-2xl font-bold mt-1">{stat.value}</p>
              </div>
              <div className={`p-3 rounded-lg ${stat.bg}`}>
                <span className={stat.color}>{stat.icon}</span>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
