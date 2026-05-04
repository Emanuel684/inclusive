import type { AnimationAction } from 'three'
import type { SignToken } from '../api/types'

/**
 * Clip base names for three.js RobotExpressive (gltf) and similar rigs.
 * Actual action keys may be "Wave" or "RobotArmature|Wave".
 */
export const ROBOT_EXPRESSIVE_CLIP_BASES = [
  'Idle',
  'Walking',
  'Running',
  'Dance',
  'Death',
  'Jump',
  'Yes',
  'No',
  'Wave',
  'Punch',
  'ThumbsUp',
] as const

const CLIP_CYCLE = ['Wave', 'ThumbsUp', 'Yes', 'No', 'Punch', 'Jump', 'Dance', 'Running', 'Walking'] as const

const LEX_CLIP_BY_SLUG: Record<string, readonly string[]> = {
  hola: ['Wave', 'Yes', 'ThumbsUp'],
  gracias: ['ThumbsUp', 'Yes', 'Wave'],
  adios: ['Wave', 'Walking', 'Running'],
  buenos: ['Yes', 'ThumbsUp', 'Jump'],
  dias: ['Jump', 'Wave', 'Dance'],
  ayuda: ['Punch', 'ThumbsUp', 'Yes'],
}

function hashSlug(slug: string): number {
  return [...slug].reduce((acc, ch) => acc + ch.charCodeAt(0), 0)
}

function rotateClipPreferences(seed: number): string[] {
  const start = Math.abs(seed) % CLIP_CYCLE.length
  const rotated = [...CLIP_CYCLE.slice(start), ...CLIP_CYCLE.slice(0, start)]
  return [...rotated, 'Idle', 'Walking']
}

function spellLetterPreferences(letter: string): string[] {
  const lower = letter.toLowerCase()
  if (lower.length !== 1 || lower < 'a' || lower > 'z') {
    return ['Idle', 'Wave']
  }
  const index = lower.charCodeAt(0) - 'a'.charCodeAt(0)
  const start = index % CLIP_CYCLE.length
  const rotated = [...CLIP_CYCLE.slice(start), ...CLIP_CYCLE.slice(0, start)]
  return [...rotated, 'Idle']
}

/**
 * Preference order of clip base names for a sign token (backend `animation_id`).
 */
export function clipPreferencesForSign(sign: SignToken): string[] {
  const { animation_id: id } = sign
  if (id.startsWith('spell_')) {
    const letter = id.slice('spell_'.length)
    return spellLetterPreferences(letter)
  }
  if (id.startsWith('lex_')) {
    const slug = id.slice('lex_'.length)
    const mapped = LEX_CLIP_BY_SLUG[slug]
    if (mapped) {
      return [...mapped, 'Idle']
    }
    return rotateClipPreferences(hashSlug(slug))
  }
  return rotateClipPreferences(hashSlug(id))
}

/**
 * Find the mixer action key for the first matching clip preference.
 */
export function findActionKey(
  actions: Record<string, AnimationAction | null>,
  preferences: string[],
): string | undefined {
  const keys = Object.keys(actions).filter((key) => actions[key] != null)
  for (const pref of preferences) {
    const lower = pref.toLowerCase()
    const hit = keys.find(
      (key) =>
        key === pref ||
        key.toLowerCase() === lower ||
        key.toLowerCase().endsWith(`|${lower}`) ||
        key.toLowerCase().endsWith(`|${pref}`),
    )
    if (hit) {
      return hit
    }
  }
  return undefined
}

export function idleActionPreferences(): string[] {
  return ['Idle', 'Walking', 'Running']
}
