import "./App.css";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "react-hot-toast";
import { Login } from "./pages/Login";
import { Dashboard } from "./pages/Dashboard";
import { Layout } from "./components/Layout";
import { AuthProvider } from "./hooks";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { Servers } from "./pages/Servers";
import { Projects } from "./pages/Projects";
import { Users } from "./pages/Users";
import { Chat } from "./pages/Chat";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <ThemeProvider theme={darkTheme}>
          <CssBaseline />
          <AuthProvider>
            <Toaster
              position="top-right"
              toastOptions={{
                style: {
                  background: "#333",
                  color: "#fff",
                },
              }}
            />
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route
                path="/"
                element={
                  <ProtectedRoute>
                    <Layout />
                  </ProtectedRoute>
                }
              >
                <Route index element={<Dashboard />} />
                <Route path="chat" element={<Chat />} />
                <Route path="servers" element={<Servers />} />
                <Route path="projects" element={<Projects />} />
                <Route path="users" element={<Users />} />
              </Route>
            </Routes>
          </AuthProvider>
        </ThemeProvider>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
