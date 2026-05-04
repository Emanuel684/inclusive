import type { UiStatus } from '../api/types'

type Props = {
  status: UiStatus
}

const labels: Record<UiStatus, string> = {
  idle: 'Listo',
  uploading: 'Subiendo',
  processing: 'Procesando',
  done: 'Completado',
  error: 'Error',
}

export function StatusBadge({ status }: Props) {
  return (
    <span className={`status-badge status-badge--${status}`} role="status" aria-live="polite">
      {labels[status]}
    </span>
  )
}
