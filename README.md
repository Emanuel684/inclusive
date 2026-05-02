# Inclusive MVP

Aplicacion MVP para traduccion de lenguaje de senas con arquitectura hibrida:
- `frontend`: React + Vite + TypeScript
- `backend`: FastAPI
- `model`: pipeline Python modular para entrenamiento e inferencia exportable

## Requisitos

- Node.js 20+
- Python 3.13+

## Variables de entorno

Copia `.env.example` y ajusta si es necesario.

## Despliegue con Docker Compose

Desde la raiz del proyecto:

```bash
docker compose up --build -d
```

Servicios:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Healthcheck: `http://localhost:8000/health`

Detener:

```bash
docker compose down
```

## Ejecutar frontend

```bash
cd frontend
npm install
npm run dev
```

## Ejecutar backend

```bash
cd backend
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Pipeline de modelo

```bash
cd model
py -m pip install -r requirements.txt
py -m model_pipeline --help
```

Para entrenar y exportar artefactos:

```bash
py -m model_pipeline train-final --data-dir <ruta_csv_sign_mnist> --genome 1 1 1 1 2 --output-dir model/artifacts
```

## Pruebas smoke

```bash
cd frontend && npm run build
cd ../backend && py -m pytest -q
```
