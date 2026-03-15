import { apiGet, apiPost } from "@/services/api";
import { Patient, PatientCreatePayload } from "@/interfaces/patient";

export const patientService = {
  getAll: () => {
    return apiGet<Patient[]>("/api/diagnosis/patients");
  },

  getById: (id: number) => {
    return apiGet<Patient>(`/api/diagnosis/patient/${id}`);
  },

  create: (data: PatientCreatePayload) => {
    return apiPost<Patient>("/api/diagnosis/patient", data);
  },
};
