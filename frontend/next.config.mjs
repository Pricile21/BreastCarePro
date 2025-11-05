/** @type {import('next').NextConfig} */
const nextConfig = {
  // Disable static optimization for dynamic pages
  experimental: {
    missingSuspenseWithCSRBailout: false,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  // Skip build-time errors for pages that use useSearchParams
  onDemandEntries: {
    maxInactiveAge: 25 * 1000,
    pagesBufferLength: 2,
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
