"use client"

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { apiClient, type User } from '@/lib/api'

interface AuthContextType {
  user: User | null
  loading: boolean
  error: string | null
  login: (email: string, password: string) => Promise<User>
  logout: () => Promise<void>
  isAuthenticated: boolean
  checkAuth: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const checkAuth = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      
      // Vérifier si un token existe
      const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
      if (!token) {
        console.log("AuthContext: Aucun token trouvé")
        setUser(null)
        return
      }

      console.log("AuthContext: Token trouvé, vérification du type d'utilisateur")
      
      // Vérifier le vrai type d'utilisateur via l'API
      try {
        const userData = await apiClient.getCurrentUser() as User & { user_type?: string }
        console.log("AuthContext: Données utilisateur récupérées:", userData)
        
        // Vérifier la compatibilité entre le type d'utilisateur et la zone actuelle
        const currentPath = window.location.pathname
        
        // Zones possibles
        const isAdminZone = currentPath.startsWith('/admin')
        const isProfessionalZone = currentPath.startsWith('/professional')
        const isMobileZone = currentPath.startsWith('/mobile')
        
        // Vérifier si le type d'utilisateur est compatible avec la zone actuelle
        if (userData.user_type === 'admin' && (isProfessionalZone || isMobileZone)) {
          console.log("AuthContext: Admin détecté dans zone non-admin, déconnexion")
          setUser(null)
          localStorage.removeItem('auth_token')
          if (!isAdminZone || !currentPath.includes('/login')) {
            window.location.href = '/admin/login'
          }
          return
        }
        
        if ((userData.user_type === 'professional' || userData.user_type === 'Professional') && (isAdminZone || isMobileZone)) {
          console.log("AuthContext: Professionnel détecté dans zone non-professionnel, déconnexion")
          setUser(null)
          localStorage.removeItem('auth_token')
          if (!isProfessionalZone || !currentPath.includes('/login')) {
            window.location.href = '/professional/login'
          }
          return
        }
        
        if (userData.user_type === 'patient' && (isAdminZone || isProfessionalZone)) {
          console.log("AuthContext: Patient détecté dans zone non-mobile, déconnexion")
          setUser(null)
          localStorage.removeItem('auth_token')
          if (!isMobileZone || !currentPath.includes('/login')) {
            window.location.href = '/mobile/login'
          }
          return
        }
        
        setUser(userData as User)
      } catch (apiError) {
        console.log("AuthContext: Erreur API lors de /auth/me, nettoyage du token et utilisateur non authentifié")
        setUser(null)
        if (typeof window !== 'undefined') {
          localStorage.removeItem('auth_token')
        }
      }
    } catch (err) {
      console.error("AuthContext: Erreur de vérification:", err)
      setUser(null)
      setError(err instanceof Error ? err.message : 'Authentication failed')
    } finally {
      setLoading(false)
    }
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    try {
      setLoading(true)
      setError(null)
      
      console.log("AuthContext: Tentative de connexion...")
      // Pas de paramètre source pour les autres plateformes (admin, professional)
      const response = await apiClient.login(email, password)
      console.log("AuthContext: Connexion réussie, token reçu")
      
      const userData = await apiClient.getCurrentUser() as User
      setUser(userData)
      console.log("AuthContext: Données utilisateur récupérées:", userData)
      
      return userData
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Login failed'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const logout = useCallback(async () => {
    try {
      // Supprimer le token du localStorage explicitement
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token')
      }
      // Appeler l'API de déconnexion (peut échouer si le token est invalide, mais on continue quand même)
      try {
        await apiClient.logout()
      } catch (apiErr) {
        // Ignorer les erreurs API lors de la déconnexion (le token peut être déjà invalide)
        console.log("Note: Erreur API lors de la déconnexion (ignorée):", apiErr)
      }
      // Nettoyer l'état local
      setUser(null)
      setError(null)
      // Ne pas rediriger ici - laisser le composant appelant gérer la redirection
      // Cela permet d'avoir des redirections différentes selon le contexte (mobile, admin, etc.)
    } catch (err) {
      console.error("Erreur lors de la déconnexion:", err)
      // Même en cas d'erreur, nettoyer l'état local
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token')
      }
      setUser(null)
      setError(null)
    }
  }, [])

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  // Écouter les changements de localStorage pour détecter les nouvelles connexions
  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'auth_token') {
        console.log("AuthContext: Changement de token détecté dans localStorage")
        checkAuth()
      }
    }

    // Écouter les événements de stockage depuis d'autres onglets/fenêtres
    window.addEventListener('storage', handleStorageChange)

    // Vérifier aussi lors du focus de la fenêtre (cas où l'utilisateur se connecte dans le même onglet)
    const handleFocus = () => {
      const token = localStorage.getItem('auth_token')
      if (token && !user) {
        console.log("AuthContext: Token trouvé au focus, vérification...")
        checkAuth()
      }
    }

    window.addEventListener('focus', handleFocus)

    // Vérifier périodiquement si un token a été ajouté (pour le cas où l'utilisateur se connecte dans le même onglet)
    const interval = setInterval(() => {
      const token = localStorage.getItem('auth_token')
      if (token && !user) {
        console.log("AuthContext: Token trouvé lors de la vérification périodique")
        checkAuth()
      }
    }, 1000) // Vérifier toutes les secondes

    return () => {
      window.removeEventListener('storage', handleStorageChange)
      window.removeEventListener('focus', handleFocus)
      clearInterval(interval)
    }
  }, [checkAuth, user])

  const value = {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated: !!user,
    checkAuth,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
