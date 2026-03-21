"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { patientService } from "@/services/patientService";
import { getErrorMessage } from "@/services/api";
import Stage1Form from "@/components/diagnosis/Stage1Form";
import Loading from "@/components/ui/Loading";

export default function Stage1Page() {
  const params = useParams();
  const router = useRouter();
  const [patientName, setPatientName] = useState("");
  const [loading, setLoading] = useState(true);

  const patientId = Number(params.patientId);

  useEffect(() => {
    const fetchPatient = async () => {
      try {
        const data = await patientService.getById(patientId);
        setPatientName(data.name);
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

  return (
    <div className="space-y-6">
      <div>
        <Link
          href={`/patients/${patientId}`}
          className="btn btn-ghost btn-sm gap-2 mb-2"
        >
          <ArrowLeft size={16} />
          Back to Patient
        </Link>
        <h1 className="text-2xl font-bold">PCOS Screening</h1>
        <p className="text-base-content/60 text-sm mt-1">
          Stage 1: Enter symptoms and vitals for initial risk assessment
        </p>
      </div>

      <Stage1Form patientId={patientId} patientName={patientName} />
    </div>
  );
}
