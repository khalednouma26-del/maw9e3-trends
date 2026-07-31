export default function PrivacyPage() {
  return (
    <div className="max-w-3xl mx-auto prose">
      <h1 className="text-3xl font-bold text-white">Privacy Policy</h1>
      <p className="text-dark-muted">Last updated: {new Date().toLocaleDateString()}</p>
      <p>At Maw9e3 Trends, we take your privacy seriously. This policy describes how we collect, use, and protect your information.</p>
      <h2 className="text-xl font-bold text-white mt-8">Information We Collect</h2>
      <ul><li>Basic analytics data (page views, referrer, browser info)</li><li>Contact form submissions (name, email, message)</li><li>Cookies for essential functionality</li></ul>
      <h2 className="text-xl font-bold text-white mt-8">How We Use Your Data</h2>
      <ul><li>To improve our content and user experience</li><li>To respond to your inquiries</li><li>To comply with legal obligations</li></ul>
      <h2 className="text-xl font-bold text-white mt-8">Third-Party Services</h2>
      <p>We use Google AdSense for monetization. Google may use cookies for ad personalization. You can manage your ad preferences through your Google account settings.</p>
      <h2 className="text-xl font-bold text-white mt-8">Contact</h2>
      <p>If you have questions about this policy, please contact us through our contact page.</p>
    </div>
  )
}
