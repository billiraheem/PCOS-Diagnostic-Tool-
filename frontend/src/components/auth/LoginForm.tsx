"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Formik, Form } from "formik";
import toast from "react-hot-toast";
import { Stethoscope } from "lucide-react";
import { loginSchema } from "@/validations/authValidation";
import { useAuth } from "@/context/AuthContext";
import { getErrorMessage } from "@/services/api";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";

export default function LoginForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login } = useAuth();
  const router = useRouter();

  const initialValues = {
    email: "",
    password: "",
  };

  const handleSubmit = async (values: typeof initialValues) => {
    setIsSubmitting(true);
    try {
      await login({ email: values.email, password: values.password });
      toast.success("Welcome back!");
      router.push("/dashboard");
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
          <h1 className="text-2xl font-bold">Welcome Back</h1>
          <p className="text-base-content/60 text-sm">
            Sign in to your PCOS Diagnostic Tool account
          </p>
        </div>

        {/* Form */}
        <Formik
          initialValues={initialValues}
          validationSchema={loginSchema}
          onSubmit={handleSubmit}
        >
          <Form className="space-y-4">
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
              placeholder="Enter your password"
            />

            <Button type="submit" fullWidth loading={isSubmitting}>
              Sign In
            </Button>
          </Form>
        </Formik>

        {/* Register link */}
        <p className="text-center text-sm mt-4">
          Don&apos;t have an account?{" "}
          <Link href="/register" className="link link-primary">
            Create one
          </Link>
        </p>
      </div>
    </div>
  );
}
