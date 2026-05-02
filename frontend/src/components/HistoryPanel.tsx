type Props = {
  entries: string[]
}

export function HistoryPanel({ entries }: Props) {
  return (
    <section className="card">
      <h3>Historial local</h3>
      {entries.length === 0 ? (
        <p>No hay traducciones todavía.</p>
      ) : (
        <ul>
          {entries.map((entry, index) => (
            <li key={`${entry}-${index}`}>{entry}</li>
          ))}
        </ul>
      )}
    </section>
  )
}
