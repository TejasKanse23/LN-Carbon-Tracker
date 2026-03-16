import Axios from "axios";

// In production (Vercel), VITE_API_URL points to the Render backend.
// Locally, it falls back to "/" so the Vite dev proxy continues to work.
const axiosInstance = Axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/",
  headers: {
    "Content-Type": "application/json",
    "Cache-Control": "no-store, max-age=0",
    "X-Content-Type-Options": "nosniff",
  },
});

axiosInstance.interceptors.request.use(
  (config) => {
    if (config.url) {
      config.url = config.url.replace(/([^:]\/)\/+/g, "$1");
    }
    return config;
  },
  (error) => Promise.reject(error)
);

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Request Error:", error);
    return Promise.reject(error);
  }
);

export default axiosInstance;
