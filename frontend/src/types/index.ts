export interface Trend {
  id: number
  keyword: string
  source: string
  score: number
  search_volume: number | null
  category: string | null
  fetched_at: string
}

export interface Article {
  id: number
  title: string
  slug: string
  summary: string
  content?: string
  meta_title?: string
  meta_description?: string
  excerpt?: string
  tags?: string
  category_name?: string
  trend_keyword?: string
  image_url?: string
  image_alt?: string
  word_count?: number
  view_count?: number
  published?: number
  published_at?: string
  created_at?: string
  faq_schema?: string
  schema?: Record<string, unknown>
}

export interface DashboardStats {
  total_views: number
  today_views: number
  unique_visitors: number
  total_articles: number
  published_articles: number
  recent_views_7d: number
  draft_articles: number
}

export interface ArticleDetail extends Article {
  breadcrumb_schema?: Record<string, unknown>
  related_articles?: Article[]
}
