"use client";

import { useAuth } from "@/context/AuthContext";
import ThemeSwitcher from "@/components/ui/ThemeSwitcher";
import { Menu } from "lucide-react";

interface NavbarProps {
  onMenuClick?: () => void;
}

export default function Navbar({ onMenuClick }: NavbarProps) {
  const { user, isAdmin } = useAuth();

  return (
    <header className="navbar bg-base-100 border-b border-base-300 px-6">
      {/* Mobile menu button */}
      <div className="flex-none lg:hidden">
        <button onClick={onMenuClick} className="btn btn-ghost btn-circle">
          <Menu size={20} />
        </button>
      </div>

      {/* Spacer */}
      <div className="flex-1">
        <h2 className="text-lg font-semibold lg:hidden">PCOS Tool</h2>
      </div>

      {/* Right side: role badge + theme switcher */}
      <div className="flex items-center gap-3">
        {isAdmin && <span className="badge badge-primary badge-sm">Admin</span>}
        <span className="text-sm text-base-content/70 hidden sm:inline">
          {user?.full_name}
        </span>
        <ThemeSwitcher />
      </div>
    </header>
  );
}
