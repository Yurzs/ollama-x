import { ReactNode } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { AuthContextType, User } from "./authTypes";
import { AuthContext } from "./AuthContext";
import { UserService, OpenAPI } from "../client";

export function AuthProvider({ children }: { children: ReactNode }) {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  // Initialize token from localStorage
  const storedToken = localStorage.getItem("token");
  if (storedToken) {
    OpenAPI.TOKEN = storedToken;
  }

  const { data: user = null, isLoading } = useQuery<User | null>({
    queryKey: ["user"],
    queryFn: async () => {
      try {
        if (!OpenAPI.TOKEN) {
          return null;
        }
        return await UserService.readUsersMe();
      } catch {
        localStorage.removeItem("token");
        OpenAPI.TOKEN = undefined;
        return null;
      }
    },
  });

  const loginMutation = useMutation({
    mutationFn: async (credentials: {
      username: string;
      password: string;
    }): Promise<User> => {
      const token = await UserService.loginForAccessToken({
        username: credentials.username,
        password: credentials.password,
      });

      // Store token and update OpenAPI config
      const accessToken = token.access_token;
      localStorage.setItem("token", accessToken);
      OpenAPI.TOKEN = accessToken;

      return await UserService.readUsersMe();
    },
    onSuccess: (userData) => {
      queryClient.setQueryData(["user"], userData);
      toast.success("Successfully logged in");
      navigate("/chat");
    },
    onError: (error: Error) => {
      localStorage.removeItem("token");
      OpenAPI.TOKEN = undefined;
      toast.error(error.message);
    },
  });

  const logout = () => {
    localStorage.removeItem("token");
    OpenAPI.TOKEN = undefined;
    queryClient.setQueryData(["user"], null);
    navigate("/login");
    toast.success("Successfully logged out");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        login: (username: string, password: string) =>
          loginMutation.mutateAsync({ username, password }),
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export type { AuthContextType, User };
