export interface Stage1Payload {
  patient_id: number;
  age?: number;
  weight: number;
  height: number;
  bmi: number;
  cycle_regularity: number; // 0 or 1
  cycle_length: number;
  weight_gain: number; // 0 or 1
  hair_growth: number; // 0 or 1
  skin_darkening: number; // 0 or 1
  hair_loss: number; // 0 or 1
  pimples: number; // 0 or 1
  fast_food: number; // 0 or 1
  reg_exercise: number; // 0 or 1
}

export interface Stage2Payload {
  fsh: number;
  lh: number;
  amh: number;
  tsh?: number;
  follicle_no_l: number;
  follicle_no_r: number;
  avg_f_size_l: number;
  avg_f_size_r: number;
  endometrium?: number;
  hip?: number;
  waist?: number;
}

export interface ShapFeature {
  feature: string;
  value: number;
  impact: number;
  direction: string; // "increases" or "decreases"
}

export interface Diagnosis {
  id: number;
  patient_id: number;
  patient_name: string;
  patient_age: number;
  risk_level: string;
  probability: number;
  is_confirmed: boolean;
  recommendation: string;
  shap_chart_data: ShapFeature[];
  created_at: string;
}

export interface DashboardStats {
  total_patients: number;
  total_diagnoses: number;
  high_risk_count: number;
  confirmed_count: number;
  recent_diagnoses: Diagnosis[];
}
