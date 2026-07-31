import { MetadataRoute } from 'next'

const BASE = process.env.SITE_URL || 'http://localhost:3000'

export default function sitemap(): MetadataRoute.Sitemap {
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
  return staticPages
}
