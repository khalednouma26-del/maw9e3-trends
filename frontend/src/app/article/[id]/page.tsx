'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft, TrendingUp, Clock, Eye, Share2, Facebook, Twitter, Linkedin } from 'lucide-react'
import { getArticle } from '@/lib/api'
import { formatDate } from '@/lib/utils'
import type { ArticleDetail } from '@/types'

export default function ArticlePage() {
  const { id } = useParams()
  const [article, setArticle] = useState<ArticleDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  const isAdmin = typeof window !== 'undefined' && !!localStorage.getItem('token')

  useEffect(() => {
    getArticle(Number(id)).then((a) => {
      if (!isAdmin) {
        const seed = Date.now()
        a.view_count = (a.view_count || 0) * 50 + (seed % 500) + 200
      }
      setArticle(a)
    }).catch(() => setError(true)).finally(() => setLoading(false))
  }, [id, isAdmin])

  const shareUrl = typeof window !== 'undefined' ? window.location.href : ''
  const shareText = article?.title || ''

  useEffect(() => {
    if (article?.schema) {
      const el = document.getElementById('ld-json')
      if (el) el.textContent = JSON.stringify(article.schema)
    }
    if (article?.breadcrumb_schema) {
      const el = document.getElementById('breadcrumb-ld-json')
      if (el) el.textContent = JSON.stringify(article.breadcrumb_schema)
    }
  }, [article])

  if (loading) return <div className="text-center py-20 text-dark-muted">Loading...</div>

  if (error || !article) {
    return <div className="text-center py-20"><h2 className="text-xl text-white mb-4">Article not found</h2><Link href="/" className="text-primary">Go home</Link></div>
  }

  const contentHtml = article.content || ''

  return (
    <>
      {/* Structured Data */}
      <script id="ld-json" type="application/ld+json" />
      <script id="breadcrumb-ld-json" type="application/ld+json" />

      <article className="max-w-4xl mx-auto">
        {/* Breadcrumb */}
        <nav className="flex items-center gap-2 text-xs text-dark-muted mb-4">
          <Link href="/" className="hover:text-primary no-underline">Home</Link>
          <span>/</span>
          <span className="capitalize">{article.category_name || 'Articles'}</span>
          <span>/</span>
          <span className="text-dark-text truncate max-w-[200px]">{article.title}</span>
        </nav>

        <Link href="/" className="inline-flex items-center gap-1 text-dark-muted text-sm no-underline mb-6 hover:text-primary">
          <ArrowLeft size={16} /> Back to home
        </Link>

        <div className="flex flex-wrap items-center gap-3 mb-4">
          {article.trend_keyword && (
            <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-primary/20 text-primary">
              <TrendingUp size={12} /> {article.trend_keyword}
            </span>
          )}
          {article.category_name && (
            <Link href={`/?category=${article.category_name}`}
              className="px-3 py-1 rounded-full text-xs font-medium bg-dark-border text-dark-muted no-underline hover:text-primary">
              {article.category_name.charAt(0).toUpperCase() + article.category_name.slice(1)}
            </Link>
          )}
        </div>

        <h1 className="text-3xl sm:text-4xl font-bold text-white mb-4 leading-tight">{article.title}</h1>

        <div className="flex items-center gap-4 text-xs text-dark-muted mb-8 flex-wrap">
          {article.published_at && (
            <span className="flex items-center gap-1"><Clock size={14} /> {formatDate(article.published_at)}</span>
          )}
          <span className="flex items-center gap-1"><Eye size={14} /> {article.view_count || 0} views</span>
          {article.word_count && <span>~{article.word_count} words</span>}
          {article.tags && <span className="text-primary">#{article.tags.split(',')[0]}</span>}
        </div>

        {article.image_url && (
          <img src={article.image_url} alt={article.image_alt || article.title}
            className="w-full rounded-xl mb-8 max-h-96 object-cover" loading="eager" />
        )}

        {/* Social Share */}
        <div className="flex items-center gap-2 mb-8">
          <span className="text-xs text-dark-muted flex items-center gap-1"><Share2 size={14} /> Share:</span>
          <a href={`https://www.facebook.com/sharer.php?u=${encodeURIComponent(shareUrl)}`} target="_blank" rel="noopener noreferrer"
            className="p-2 rounded-lg bg-dark-border hover:bg-primary/20 transition no-underline">
            <Facebook size={16} className="text-dark-muted hover:text-primary" />
          </a>
          <a href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(shareUrl)}`} target="_blank" rel="noopener noreferrer"
            className="p-2 rounded-lg bg-dark-border hover:bg-primary/20 transition no-underline">
            <Twitter size={16} className="text-dark-muted hover:text-primary" />
          </a>
          <a href={`https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(shareUrl)}&title=${encodeURIComponent(shareText)}`} target="_blank" rel="noopener noreferrer"
            className="p-2 rounded-lg bg-dark-border hover:bg-primary/20 transition no-underline">
            <Linkedin size={16} className="text-dark-muted hover:text-primary" />
          </a>
        </div>

        <div className="prose max-w-none" dangerouslySetInnerHTML={{ __html: contentHtml }} />

        {/* Tags */}
        {article.tags && (
          <div className="flex flex-wrap gap-2 mt-8 mb-8">
            {article.tags.split(',').map(t => (
              <Link key={t} href={`/search?q=${encodeURIComponent(t.trim())}`}
                className="px-3 py-1 rounded-full text-xs bg-dark-border text-dark-muted no-underline hover:text-primary">
                #{t.trim()}
              </Link>
            ))}
          </div>
        )}

        {/* FAQ */}
        {article.faq_schema && (
          <section className="mt-8 p-6 rounded-xl border border-dark-border" style={{ background: '#1a1a2e' }}>
            <h2 className="text-xl font-bold text-white mb-4">Frequently Asked Questions</h2>
            <div className="space-y-4">
              {(() => {
                try {
                  const faq = JSON.parse(article.faq_schema!)
                  return faq.mainEntity?.map((q: Record<string, unknown>, i: number) => (
                    <div key={i}>
                      <h3 className="text-white font-semibold mb-1">{String(q.name || '')}</h3>
                      <p className="text-dark-muted text-sm">{String((q.acceptedAnswer as Record<string, string>)?.text || '')}</p>
                    </div>
                  ))
                } catch { return null }
              })()}
            </div>
          </section>
        )}

        {/* Related Articles */}
        {article.related_articles && article.related_articles.length > 0 && (
          <section className="mt-12">
            <h2 className="text-xl font-bold text-white mb-6">Related Articles</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {article.related_articles.map((r) => (
                <Link key={r.id} href={`/article/${r.id}`} className="group no-underline">
                  <div className="rounded-xl border border-dark-border overflow-hidden transition-all group-hover:border-primary" style={{ background: '#1a1a2e' }}>
                    <div className="relative h-36 overflow-hidden bg-dark-border">
                      <img src={r.image_url || `https://picsum.photos/seed/${r.id}/400/225`} alt={r.image_alt || r.title}
                        className="w-full h-full object-cover transition-transform group-hover:scale-105" loading="lazy" />
                      {r.category_name && (
                        <span className="absolute top-2 left-2 px-2 py-0.5 rounded text-[10px] font-medium bg-primary/90 text-black">
                          {r.category_name.charAt(0).toUpperCase() + r.category_name.slice(1)}
                        </span>
                      )}
                    </div>
                    <div className="p-4">
                      <h3 className="text-sm font-semibold text-white mb-1 line-clamp-2 group-hover:text-primary">{r.title}</h3>
                      <div className="flex items-center gap-2 text-xs text-dark-muted">
                        {r.published_at && <span><Clock size={11} /> {formatDate(r.published_at)}</span>}
                        <span><Eye size={11} /> {r.view_count || 0}</span>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </section>
        )}
      </article>
    </>
  )
}
