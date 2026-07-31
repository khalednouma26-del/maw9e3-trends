import type { Metadata, Viewport } from 'next'
import './globals.css'

export const viewport: Viewport = {
  themeColor: '#0f0f1a',
  width: 'device-width',
  initialScale: 1,
}
import ThemeProvider from '@/components/layout/ThemeProvider'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'

const siteUrl = process.env.SITE_URL || 'http://localhost:3000'

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: { default: 'Maw9e3 Trends - Trending Topics & Fresh Content', template: '%s | Maw9e3 Trends' },
  description: 'Discover trending topics, read insightful articles, and stay informed about what matters.',
  robots: { index: true, follow: true },
  icons: { icon: '/favicon.ico' },
  openGraph: { title: 'Maw9e3 Trends', description: 'Trending topics and fresh content daily', type: 'website', siteName: 'Maw9e3 Trends' },
  twitter: { card: 'summary_large_image', title: 'Maw9e3 Trends', description: 'Trending topics and fresh content daily' },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-dark-bg text-dark-text antialiased">
        <ThemeProvider>
          <Header />
          <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8">{children}</main>
          <Footer />
        </ThemeProvider>
      </body>
    </html>
  )
}
