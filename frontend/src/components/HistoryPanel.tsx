type Props = {
  entries: string[]
}

export function HistoryPanel({ entries }: Props) {
  return (
    <section className="card card--muted">
      <h3 className="section-title">Historial local</h3>
      {entries.length === 0 ? (
        <p className="muted">No hay traducciones todavía.</p>
      ) : (
        <ul className="history-list">
          {entries.map((entry, index) => (
            <li key={`${entry}-${index}`}>{entry}</li>
          ))}
        </ul>
      )}
    </section>
  )
}
