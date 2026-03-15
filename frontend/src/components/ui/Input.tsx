import { useField } from "formik";

interface InputProps {
  label: string;
  name: string;
  type?: string;
  placeholder?: string;
  disabled?: boolean;
}

export default function Input({ label, ...props }: InputProps) {
  // useField connects this input to Formik's form state
  const [field, meta] = useField(props.name);

  return (
    <div className="form-control w-full">
      <label className="label">
        <span className="label-text font-medium">{label}</span>
      </label>
      <input
        {...field}
        {...props}
        className={`input input-bordered w-full ${
          meta.touched && meta.error ? "input-error" : ""
        }`}
      />
      {meta.touched && meta.error && (
        <label className="label">
          <span className="label-text-alt text-error">{meta.error}</span>
        </label>
      )}
    </div>
  );
}
