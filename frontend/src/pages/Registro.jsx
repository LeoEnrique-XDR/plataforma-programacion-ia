import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Registro() {
  const { registro } = useAuth();
  const navegar = useNavigate();
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const cambiar = (campo) => (e) => setForm({ ...form, [campo]: e.target.value });

  const enviar = async (e) => {
    e.preventDefault();
    try {
      await registro(form.username, form.email, form.password);
      navegar("/");
    } catch {
      setError("No se pudo crear la cuenta. Revisa los datos (contraseña de 8 caracteres o más).");
    }
  };

  return (
    <div className="contenedor" style={{ maxWidth: 420 }}>
      <h1>Crear cuenta</h1>
      <form className="tarjeta" onSubmit={enviar}>
        <p><input placeholder="Usuario" value={form.username} onChange={cambiar("username")} /></p>
        <p><input type="email" placeholder="Correo" value={form.email} onChange={cambiar("email")} /></p>
        <p><input type="password" placeholder="Contraseña" value={form.password} onChange={cambiar("password")} /></p>
        {error && <p className="mal">{error}</p>}
        <button className="boton">Registrarme</button>
      </form>
      <p>¿Ya tienes cuenta? <Link to="/login">Inicia sesión</Link></p>
    </div>
  );
}
