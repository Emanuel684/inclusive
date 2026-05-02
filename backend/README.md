# Backend - Inclusive API

Backend FastAPI para orquestar traducciones hibridas.

## Endpoints

- `GET /health`
- `POST /translate/text-to-sign`
- `POST /translate/image-to-sign` (multipart file png/jpg)
- `POST /translate/video-sign-to-text` (multipart file mp4/webm)

## Levantar servicio

```bash
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker

```bash
docker build -t inclusive-backend ./backend
docker run --rm -p 8000:8000 inclusive-backend
```

## Tests

```bash
py -m pytest -q
```
