from pathlib import Path
import os

MODEL_DIR = Path(os.getenv("MODEL_DIR", "model/artifacts"))
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "backend/uploads"))
TEMP_DIR = Path(os.getenv("TEMP_DIR", "backend/tmp"))

ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm"}
MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024
MAX_VIDEO_SIZE_BYTES = 20 * 1024 * 1024
