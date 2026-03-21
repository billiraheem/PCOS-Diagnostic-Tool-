"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { diagnosisService } from "@/services/diagnosisService";
import { getErrorMessage } from "@/services/api";
import Stage2Form from "@/components/diagnosis/Stage2Form";
import Loading from "@/components/ui/Loading";

export default function Stage2Page() {
  const params = useParams();
  const router = useRouter();
  const [patientName, setPatientName] = useState("");
  const [patientId, setPatientId] = useState<number>(0);
  const [loading, setLoading] = useState(true);

  const diagnosisId = Number(params.diagnosisId);

  useEffect(() => {
    const fetchDiagnosis = async () => {
      try {
        const data = await diagnosisService.getById(diagnosisId);
        setPatientName(data.patient_name);
        setPatientId(data.patient_id);
      } catch (error) {
        toast.error(getErrorMessage(error));
        router.push("/dashboard");
      } finally {
        setLoading(false);
      }
    };

    fetchDiagnosis();
  }, [diagnosisId, router]);

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
        <h1 className="text-2xl font-bold">Clinical Confirmation</h1>
        <p className="text-base-content/60 text-sm mt-1">
          Stage 2: Enter lab results and ultrasound data
        </p>
      </div>

      <Stage2Form diagnosisId={diagnosisId} patientName={patientName} />
    </div>
  );
}
