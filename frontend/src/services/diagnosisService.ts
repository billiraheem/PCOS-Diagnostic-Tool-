import Cookies from "js-cookie";
import { apiGet, apiPost, apiPut } from "@/services/api";
import {
  Stage1Payload,
  Stage2Payload,
  Diagnosis,
} from "@/interfaces/diagnosis";
import { API_URL } from "@/utils/constants";

interface DashboardResponse {
  total_patients: number;
  patients: DashboardPatient[];
}

export interface DashboardPatient {
  id: number;
  name: string;
  age: number;
  created_at: string;
  has_diagnosis: boolean;
  latest_diagnosis_id: number | null;
  probability: number | null;
  risk_level: string | null;
  is_confirmed: boolean;
  diagnosis_date: string | null;
}

export const diagnosisService = {
  runStage1: (patientId: number, data: Omit<Stage1Payload, "patient_id">) => {
    return apiPost<Diagnosis>(`/api/diagnosis/stage1/${patientId}`, data);
  },

  runStage2: (diagnosisId: number, data: Stage2Payload) => {
    return apiPut<Diagnosis>(`/api/diagnosis/stage2/${diagnosisId}`, data);
  },

  getById: (id: number) => {
    return apiGet<Diagnosis>(`/api/diagnosis/diagnosis/${id}`);
  },

  getDashboard: () => {
    return apiGet<DashboardResponse>("/api/diagnosis/dashboard");
  },

  // Download PDF report
  downloadReport: async (diagnosisId: number): Promise<void> => {
    const token = Cookies.get("access_token");
    const response = await fetch(
      `${API_URL}/api/diagnosis/${diagnosisId}/report`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    // Open PDF in new tab
    window.open(url, "_blank");
  },
};
