export interface PatientCreatePayload {
  name: string;
  date_of_birth: string; // "YYYY-MM-DD" format
  phone?: string;
  email?: string;
  address?: string;
}

export interface Patient {
  id: number;
  name: string;
  date_of_birth: string;
  age: number; // Calculated by backend
  phone: string | null;
  email: string | null;
  address: string | null;
  user_id: number;
  created_at: string;
  latest_diagnosis?: DiagnosisSummary;
}

export interface DiagnosisSummary {
  id: number;
  risk_level: string;
  probability: number;
  is_confirmed: boolean;
  created_at: string;
}
