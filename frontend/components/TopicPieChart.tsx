"use client";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  TooltipItem,
  ChartOptions,
} from "chart.js";

import { Pie } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

type Props = {
  summary: Record<string, number>;
};

export default function TopicPieChart({ summary }: Props) {
  const labels = Object.keys(summary);

  const values = Object.values(summary).map(Number);

  const total = values.reduce((a, b) => a + b, 0);

  const colorMap: Record<string, string> = {
    "Kendala Login dan Akses": "#8b5cf6",
    "Permasalahan Sistem Aplikasi": "#ef4444",
    "Layanan Transaksi Perbankan": "#22c55e",
    "Kemudahan dan Kepuasan Pengguna": "#3b82f6",
    "Topik Umum Pengguna": "#6b7280",
  };

  const backgroundColor = labels.map((label) => colorMap[label] ?? "#f59e0b");

  const data = {
    labels,

    datasets: [
      {
        data: values,

        backgroundColor,

        borderColor: "#1e293b",

        borderWidth: 2,
      },
    ],
  };

  const options: ChartOptions<"pie"> = {
    responsive: true,

    maintainAspectRatio: false,

    plugins: {
      legend: {
        position: "bottom",

        labels: {
          color: "#ffffff",

          padding: 20,
        },
      },

      tooltip: {
        callbacks: {
          label: (context: TooltipItem<"pie">) => {
            const value = Number(context.raw);

            const percent = ((value / total) * 100).toFixed(1);

            return `${context.label}: ${value} (${percent}%)`;
          },
        },
      },
    },
  };

  return (
    <div className="w-full">
      <div className="h-87.5">
        <Pie data={data} options={options} />
      </div>

      <div className="mt-4 space-y-2">
        {labels.map((label, index) => {
          const percent = ((values[index] / total) * 100).toFixed(1);

          return (
            <div key={label} className="flex justify-between text-sm">
              <span>{label}</span>

              <span>
                {values[index]} ({percent}%)
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
