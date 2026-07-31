'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Sparkles, LogIn } from 'lucide-react'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const form = new URLSearchParams()
      form.set('username', email)
      form.set('password', password)
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: form,
      })
      if (!res.ok) { setError('Invalid credentials'); return }
      const data = await res.json()
      localStorage.setItem('token', data.access_token)
      router.push('/dashboard')
    } catch { setError('Connection error') }
    finally { setLoading(false) }
  }

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="w-full max-w-md rounded-xl p-8 border border-dark-border" style={{ background: '#1a1a2e' }}>
        <div className="flex items-center gap-2 text-primary font-bold text-xl mb-6 justify-center">
          <Sparkles size={24} /> Admin Login
        </div>
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm text-dark-muted mb-1">Email</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)}
              className="w-full px-4 py-2.5 rounded-lg border border-dark-border bg-dark-bg text-white text-sm outline-none focus:border-primary" required />
          </div>
          <div>
            <label className="block text-sm text-dark-muted mb-1">Password</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)}
              className="w-full px-4 py-2.5 rounded-lg border border-dark-border bg-dark-bg text-white text-sm outline-none focus:border-primary" required />
          </div>
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button type="submit" disabled={loading}
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-gradient-to-r from-primary to-primary-dark text-white text-sm font-semibold cursor-pointer disabled:opacity-50 hover:opacity-90 transition">
            <LogIn size={16} /> {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  )
}
