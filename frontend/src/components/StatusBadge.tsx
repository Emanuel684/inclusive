import type { UiStatus } from '../api/types'

type Props = {
  status: UiStatus
}

const labels: Record<UiStatus, string> = {
  idle: 'Idle',
  uploading: 'Uploading',
  processing: 'Processing',
  done: 'Done',
  error: 'Error',
}

export function StatusBadge({ status }: Props) {
  return <span className="chip">{labels[status]}</span>
}
