import { createContext, useContext, ReactNode } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

interface AuthContextType {
  user: any | null;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const { data: user, isLoading } = useQuery({
    queryKey: ["user"],
    queryFn: async () => {
      const token = localStorage.getItem("token");
      if (!token) return null;

      const response = await fetch("/api/user/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        localStorage.removeItem("token");
        throw new Error("Failed to get user");
      }
      return response.json();
    },
  });

  const loginMutation = useMutation({
    mutationFn: async (credentials: { username: string; password: string }) => {
      const response = await fetch("/api/user.login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
      });
      if (!response.ok) {
        throw new Error("Invalid credentials");
      }
      return response.json();
    },
    onSuccess: (data) => {
      localStorage.setItem("token", data.access_token);
      queryClient.invalidateQueries({ queryKey: ["user"] });
      navigate("/");
      toast.success("Successfully logged in");
    },
    onError: (error: Error) => {
      toast.error(error.message);
    },
  });

  const logout = () => {
    localStorage.removeItem("token");
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

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
