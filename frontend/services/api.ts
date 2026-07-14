import axios from "axios";

const API = "http://127.0.0.1:8000";

export const uploadDataset = async (file: File) => {

  const formData = new FormData();

  formData.append("file", file);

  const response = await axios.post(
    `${API}/analyze`,
    formData
  );

  return response.data;
};

export async function scrapeDataset(
  reviewCount: number,
  newest: boolean,
  startDate?: string,
  endDate?: string,
) {
  return fetch("http://127.0.0.1:8000/scrape", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      review_count: reviewCount,
      newest,
      start_date: startDate,
      end_date: endDate,
    }),
  });
}