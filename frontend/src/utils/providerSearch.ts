/** Normalize for case- and accent-insensitive matching. */
export function normalizeText(s: string): string {
  return s
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{M}/gu, "")
    .trim()
}

function levenshtein(a: string, b: string): number {
  const m = a.length
  const n = b.length
  if (m === 0) return n
  if (n === 0) return m
  const dp: number[][] = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0))
  for (let i = 0; i <= m; i++) dp[i][0] = i
  for (let j = 0; j <= n; j++) dp[0][j] = j
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1
      dp[i][j] = Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    }
  }
  return dp[m][n]
}

export function haystackForProvider(p: Record<string, unknown>): string {
  const parts: string[] = [
    p.shop_name,
    p.description,
    p.address,
    p.phone,
    p.email,
    String(p.id ?? ""),
    ...(Array.isArray(p.service_names) ? (p.service_names as string[]) : []),
    ...(Array.isArray(p.category_names) ? (p.category_names as string[]) : []),
  ]
    .filter((x) => x != null && String(x).length > 0)
    .map((x) => String(x))
  return normalizeText(parts.join(" "))
}

function tokenScore(token: string, haystack: string, words: string[]): number {
  if (!token.length) return 1
  if (haystack.includes(token)) return 1

  for (const w of words) {
    if (w.length < 2) continue
    if (w.startsWith(token)) return 0.92
    if (token.length >= 3 && w.includes(token)) return 0.88
  }

  const maxDist = Math.min(2, Math.max(1, Math.floor(token.length / 3)))

  let best = 0
  for (const w of words) {
    if (w.length < 2) continue
    if (Math.abs(w.length - token.length) > 5) continue
    const d = levenshtein(token, w)
    if (d <= maxDist) {
      const s = 0.42 + 0.58 * (1 - d / (maxDist + 1))
      if (s > best) best = s
    }
  }

  if (token.length >= 4 && haystack.length >= token.length) {
    for (let i = 0; i <= haystack.length - 4; i++) {
      const slice = haystack.slice(i, Math.min(i + token.length + 3, haystack.length))
      const d = levenshtein(token, slice.slice(0, token.length + 2))
      if (d <= maxDist) {
        const s = 0.38 + 0.5 * (1 - d / (maxDist + 1))
        if (s > best) best = s
      }
    }
  }

  return best
}

/** 0..1 relevance; 1 = empty query (show all). */
export function scoreProviderQuery(queryRaw: string, p: Record<string, unknown>): number {
  const q = normalizeText(queryRaw).replace(/\s+/g, " ").trim()
  if (!q) return 1

  const haystack = haystackForProvider(p)
  const tokens = q.split(/\s+/).filter((t) => t.length > 0)
  if (!tokens.length) return 1

  const words = haystack.split(/\s+/).filter(Boolean)
  let sum = 0
  for (const token of tokens) {
    sum += tokenScore(token, haystack, words)
  }
  return sum / tokens.length
}

/** Minimum average token score to include a provider as a “similar” match. */
export const SEARCH_MATCH_THRESHOLD = 0.3
