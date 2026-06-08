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

export default function PieChart({ summary }: Props) {
  const labels = ["Neutral", "Negative", "Positive"];

  const values = [
    Number(summary?.neutral ?? 0),
    Number(summary?.negative ?? 0),
    Number(summary?.positive ?? 0),
  ];

  const total = values.reduce((sum, value) => sum + value, 0);

  const data = {
    labels,

    datasets: [
      {
        data: values,

        backgroundColor: [
          "#828282", 
          "#ef4444", 
          "#22c55e",
        ],
        borderColor: "#1e293b",

        borderWidth: 2,
      },
    ],
  };

  const options: ChartOptions<"pie"> = {
    responsive: true,
    rotation: 0,
    maintainAspectRatio: false,

    plugins: {
      legend: {
        position: "bottom",

        labels: {
          color: "#ffffff",
          padding: 20,

          font: {
            size: 14,
          },
        },
      },

      tooltip: {
        callbacks: {
          label: (context: TooltipItem<"pie">) => {
            const value = Number(context.raw);

            const percent = ((value / total) * 100).toFixed(1);

            return `${context.label}: ${value.toLocaleString()} (${percent}%)`;
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
                {values[index].toLocaleString()} ({percent}%)
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
