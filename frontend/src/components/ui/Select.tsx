import { useField } from "formik";

interface SelectOption {
  value: string | number;
  label: string;
}

interface SelectProps {
  label: string;
  name: string;
  options: SelectOption[];
  disabled?: boolean;
}

export default function Select({ label, options, ...props }: SelectProps) {
  const [field, meta] = useField(props.name);

  return (
    <div className="form-control w-full">
      <label className="label">
        <span className="label-text font-medium">{label}</span>
      </label>
      <select
        {...field}
        {...props}
        className={`select select-bordered w-full ${
          meta.touched && meta.error ? "select-error" : ""
        }`}
      >
        <option value="">Select...</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {meta.touched && meta.error && (
        <label className="label">
          <span className="label-text-alt text-error">{meta.error}</span>
        </label>
      )}
    </div>
  );
}
