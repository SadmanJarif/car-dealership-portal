import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Dev/preview proxy: the Django back end runs on 127.0.0.1:8000.
// Proxying makes API + form calls same-origin from the browser, so the
// Django session cookie (login) and CSRF token work for the add-review POST.
// In production set VITE_API_BASE_URL to the Django host instead.
const proxy = {
  "/api": "http://127.0.0.1:8000",
  "/dealer": "http://127.0.0.1:8000",
  "/login": "http://127.0.0.1:8000",
  "/logout": "http://127.0.0.1:8000",
  "/register": "http://127.0.0.1:8000",
};

export default defineConfig({
  plugins: [react()],
  server: { proxy, port: 5173 },
  preview: { proxy, port: 4173 },
});
