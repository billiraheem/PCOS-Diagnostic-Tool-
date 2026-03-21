"use client";

import { useRouter } from "next/navigation";
import { DashboardPatient } from "@/services/diagnosisService";
import StatusBadge from "@/components/ui/StatusBadge";
import Empty from "@/components/ui/Empty";
import { formatDate, formatProbability } from "@/utils/helpers";
import { Users, Eye, Stethoscope } from "lucide-react";

interface PatientTableProps {
  patients: DashboardPatient[];
}

export default function PatientTable({ patients }: PatientTableProps) {
  const router = useRouter();

  if (patients.length === 0) {
    return (
      <Empty
        title="No patients yet"
        description="Start by creating your first patient record to begin screening."
        Icon={Users}
        action={{
          label: "Add Patient",
          onClick: () => router.push("/patients/new"),
        }}
      />
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="table table-zebra">
        <thead>
          <tr>
            <th>Patient Name</th>
            <th>Age</th>
            <th>Risk Level</th>
            <th>Probability</th>
            <th>Status</th>
            <th>Last Assessed</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {patients.map((patient) => (
            <tr key={patient.id} className="hover">
              <td className="font-medium">{patient.name}</td>
              <td>{patient.age || "—"}</td>
              <td>
                {patient.risk_level ? (
                  <StatusBadge
                    riskLevel={patient.risk_level}
                    isConfirmed={patient.is_confirmed}
                  />
                ) : (
                  <span className="badge badge-ghost badge-sm">
                    No screening
                  </span>
                )}
              </td>
              <td>
                {patient.probability !== null
                  ? formatProbability(patient.probability)
                  : "—"}
              </td>
              <td>
                {patient.has_diagnosis ? (
                  <span
                    className={`badge badge-sm ${patient.is_confirmed ? "badge-info" : "badge-warning"}`}
                  >
                    {patient.is_confirmed ? "Confirmed" : "Presumptive"}
                  </span>
                ) : (
                  <span className="badge badge-ghost badge-sm">Pending</span>
                )}
              </td>
              <td className="text-sm text-base-content/60">
                {patient.diagnosis_date
                  ? formatDate(patient.diagnosis_date)
                  : "—"}
              </td>
              <td>
                <div className="flex gap-1">
                  <button
                    onClick={() => router.push(`/patients/${patient.id}`)}
                    className="btn btn-ghost btn-xs"
                    title="View Patient"
                  >
                    <Eye size={14} />
                  </button>
                  {!patient.has_diagnosis && (
                    <button
                      onClick={() =>
                        router.push(`/diagnosis/stage1/${patient.id}`)
                      }
                      className="btn btn-primary btn-xs"
                      title="Start Screening"
                    >
                      <Stethoscope size={14} />
                    </button>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
