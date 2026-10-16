import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navegar = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const enviar = async (e) => {
    e.preventDefault();
    try {
      await login(username, password);
      navegar("/");
    } catch {
      setError("Usuario o contraseña incorrectos.");
    }
  };

  return (
    <div className="contenedor" style={{ maxWidth: 420 }}>
      <h1>Iniciar sesión</h1>
      <form className="tarjeta" onSubmit={enviar}>
        <p><input placeholder="Usuario" value={username} onChange={(e) => setUsername(e.target.value)} /></p>
        <p><input type="password" placeholder="Contraseña" value={password} onChange={(e) => setPassword(e.target.value)} /></p>
        {error && <p className="mal">{error}</p>}
        <button className="boton">Entrar</button>
      </form>
      <p>¿No tienes cuenta? <Link to="/registro">Regístrate</Link></p>
    </div>
  );
}
