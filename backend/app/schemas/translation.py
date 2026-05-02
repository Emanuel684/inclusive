from pydantic import BaseModel, Field


class SignToken(BaseModel):
    token: str
    sign_gloss: str
    source: str


class TextToSignRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class TextToSignResponse(BaseModel):
    mode: str = "text-to-sign"
    normalized_text: str
    signs: list[SignToken]


class ImageToSignResponse(BaseModel):
    mode: str = "image-to-sign"
    predicted_label: int
    predicted_letter: str
    confidence: float
    signs: list[SignToken]


class VideoSignToTextResponse(BaseModel):
    mode: str = "video-sign-to-text"
    frame_predictions: list[str]
    transcript: str
