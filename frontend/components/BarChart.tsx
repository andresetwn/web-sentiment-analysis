"use client";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions,
  TooltipItem,
} from "chart.js";

import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
);

type Props = {
  summary: Record<string, number>;
};

export default function BarChart({ summary }: Props) {
  const labels = ["Netral", "Negatif", "Positif"];

  const values = [
    Number(summary?.netral ?? 0),
    Number(summary?.negatif ?? 0),
    Number(summary?.positif ?? 0),
  ];

  const total = values.reduce((sum, value) => sum + value, 0);

  const data = {
    labels,

    datasets: [
      {
        label: "Jumlah Sentimen",

        data: values,

        backgroundColor: ["#828282", "#ef4444", "#22c55e"],

        borderRadius: 12,

        borderSkipped: false,
      },
    ],
  };

  const options: ChartOptions<"bar"> = {
    responsive: true,

    maintainAspectRatio: false,

    plugins: {
      legend: {
        display: false,
      },

      tooltip: {
        callbacks: {
          label: (context: TooltipItem<"bar">) => {
            const value = Number(context.raw);

            const percent = ((value / total) * 100).toFixed(1);

            return `${value.toLocaleString()} (${percent}%)`;
          },
        },
      },
    },

    scales: {
      x: {
        ticks: {
          color: "#ffffff",
        },

        grid: {
          display: false,
        },
      },

      y: {
        ticks: {
          color: "#94a3b8",
        },

        grid: {
          color: "#334155",
        },

        beginAtZero: true,
      },
    },
  };

  return (
    <div className="w-full">
      <div className="h-87.5">
        <Bar data={data} options={options} />
      </div>
      <div className="mt-4 space-y-2">
        {labels.map((label, index) => (
          <div
            key={label}
            className="flex justify-between items-center text-sm"
          >
            <span>{label}</span>

            <span>{values[index].toLocaleString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
