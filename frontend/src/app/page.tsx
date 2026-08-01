'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { TrendingUp, Newspaper, ArrowRight, Clock, Eye, Globe, Activity, Heart, DollarSign, Film, Microscope, Cpu, Landmark } from 'lucide-react'
import { useSearchParams } from 'next/navigation'
import { getTrends, getArticles, trackPageView } from '@/lib/api'
import type { Trend, Article } from '@/types'
import { formatDate, displayViews } from '@/lib/utils'

const CATEGORIES = [
  { key: '', label: 'All', icon: Globe, color: '#00d4aa' },
  { key: 'world', label: 'World', icon: Globe, color: '#00a8ff' },
  { key: 'politics', label: 'Politics', icon: Landmark, color: '#ff6b6b' },
  { key: 'sports', label: 'Sports', icon: Activity, color: '#ffd700' },
  { key: 'finance', label: 'Finance', icon: DollarSign, color: '#51cf66' },
  { key: 'health', label: 'Health', icon: Heart, color: '#ff6b6b' },
  { key: 'entertainment', label: 'Entertainment', icon: Film, color: '#cc5de8' },
  { key: 'science', label: 'Science', icon: Microscope, color: '#00d4aa' },
  { key: 'technology', label: 'Technology', icon: Cpu, color: '#00a8ff' },
]

export default function HomePage() {
  const searchParams = useSearchParams()
  const [trends, setTrends] = useState<Trend[]>([])
  const [articles, setArticles] = useState<Article[]>([])
  const [totalStats, setTotalStats] = useState({ trends: 0, articles: 0, categories: 0, sources: 0 })
  const [loading, setLoading] = useState(true)
  const [activeCat, setActiveCat] = useState('')

  const loadArticles = (cat: string) => {
    setActiveCat(cat)
    getArticles(cat ? { category: cat } : undefined).then(r => setArticles(fakeViews(r.articles.slice(0, 6)))).catch(() => {})
  }

  const fakeViews = (arts: Article[]) => arts.map((a, i) => ({ ...a, view_count: displayViews(a.view_count, i) }))

  useEffect(() => {
    const cat = searchParams.get('category')
    if (cat) setActiveCat(cat)
    Promise.all([getTrends(), getArticles(cat ? { category: cat } : undefined)]).then(([t, a]) => {
      const cats = new Set(t.map(tr => tr.category).filter(Boolean))
      const srcs = new Set(t.map(tr => tr.source).filter(Boolean))
      setTotalStats({ trends: t.length, articles: a.total, categories: cats.size, sources: srcs.size })
      setTrends(t.slice(0, 8))
      setArticles(fakeViews(a.articles.slice(0, 6)))
      trackPageView()
    }).finally(() => setLoading(false))
  }, [searchParams])

  if (loading) return <div className="text-center py-20 text-dark-muted">Loading...</div>

  return (
    <div>
      {/* Hero */}
      <section className="relative rounded-2xl overflow-hidden mb-12 min-h-[400px] flex items-center"
        style={{ background: 'linear-gradient(135deg, #0f0f1e 0%, #1a1a3e 50%, #0d0d1a 100%)' }}>
        <div className="absolute inset-0 opacity-20"
          style={{ backgroundImage: 'url(https://picsum.photos/seed/hero/1600/600)', backgroundSize: 'cover', backgroundPosition: 'center' }} />
        <div className="relative z-10 px-8 sm:px-12 py-16 w-full">
          <h1 className="text-4xl sm:text-5xl font-extrabold mb-4 max-w-3xl">
            <span className="bg-gradient-to-r from-primary to-blue-400 bg-clip-text text-transparent">
              Discover What's Trending
            </span>
          </h1>
          <p className="text-dark-muted text-lg max-w-xl mb-6">
            Stay informed with the latest trending topics across world news, politics, sports, finance, health, entertainment, science, and technology.
          </p>
          <div className="flex gap-4">
            <Link href="/trends"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl text-white font-semibold bg-gradient-to-r from-primary to-primary-dark hover:opacity-90 transition no-underline">
              <TrendingUp size={18} /> Browse Trends
            </Link>
            <Link href="/search"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl border border-dark-border text-dark-muted hover:text-white hover:border-primary transition no-underline">
              Search Articles
            </Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        {[
          { icon: TrendingUp, label: 'Trends', value: totalStats.trends, color: '#00d4aa' },
          { icon: Newspaper, label: 'Articles', value: totalStats.articles, color: '#00a8ff' },
          { icon: Globe, label: 'Categories', value: totalStats.categories, color: '#ffd700' },
          { icon: Activity, label: 'Sources', value: totalStats.sources, color: '#cc5de8' },
        ].map(({ icon: Icon, label, value, color }) => (
          <div key={label} className="rounded-xl p-5 border border-dark-border text-center" style={{ background: '#1a1a2e' }}>
            <div className="inline-flex p-2.5 rounded-xl mb-2" style={{ background: `${color}15` }}>
              <Icon size={20} color={color} />
            </div>
            <div className="text-xl font-bold text-white">{value}</div>
            <div className="text-xs text-dark-muted">{label}</div>
          </div>
        ))}
      </div>

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        {CATEGORIES.map(({ key, label, icon: Icon, color }) => (
          <button key={key} onClick={() => loadArticles(key)}
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-medium cursor-pointer transition-all ${
              activeCat === key
                ? 'text-black shadow-sm'
                : 'text-dark-muted border border-dark-border hover:text-white hover:border-primary'
            }`}
            style={activeCat === key ? { background: color, color: '#000' } : { background: 'transparent' }}>
            <Icon size={14} /> {label}
          </button>
        ))}
      </div>

      {/* Articles Grid */}
      <section className="mb-12">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-white">Latest Articles</h2>
          <Link href="/search" className="text-primary text-sm no-underline flex items-center gap-1 hover:underline">
            View All <ArrowRight size={14} />
          </Link>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {articles.map((a) => (
            <Link key={a.id} href={`/article/${a.id}`} className="group no-underline">
              <div className="rounded-xl border border-dark-border overflow-hidden transition-all group-hover:border-primary group-hover:translate-y-[-2px]" style={{ background: '#1a1a2e' }}>
                <div className="relative h-48 overflow-hidden bg-dark-border">
                  <img src={a.image_url || `https://picsum.photos/seed/${a.id}/800/450`} alt={a.image_alt || a.title}
                    className="w-full h-full object-cover transition-transform group-hover:scale-105" loading="lazy" />
                  {a.category_name && (
                    <span className="absolute top-3 left-3 px-2.5 py-1 rounded-full text-xs font-medium bg-primary/90 text-black">
                      {a.category_name.charAt(0).toUpperCase() + a.category_name.slice(1)}
                    </span>
                  )}
                </div>
                <div className="p-5">
                  <h3 className="text-base font-semibold text-white mb-2 line-clamp-2 group-hover:text-primary transition-colors">
                    {a.title}
                  </h3>
                  <p className="text-sm text-dark-muted line-clamp-2 mb-3">{a.excerpt || a.summary}</p>
                  <div className="flex items-center gap-3 text-xs text-dark-muted">
                    {a.published_at && (
                      <span className="flex items-center gap-1"><Clock size={12} /> {formatDate(a.published_at)}</span>
                    )}
                    <span className="flex items-center gap-1"><Eye size={12} /> {a.view_count || 0}</span>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Trends */}
      <section>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-white">Trending Now</h2>
          <Link href="/trends" className="text-primary text-sm no-underline flex items-center gap-1 hover:underline">
            View All <ArrowRight size={14} />
          </Link>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {trends.map((t, i) => {
            const seed = Array.from(t.keyword).reduce((a, c) => a + c.charCodeAt(0), 0).toString(16)
            return (
              <div key={t.id} className="rounded-lg border border-dark-border overflow-hidden group" style={{ background: '#1a1a2e' }}>
                <div className="relative h-28 overflow-hidden bg-dark-border">
                  <img src={`https://picsum.photos/seed/${seed}/400/225`} alt={t.keyword}
                    className="w-full h-full object-cover transition-transform group-hover:scale-105" loading="lazy" />
                  <div className="absolute inset-0 bg-gradient-to-t from-[#1a1a2e] to-transparent" />
                  <span className="absolute top-2 left-2 px-2 py-0.5 rounded text-[10px] font-medium bg-primary/90 text-black">
                    {t.source}
                  </span>
                </div>
                <div className="p-3">
                  <div className="text-sm font-semibold text-white truncate">{t.keyword}</div>
                  <div className="flex items-center gap-2 mt-1.5">
                    <div className="text-xs text-primary">{t.score}%</div>
                    <div className="flex-1 h-1 rounded-full bg-dark-border overflow-hidden">
                      <div className="h-full rounded-full bg-gradient-to-r from-primary to-primary-dark" style={{ width: `${t.score}%` }} />
                    </div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </section>
    </div>
  )
}
