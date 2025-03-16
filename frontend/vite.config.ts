import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: true,
    port: 3000,
    proxy: {
      "/api": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
      "/ollama": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
      "/continue": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
    },
  },
});
