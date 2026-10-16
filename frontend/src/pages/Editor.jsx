import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/client";
import TutorChat from "../components/TutorChat";

// Editor de código: escribe, envía y recibe retroalimentación + tutor virtual.
// TODO: reemplazar el textarea por el editor Monaco (@monaco-editor/react).
export default function Editor() {
  const { id } = useParams();
  const [ejercicio, setEjercicio] = useState(null);
  const [codigo, setCodigo] = useState("");
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get(`/contenidos/ejercicios/${id}/`).then((r) => {
      setEjercicio(r.data);
      setCodigo(r.data.codigo_inicial || "");
    });
  }, [id]);

  const enviar = async () => {
    setError("");
    try {
      const { data } = await api.post(`/progreso/ejercicios/${id}/enviar/`, { respuesta: codigo });
      setResultado(data);
    } catch (e) {
      setError(e.response?.data?.detail || "No se pudo evaluar tu respuesta.");
    }
  };

  if (!ejercicio) return <div className="contenedor">Cargando...</div>;
  return (
    <div className="contenedor">
      <h1>{ejercicio.titulo}</h1>
      <p>{ejercicio.enunciado}</p>
      <textarea className="codigo" value={codigo} onChange={(e) => setCodigo(e.target.value)} spellCheck={false} />
      <p><button className="boton" onClick={enviar}>Ejecutar y evaluar</button></p>
      {error && <p className="mal">{error}</p>}
      {resultado && (
        <div className="tarjeta">
          <p className={resultado.correcto ? "ok" : "mal"}>{resultado.mensaje}</p>
          {resultado.xp_ganado > 0 && <p className="ok">+{resultado.xp_ganado} XP</p>}
        </div>
      )}
      <TutorChat ejercicioId={ejercicio.id} codigo={codigo} />
    </div>
  );
}
