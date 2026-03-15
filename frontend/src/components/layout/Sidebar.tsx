"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import {
  LayoutDashboard,
  Users,
  Stethoscope,
  Shield,
  LogOut,
} from "lucide-react";

interface NavItem {
  href: string;
  label: string;
  icon: React.ReactNode;
  adminOnly?: boolean;
}

const navItems: NavItem[] = [
  {
    href: "/dashboard",
    label: "Dashboard",
    icon: <LayoutDashboard size={20} />,
  },
  { href: "/patients", label: "Patients", icon: <Users size={20} /> },
  {
    href: "/admin/users",
    label: "User Management",
    icon: <Shield size={20} />,
    adminOnly: true,
  },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { user, isAdmin, logout } = useAuth();

  return (
    <aside className="w-64 min-h-screen bg-base-200 border-r border-base-300 flex flex-col">
      {/* Logo / Brand */}
      <div className="p-5 border-b border-base-300">
        <Link href="/dashboard" className="flex items-center gap-2">
          <Stethoscope size={28} className="text-primary" />
          <span className="text-lg font-bold text-base-content">PCOS Tool</span>
        </Link>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 p-4">
        <ul className="menu gap-1">
          {navItems
            .filter((item) => !item.adminOnly || isAdmin)
            .map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={pathname.startsWith(item.href) ? "active" : ""}
                >
                  {item.icon}
                  {item.label}
                </Link>
              </li>
            ))}
        </ul>
      </nav>

      {/* User Info + Logout */}
      <div className="p-4 border-t border-base-300">
        <div className="flex items-center gap-3 mb-3 px-2">
          <div className="avatar placeholder">
            <div className="bg-primary text-primary-content rounded-full w-9">
              <span className="text-sm">
                {user?.full_name?.charAt(0)?.toUpperCase() || "U"}
              </span>
            </div>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">
              {user?.full_name || "User"}
            </p>
            <p className="text-xs text-base-content/60 truncate">
              {user?.email}
            </p>
          </div>
        </div>
        <button
          onClick={logout}
          className="btn btn-ghost btn-sm w-full justify-start gap-2"
        >
          <LogOut size={16} />
          Logout
        </button>
      </div>
    </aside>
  );
}
