import { useState } from 'react'
import { translateImageToSign } from '../api/client'
import type { ImageToSignResponse, UiStatus } from '../api/types'
import { FileUploader } from '../components/FileUploader'
import { HistoryPanel } from '../components/HistoryPanel'
import { StatusBadge } from '../components/StatusBadge'

const MAX_IMAGE_SIZE = 5 * 1024 * 1024

export function ImageToSignPage() {
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState<UiStatus>('idle')
  const [error, setError] = useState('')
  const [result, setResult] = useState<ImageToSignResponse | null>(null)
  const [history, setHistory] = useState<string[]>([])

  const submit = async () => {
    if (!file) {
      setError('Selecciona una imagen.')
      setStatus('error')
      return
    }
    if (file.size > MAX_IMAGE_SIZE) {
      setError('La imagen excede el máximo de 5MB.')
      setStatus('error')
      return
    }

    try {
      setStatus('uploading')
      setError('')
      const data = await translateImageToSign(file)
      setResult(data)
      setHistory((prev) => [`${file.name} -> ${data.predicted_letter}`, ...prev].slice(0, 8))
      setStatus('done')
    } catch {
      setStatus('error')
      setError('No fue posible procesar la imagen.')
    }
  }

  return (
    <>
      <section className="card">
        <div className="page-toolbar">
          <h2>Imagen a lenguaje de señas</h2>
          <StatusBadge status={status} />
        </div>
        <FileUploader label="Subir imagen (PNG o JPEG)" accept="image/png,image/jpeg" onFileSelected={setFile} />
        <div className="row btn-row">
          <button type="button" onClick={submit} disabled={!file}>
            Traducir imagen
          </button>
        </div>
        {error ? <p className="alert">{error}</p> : null}
        {result ? (
          <div className="result-block">
            <strong>Resultado</strong>
            <div className="result-list" role="list">
              <span className="chip" role="listitem">
                Letra: {result.predicted_letter}
              </span>
              <span className="chip" role="listitem">
                Confianza: {(result.confidence * 100).toFixed(1)}%
              </span>
              {result.signs.map((sign, index) => (
                <span className="chip" key={`${sign.animation_id ?? sign.sign_gloss}-${index}`} role="listitem">
                  {sign.sign_gloss}
                </span>
              ))}
            </div>
          </div>
        ) : null}
      </section>
      <HistoryPanel entries={history} />
    </>
  )
}
