"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/contexts/auth-context"
import { Loader2 } from "lucide-react"

interface AuthGuardProps {
  children: React.ReactNode
  fallback?: React.ReactNode
}

export function AuthGuard({ children, fallback }: AuthGuardProps) {
  const { user, loading, isAuthenticated } = useAuth()
  const router = useRouter()

  // Vérification du token avec gestion d'erreur
  const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
  
  // Gérer les redirections dans useEffect pour éviter les erreurs de rendu
  useEffect(() => {
    // Si pas de token ET pas en cours de chargement, rediriger
    if (!token && !loading) {
      console.log("AuthGuard: Pas de token, redirection vers login")
      router.push("/admin/login")
    }
  }, [token, loading, router])

  // Si pas de token ET pas en cours de chargement, ne rien afficher (redirection en cours)
  if (!token && !loading) {
    return null
  }

  // Si en cours de chargement, afficher le loader
  if (loading) {
    return (
      fallback || (
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
            <p className="text-muted-foreground">Vérification de l'authentification...</p>
          </div>
        </div>
      )
    )
  }

  // Si authentifié, afficher le contenu
  if (isAuthenticated && user) {
    return <>{children}</>
  }

  // Gérer la redirection si pas authentifié après chargement
  useEffect(() => {
    if (!isAuthenticated && !loading) {
      console.log("AuthGuard: Pas authentifié, redirection vers login")
      router.push("/admin/login")
    }
  }, [isAuthenticated, loading, router])

  // Si pas authentifié après chargement, ne rien afficher (redirection en cours)
  if (!isAuthenticated && !loading) {
    return null
  }

  return null
}
