from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import MODEL_DIR
from app.routers.translation import build_router
from app.services.inference import InferenceService
from app.services.orchestrator import TranslationOrchestrator

app = FastAPI(title="Inclusive Translation API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

inference_service = InferenceService(MODEL_DIR)
orchestrator = TranslationOrchestrator(inference_service)
app.include_router(build_router(orchestrator))


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
