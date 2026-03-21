import * as Yup from "yup";

// Stage 1: Non-invasive screening (symptoms + vitals)
export const stage1Schema = Yup.object().shape({
  weight: Yup.number()
    .min(20, "Weight must be at least 20 kg")
    .max(300, "Weight seems too high")
    .required("Weight is required"),
  height: Yup.number()
    .min(100, "Height must be at least 100 cm")
    .max(250, "Height seems too high")
    .required("Height is required"),
  cycle_regularity: Yup.number()
    .oneOf([2, 4], "Please select cycle regularity")
    .required("Cycle regularity is required"),
  cycle_length: Yup.number()
    .min(0, "Cycle length must be positive")
    .max(60, "Cycle length must be 60 or less")
    .required("Cycle length is required"),
  weight_gain: Yup.number()
    .oneOf([0, 1], "Please select yes or no")
    .required("Required"),
  hair_growth: Yup.number()
    .oneOf([0, 1], "Please select yes or no")
    .required("Required"),
  skin_darkening: Yup.number()
    .oneOf([0, 1], "Please select yes or no")
    .required("Required"),
  hair_loss: Yup.number()
    .oneOf([0, 1], "Please select yes or no")
    .required("Required"),
  pimples: Yup.number()
    .oneOf([0, 1], "Please select yes or no")
    .required("Required"),
  fast_food: Yup.number()
    .oneOf([0, 1], "Please select yes or no")
    .required("Required"),
  reg_exercise: Yup.number()
    .oneOf([0, 1], "Please select yes or no")
    .required("Required"),
});

// Stage 2: Clinical confirmation (hormones + ultrasound)
export const stage2Schema = Yup.object().shape({
  fsh: Yup.number()
    .min(0, "FSH must be positive")
    .required("FSH level is required"),
  lh: Yup.number()
    .min(0, "LH must be positive")
    .required("LH level is required"),
  amh: Yup.number()
    .min(0, "AMH must be positive")
    .required("AMH level is required"),
  tsh: Yup.number().min(0, "TSH must be positive").nullable(),
  follicle_no_l: Yup.number()
    .min(0, "Must be 0 or more")
    .required("Left follicle count is required"),
  follicle_no_r: Yup.number()
    .min(0, "Must be 0 or more")
    .required("Right follicle count is required"),
  avg_f_size_l: Yup.number()
    .min(0, "Must be positive")
    .required("Left follicle size is required"),
  avg_f_size_r: Yup.number()
    .min(0, "Must be positive")
    .required("Right follicle size is required"),
  endometrium: Yup.number().min(0, "Must be positive").nullable(),
  hip: Yup.number().min(0, "Must be positive").nullable(),
  waist: Yup.number().min(0, "Must be positive").nullable(),
});
