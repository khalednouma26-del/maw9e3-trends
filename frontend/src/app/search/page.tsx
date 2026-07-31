'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Search, ArrowRight, Clock, Eye } from 'lucide-react'
import { getArticles } from '@/lib/api'
import type { Article } from '@/types'
import { formatDate } from '@/lib/utils'

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<Article[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => { loadAll() }, [])

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await getArticles(query.trim() ? { search: query } : undefined)
      setResults(res.articles)
    } catch { setResults([]); setQuery('') }
    setLoading(false)
  }

  const loadAll = () => {
    setLoading(true)
    getArticles().then(r => setResults(r.articles)).catch(() => {}).finally(() => setLoading(false))
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-white mb-6">All Articles</h1>

      <form onSubmit={handleSearch} className="relative mb-8">
        <input type="text" value={query} onChange={e => setQuery(e.target.value)}
          placeholder="Search articles, topics, keywords..."
          className="w-full px-5 py-3.5 pr-12 rounded-xl border border-dark-border bg-dark-card text-white placeholder-dark-muted outline-none focus:border-primary transition" />
        <button type="submit" className="absolute right-3 top-1/2 -translate-y-1/2 p-2 text-dark-muted hover:text-primary cursor-pointer">
          <Search size={20} />
        </button>
      </form>

      {loading && <div className="text-center py-12 text-dark-muted">Loading...</div>}

      {!loading && (
        <div className="space-y-3">
          <p className="text-sm text-dark-muted mb-4">{results.length} article{results.length !== 1 ? 's' : ''}</p>
          {results.map((a) => (
            <Link key={a.id} href={`/article/${a.id}`} className="group no-underline block">
              <div className="flex gap-4 rounded-xl p-4 border border-dark-border transition-colors group-hover:border-primary" style={{ background: '#1a1a2e' }}>
                <div className="w-24 h-20 shrink-0 rounded-lg overflow-hidden bg-dark-border hidden sm:block">
                  <img src={a.image_url || `https://picsum.photos/seed/${a.id}/200/150`} alt={a.image_alt || a.title}
                    className="w-full h-full object-cover" loading="lazy" />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-base font-semibold text-white mb-1 line-clamp-2 group-hover:text-primary">{a.title}</h3>
                  <p className="text-sm text-dark-muted line-clamp-1">{a.excerpt || a.summary}</p>
                  <div className="flex items-center gap-3 text-xs text-dark-muted mt-2">
                    {a.category_name && <span className="text-primary">{a.category_name.charAt(0).toUpperCase() + a.category_name.slice(1)}</span>}
                    {a.published_at && <span className="flex items-center gap-1"><Clock size={11} /> {formatDate(a.published_at)}</span>}
                    <span className="flex items-center gap-1"><Eye size={11} /> {a.view_count || 0}</span>
                  </div>
                </div>
                <div className="flex items-center">
                  <ArrowRight size={16} className="text-dark-muted group-hover:text-primary" />
                </div>
              </div>
            </Link>
          ))}
          {results.length === 0 && <div className="text-center py-12 text-dark-muted">No articles found.</div>}
        </div>
      )}
    </div>
  )
}
