"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { ShapFeature } from "@/interfaces/diagnosis";

interface ShapChartProps {
  data: ShapFeature[];
}

export default function ShapChart({ data }: ShapChartProps) {
  if (!data || data.length === 0) return null;

  // Sort by absolute impact (most impactful first)
  const sortedData = [...data]
    .sort((a, b) => Math.abs(b.impact) - Math.abs(a.impact))
    .slice(0, 10); // Top 10 features

  return (
    <div className="w-full">
      <h3 className="text-sm font-semibold text-primary uppercase tracking-wider mb-3">
        Feature Impact (SHAP Explanation)
      </h3>
      <p className="text-xs text-base-content/60 mb-4">
        Shows which features pushed the prediction towards positive (right) or
        negative (left)
      </p>
      <ResponsiveContainer width="100%" height={sortedData.length * 40 + 40}>
        <BarChart
          data={sortedData}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 120, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
          <XAxis type="number" tick={{ fontSize: 12 }} />
          <YAxis
            type="category"
            dataKey="feature"
            tick={{ fontSize: 12 }}
            width={110}
          />
          <Tooltip
            formatter={(value) => [Number(value).toFixed(4), "Impact"]}
            labelFormatter={(label) => `Feature: ${label}`}
          />
          <Bar dataKey="impact" radius={[0, 4, 4, 0]}>
            {sortedData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.impact > 0 ? "#ef4444" : "#22c55e"}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="flex justify-center gap-6 mt-2 text-xs">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded bg-[#ef4444]"></div>
          <span>Increases Risk</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded bg-[#22c55e]"></div>
          <span>Decreases Risk</span>
        </div>
      </div>
    </div>
  );
}
