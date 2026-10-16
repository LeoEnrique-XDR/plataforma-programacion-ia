# Plataforma de programación con IA

Plataforma web gamificada, inspirada en Duolingo, para aprender programación.
El estudiante elige uno o varios lenguajes y avanza con lecciones, ejercicios de código y un
tutor virtual que **guía con pistas pero no entrega la solución**.

> "Aprender a programar con IA, no dejar que la IA programe por ti."

## Tecnologías

| Parte | Tecnología |
|---|---|
| Frontend | React (Vite), HTML, CSS, JavaScript |
| Backend | Django + Django REST Framework (Python) |
| Base de datos | PostgreSQL |
| IA | PLN (NLTK/spaCy), Machine Learning (scikit-learn), tutor con Claude (API), análisis de código, recomendación |

## Estructura

```
backend/    API en Django (apps: usuarios, contenidos, progreso, tutor, ia)
frontend/   Interfaz en React
docs/       Informe y diagramas
```

## Puesta en marcha

### 1. Base de datos (PostgreSQL)

Crea la base de datos (desde pgAdmin o `psql`):

```sql
CREATE DATABASE plataforma_db;
```

### 2. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows  (en Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env         # Windows  (en Linux/Mac: cp .env.example .env)
# Edita .env con tu contraseña de PostgreSQL
python manage.py migrate
python manage.py cargar_datos_demo
python manage.py createsuperuser
python manage.py runserver
```

- API: http://localhost:8000/api/
- Panel de administración (gestión de lenguajes, lecciones y ejercicios): http://localhost:8000/admin/
- Para probar sin PostgreSQL: agrega `USE_SQLITE=1` en `.env`.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Abre http://localhost:5173

### 4. Tutor virtual (opcional al inicio)

```bash
cd backend
pip install -r requirements-ia.txt
```

Agrega tu `ANTHROPIC_API_KEY` en `.env`. Sin la clave, el tutor responde que no está configurado.

## Estado actual

| Función | Estado |
|---|---|
| Registro, login, logout | Listo |
| Elegir lenguaje y nivel (por lenguaje) | Listo |
| Lecciones y ejercicios | Listo |
| Evaluación de código | Listo para Python (ver advertencia de seguridad) |
| Tutor con pistas en 3 niveles + filtro anti-solución | Listo (requiere API key) |
| PLN (detección de conceptos) | Versión inicial por palabras clave |
| ML (temas a reforzar) | Versión inicial por reglas |
| Recomendaciones | Listo |
| Prueba diagnóstica, gráficos, editor Monaco | Pendiente |
| Otros lenguajes (C, C++, Java, C#, JavaScript, SQL) | Pendiente |

**Seguridad:** `analisis_codigo.py` ejecuta el código del estudiante en el mismo servidor.
Es solo para desarrollo. Antes de publicar, debe ejecutarse en un contenedor aislado (Docker) o con Judge0.

## Convención de commits

`feat:` nueva función · `fix:` corrección · `docs:` documentación · `refactor:` mejora interna
