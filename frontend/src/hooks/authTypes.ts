import type { UserBase } from "../client";

export interface User {
  username: string;
  email: string;
  is_admin: boolean;
}

export interface AuthContextType {
  user: UserBase | null;
  isLoading: boolean;
  login: (token: string) => Promise<void>;
  logout: () => void;
}
