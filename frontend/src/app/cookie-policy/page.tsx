export default function CookiePolicyPage() {
  return (
    <div className="max-w-3xl mx-auto prose">
      <h1 className="text-3xl font-bold text-white">Cookie Policy</h1>
      <p className="text-dark-muted">Last updated: {new Date().toLocaleDateString()}</p>
      <p>This website uses cookies to enhance your browsing experience and provide analytics.</p>
      <h2 className="text-xl font-bold text-white mt-8">What Are Cookies</h2>
      <p>Cookies are small text files stored on your device when you visit a website. They help us remember your preferences and understand how you use our site.</p>
      <h2 className="text-xl font-bold text-white mt-8">Types of Cookies We Use</h2>
      <ul><li><strong>Essential:</strong> Required for basic site functionality</li><li><strong>Analytics:</strong> Help us understand traffic patterns</li><li><strong>Advertising:</strong> Used by Google AdSense to serve relevant ads</li></ul>
      <h2 className="text-xl font-bold text-white mt-8">Managing Cookies</h2>
      <p>You can control cookies through your browser settings. Disabling cookies may affect site functionality.</p>
      <h2 className="text-xl font-bold text-white mt-8">Third-Party Cookies</h2>
      <p>Google AdSense uses cookies for ad personalization. You can opt out of personalized advertising at <a href="https://www.google.com/settings/ads" className="text-primary">Google Ad Settings</a>.</p>
    </div>
  )
}
