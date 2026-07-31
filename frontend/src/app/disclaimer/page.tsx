export default function DisclaimerPage() {
  return (
    <div className="max-w-3xl mx-auto prose">
      <h1 className="text-3xl font-bold text-white">Disclaimer</h1>
      <p className="text-dark-muted">Last updated: {new Date().toLocaleDateString()}</p>
      <h2 className="text-xl font-bold text-white mt-8">Content Disclaimer</h2>
      <p>The content on Maw9e3 Trends is generated using artificial intelligence. While we strive for accuracy and quality, we make no representations or warranties about the completeness, accuracy, or reliability of any content.</p>
      <h2 className="text-xl font-bold text-white mt-8">Not Professional Advice</h2>
      <p>The information provided on this website is for general informational purposes only and does not constitute professional advice. You should consult appropriate professionals for advice tailored to your situation.</p>
      <h2 className="text-xl font-bold text-white mt-8">External Links</h2>
      <p>This website may contain links to external sites. We are not responsible for the content or practices of any third-party websites.</p>
      <h2 className="text-xl font-bold text-white mt-8">Affiliate Disclosure</h2>
      <p>This website may use Google AdSense and other advertising networks. We may earn commissions from qualifying purchases or clicks.</p>
      <h2 className="text-xl font-bold text-white mt-8">Changes</h2>
      <p>This disclaimer may be updated periodically. Please check back for changes.</p>
    </div>
  )
}
