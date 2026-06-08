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