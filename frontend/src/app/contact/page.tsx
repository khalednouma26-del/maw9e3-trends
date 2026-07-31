'use client'
import { useState } from 'react'
import { Send } from 'lucide-react'
import { submitContact } from '@/lib/api'

export default function ContactPage() {
  const [form, setForm] = useState({ name: '', email: '', subject: '', message: '' })
  const [sent, setSent] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await submitContact(form)
      setSent(true)
    } catch { setError('Failed to send message. Please try again.') }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-6">Contact Us</h1>
      {sent ? (
        <div className="p-8 rounded-xl border border-primary/30 bg-primary/5 text-center">
          <p className="text-lg text-white mb-2">Thank you!</p>
          <p className="text-dark-muted">We've received your message and will get back to you soon.</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <input type="text" placeholder="Your Name" required value={form.name} onChange={e => setForm({ ...form, name: e.target.value })}
              className="w-full px-4 py-3 rounded-lg border border-dark-border bg-dark-card text-white placeholder-dark-muted outline-none focus:border-primary" />
            <input type="email" placeholder="Your Email" required value={form.email} onChange={e => setForm({ ...form, email: e.target.value })}
              className="w-full px-4 py-3 rounded-lg border border-dark-border bg-dark-card text-white placeholder-dark-muted outline-none focus:border-primary" />
          </div>
          <input type="text" placeholder="Subject" required value={form.subject} onChange={e => setForm({ ...form, subject: e.target.value })}
            className="w-full px-4 py-3 rounded-lg border border-dark-border bg-dark-card text-white placeholder-dark-muted outline-none focus:border-primary" />
          <textarea placeholder="Your Message" required rows={6} value={form.message} onChange={e => setForm({ ...form, message: e.target.value })}
            className="w-full px-4 py-3 rounded-lg border border-dark-border bg-dark-card text-white placeholder-dark-muted outline-none focus:border-primary resize-none" />
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button type="submit"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-gradient-to-r from-primary to-primary-dark text-white font-semibold hover:opacity-90 transition cursor-pointer">
            <Send size={16} /> Send Message
          </button>
        </form>
      )}
    </div>
  )
}
