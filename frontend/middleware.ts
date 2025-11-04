import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Vérifier si l'utilisateur est sur une route admin
  if (request.nextUrl.pathname.startsWith('/admin')) {
    // Exclure la page de login
    if (request.nextUrl.pathname === '/admin/login') {
      return NextResponse.next()
    }

    // SOLUTION 1: Désactiver temporairement le middleware pour les routes admin
    // et laisser AuthGuard gérer l'authentification côté client
    return NextResponse.next()
    
    // SOLUTION 2 (Alternative): Vérifier le token dans les cookies ET localStorage
    // const token = request.cookies.get('auth_token')?.value
    // if (!token) {
    //   return NextResponse.redirect(new URL('/admin/login', request.url))
    // }
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    '/admin/:path*',
  ],
}
