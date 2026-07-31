import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="flex items-center justify-center min-h-[60vh] text-center">
      <div>
        <h1 className="text-6xl font-bold text-primary mb-4">404</h1>
        <h2 className="text-2xl text-white mb-2">Page not found</h2>
        <p className="text-dark-muted mb-6">The page you are looking for does not exist or has been moved.</p>
        <Link href="/" className="inline-flex items-center gap-2 px-6 py-3 rounded-xl text-white font-semibold bg-gradient-to-r from-primary to-primary-dark hover:opacity-90 transition no-underline">
          Go Home
        </Link>
      </div>
    </div>
  )
}
