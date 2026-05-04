import { useMemo, useState } from 'react'
import { translateTextToSign } from '../api/client'
import type { TextToSignResponse, UiStatus } from '../api/types'
import { HistoryPanel } from '../components/HistoryPanel'
import { SignAvatarPlayer } from '../components/SignAvatarPlayer'
import { StatusBadge } from '../components/StatusBadge'
import { groupSignsByWord } from '../lib/groupSignsByWord'

export function TextToSignPage() {
  const [text, setText] = useState('')
  const [status, setStatus] = useState<UiStatus>('idle')
  const [error, setError] = useState('')
  const [result, setResult] = useState<TextToSignResponse | null>(null)
  const [history, setHistory] = useState<string[]>([])
  const [playbackSeq, setPlaybackSeq] = useState(0)
  const [activeSignIndex, setActiveSignIndex] = useState<number | null>(null)

  const wordGroups = useMemo(() => (result ? groupSignsByWord(result.signs) : []), [result])

  const progress =
    result && result.signs.length > 0 && activeSignIndex !== null && activeSignIndex >= 0
      ? Math.round(((activeSignIndex + 1) / result.signs.length) * 100)
      : 0

  const currentGloss =
    result && activeSignIndex !== null && activeSignIndex >= 0
      ? result.signs[activeSignIndex]?.sign_gloss
      : null

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
            placeholder="Ej. hola como estas?"
            aria-label="Texto a traducir"
          />
          <div className="row btn-row">
            <button type="button" onClick={submit}>
              Traducir a señas
            </button>
          </div>
          {error ? <p className="alert">{error}</p> : null}

          {result ? (
            <>
              <div className="translation-summary">
                <div>
                  <span className="translation-summary__label">Secuencia normalizada</span>
                  <p className="translation-summary__text">{result.normalized_text}</p>
                </div>
                <div className="translation-summary__meta">
                  <span className="translation-summary__pill">
                    {result.signs.length} signo{result.signs.length === 1 ? '' : 's'}
                  </span>
                  <span className="translation-summary__pill">{wordGroups.length} palabra{wordGroups.length === 1 ? '' : 's'}</span>
                </div>
              </div>

              <div className="playback-panel" aria-live="polite">
                <div className="playback-panel__header">
                  <span className="playback-panel__title">Reproducción</span>
                  <span className="playback-panel__percent">{activeSignIndex !== null && activeSignIndex >= 0 ? `${progress}%` : '—'}</span>
                </div>
                <div className="progress-bar" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress}>
                  <div className="progress-bar__fill" style={{ width: `${progress}%` }} />
                </div>
                <div className="current-sign" aria-atomic="true">
                  {currentGloss ? (
                    <>
                      <span className="current-sign__label">Signo actual</span>
                      <span className="current-sign__gloss">{currentGloss}</span>
                    </>
                  ) : (
                    <span className="current-sign__idle">Pulsa traducir para ver la secuencia en el avatar.</span>
                  )}
                </div>
              </div>

              <p className="playback-hint">Cada palabra se agrupa; las no reconocidas se deletrean letra a letra.</p>

              <div className="sign-sequence" role="list" aria-label="Secuencia de lenguaje de señas por palabra">
                {wordGroups.map((group) => (
                  <div className="sign-word-block" key={group.wordIndex} role="listitem">
                    <div className="sign-word-block__header">
                      <span className="sign-word-block__word">{group.surfaceWord}</span>
                      <span className="sign-word-block__count">
                        {group.items.length} signo{group.items.length === 1 ? '' : 's'}
                      </span>
                    </div>
                    <div className="sign-word-block__chips">
                      {group.items.map(({ sign, globalIndex }) => (
                        <span
                          className={`sign-chip${activeSignIndex === globalIndex ? ' sign-chip--active' : ''}`}
                          key={`${sign.animation_id}-${globalIndex}`}
                          title={sign.animation_id}
                        >
                          {sign.sign_gloss}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </>
          ) : null}
        </div>
        <div className="text-sign-avatar">
          <h3 className="section-title">Avatar</h3>
          <p className="avatar-caption">Recorre toda la frase signo a signo; pausa breve entre palabras.</p>
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
