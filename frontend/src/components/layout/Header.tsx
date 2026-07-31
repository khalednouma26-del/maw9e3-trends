'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Sparkles, TrendingUp, Home, Search, LayoutDashboard, Sun, Moon, Menu, X, LogOut } from 'lucide-react'
import { useState, useEffect } from 'react'
import { useTheme } from './ThemeProvider'

const navLinks = [
  { href: '/', label: 'Home', icon: Home },
  { href: '/trends', label: 'Trends', icon: TrendingUp },
  { href: '/search', label: 'Search', icon: Search },
]

export default function Header() {
  const pathname = usePathname()
  const { theme, toggleTheme } = useTheme()
  const [menuOpen, setMenuOpen] = useState(false)
  const [user, setUser] = useState<{ username: string } | null>(null)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      fetch('/api/auth/me', { headers: { Authorization: `Bearer ${token}` } })
        .then(r => r.ok ? r.json() : null)
        .then(u => setUser(u))
        .catch(() => {})
    }
  }, [])

  const isAdmin = user !== null

  return (
    <header className="border-b border-dark-border" style={{ background: '#1a1a2e' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2 text-primary font-bold text-xl no-underline">
            <Sparkles size={24} /> Maw9e3 Trends
          </Link>

          <nav className="hidden md:flex items-center gap-1" aria-label="Main navigation">
            {navLinks.map(({ href, label, icon: Icon }) => (
              <Link
                key={href}
                href={href}
                className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium no-underline transition-colors ${
                  pathname === href ? 'text-primary bg-primary/10' : 'text-dark-muted hover:text-gray-200'
                }`}
              >
                <Icon size={16} /> {label}
              </Link>
            ))}
            {isAdmin && (
              <Link href="/dashboard"
                className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium no-underline transition-colors ${
                  pathname === '/dashboard' ? 'text-primary bg-primary/10' : 'text-dark-muted hover:text-gray-200'
                }`}
              >
                <LayoutDashboard size={16} /> Dashboard
              </Link>
            )}
            {isAdmin && (
              <button onClick={() => { localStorage.removeItem('token'); setUser(null) }}
                className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm text-dark-muted hover:text-gray-200">
                <LogOut size={16} /> Logout
              </button>
            )}
            <button onClick={toggleTheme} aria-label="Toggle theme" className="ml-2 p-2 rounded-lg text-dark-muted hover:text-gray-200 cursor-pointer">
              {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </nav>

          <button className="md:hidden p-2 text-dark-muted" onClick={() => setMenuOpen(!menuOpen)} aria-label={menuOpen ? 'Close menu' : 'Open menu'}>
            {menuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {menuOpen && (
          <div className="md:hidden pb-4 space-y-1" role="navigation" aria-label="Mobile navigation">
            {navLinks.map(({ href, label, icon: Icon }) => (
              <Link key={href} href={href} onClick={() => setMenuOpen(false)}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm no-underline ${
                  pathname === href ? 'text-primary bg-primary/10' : 'text-dark-muted'
                }`}
              >
                <Icon size={16} /> {label}
              </Link>
            ))}
            {isAdmin && (
              <Link href="/dashboard" onClick={() => setMenuOpen(false)}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm no-underline ${
                  pathname === '/dashboard' ? 'text-primary bg-primary/10' : 'text-dark-muted'
                }`}
              >
                <LayoutDashboard size={16} /> Dashboard
              </Link>
            )}
          </div>
        )}
      </div>
    </header>
  )
}
