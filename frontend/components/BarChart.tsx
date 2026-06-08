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
  const labels = ["Positive", "Negative", "Neutral"];

  const values = [
    Number(summary?.positive ?? 0),
    Number(summary?.negative ?? 0),
    Number(summary?.neutral ?? 0),
  ];

  const total = values.reduce((sum, value) => sum + value, 0);

  const data = {
    labels,

    datasets: [
      {
        label: "Jumlah Sentimen",

        data: values,

        backgroundColor: ["#22c55e", "#ef4444", "#828282"],

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
    <div className="h-100">
      <Bar data={data} options={options} />
    </div>
  );
}
