import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// El proxy envía /api al servidor de Django (puerto 8000) durante el desarrollo.
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, proxy: { "/api": "http://localhost:8000" } },
});
