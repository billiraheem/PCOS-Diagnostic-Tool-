"use client";

import { useState, useEffect } from "react";
import { Palette } from "lucide-react";
import { THEMES } from "@/utils/constants";

export default function ThemeSwitcher() {
  const [currentTheme, setCurrentTheme] = useState("valentine");

  // Load saved theme on mount
  useEffect(() => {
    const saved = localStorage.getItem("theme") || "valentine";
    setCurrentTheme(saved);
    document.documentElement.setAttribute("data-theme", saved);
  }, []);

  const handleThemeChange = (theme: string) => {
    setCurrentTheme(theme);
    localStorage.setItem("theme", theme);
    document.documentElement.setAttribute("data-theme", theme);
  };

  return (
    <div className="dropdown dropdown-end">
      <div tabIndex={0} role="button" className="btn btn-ghost btn-circle">
        <Palette size={20} />
      </div>
      <ul
        tabIndex={0}
        className="dropdown-content z-[1] menu p-2 shadow-lg bg-base-200 rounded-box w-44 max-h-80 overflow-y-auto"
      >
        {THEMES.map((theme) => (
          <li key={theme.name}>
            <button
              onClick={() => handleThemeChange(theme.name)}
              className={currentTheme === theme.name ? "active" : ""}
            >
              {theme.label}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
