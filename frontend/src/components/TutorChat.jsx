import { useState } from "react";
import api from "../api/client";

// Tutor virtual: pide una pista. El nivel de la pista lo decide el backend.
export default function TutorChat({ ejercicioId, codigo }) {
  const [mensaje, setMensaje] = useState("");
  const [pista, setPista] = useState(null);
  const [cargando, setCargando] = useState(false);

  const pedir = async () => {
    setCargando(true);
    try {
      const { data } = await api.post("/tutor/pista/", { ejercicio: ejercicioId, mensaje, codigo });
      setPista(data);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="tarjeta">
      <h3 className="pista">Tutor virtual</h3>
      <input placeholder="¿Qué no entiendes? (opcional)" value={mensaje} onChange={(e) => setMensaje(e.target.value)} />
      <p><button className="boton tutor" onClick={pedir} disabled={cargando}>{cargando ? "Pensando..." : "Pedir pista"}</button></p>
      {pista && (<>
        <p className="pista">Pista nivel {pista.nivel_pista} de 3</p>
        <p>{pista.respuesta}</p>
      </>)}
    </div>
  );
}
