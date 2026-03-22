export function normalizeText(s: string): string {
  return s
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{M}/gu, "")
    .trim()
}

function getPrimaryFields(p: Record<string, unknown>): string[] {
  return [
    p.shop_name,
    ...(Array.isArray(p.service_names) ? (p.service_names as string[]) : []),
    ...(Array.isArray(p.category_names) ? (p.category_names as string[]) : []),
  ]
    .filter((x) => x != null && String(x).length > 0)
    .map((x) => normalizeText(String(x)))
}

function getSecondaryFields(p: Record<string, unknown>): string[] {
  return [
    p.description,
    p.address,
  ]
    .filter((x) => x != null && String(x).length > 0)
    .map((x) => normalizeText(String(x)))
}

function tokenize(s: string): string[] {
  return normalizeText(s).split(/\s+/).filter(Boolean)
}

function matchToken(token: string, words: string[]): number {
  let score = 0

  for (const w of words) {
    if (w === token) return 1
    if (w.startsWith(token)) score = Math.max(score, 0.9)
    else if (w.includes(token)) score = Math.max(score, 0.75)
  }

  return score
}

export function scoreProviderQuery(queryRaw: string, p: Record<string, unknown>): number {
  const tokens = tokenize(queryRaw)
  if (!tokens.length) return 1

  const primaryWords = getPrimaryFields(p).flatMap(tokenize)
  const secondaryWords = getSecondaryFields(p).flatMap(tokenize)

  let total = 0
  let matchedTokens = 0

  for (const token of tokens) {
    const primaryScore = matchToken(token, primaryWords)
    const secondaryScore = matchToken(token, secondaryWords) * 0.5

    const best = Math.max(primaryScore, secondaryScore)

    if (best > 0) {
      matchedTokens++
      total += best
    }
  }

  if (matchedTokens === 0) return 0

  return total / tokens.length
}

export const SEARCH_MATCH_THRESHOLD = 0.6