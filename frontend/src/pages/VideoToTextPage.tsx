import { useState } from 'react'
import { translateVideoSignToText } from '../api/client'
import type { UiStatus, VideoToTextResponse } from '../api/types'
import { FileUploader } from '../components/FileUploader'
import { HistoryPanel } from '../components/HistoryPanel'
import { StatusBadge } from '../components/StatusBadge'

const MAX_VIDEO_SIZE = 20 * 1024 * 1024

export function VideoToTextPage() {
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState<UiStatus>('idle')
  const [error, setError] = useState('')
  const [result, setResult] = useState<VideoToTextResponse | null>(null)
  const [history, setHistory] = useState<string[]>([])

  const submit = async () => {
    if (!file) {
      setError('Selecciona un video.')
      setStatus('error')
      return
    }
    if (file.size > MAX_VIDEO_SIZE) {
      setError('El video excede el máximo de 20MB.')
      setStatus('error')
      return
    }

    try {
      setStatus('processing')
      setError('')
      const data = await translateVideoSignToText(file)
      setResult(data)
      setHistory((prev) => [data.transcript, ...prev].slice(0, 8))
      setStatus('done')
    } catch {
      setStatus('error')
      setError('No fue posible traducir el video.')
    }
  }

  return (
    <>
      <section className="card">
        <div className="page-toolbar">
          <h2>Video de señas a texto</h2>
          <StatusBadge status={status} />
        </div>
        <FileUploader label="Subir video (MP4 o WebM)" accept="video/mp4,video/webm" onFileSelected={setFile} />
        <div className="row btn-row">
          <button type="button" onClick={submit} disabled={!file}>
            Traducir video
          </button>
        </div>
        {error ? <p className="alert">{error}</p> : null}
        {result ? (
          <div className="result-block">
            <strong>Texto detectado</strong>
            <p>{result.transcript}</p>
            <p className="muted-spaced">Predicciones por frame (muestra):</p>
            <div className="result-list" role="list">
              {result.frame_predictions.map((label, index) => (
                <span className="chip" key={`${label}-${index}`} role="listitem">
                  {label}
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
