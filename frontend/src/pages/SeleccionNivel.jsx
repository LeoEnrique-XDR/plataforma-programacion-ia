import { useNavigate, useParams } from "react-router-dom";
import api from "../api/client";

// Evaluación inicial por lenguaje (por ahora: el estudiante indica su nivel).
// TODO: agregar la prueba diagnóstica de 10 preguntas.
export default function SeleccionNivel() {
  const { lenguaje } = useParams();
  const navegar = useNavigate();

  const elegir = async (nivel) => {
    await api.post("/progreso/lenguajes/seleccionar/", { lenguaje, nivel });
    navegar(`/aprender/${lenguaje}`);
  };

  return (
    <div className="contenedor">
      <h1>¿Cuál es tu nivel en este lenguaje?</h1>
      {["principiante", "intermedio", "avanzado"].map((n) => (
        <button key={n} className="boton" style={{ marginRight: 8 }} onClick={() => elegir(n)}>
          {n[0].toUpperCase() + n.slice(1)}
        </button>
      ))}
    </div>
  );
}
