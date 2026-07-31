export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-6">About Maw9e3 Trends</h1>
      <div className="prose max-w-none space-y-4 text-dark-text">
        <p>Maw9e3 Trends is a trending topics and content platform. We monitor multiple sources including Google Trends, Google News, RSS feeds, Reddit, YouTube, Twitter, Hacker News, and GitHub to identify relevant trending topics.</p>
        <p>Our goal is to provide readers with insightful, well-structured articles about what's happening in the world right now.</p>
        <h2 className="text-xl font-bold text-white mt-8 mb-4">Our Mission</h2>
        <p>To help people stay informed about trending topics by providing accessible, quality content that explains what's happening and why it matters.</p>
        <h2 className="text-xl font-bold text-white mt-8 mb-4">How It Works</h2>
        <ol className="list-decimal pl-5 space-y-2">
          <li><strong>Discover</strong> - We monitor 8+ sources for trending topics</li>
          <li><strong>Research</strong> - Each topic is researched for quality and relevance</li>
          <li><strong>Write</strong> - We create original content with proper structure</li>
          <li><strong>Publish</strong> - Articles are published and made available to readers</li>
          <li><strong>Update</strong> - Content is refreshed to keep it current</li>
        </ol>
      </div>
    </div>
  )
}
