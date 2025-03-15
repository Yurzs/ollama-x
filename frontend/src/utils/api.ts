import axios from "axios";
import toast from "react-hot-toast";

const api = axios.create({
  baseURL: "/api",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
      toast.error("Session expired. Please login again.");
    } else {
      toast.error(error.response?.data?.detail || "An error occurred");
    }
    return Promise.reject(error);
  }
);

export default api;
