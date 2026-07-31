'use client'
import { useEffect } from 'react'

export default function Error({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  useEffect(() => { console.error(error) }, [error])
  return (
    <div className="flex items-center justify-center min-h-[60vh] text-center">
      <div>
        <h2 className="text-2xl text-white mb-2">Something went wrong</h2>
        <p className="text-dark-muted mb-6">An unexpected error occurred. Please try again.</p>
        <button onClick={reset}
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl text-white font-semibold bg-gradient-to-r from-primary to-primary-dark hover:opacity-90 transition cursor-pointer">
          Try Again
        </button>
      </div>
    </div>
  )
}
