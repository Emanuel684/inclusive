import type { SignToken } from '../api/types'

export type GroupedSign = {
  sign: SignToken
  globalIndex: number
}

export type WordSignGroup = {
  wordIndex: number
  surfaceWord: string
  items: GroupedSign[]
}

export function groupSignsByWord(signs: SignToken[]): WordSignGroup[] {
  const order: number[] = []
  const byIndex = new Map<number, GroupedSign[]>()

  signs.forEach((sign, globalIndex) => {
    const wi = sign.word_index ?? 0
    if (!byIndex.has(wi)) {
      byIndex.set(wi, [])
      order.push(wi)
    }
    byIndex.get(wi)!.push({ sign, globalIndex })
  })

  return order.map((wi) => {
    const items = byIndex.get(wi) ?? []
    const surface = items[0]?.sign.surface_word ?? items[0]?.sign.token ?? ''
    return { wordIndex: wi, surfaceWord: surface, items }
  })
}
