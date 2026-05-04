type Props = {
  label: string
  accept: string
  onFileSelected: (file: File | null) => void
}

export function FileUploader({ label, accept, onFileSelected }: Props) {
  return (
    <label className="file-drop">
      <span className="file-drop__title">{label}</span>
      <input
        className="file-drop__input"
        type="file"
        accept={accept}
        onChange={(event) => onFileSelected(event.target.files?.[0] ?? null)}
      />
    </label>
  )
}
