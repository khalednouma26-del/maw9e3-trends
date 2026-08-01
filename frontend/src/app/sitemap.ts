import { MetadataRoute } from 'next'

const BASE = process.env.SITE_URL || 'http://localhost:3000'
const API = process.env.API_URL || 'http://localhost:8000'

export const revalidate = 3600

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const staticPages = [
    { url: BASE, changeFrequency: 'hourly' as const, priority: 1 },
    { url: `${BASE}/trends`, changeFrequency: 'hourly' as const, priority: 0.9 },
    { url: `${BASE}/search`, changeFrequency: 'daily' as const, priority: 0.8 },
    { url: `${BASE}/about`, changeFrequency: 'monthly' as const, priority: 0.5 },
    { url: `${BASE}/contact`, changeFrequency: 'monthly' as const, priority: 0.4 },
    { url: `${BASE}/privacy`, changeFrequency: 'monthly' as const, priority: 0.3 },
    { url: `${BASE}/terms`, changeFrequency: 'monthly' as const, priority: 0.3 },
    { url: `${BASE}/cookie-policy`, changeFrequency: 'monthly' as const, priority: 0.3 },
    { url: `${BASE}/disclaimer`, changeFrequency: 'monthly' as const, priority: 0.3 },
  ]

  try {
    const res = await fetch(`${API}/api/articles?per_page=100`, { next: { revalidate: 3600 } })
    if (res.ok) {
      const articles = await res.json()
      const list = Array.isArray(articles) ? articles : articles.articles || articles.items || []
      const articleUrls = list
        .filter((a: any) => a && a.id)
        .map((a: any) => ({
          url: `${BASE}/article/${a.id}`,
          lastModified: a.published_at || a.updated_at || new Date(),
          changeFrequency: 'daily' as const,
          priority: 0.7,
        }))
      return [...staticPages, ...articleUrls]
    }
  } catch (e) {
    console.error('sitemap fetch failed', e)
  }

  return staticPages
}
