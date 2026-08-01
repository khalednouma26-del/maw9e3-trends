export function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric', month: 'long', day: 'numeric',
  })
}

export function truncate(text: string, max: number): string {
  return text.length > max ? text.slice(0, max) + '...' : text
}

export const isAdminClient = () => typeof window !== 'undefined' && !!localStorage.getItem('token')

export const displayViews = (real: number | null | undefined, seedOffset = 0): number => {
  if (isAdminClient()) return real || 0
  return (real || 0) * 50 + ((Date.now() + seedOffset * 7) % 500) + 200
}
