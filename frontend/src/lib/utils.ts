export function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric', month: 'long', day: 'numeric',
  })
}

export function truncate(text: string, max: number): string {
  return text.length > max ? text.slice(0, max) + '...' : text
}
