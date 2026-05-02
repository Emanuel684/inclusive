import axios from 'axios'
import type {
  ImageToSignResponse,
  TextToSignRequest,
  TextToSignResponse,
  VideoToTextResponse,
} from './types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000',
  timeout: 120000,
})

export async function translateTextToSign(payload: TextToSignRequest): Promise<TextToSignResponse> {
  const { data } = await api.post<TextToSignResponse>('/translate/text-to-sign', payload)
  return data
}

export async function translateImageToSign(file: File): Promise<ImageToSignResponse> {
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await api.post<ImageToSignResponse>('/translate/image-to-sign', formData)
  return data
}

export async function translateVideoSignToText(file: File): Promise<VideoToTextResponse> {
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await api.post<VideoToTextResponse>('/translate/video-sign-to-text', formData)
  return data
}
