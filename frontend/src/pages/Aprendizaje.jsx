import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../api/client";

// Panel de aprendizaje: temas del lenguaje, lecciones y ejercicios recomendados.
export default function Aprendizaje() {
  const { lenguaje } = useParams();
  const [temas, setTemas] = useState([]);
  const [lecciones, setLecciones] = useState({});
  const [recomendados, setRecomendados] = useState([]);

  useEffect(() => {
    api.get(`/contenidos/temas/?lenguaje=${lenguaje}`).then(async (r) => {
      setTemas(r.data);
      const mapa = {};
      for (const t of r.data) mapa[t.id] = (await api.get(`/contenidos/lecciones/?tema=${t.id}`)).data;
      setLecciones(mapa);
    });
    api.get(`/progreso/recomendaciones/?lenguaje=${lenguaje}`).then((r) => setRecomendados(r.data));
  }, [lenguaje]);

  return (
    <div className="contenedor">
      <h1>Tu ruta de aprendizaje</h1>
      {recomendados.length > 0 && (
        <div className="tarjeta">
          <h3>Recomendado para ti</h3>
          {recomendados.map((r) => (
            <p key={r.ejercicio.id}>
              <Link to={`/ejercicio/${r.ejercicio.id}`}>{r.ejercicio.titulo}</Link> · {r.motivo}
            </p>
          ))}
        </div>
      )}
      {temas.map((t) => (
        <div className="tarjeta" key={t.id}>
          <h3>{t.titulo} <small>({t.nivel})</small></h3>
          {(lecciones[t.id] || []).map((l) => (
            <p key={l.id}><Link to={`/leccion/${l.id}`}>{l.titulo}</Link></p>
          ))}
        </div>
      ))}
    </div>
  );
}
