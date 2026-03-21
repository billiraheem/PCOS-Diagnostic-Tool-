import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import PatientForm from "@/components/patients/PatientForm";

export default function NewPatientPage() {
  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <Link href="/patients" className="btn btn-ghost btn-sm gap-2 mb-2">
          <ArrowLeft size={16} />
          Back to Patients
        </Link>
        <h1 className="text-2xl font-bold">New Patient</h1>
        <p className="text-base-content/60 text-sm mt-1">
          Register a new patient to begin PCOS screening
        </p>
      </div>

      {/* Form */}
      <PatientForm />
    </div>
  );
}
