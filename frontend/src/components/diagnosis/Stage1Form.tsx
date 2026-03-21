"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Formik, Form } from "formik";
import toast from "react-hot-toast";
import { stage1Schema } from "@/validations/diagnosisValidation";
import { diagnosisService } from "@/services/diagnosisService";
import { getErrorMessage } from "@/services/api";
import Input from "@/components/ui/Input";
import Select from "@/components/ui/Select";
import Button from "@/components/ui/Button";

interface Stage1FormProps {
  patientId: number;
  patientName: string;
}

const yesNoOptions = [
  { value: 1, label: "Yes" },
  { value: 0, label: "No" },
];

const cycleOptions = [
  { value: 2, label: "Regular" },
  { value: 4, label: "Irregular" },
];

export default function Stage1Form({
  patientId,
  patientName,
}: Stage1FormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();

  const initialValues = {
    weight: "",
    height: "",
    cycle_regularity: "",
    cycle_length: "",
    weight_gain: "",
    hair_growth: "",
    skin_darkening: "",
    hair_loss: "",
    pimples: "",
    fast_food: "",
    reg_exercise: "",
  };

  const handleSubmit = async (values: typeof initialValues) => {
    setIsSubmitting(true);
    try {
      // Convert string values to numbers for the API
      const payload = {
        weight: Number(values.weight),
        height: Number(values.height),
        cycle_regularity: Number(values.cycle_regularity),
        cycle_length: Number(values.cycle_length),
        weight_gain: Number(values.weight_gain),
        hair_growth: Number(values.hair_growth),
        skin_darkening: Number(values.skin_darkening),
        hair_loss: Number(values.hair_loss),
        pimples: Number(values.pimples),
        fast_food: Number(values.fast_food),
        regular_exercise: Number(values.reg_exercise),
      };

      const result = await diagnosisService.runStage1(patientId, payload);
      toast.success("Screening complete!");
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
            Stage 1: Non-Invasive Screening
          </h2>
          <p className="text-base-content/60 text-sm">
            Patient: <span className="font-medium">{patientName}</span>
          </p>
        </div>

        <Formik
          initialValues={initialValues}
          validationSchema={stage1Schema}
          onSubmit={handleSubmit}
        >
          <Form className="space-y-6">
            {/* Section A: Vitals */}
            <div>
              <h3 className="text-sm font-semibold text-primary uppercase tracking-wider mb-3">
                Vitals & History
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="Weight (kg)"
                  name="weight"
                  type="number"
                  placeholder="e.g. 65"
                />
                <Input
                  label="Height (cm)"
                  name="height"
                  type="number"
                  placeholder="e.g. 165"
                />
                <Select
                  label="Cycle Regularity"
                  name="cycle_regularity"
                  options={cycleOptions}
                />
                <Input
                  label="Cycle Length (days)"
                  name="cycle_length"
                  type="number"
                  placeholder="e.g. 28"
                />
              </div>
            </div>

            <div className="divider"></div>

            {/* Section B: Physical Signs */}
            <div>
              <h3 className="text-sm font-semibold text-primary uppercase tracking-wider mb-3">
                Physical Signs
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <Select
                  label="Weight Gain"
                  name="weight_gain"
                  options={yesNoOptions}
                />
                <Select
                  label="Excess Hair Growth"
                  name="hair_growth"
                  options={yesNoOptions}
                />
                <Select
                  label="Skin Darkening"
                  name="skin_darkening"
                  options={yesNoOptions}
                />
                <Select
                  label="Hair Loss"
                  name="hair_loss"
                  options={yesNoOptions}
                />
                <Select
                  label="Acne / Pimples"
                  name="pimples"
                  options={yesNoOptions}
                />
                <Select
                  label="Fast Food Regularly"
                  name="fast_food"
                  options={yesNoOptions}
                />
                <Select
                  label="Regular Exercise"
                  name="reg_exercise"
                  options={yesNoOptions}
                />
              </div>
            </div>

            <div className="flex gap-3 pt-4">
              <Button type="submit" loading={isSubmitting}>
                Analyze Risk
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
