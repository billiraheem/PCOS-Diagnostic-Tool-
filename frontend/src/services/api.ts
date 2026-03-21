import axios, { AxiosError } from "axios";
import Cookies from "js-cookie";
import { API_URL } from "@/utils/constants";

//  a single Axios instance with default settings
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Automatically attach token to every request
api.interceptors.request.use(
  (config) => {
    const token = Cookies.get("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Handle 401 errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid — clear cookie and redirect to login
      Cookies.remove("access_token");
      if (typeof window !== "undefined") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  },
);

export default api;

export const getErrorMessage = (error: unknown): string => {
  if (error instanceof AxiosError) {
    const detail = error.response?.data?.detail;

    // Pydantic validation errors return detail as an array of objects
    if (Array.isArray(detail)) {
      return detail
        .map((err: { loc?: string[]; msg?: string }) => {
          const field = err.loc?.slice(-1)[0] || "field";
          return `${field}: ${err.msg}`;
        })
        .join(", ");
    }

    // Simple string error
    if (typeof detail === "string") {
      return detail;
    }

    return error.message || "Something went wrong";
  }
  return "An unexpected error occurred";
};

export const apiGet = async <T>(url: string): Promise<T> => {
  const response = await api.get<T>(url);
  return response.data;
};

export const apiPost = async <T>(url: string, data?: unknown): Promise<T> => {
  const response = await api.post<T>(url, data);
  return response.data;
};

export const apiPut = async <T>(url: string, data?: unknown): Promise<T> => {
  const response = await api.put<T>(url, data);
  return response.data;
};

export const apiDelete = async <T>(url: string): Promise<T> => {
  const response = await api.delete<T>(url);
  return response.data;
};
