import { createContext, useContext, useState } from "react";
import api from "../api/client";

const AuthContext = createContext(null);
export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const guardar = (nuevo) => {
    localStorage.setItem("token", nuevo);
    setToken(nuevo);
  };

  const login = async (username, password) => {
    const { data } = await api.post("/auth/login/", { username, password });
    guardar(data.token);
  };

  const registro = async (username, email, password) => {
    const { data } = await api.post("/auth/registro/", { username, email, password });
    guardar(data.token);
  };

  const logout = async () => {
    try { await api.post("/auth/logout/"); } catch { /* el token pudo haber expirado */ }
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, login, registro, logout }}>{children}</AuthContext.Provider>
  );
}
