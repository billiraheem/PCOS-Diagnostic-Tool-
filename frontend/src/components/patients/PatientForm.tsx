"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Formik, Form } from "formik";
import toast from "react-hot-toast";
import { patientSchema } from "@/validations/patientValidation";
import { patientService } from "@/services/patientService";
import { getErrorMessage } from "@/services/api";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";

export default function PatientForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();

  const initialValues = {
    name: "",
    date_of_birth: "",
    phone: "",
    email: "",
    address: "",
  };

  const handleSubmit = async (values: typeof initialValues) => {
    setIsSubmitting(true);
    try {
      const patient = await patientService.create({
        name: values.name,
        date_of_birth: values.date_of_birth,
        phone: values.phone || undefined,
        email: values.email || undefined,
        address: values.address || undefined,
      });
      toast.success("Patient created successfully!");
      router.push(`/patients/${patient.id}`);
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="card bg-base-100 shadow-sm border border-base-300 max-w-2xl mx-auto">
      <div className="card-body">
        <Formik
          initialValues={initialValues}
          validationSchema={patientSchema}
          onSubmit={handleSubmit}
        >
          <Form className="space-y-4">
            <Input
              label="Full Name"
              name="name"
              placeholder="Patient's full name"
            />
            <Input label="Date of Birth" name="date_of_birth" type="date" />
            <Input label="Phone Number" name="phone" placeholder="Optional" />
            <Input
              label="Email Address"
              name="email"
              type="email"
              placeholder="Optional"
            />
            <Input label="Address" name="address" placeholder="Optional" />

            <div className="flex gap-3 pt-2">
              <Button type="submit" loading={isSubmitting}>
                Create Patient
              </Button>
              <Button variant="ghost" onClick={() => router.back()}>
                Cancel
              </Button>
            </div>
          </Form>
        </Formik>
      </div>
    </div>
  );
}
