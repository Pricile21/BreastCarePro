import type { Metadata } from 'next'
import { Geist, Geist_Mono } from 'next/font/google'
import { AuthProvider } from '@/contexts/auth-context'
import './globals.css'

const _geist = Geist({ subsets: ["latin"] });
const _geistMono = Geist_Mono({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: 'BreastCare Pro',
  description: 'Plateforme d\'analyse mammographique avec IA - Dépistage du cancer du sein',
  generator: 'BreastCare Pro',
  icons: {
    icon: '/favicon.svg',
    apple: '/favicon.svg',
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`font-sans antialiased`} suppressHydrationWarning>
        <AuthProvider>
          {children}
        </AuthProvider>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              // Tempoirement activé pour debug Docker
              // if (typeof console !== 'undefined') {
              //   console.log = function() {};
              //   console.warn = function() {};
              //   console.error = function() {};
              //   console.info = function() {};
              //   console.debug = function() {};
              // }
              
              // Ignorer les erreurs des extensions de navigateur
              window.addEventListener('error', function(e) {
                if (e.message.includes('translate-page') || 
                    e.message.includes('jquery') ||
                    e.message.includes('content-all')) {
                  e.preventDefault();
                  return false;
                }
              });
            `,
          }}
        />
      </body>
    </html>
  )
}
