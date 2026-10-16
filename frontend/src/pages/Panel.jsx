import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";

// Panel principal: lenguajes habilitados. El estudiante puede elegir varios.
export default function Panel() {
  const [lenguajes, setLenguajes] = useState([]);

  useEffect(() => {
    api.get("/contenidos/lenguajes/").then((r) => setLenguajes(r.data));
  }, []);

  return (
    <div className="contenedor">
      <h1>¿Qué lenguaje quieres aprender?</h1>
      <p>Puedes empezar con uno y sumar otros cuando quieras.</p>
      {lenguajes.map((l) => (
        <div className="tarjeta" key={l.id}>
          <h3>{l.nombre}</h3>
          <p>{l.descripcion}</p>
          <Link className="boton" to={`/nivel/${l.slug}`} style={{ textDecoration: "none" }}>Elegir</Link>
        </div>
      ))}
    </div>
  );
}
