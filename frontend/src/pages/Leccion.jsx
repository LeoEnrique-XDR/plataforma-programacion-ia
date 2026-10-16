import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../api/client";

// Pantalla de lección: explicación, ejemplo y lista de ejercicios.
export default function Leccion() {
  const { id } = useParams();
  const [leccion, setLeccion] = useState(null);
  const [ejercicios, setEjercicios] = useState([]);

  useEffect(() => {
    api.get(`/contenidos/lecciones/${id}/`).then((r) => setLeccion(r.data));
    api.get(`/contenidos/ejercicios/?leccion=${id}`).then((r) => setEjercicios(r.data));
  }, [id]);

  if (!leccion) return <div className="contenedor">Cargando...</div>;
  return (
    <div className="contenedor">
      <h1>{leccion.titulo}</h1>
      <div className="tarjeta"><p>{leccion.contenido}</p>
        {leccion.ejemplo_codigo && <pre>{leccion.ejemplo_codigo}</pre>}</div>
      <h3>Ejercicios</h3>
      {ejercicios.map((e) => (
        <p key={e.id}><Link to={`/ejercicio/${e.id}`}>{e.titulo}</Link> · {e.puntos} XP</p>
      ))}
    </div>
  );
}
