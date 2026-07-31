'use client'
import { useEffect, useState } from 'react'
import { RefreshCw, Globe, Newspaper, MessageCircle } from 'lucide-react'
import { getTrends, refreshTrends } from '@/lib/api'
import type { Trend } from '@/types'

const sourceIcons: Record<string, typeof Globe> = {
  google_trends: Globe, google_news: Newspaper, reddit: MessageCircle,
  youtube: MessageCircle, twitter: MessageCircle, rss: Newspaper,
}

export default function TrendsPage() {
  const [trends, setTrends] = useState<Trend[]>([])
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)

  const load = () => getTrends().then(setTrends).catch(() => {}).finally(() => setLoading(false))
  useEffect(() => { load() }, [])

  const handleRefresh = async () => {
    setRefreshing(true)
    await refreshTrends()
    await load()
    setRefreshing(false)
  }

  if (loading) return <div className="text-center py-20 text-dark-muted">Loading...</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-white">Trending Searches</h1>
        <button onClick={handleRefresh} disabled={refreshing}
          className="flex items-center gap-2 px-4 py-2 rounded-lg border border-dark-border text-sm text-dark-text cursor-pointer hover:border-primary transition"
        >
          <RefreshCw size={15} className={refreshing ? 'animate-spin' : ''} />
          {refreshing ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      <div className="space-y-2">
        {trends.map((t, i) => {
          const Icon = sourceIcons[t.source] || Globe
          return (
            <div key={t.id} className="flex items-center gap-4 p-4 rounded-xl border border-dark-border" style={{ background: '#1a1a2e' }}>
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold ${i < 3 ? 'bg-primary text-black' : 'bg-dark-border text-dark-muted'}`}>
                {i + 1}
              </div>
              <Icon size={16} className="text-dark-muted shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="text-sm font-semibold text-white truncate">{t.keyword}</div>
                <div className="text-xs text-dark-muted">{t.source}</div>
              </div>
              <div className="text-sm text-primary font-medium">{t.score}%</div>
              <div className="w-20 h-2 rounded-full bg-dark-border overflow-hidden hidden sm:block">
                <div className="h-full rounded-full bg-gradient-to-r from-primary to-primary-dark" style={{ width: `${t.score}%` }} />
              </div>
            </div>
          )
        })}
      </div>

      {trends.length === 0 && (
        <div className="text-center py-16 text-dark-muted">
          No trends yet. Click "Refresh" to discover trending topics from 8 sources.
        </div>
      )}
    </div>
  )
}
