export const formatDate = (dateString: string | Date): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

export const getRiskBadgeClass = (riskLevel: string): string => {
  switch (riskLevel?.toUpperCase()) {
    case "HIGH":
      return "badge-error";
    case "MODERATE":
      return "badge-warning";
    case "LOW":
      return "badge-success";
    default:
      return "badge-ghost";
  }
};

export const formatProbability = (probability: number): string => {
  return `${(probability * 100).toFixed(1)}%`;
};

export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + "...";
};

export const getRiskLevel = (probability: number): string => {
  if (probability >= 0.7) return "HIGH";
  if (probability >= 0.3) return "MODERATE";
  return "LOW";
};
