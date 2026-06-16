"use client";

import { useEffect, useState } from "react";
import {
  Upload,
  MessageSquare,
  Smile,
  Meh,
  Frown,
  BarChart3,
  Brain,
} from "lucide-react";

import PieChart from "@/components/PieChart";
import BarChart from "@/components/BarChart";
import { uploadDataset } from "@/services/api";

type TopicType = {
  topic: number;
  title: string;
  keywords: string[];
};

type ResultType = {
  summary: Record<string, number>;
  topics: TopicType[];
  results: {
    review: string;
    sentiment: string;
    score: number;
  }[];
};

export default function Home() {
 const [result, setResult] = useState<ResultType | null>(null);
 const [loading, setLoading] = useState(false);

 useEffect(() => {
   const saved = localStorage.getItem("analysis_result");

   if (saved) {
     // eslint-disable-next-line react-hooks/set-state-in-effect
     setResult(JSON.parse(saved));
   }
 }, []);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;

    const file = e.target.files[0];

    setLoading(true);

    try {
      const data = await uploadDataset(file);

      setResult(data);

      localStorage.setItem("analysis_result", JSON.stringify(data));
    } catch (error) {
      console.error(error);
      alert("Gagal memproses dataset");
    }

    setLoading(false);
  };

  const positive = result?.summary?.positive || 0;
  const neutral = result?.summary?.neutral || 0;
  const negative = result?.summary?.negative || 0;
  const total = result?.results?.length || 0;

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-950 via-slate-900 to-slate-950 text-white">
      {/* HEADER */}
      <div className="border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-8 py-6 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold">OCTO Mobile Dashboard</h1>

            <p className="text-slate-400 mt-2">
              Analisis Sentimen Menggunakan IndoBERT & LDA
            </p>
          </div>

          <div className="flex gap-3">
            <label className="cursor-pointer bg-violet-600 hover:bg-violet-700 transition px-5 py-3 rounded-xl flex items-center gap-2">
              <Upload size={18} />
              Upload Dataset
              <input type="file" className="hidden" onChange={handleUpload} />
            </label>

            <button
              onClick={() => {
                localStorage.removeItem("analysis_result");

                setResult(null);
              }}
              className="bg-red-600 hover:bg-red-700 transition px-5 py-3 rounded-xl"
            >
              Reset
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto p-8">
        {/* LOADING */}
        {loading && (
          <div className="bg-slate-800 rounded-2xl p-8 text-center">
            <p className="text-xl font-semibold">Memproses Dataset...</p>
          </div>
        )}

        {/* DASHBOARD */}
        {result && (
          <>
            {/* CARD SUMMARY */}

            <div className="grid md:grid-cols-4 gap-5 mb-8">
              <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-slate-400">Total Ulasan</p>

                    <h2 className="text-4xl font-bold mt-2">{total}</h2>
                  </div>

                  <MessageSquare size={40} className="text-violet-400" />
                </div>
              </div>

              <div className="bg-green-900/20 border border-green-500 rounded-2xl p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-green-400">Positif</p>

                    <h2 className="text-4xl font-bold mt-2">{positive}</h2>
                  </div>

                  <Smile size={40} className="text-green-400" />
                </div>
              </div>

              <div className="bg-slate-500/20 border border-slate-400 rounded-2xl p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-slate-300">Netral</p>

                    <h2 className="text-4xl font-bold mt-2 text-white">
                      {neutral}
                    </h2>
                  </div>

                  <Meh size={40} className="text-slate-300" />
                </div>
              </div>

              <div className="bg-red-900/20 border border-red-500 rounded-2xl p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-red-400">Negatif</p>

                    <h2 className="text-4xl font-bold mt-2">{negative}</h2>
                  </div>

                  <Frown size={40} className="text-red-400" />
                </div>
              </div>
            </div>

            {/* CHART */}

            <div className="grid lg:grid-cols-2 gap-6 mb-8">
              <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700">
                <div className="flex items-center gap-2 mb-5">
                  <BarChart3 size={22} />

                  <h2 className="text-xl font-bold">Distribusi Sentimen</h2>
                </div>

                <div className="max-w-md mx-auto">
                  <PieChart summary={result.summary} />
                </div>
              </div>

              <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700">
                <div className="flex items-center gap-2 mb-5">
                  <BarChart3 size={22} />

                  <h2 className="text-xl font-bold">Perbandingan Sentimen</h2>
                </div>

                <BarChart summary={result.summary} />
              </div>
            </div>

            {/* TOPIC MODELING */}

            <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700 mb-8">
              <div className="flex items-center gap-2 mb-6">
                <Brain size={22} className="text-violet-400" />

                <h2 className="text-xl font-bold">Topic Modeling (LDA)</h2>
              </div>

              <div className="space-y-4">
                {result.topics.map((topic, index) => (
                  <div key={index} className="bg-slate-700 rounded-xl p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-bold text-violet-400 text-lg">
                        Topik {topic.topic}
                      </h3>

                      <span className="bg-violet-500/20 text-violet-300 px-3 py-1 rounded-full text-sm">
                        {topic.title}
                      </span>
                    </div>

                    <div className="flex flex-wrap gap-2">
                      {topic.keywords.map((word: string, idx: number) => (
                        <span
                          key={idx}
                          className="bg-violet-600 px-3 py-1 rounded-full text-sm"
                        >
                          {word}
                        </span>
                      ))}
                    </div>
                    <p className="mt-4 text-slate-300 text-sm border-t border-slate-600 pt-3">
                      <span className="font-semibold text-white">
                        Interpretasi:
                      </span>{" "}
                      {topic.title}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* TABEL */}

            <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700">
              <h2 className="text-2xl font-bold mb-6">
                Hasil Analisis Sentimen
              </h2>

              <div className="overflow-auto max-h-150">
                <table className="w-full">
                  <thead className="sticky top-0 bg-slate-900">
                    <tr>
                      <th className="text-left p-4">Review</th>

                      <th className="text-left p-4">Sentimen</th>

                      <th className="text-left p-4">Score</th>
                    </tr>
                  </thead>

                  <tbody>
                    {result.results.map((item, index) => (
                      <tr key={index} className="border-t border-slate-700">
                        <td className="p-4">{item.review}</td>

                        <td className="p-4">
                          <span
                            className={
                              item.sentiment === "positive"
                                ? "text-green-400 font-semibold"
                                : item.sentiment === "negative"
                                  ? "text-red-400 font-semibold"
                                  : "text-yellow-400 font-semibold"
                            }
                          >
                            {item.sentiment}
                          </span>
                        </td>

                        <td className="p-4">{item.score.toFixed(4)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
