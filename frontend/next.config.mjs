/** @type {import('next').NextConfig} */
const nextConfig = {
  // Use standalone output for Docker deployment (avoids prerendering issues)
  output: 'standalone',
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'upload.wikimedia.org',
      },
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
      },
      {
        protocol: 'https',
        hostname: '**.wikimedia.org',
      },
      {
        protocol: 'https',
        hostname: 'www.cancer.ca',
      },
      {
        protocol: 'https',
        hostname: 'www.cancerresearchuk.org',
      },
      {
        protocol: 'https',
        hostname: 'cdn.cancer.org',
      },
      {
        protocol: 'https',
        hostname: 'www.mayoclinic.org',
      },
      {
        protocol: 'https',
        hostname: 'via.placeholder.com',
      },
    ],
  },
}

export default nextConfig
