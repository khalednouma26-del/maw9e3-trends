'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Eye, FileText, Users, Activity, RefreshCw, Play } from 'lucide-react'
import { getDashboardStats, runPipeline } from '@/lib/api'
import type { DashboardStats } from '@/types'

export default function DashboardPage() {
  const router = useRouter()
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.push('/login'); return }
    getDashboardStats().then(setStats).catch(() => { setStats(null) }).finally(() => setLoading(false))
  }, [router])

  const handlePipeline = async () => {
    setRunning(true)
    await runPipeline()
    await getDashboardStats().then(setStats)
    setRunning(false)
  }

  if (loading) return <div className="text-center py-20 text-dark-muted">Loading...</div>

  const cards = [
    { icon: Eye, label: 'Total Views', value: stats?.total_views ?? 0, color: '#00d4aa' },
    { icon: Eye, label: 'Today Views', value: stats?.today_views ?? 0, color: '#00a8ff' },
    { icon: Users, label: 'Unique Visitors', value: stats?.unique_visitors ?? 0, color: '#ffd700' },
    { icon: FileText, label: 'Total Articles', value: stats?.total_articles ?? 0, color: '#ff6b6b' },
    { icon: FileText, label: 'Published', value: stats?.published_articles ?? 0, color: '#51cf66' },
    { icon: Activity, label: 'Views (7 days)', value: stats?.recent_views_7d ?? 0, color: '#cc5de8' },
  ]

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <div className="flex gap-3">
          <button onClick={() => getDashboardStats().then(setStats)}
            className="flex items-center gap-2 px-4 py-2 rounded-lg border border-dark-border text-sm cursor-pointer hover:border-primary transition">
            <RefreshCw size={15} /> Refresh
          </button>
          <button onClick={handlePipeline} disabled={running}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-primary to-primary-dark text-white text-sm font-semibold cursor-pointer disabled:opacity-50 hover:opacity-90 transition">
            <Play size={15} className={running ? 'animate-spin' : ''} />
            {running ? 'Running...' : 'Run Pipeline'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {cards.map(({ icon: Icon, label, value, color }) => (
          <div key={label} className="rounded-xl p-6 border border-dark-border" style={{ background: '#1a1a2e' }}>
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl" style={{ background: `${color}15` }}>
                <Icon size={22} color={color} />
              </div>
              <div>
                <div className="text-xs text-dark-muted">{label}</div>
                <div className="text-2xl font-bold text-white">{value.toLocaleString()}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
