import { useState } from 'react'
import { translateTextToSign } from '../api/client'
import type { TextToSignResponse, UiStatus } from '../api/types'
import { HistoryPanel } from '../components/HistoryPanel'
import { SignAvatarPlayer } from '../components/SignAvatarPlayer'
import { StatusBadge } from '../components/StatusBadge'

export function TextToSignPage() {
  const [text, setText] = useState('')
  const [status, setStatus] = useState<UiStatus>('idle')
  const [error, setError] = useState('')
  const [result, setResult] = useState<TextToSignResponse | null>(null)
  const [history, setHistory] = useState<string[]>([])
  const [playbackSeq, setPlaybackSeq] = useState(0)
  const [activeSignIndex, setActiveSignIndex] = useState<number | null>(null)

  const submit = async () => {
    if (!text.trim()) {
      setError('Ingresa un texto para traducir.')
      setStatus('error')
      return
    }

    try {
      setStatus('processing')
      setError('')
      const data = await translateTextToSign({ text })
      setResult(data)
      setPlaybackSeq((value) => value + 1)
      setActiveSignIndex(null)
      setHistory((prev) => [data.normalized_text, ...prev].slice(0, 8))
      setStatus('done')
    } catch {
      setStatus('error')
      setError('No fue posible traducir el texto.')
    }
  }

  return (
    <>
      <section className="card text-sign-layout">
        <div className="text-sign-main">
          <div className="page-toolbar">
            <h2>Texto a lenguaje de señas</h2>
            <StatusBadge status={status} />
          </div>
          <textarea
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Escribe una frase en español..."
            aria-label="Texto a traducir"
          />
          <div className="row btn-row">
            <button type="button" onClick={submit}>
              Traducir
            </button>
          </div>
          {error ? <p className="alert">{error}</p> : null}
          {result ? (
            <>
              <p className="playback-hint">
                Secuencia de señas (el chip resaltado coincide con el gesto del avatar).
              </p>
              <div className="result-list" role="list">
                {result.signs.map((sign, index) => (
                  <span
                    className={`chip${activeSignIndex === index ? ' chip-active' : ''}`}
                    key={`${sign.animation_id}-${index}`}
                    role="listitem"
                  >
                    {sign.sign_gloss}
                  </span>
                ))}
              </div>
            </>
          ) : null}
        </div>
        <div className="text-sign-avatar">
          <h3 className="section-title">Avatar</h3>
          <SignAvatarPlayer
            key={playbackSeq}
            signs={result?.signs ?? []}
            onStepChange={(index) => setActiveSignIndex(index === -1 ? null : index)}
          />
        </div>
      </section>
      <HistoryPanel entries={history} />
    </>
  )
}
