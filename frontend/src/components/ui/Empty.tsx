import { ClipboardList, LucideIcon } from "lucide-react";

interface EmptyProps {
  title?: string;
  description?: string;
  Icon?: LucideIcon;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export default function Empty({
  title = "No data found",
  description = "There's nothing here yet.",
  Icon = ClipboardList,
  action,
}: EmptyProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <Icon size={48} className="text-base-content/30 mb-4" />
      <h3 className="text-lg font-semibold text-base-content">{title}</h3>
      <p className="text-base-content/60 mt-1 max-w-md">{description}</p>
      {action && (
        <button
          onClick={action.onClick}
          className="btn btn-primary btn-sm mt-4"
        >
          {action.label}
        </button>
      )}
    </div>
  );
}
