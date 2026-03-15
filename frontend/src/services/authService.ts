import Cookies from "js-cookie";
import { apiPost, apiGet } from "@/services/api";
import {
  LoginPayload,
  RegisterPayload,
  TokenResponse,
  User,
} from "@/interfaces/auth";

export const authService = {
  register: (data: RegisterPayload) => {
    return apiPost<User>("/api/auth/register", data);
  },

  login: async (data: LoginPayload) => {
    const response = await apiPost<TokenResponse>("/api/auth/login/json", data);
    Cookies.set("access_token", response.access_token, { expires: 1 }); // 1 day
    return response;
  },

  // Get the current logged-in user
  getMe: () => {
    return apiGet<User>("/api/auth/me");
  },

  logout: () => {
    Cookies.remove("access_token");
    window.location.href = "/login";
  },

  isAuthenticated: (): boolean => {
    return !!Cookies.get("access_token");
  },
};
