export default function TermsPage() {
  return (
    <div className="max-w-3xl mx-auto prose">
      <h1 className="text-3xl font-bold text-white">Terms of Service</h1>
      <p className="text-dark-muted">Last updated: {new Date().toLocaleDateString()}</p>
      <p>By using Maw9e3 Trends, you agree to these terms of service.</p>
      <h2 className="text-xl font-bold text-white mt-8">Use of Content</h2>
      <p>All content on this website is for informational purposes only. We strive for accuracy but make no guarantees. Information should be verified independently where appropriate.</p>
      <h2 className="text-xl font-bold text-white mt-8">Intellectual Property</h2>
      <p>All content published on Maw9e3 Trends is owned by us unless otherwise stated. Unauthorized reproduction is prohibited.</p>
      <h2 className="text-xl font-bold text-white mt-8">Limitation of Liability</h2>
      <p>We are not liable for any damages arising from the use of this website or its content.</p>
      <h2 className="text-xl font-bold text-white mt-8">Changes</h2>
      <p>We reserve the right to modify these terms at any time. Continued use constitutes acceptance of changes.</p>
    </div>
  )
}
