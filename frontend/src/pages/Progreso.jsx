import { useEffect, useState } from "react";
import api from "../api/client";

// Progreso y estadísticas. TODO: elegir lenguaje y agregar gráficos (Chart.js o Recharts).
export default function Progreso() {
  const [datos, setDatos] = useState(null);

  useEffect(() => {
    api.get("/progreso/resumen/?lenguaje=python").then((r) => setDatos(r.data));
  }, []);

  if (!datos) return <div className="contenedor">Cargando...</div>;
  return (
    <div className="contenedor">
      <h1>Mi progreso en Python</h1>
      <div className="tarjeta">
        <p>XP: <strong>{datos.xp}</strong> · Racha: <strong>{datos.racha}</strong> días</p>
        <p>Ejercicios resueltos: {datos.ejercicios_resueltos} · Precisión: {datos.precision}%</p>
      </div>
      <div className="tarjeta">
        <h3>Temas por reforzar</h3>
        {datos.temas_a_reforzar.length === 0 && <p>¡Sin dificultades detectadas por ahora!</p>}
        {datos.temas_a_reforzar.map((t) => (
          <p key={t.concepto}>{t.concepto} · {t.errores} errores</p>
        ))}
      </div>
    </div>
  );
}
