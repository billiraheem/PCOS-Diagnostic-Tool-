"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { Plus } from "lucide-react";
import {
  diagnosisService,
  DashboardPatient,
} from "@/services/diagnosisService";
import { getErrorMessage } from "@/services/api";
import StatsCards from "@/components/dashboard/StatsCards";
import PatientTable from "@/components/dashboard/PatientTable";
import Loading from "@/components/ui/Loading";

export default function DashboardPage() {
  const [patients, setPatients] = useState<DashboardPatient[]>([]);
  const [totalPatients, setTotalPatients] = useState(0);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const data = await diagnosisService.getDashboard();
        setPatients(data.patients);
        setTotalPatients(data.total_patients);
      } catch (error) {
        toast.error(getErrorMessage(error));
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <Loading type="card" count={4} />
        <Loading type="table" count={5} />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-base-content/60 text-sm mt-1">
            Overview of your patients and screening results
          </p>
        </div>
        <button
          onClick={() => router.push("/patients/new")}
          className="btn btn-primary btn-sm gap-2"
        >
          <Plus size={16} />
          New Patient
        </button>
      </div>

      {/* Stats Cards */}
      <StatsCards patients={patients} totalPatients={totalPatients} />

      {/* Patient Table */}
      <div className="card bg-base-100 shadow-sm border border-base-300">
        <div className="card-body">
          <h2 className="card-title text-lg">Recent Patients</h2>
          <PatientTable patients={patients} />
        </div>
      </div>
    </div>
  );
}
