/**
 * Application configuration
 */

export const config = {
  api: {
    baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
    timeout: 30000,
  },
  app: {
    name: process.env.NEXT_PUBLIC_APP_NAME || 'BreastCare Pro',
    version: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
  },
  features: {
    enableAnalytics: process.env.NODE_ENV === 'production',
    enableDebug: process.env.NODE_ENV === 'development',
  },
} as const;
