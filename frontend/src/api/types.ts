export type UiStatus = 'idle' | 'uploading' | 'processing' | 'done' | 'error'

export type TextToSignRequest = {
  text: string
}

export type SignToken = {
  token: string
  sign_gloss: string
  source: 'dictionary' | 'spelling'
}

export type TextToSignResponse = {
  mode: 'text-to-sign'
  normalized_text: string
  signs: SignToken[]
}

export type ImageToSignResponse = {
  mode: 'image-to-sign'
  predicted_label: number
  predicted_letter: string
  confidence: number
  signs: SignToken[]
}

export type VideoToTextResponse = {
  mode: 'video-sign-to-text'
  frame_predictions: string[]
  transcript: string
}
