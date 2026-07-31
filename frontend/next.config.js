/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  images: { domains: [] },
  async rewrites() {
    return [
      { source: '/api/:path*', destination: `${process.env.API_URL || 'http://localhost:8000'}/api/:path*` },
    ]
  },
}

module.exports = nextConfig
