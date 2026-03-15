export const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const THEMES = [
  { name: "valentine", label: "Valentine" },
  { name: "dark", label: "Dark" },
  { name: "cupcake", label: "Cupcake" },
  { name: "pastel", label: "Pastel" },
  { name: "wireframe", label: "Wireframe" },
  { name: "autumn", label: "Autumn" },
  { name: "forest", label: "Forest" },
  { name: "aqua", label: "Aqua" },
  { name: "lofi", label: "Lo-Fi" },
  { name: "fantasy", label: "Fantasy" },
  { name: "dracula", label: "Dracula" },
  { name: "cmyk", label: "CMYK" },
  { name: "lemonade", label: "Lemonade" },
  { name: "night", label: "Night" },
  { name: "coffee", label: "Coffee" },
  { name: "winter", label: "Winter" },
  { name: "dim", label: "Dim" },
  { name: "nord", label: "Nord" },
  { name: "sunset", label: "Sunset" },
];

export const RISK_THRESHOLDS = {
  HIGH: 0.7,
  MODERATE: 0.3,
};

export const ROLES = {
  ADMIN: "admin",
  CLINICIAN: "clinician",
} as const;
