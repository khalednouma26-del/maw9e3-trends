const BASE = '/api'

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${BASE}${url}`, { headers: { ...headers, ...options?.headers as Record<string, string> }, ...options })
  if (res.status === 401 && typeof window !== 'undefined') {
    localStorage.removeItem('token')
    window.location.href = '/login'
    throw new Error('Unauthorized')
  }
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

export const getTrends = () => fetchJSON<import('@/types').Trend[]>('/trends')
export const refreshTrends = () => fetchJSON<{ message: string; total: number }>('/trends/refresh', { method: 'POST' })
export const getArticles = (params?: { page?: number; category?: string; search?: string }) => {
  const q = new URLSearchParams()
  if (params?.page) q.set('page', String(params.page))
  if (params?.category) q.set('category', params.category)
  if (params?.search) q.set('search', params.search)
  return fetchJSON<{ articles: import('@/types').Article[]; total: number; page: number }>(`/articles?${q}`)
}
export const getArticle = (id: number) => fetchJSON<import('@/types').Article>(`/articles/${id}`)
export const runPipeline = () => fetchJSON<Record<string, unknown>>('/pipeline/run', { method: 'POST' })
export const submitContact = (data: { name: string; email: string; subject: string; message: string }) =>
  fetchJSON<{ message: string }>('/contact', { method: 'POST', body: JSON.stringify(data) })
export const getDashboardStats = () => fetchJSON<import('@/types').DashboardStats>('/dashboard/stats')
