import * as Yup from "yup";

export const patientSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, "Name must be at least 2 characters")
    .required("Patient name is required"),
  date_of_birth: Yup.string().required("Date of birth is required"),
  phone: Yup.string().nullable(),
  email: Yup.string().email("Please enter a valid email").nullable(),
  address: Yup.string().nullable(),
});
