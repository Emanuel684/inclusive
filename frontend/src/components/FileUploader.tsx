type Props = {
  label: string
  accept: string
  onFileSelected: (file: File | null) => void
}

export function FileUploader({ label, accept, onFileSelected }: Props) {
  return (
    <label className="card">
      <strong>{label}</strong>
      <div style={{ marginTop: '0.5rem' }}>
        <input
          type="file"
          accept={accept}
          onChange={(event) => onFileSelected(event.target.files?.[0] ?? null)}
        />
      </div>
    </label>
  )
}
