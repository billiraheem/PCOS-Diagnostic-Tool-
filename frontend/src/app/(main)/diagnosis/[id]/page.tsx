"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { ArrowLeft, Download, Stethoscope } from "lucide-react";
import Link from "next/link";
import { diagnosisService } from "@/services/diagnosisService";
import { Diagnosis } from "@/interfaces/diagnosis";
import { getErrorMessage } from "@/services/api";
import ResultCard from "@/components/diagnosis/ResultCard";
import ShapChart from "@/components/diagnosis/SharpChart";
import Loading from "@/components/ui/Loading";

export default function DiagnosisResultPage() {
  const params = useParams();
  const router = useRouter();
  const [diagnosis, setDiagnosis] = useState<Diagnosis | null>(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);

  const diagnosisId = Number(params.id);

  useEffect(() => {
    const fetchDiagnosis = async () => {
      try {
        const data = await diagnosisService.getById(diagnosisId);
        setDiagnosis(data);
      } catch (error) {
        toast.error(getErrorMessage(error));
        router.push("/dashboard");
      } finally {
        setLoading(false);
      }
    };

    fetchDiagnosis();
  }, [diagnosisId, router]);

  const handleDownload = async () => {
    setDownloading(true);
    try {
      await diagnosisService.downloadReport(diagnosisId);
      toast.success("Report opened in new tab");
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setDownloading(false);
    }
  };

  if (loading) return <Loading type="page" />;
  if (!diagnosis) return null;

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div>
        <Link
          href={`/patients/${diagnosis.patient_id}`}
          className="btn btn-ghost btn-sm gap-2 mb-2"
        >
          <ArrowLeft size={16} />
          Back to Patient
        </Link>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Diagnosis Result</h1>
            <p className="text-base-content/60 text-sm mt-1">
              {diagnosis.patient_name} &bull; Age: {diagnosis.patient_age}
            </p>
          </div>
          <div className="flex gap-2">
            {!diagnosis.is_confirmed && (
              <button
                onClick={() => router.push(`/diagnosis/stage2/${diagnosis.id}`)}
                className="btn btn-secondary btn-sm gap-2"
              >
                <Stethoscope size={16} />
                Run Stage 2
              </button>
            )}
            <button
              onClick={handleDownload}
              className="btn btn-primary btn-sm gap-2"
              disabled={downloading}
            >
              {downloading ? (
                <span className="loading loading-spinner loading-sm"></span>
              ) : (
                <Download size={16} />
              )}
              Download PDF
            </button>
          </div>
        </div>
      </div>

      {/* Result Card */}
      <ResultCard
        probability={diagnosis.probability}
        riskLevel={diagnosis.risk_level}
        isConfirmed={diagnosis.is_confirmed}
        recommendation={diagnosis.recommendation}
      />

      {/* SHAP Chart */}
      <div className="card bg-base-100 shadow-sm border border-base-300">
        <div className="card-body">
          <ShapChart data={diagnosis.shap_chart_data} />
        </div>
      </div>
    </div>
  );
}
