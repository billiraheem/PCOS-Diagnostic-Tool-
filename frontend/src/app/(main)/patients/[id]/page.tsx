"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { ArrowLeft, Stethoscope, FileText, Eye } from "lucide-react";
import Link from "next/link";
import { patientService } from "@/services/patientService";
import { getErrorMessage } from "@/services/api";
import { formatDate, formatProbability } from "@/utils/helpers";
import StatusBadge from "@/components/ui/StatusBadge";
import Loading from "@/components/ui/Loading";
import Empty from "@/components/ui/Empty";

interface PatientDetail {
  id: number;
  name: string;
  age: number;
  created_at: string;
  clinician_id: number;
  diagnoses: DiagnosisItem[];
  latest_diagnosis: DiagnosisItem | null;
}

interface DiagnosisItem {
  id: number;
  probability: number;
  risk_level: string;
  is_confirmed: boolean;
  created_at: string;
  updated_at: string;
}

export default function PatientDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [patient, setPatient] = useState<PatientDetail | null>(null);
  const [loading, setLoading] = useState(true);

  const patientId = Number(params.id);

  useEffect(() => {
    const fetchPatient = async () => {
      try {
        const data = await patientService.getById(patientId);
        setPatient(data as unknown as PatientDetail);
      } catch (error) {
        toast.error(getErrorMessage(error));
        router.push("/patients");
      } finally {
        setLoading(false);
      }
    };

    fetchPatient();
  }, [patientId, router]);

  if (loading) return <Loading type="page" />;
  if (!patient) return null;

  return (
    <div className="space-y-6">
      {/* Back + Header */}
      <div>
        <Link href="/patients" className="btn btn-ghost btn-sm gap-2 mb-2">
          <ArrowLeft size={16} />
          Back to Patients
        </Link>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">{patient.name}</h1>
            <p className="text-base-content/60 text-sm mt-1">
              Age: {patient.age || "N/A"} &bull; Added:{" "}
              {formatDate(patient.created_at)}
            </p>
          </div>
          <button
            onClick={() => router.push(`/diagnosis/stage1/${patient.id}`)}
            className="btn btn-primary btn-sm gap-2"
          >
            <Stethoscope size={16} />
            New Screening
          </button>
        </div>
      </div>

      {/* Diagnosis History */}
      <div className="card bg-base-100 shadow-sm border border-base-300">
        <div className="card-body">
          <h2 className="card-title text-lg">Diagnosis History</h2>

          {patient.diagnoses.length === 0 ? (
            <Empty
              title="No diagnoses yet"
              description="Run a screening to get the first diagnosis for this patient."
              Icon={FileText}
              action={{
                label: "Start Screening",
                onClick: () => router.push(`/diagnosis/stage1/${patient.id}`),
              }}
            />
          ) : (
            <div className="overflow-x-auto">
              <table className="table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Risk Level</th>
                    <th>Probability</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {patient.diagnoses.map((diagnosis) => (
                    <tr key={diagnosis.id} className="hover">
                      <td>{formatDate(diagnosis.created_at)}</td>
                      <td>
                        <StatusBadge riskLevel={diagnosis.risk_level} />
                      </td>
                      <td>{formatProbability(diagnosis.probability)}</td>
                      <td>
                        <span
                          className={`badge badge-sm ${
                            diagnosis.is_confirmed
                              ? "badge-info"
                              : "badge-warning"
                          }`}
                        >
                          {diagnosis.is_confirmed ? "Confirmed" : "Presumptive"}
                        </span>
                      </td>
                      <td>
                        <div className="flex gap-1">
                          <button
                            onClick={() =>
                              router.push(`/diagnosis/${diagnosis.id}`)
                            }
                            className="btn btn-ghost btn-xs"
                            title="View Result"
                          >
                            <Eye size={14} />
                          </button>
                          {!diagnosis.is_confirmed && (
                            <button
                              onClick={() =>
                                router.push(`/diagnosis/stage2/${diagnosis.id}`)
                              }
                              className="btn btn-secondary btn-xs"
                              title="Run Stage 2"
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
          )}
        </div>
      </div>
    </div>
  );
}
