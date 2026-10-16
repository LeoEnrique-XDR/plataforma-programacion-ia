import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { token, logout } = useAuth();
  if (!token) return null;
  return (
    <nav className="barra">
      <Link to="/"><strong>Plataforma de programación</strong></Link>
      <span>
        <Link to="/progreso">Mi progreso</Link>{" · "}
        <button className="boton suave" onClick={logout}>Cerrar sesión</button>
      </span>
    </nav>
  );
}
