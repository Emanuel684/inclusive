import { useState } from 'react'
import { translateTextToSign } from '../api/client'
import type { TextToSignResponse, UiStatus } from '../api/types'
import { HistoryPanel } from '../components/HistoryPanel'
import { StatusBadge } from '../components/StatusBadge'

export function TextToSignPage() {
  const [text, setText] = useState('')
  const [status, setStatus] = useState<UiStatus>('idle')
  const [error, setError] = useState('')
  const [result, setResult] = useState<TextToSignResponse | null>(null)
  const [history, setHistory] = useState<string[]>([])

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
      setHistory((prev) => [data.normalized_text, ...prev].slice(0, 8))
      setStatus('done')
    } catch {
      setStatus('error')
      setError('No fue posible traducir el texto.')
    }
  }

  return (
    <>
      <section className="card">
        <div className="row">
          <h2>Texto a lenguaje de señas</h2>
          <StatusBadge status={status} />
        </div>
        <textarea
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder="Escribe una frase en español..."
        />
        <div className="row" style={{ marginTop: '0.7rem' }}>
          <button onClick={submit}>Traducir</button>
        </div>
        {error && <p>{error}</p>}
        {result && (
          <div className="result-list">
            {result.signs.map((sign, index) => (
              <span className="chip" key={`${sign.sign_gloss}-${index}`}>
                {sign.sign_gloss}
              </span>
            ))}
          </div>
        )}
      </section>
      <HistoryPanel entries={history} />
    </>
  )
}
