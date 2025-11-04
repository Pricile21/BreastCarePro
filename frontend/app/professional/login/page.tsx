"use client"

import type React from "react"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Activity, ArrowLeft } from "lucide-react"
import { apiClient } from "@/lib/api"

export default function ProfessionalLoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError("")

    try {
      // Utiliser apiClient pour l'authentification (envoie 'email' au lieu de 'username')
      const response = await apiClient.login(email, password, 'professional')
      
      // Le token est déjà stocké par apiClient.login, récupérer l'utilisateur
      const userData = await apiClient.getCurrentUser()
      
      // Empêcher l'admin de se connecter sur la page professionnelle
      if (userData.user_type === 'admin') {
        setError("❌ Cette page est réservée aux professionnels de santé. Les administrateurs doivent utiliser la page d'administration.")
        localStorage.removeItem('auth_token')
        return
      }
      
      // Vérifier que c'est un professionnel ou un patient
      if (userData.user_type !== 'professional' && userData.user_type !== 'patient') {
        setError("❌ Votre compte n'a pas les permissions nécessaires pour accéder à cette plateforme.")
        localStorage.removeItem('auth_token')
        return
      }
      
      // Redirection vers le dashboard professionnel
      router.push("/professional/dashboard")
    } catch (error: any) {
      console.error("Erreur de connexion:", error)
      
      // Extraire un message d'erreur approprié
      let errorMessage = "❌ Erreur de connexion"
      
      if (error?.message) {
        if (error.message.includes("Incorrect email or password")) {
          errorMessage = "❌ Identifiants incorrects. Vérifiez votre email et mot de passe."
        } else if (error.message.includes("accès") || error.message.includes("access")) {
          errorMessage = "❌ Identifiants incorrects. Assurez-vous que votre demande d'accès a été approuvée."
        } else {
          errorMessage = error.message
        }
      }
      
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Back Button */}
        <Button variant="ghost" asChild className="mb-4">
          <Link href="/">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour
          </Link>
        </Button>

        {/* Login Card */}
        <Card className="border-2">
          <CardHeader className="text-center">
            <div className="flex items-center justify-center gap-2 mb-2">
              <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
                <Activity className="w-6 h-6 text-primary-foreground" />
              </div>
              <CardTitle className="text-2xl">BreastCare Pro</CardTitle>
            </div>
            <CardDescription>Connexion à la plateforme professionnelle</CardDescription>
          </CardHeader>
          <CardContent>
            {error && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-start gap-2">
                  <div className="text-red-500 text-lg">⚠️</div>
                  <div>
                    <p className="text-red-700 font-medium text-sm">{error}</p>
                    <p className="text-red-600 text-xs mt-1">
                      Utilisez le lien "Demander un accès" ci-dessous pour vous inscrire.
                    </p>
                  </div>
                </div>
              </div>
            )}
            
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email professionnel</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="radiologue@hopital.bj"
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
              <Button type="submit" className="w-full" size="lg" disabled={isLoading}>
                {isLoading ? "Connexion..." : "Se connecter"}
              </Button>
            </form>

            <div className="mt-6 text-center text-sm">
              <span className="text-muted-foreground">Pas encore de compte? </span>
              <Link href="/professional/request-access" className="text-primary hover:underline font-medium">
                Demander un accès
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Security Notice */}
        <p className="mt-4 text-xs text-center text-muted-foreground">
          Plateforme sécurisée conforme aux normes médicales
        </p>
      </div>
    </div>
  )
}
