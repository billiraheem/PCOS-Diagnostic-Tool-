"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Formik, Form } from "formik";
import toast from "react-hot-toast";
import { stage2Schema } from "@/validations/diagnosisValidation";
import { diagnosisService } from "@/services/diagnosisService";
import { getErrorMessage } from "@/services/api";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";

interface Stage2FormProps {
  diagnosisId: number;
  patientName: string;
}

export default function Stage2Form({
  diagnosisId,
  patientName,
}: Stage2FormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();

  const initialValues = {
    fsh: "",
    lh: "",
    amh: "",
    tsh: "",
    follicle_no_l: "",
    follicle_no_r: "",
    avg_f_size_l: "",
    avg_f_size_r: "",
    endometrium: "",
    hip: "",
    waist: "",
  };

  const handleSubmit = async (values: typeof initialValues) => {
    setIsSubmitting(true);
    try {
      const payload = {
        fsh: Number(values.fsh),
        lh: Number(values.lh),
        amh: Number(values.amh),
        tsh: values.tsh ? Number(values.tsh) : undefined,
        follicle_l: Number(values.follicle_no_l),
        follicle_r: Number(values.follicle_no_r),
        avg_f_size_l: Number(values.avg_f_size_l),
        avg_f_size_r: Number(values.avg_f_size_r),
        endometrium: values.endometrium
          ? Number(values.endometrium)
          : undefined,
        hip: values.hip ? Number(values.hip) : undefined,
        waist: values.waist ? Number(values.waist) : undefined,
      };

      const result = await diagnosisService.runStage2(diagnosisId, payload);
      toast.success("Diagnosis confirmed!");
      router.push(`/diagnosis/${result.id}`);
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="card bg-base-100 shadow-sm border border-base-300 max-w-3xl mx-auto">
      <div className="card-body">
        <div className="mb-4">
          <h2 className="text-lg font-semibold">
            Stage 2: Clinical Confirmation
          </h2>
          <p className="text-base-content/60 text-sm">
            Patient: <span className="font-medium">{patientName}</span>
          </p>
          <div className="alert alert-info mt-3 text-sm">
            <span>
              Enter the patient&apos;s lab results and ultrasound data to
              confirm the diagnosis.
            </span>
          </div>
        </div>

        <Formik
          initialValues={initialValues}
          validationSchema={stage2Schema}
          onSubmit={handleSubmit}
        >
          <Form className="space-y-6">
            {/* Hormonal Data */}
            <div>
              <h3 className="text-sm font-semibold text-primary uppercase tracking-wider mb-3">
                Hormonal Panel
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="FSH (mIU/mL)"
                  name="fsh"
                  type="number"
                  placeholder="e.g. 5.2"
                />
                <Input
                  label="LH (mIU/mL)"
                  name="lh"
                  type="number"
                  placeholder="e.g. 12.1"
                />
                <Input
                  label="AMH (ng/mL)"
                  name="amh"
                  type="number"
                  placeholder="e.g. 3.5"
                />
                <Input
                  label="TSH (mIU/L) — Optional"
                  name="tsh"
                  type="number"
                  placeholder="e.g. 2.1"
                />
              </div>
            </div>

            <div className="divider"></div>

            {/* Ultrasound Data */}
            <div>
              <h3 className="text-sm font-semibold text-primary uppercase tracking-wider mb-3">
                Ultrasound Data
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="Follicle Count (Left)"
                  name="follicle_no_l"
                  type="number"
                  placeholder="e.g. 12"
                />
                <Input
                  label="Follicle Count (Right)"
                  name="follicle_no_r"
                  type="number"
                  placeholder="e.g. 10"
                />
                <Input
                  label="Avg Follicle Size Left (mm)"
                  name="avg_f_size_l"
                  type="number"
                  placeholder="e.g. 4.5"
                />
                <Input
                  label="Avg Follicle Size Right (mm)"
                  name="avg_f_size_r"
                  type="number"
                  placeholder="e.g. 5.0"
                />
                <Input
                  label="Endometrium (mm) — Optional"
                  name="endometrium"
                  type="number"
                  placeholder="e.g. 8.2"
                />
              </div>
            </div>

            <div className="divider"></div>

            {/* Body Measurements (Optional) */}
            <div>
              <h3 className="text-sm font-semibold text-primary uppercase tracking-wider mb-3">
                Body Measurements (Optional)
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="Hip (inches)"
                  name="hip"
                  type="number"
                  placeholder="e.g. 38"
                />
                <Input
                  label="Waist (inches)"
                  name="waist"
                  type="number"
                  placeholder="e.g. 32"
                />
              </div>
            </div>

            <div className="flex gap-3 pt-4">
              <Button type="submit" loading={isSubmitting}>
                Confirm Diagnosis
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
