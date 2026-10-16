import { Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import RutaProtegida from "./components/RutaProtegida";
import Aprendizaje from "./pages/Aprendizaje";
import Editor from "./pages/Editor";
import Leccion from "./pages/Leccion";
import Login from "./pages/Login";
import Panel from "./pages/Panel";
import Progreso from "./pages/Progreso";
import Registro from "./pages/Registro";
import SeleccionNivel from "./pages/SeleccionNivel";

const protegida = (el) => <RutaProtegida>{el}</RutaProtegida>;

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />
        <Route path="/" element={protegida(<Panel />)} />
        <Route path="/nivel/:lenguaje" element={protegida(<SeleccionNivel />)} />
        <Route path="/aprender/:lenguaje" element={protegida(<Aprendizaje />)} />
        <Route path="/leccion/:id" element={protegida(<Leccion />)} />
        <Route path="/ejercicio/:id" element={protegida(<Editor />)} />
        <Route path="/progreso" element={protegida(<Progreso />)} />
      </Routes>
    </>
  );
}
