from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, HTTPException, UploadFile

from app.core.config import (
    ALLOWED_IMAGE_TYPES,
    ALLOWED_VIDEO_TYPES,
    MAX_IMAGE_SIZE_BYTES,
    MAX_VIDEO_SIZE_BYTES,
    TEMP_DIR,
)
from app.schemas.translation import (
    ImageToSignResponse,
    TextToSignRequest,
    TextToSignResponse,
    VideoSignToTextResponse,
)
from app.services.orchestrator import TranslationOrchestrator

router = APIRouter(prefix="/translate", tags=["translation"])


def _validate_upload(file: UploadFile, allowed_types: set[str]) -> None:
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")


async def _save_upload_to_temp(file: UploadFile, max_size: int) -> Path:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    extension = Path(file.filename or "upload.bin").suffix
    path = TEMP_DIR / f"{uuid4().hex}{extension}"
    data = await file.read()
    if len(data) > max_size:
        raise HTTPException(status_code=413, detail="File too large")
    path.write_bytes(data)
    return path


def build_router(orchestrator: TranslationOrchestrator) -> APIRouter:
    @router.post("/text-to-sign", response_model=TextToSignResponse)
    async def text_to_sign(payload: TextToSignRequest) -> TextToSignResponse:
        translated = orchestrator.translate_text_to_sign(payload.text)
        return TextToSignResponse(**translated)

    @router.post("/image-to-sign", response_model=ImageToSignResponse)
    async def image_to_sign(file: UploadFile) -> ImageToSignResponse:
        _validate_upload(file, ALLOWED_IMAGE_TYPES)
        path = await _save_upload_to_temp(file, MAX_IMAGE_SIZE_BYTES)
        translated = orchestrator.translate_image_to_sign(path)
        path.unlink(missing_ok=True)
        return ImageToSignResponse(**translated)

    @router.post("/video-sign-to-text", response_model=VideoSignToTextResponse)
    async def video_sign_to_text(file: UploadFile) -> VideoSignToTextResponse:
        _validate_upload(file, ALLOWED_VIDEO_TYPES)
        path = await _save_upload_to_temp(file, MAX_VIDEO_SIZE_BYTES)
        translated = orchestrator.translate_video_sign_to_text(path)
        path.unlink(missing_ok=True)
        return VideoSignToTextResponse(**translated)

    return router
