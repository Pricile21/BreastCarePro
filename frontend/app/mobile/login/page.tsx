"use client"

import type React from "react"

import { useState, useEffect } from "react"
import Link from "next/link"
import { useRouter, useSearchParams } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Heart, ArrowLeft } from "lucide-react"
import { apiClient } from "@/lib/api"
import { useAuth } from "@/contexts/auth-context"

export default function MobileLoginPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const { checkAuth } = useAuth()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setIsLoading(true)

    try {
      // Call the real API avec le paramètre source='mobile' pour bloquer les admins côté backend
      // Le backend retournera une erreur 403 si c'est un admin
      const response = await apiClient.login(email, password, 'mobile')
      
      // Store the token
      if (typeof window !== 'undefined') {
        localStorage.setItem('auth_token', response.access_token)
      }
      
      // Mettre à jour le contexte d'authentification
      await checkAuth()
      await new Promise(resolve => setTimeout(resolve, 200))
      
      // Vérifier le type d'utilisateur après la connexion
      try {
        const userData = await apiClient.getCurrentUser()
        
        // Bloquer les admins (le backend devrait déjà le faire, mais vérification supplémentaire)
        if (userData.user_type === 'admin') {
          setError("❌ Les administrateurs doivent se connecter via la plateforme d'administration.")
          localStorage.removeItem('auth_token')
          return
        }
        
        // Bloquer les professionnels de santé (ils doivent utiliser /professional/login)
        if (userData.user_type === 'professional') {
          setError("❌ Les professionnels de santé doivent se connecter via la plateforme professionnelle (/professional/login).")
          localStorage.removeItem('auth_token')
          return
        }
      } catch (userErr) {
        console.error('Erreur lors de la récupération du profil utilisateur:', userErr)
        // Continuer quand même la connexion si on ne peut pas vérifier le type
      }
      
      console.log('✅ Connexion réussie pour la plateforme mobile')
      
      // FORCER la redirection vers /mobile (page d'accueil) et NON vers /mobile/dashboard
      const redirectParam = searchParams.get('redirect')
      const redirectUrl = redirectParam || '/mobile'
      
      console.log('🔀 Mobile Login - Redirection vers:', redirectUrl)
      console.log('🔀 Paramètre redirect dans URL:', redirectParam)
      
      // Utiliser replace pour éviter d'ajouter une entrée dans l'historique
      router.replace(redirectUrl)
    } catch (err: any) {
      // Extraire le message d'erreur de manière plus détaillée
      let errorMessage = 'Erreur de connexion'
      
      if (err instanceof Error) {
        errorMessage = err.message || err.toString()
        
        // Vérifier si c'est un blocage admin (comportement attendu, pas une vraie erreur)
        if (errorMessage.includes('administrateurs doivent se connecter') || 
            errorMessage.includes('admin/login')) {
          // C'est normal, juste afficher le message sans log d'erreur alarmant
          setError(errorMessage)
          return
        }
        
        // Vérifier si c'est une erreur de connexion au serveur
        if (errorMessage.includes('connexion au serveur') || 
            errorMessage.includes('Failed to fetch') ||
            errorMessage.includes('NetworkError') ||
            errorMessage.includes('fetch')) {
          errorMessage = 'Erreur de connexion au serveur. Vérifiez que le backend est démarré sur http://localhost:8000'
        }
      } else if (typeof err === 'string') {
        errorMessage = err
      } else if (err?.message) {
        errorMessage = err.message
      } else if (err?.detail) {
        errorMessage = err.detail
      } else {
        errorMessage = String(err) || 'Erreur de connexion'
      }
      
      // Logger seulement les vraies erreurs
      if (!errorMessage.includes('administrateurs doivent se connecter')) {
        console.error('❌ Login error:', err)
      }
      
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-accent/5 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <Button variant="ghost" asChild className="mb-4">
          <Link href="/mobile">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour
          </Link>
        </Button>

        <Card className="border-2">
          <CardHeader className="text-center">
            <div className="flex items-center justify-center gap-2 mb-2">
              <div className="w-10 h-10 rounded-lg bg-accent flex items-center justify-center">
                <Heart className="w-6 h-6 text-accent-foreground" />
              </div>
              <CardTitle className="text-2xl">BreastCare</CardTitle>
            </div>
            <CardDescription>Connectez-vous à votre compte</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="votre@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Mot de passe</Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              
              {error && (
                <div className="text-sm text-red-600 bg-red-50 dark:bg-red-950/20 p-3 rounded-lg border border-red-200">
                  <p className="font-medium">❌ {error}</p>
                </div>
              )}
              
              <Button
                type="submit"
                className="w-full bg-accent hover:bg-accent/90 text-accent-foreground"
                size="lg"
                disabled={isLoading}
              >
                {isLoading ? "Connexion..." : "Se connecter"}
              </Button>
            </form>

            <div className="mt-6 text-center text-sm">
              <span className="text-muted-foreground">Pas encore de compte? </span>
              <Link href="/mobile/signup" className="text-accent hover:underline font-medium">
                Créer un compte
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
