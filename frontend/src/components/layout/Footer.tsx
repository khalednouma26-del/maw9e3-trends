import Link from 'next/link'
import { Sparkles } from 'lucide-react'

export default function Footer() {
  const links = [
    { href: '/about', label: 'About Us' },
    { href: '/contact', label: 'Contact' },
    { href: '/privacy', label: 'Privacy Policy' },
    { href: '/terms', label: 'Terms of Service' },
    { href: '/cookie-policy', label: 'Cookie Policy' },
    { href: '/disclaimer', label: 'Disclaimer' },
  ]

  return (
    <footer className="border-t border-dark-border mt-16" style={{ background: '#1a1a2e' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div className="flex items-center gap-2 text-primary font-bold text-lg mb-4">
              <Sparkles size={20} /> Maw9e3 Trends
            </div>
            <p className="text-dark-muted text-sm leading-relaxed">
              Your source for trending topics and insightful articles. Stay informed about what's happening in the world.
            </p>
          </div>
          <div>
            <h3 className="text-white font-semibold mb-4">Quick Links</h3>
            <div className="space-y-2">
              {links.slice(0, 3).map(({ href, label }) => (
                <Link key={href} href={href} className="block text-dark-muted text-sm no-underline hover:text-primary transition-colors">
                  {label}
                </Link>
              ))}
            </div>
          </div>
          <div>
            <h3 className="text-white font-semibold mb-4">Policies</h3>
            <div className="space-y-2">
              {links.slice(3).map(({ href, label }) => (
                <Link key={href} href={href} className="block text-dark-muted text-sm no-underline hover:text-primary transition-colors">
                  {label}
                </Link>
              ))}
            </div>
          </div>
        </div>
        <div className="border-t border-dark-border mt-8 pt-8 text-center text-dark-muted text-sm">
          &copy; {new Date().getFullYear()} Maw9e3 Trends. All rights reserved.
        </div>
      </div>
    </footer>
  )
}
