"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { Plus, Users, Eye, Stethoscope } from "lucide-react";
import { patientService } from "@/services/patientService";
import { Patient } from "@/interfaces/patient";
import { getErrorMessage } from "@/services/api";
import { formatDate } from "@/utils/helpers";
import Loading from "@/components/ui/Loading";
import Empty from "@/components/ui/Empty";

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const data = await patientService.getAll();
        setPatients(data);
      } catch (error) {
        toast.error(getErrorMessage(error));
      } finally {
        setLoading(false);
      }
    };

    fetchPatients();
  }, []);

  if (loading) return <Loading type="table" count={5} />;

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Patients</h1>
          <p className="text-base-content/60 text-sm mt-1">
            Manage your patient records
          </p>
        </div>
        <button
          onClick={() => router.push("/patients/new")}
          className="btn btn-primary btn-sm gap-2"
        >
          <Plus size={16} />
          Add Patient
        </button>
      </div>

      {/* Patient List */}
      {patients.length === 0 ? (
        <Empty
          title="No patients yet"
          description="Create your first patient record to begin screening."
          Icon={Users}
          action={{
            label: "Add Patient",
            onClick: () => router.push("/patients/new"),
          }}
        />
      ) : (
        <div className="card bg-base-100 shadow-sm border border-base-300">
          <div className="card-body">
            <div className="overflow-x-auto">
              <table className="table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Date of Birth</th>
                    <th>Phone</th>
                    <th>Added</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {patients.map((patient) => (
                    <tr key={patient.id} className="hover">
                      <td className="font-medium">{patient.name}</td>
                      <td>{patient.age || "—"}</td>
                      <td>{formatDate(patient.date_of_birth)}</td>
                      <td>{patient.phone || "—"}</td>
                      <td className="text-sm text-base-content/60">
                        {formatDate(patient.created_at)}
                      </td>
                      <td>
                        <div className="flex gap-1">
                          <button
                            onClick={() =>
                              router.push(`/patients/${patient.id}`)
                            }
                            className="btn btn-ghost btn-xs"
                            title="View Details"
                          >
                            <Eye size={14} />
                          </button>
                          <button
                            onClick={() =>
                              router.push(`/diagnosis/stage1/${patient.id}`)
                            }
                            className="btn btn-primary btn-xs"
                            title="Start Screening"
                          >
                            <Stethoscope size={14} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
