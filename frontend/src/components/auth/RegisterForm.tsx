"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Formik, Form } from "formik";
import toast from "react-hot-toast";
import { Stethoscope } from "lucide-react";
import { registerSchema } from "@/validations/authValidation";
import { useAuth } from "@/context/AuthContext";
import { getErrorMessage } from "@/services/api";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";

export default function RegisterForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { register } = useAuth();
  const router = useRouter();

  const initialValues = {
    full_name: "",
    email: "",
    password: "",
    confirm_password: "",
  };

  const handleSubmit = async (values: typeof initialValues) => {
    setIsSubmitting(true);
    try {
      await register({
        full_name: values.full_name,
        email: values.email,
        password: values.password,
      });
      toast.success("Account created! Please sign in.");
      router.push("/login");
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="card bg-base-100 shadow-xl">
      <div className="card-body">
        {/* Header */}
        <div className="text-center mb-4">
          <Stethoscope size={40} className="text-primary mx-auto mb-2" />
          <h1 className="text-2xl font-bold">Create Account</h1>
          <p className="text-base-content/60 text-sm">
            Register as a clinician to start screening patients
          </p>
        </div>

        {/* Form */}
        <Formik
          initialValues={initialValues}
          validationSchema={registerSchema}
          onSubmit={handleSubmit}
        >
          <Form className="space-y-4">
            <Input
              label="Full Name"
              name="full_name"
              placeholder="Dr. Jane Doe"
            />
            <Input
              label="Email"
              name="email"
              type="email"
              placeholder="doctor@example.com"
            />
            <Input
              label="Password"
              name="password"
              type="password"
              placeholder="Min 6 characters"
            />
            <Input
              label="Confirm Password"
              name="confirm_password"
              type="password"
              placeholder="Re-enter password"
            />

            <Button type="submit" fullWidth loading={isSubmitting}>
              Create Account
            </Button>
          </Form>
        </Formik>

        {/* Login link */}
        <p className="text-center text-sm mt-4">
          Already have an account?{" "}
          <Link href="/login" className="link link-primary">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
