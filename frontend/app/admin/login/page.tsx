"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Eye, EyeOff, Loader2 } from "lucide-react"
import { useAuth } from "@/contexts/auth-context"

export default function AdminLoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState("")
  
  const { login, loading, isAuthenticated, user } = useAuth()
  const router = useRouter()

  // Debug: Afficher l'état d'authentification
  useEffect(() => {
    console.log("Login Page - isAuthenticated:", isAuthenticated, "user:", user)
  }, [isAuthenticated, user])

  // Pas de redirection automatique - laisser l'utilisateur gérer sa connexion
  // La redirection se fera uniquement après une connexion réussie dans handleSubmit

  // S'assurer que les champs sont vides au chargement de la page
  useEffect(() => {
    setEmail("")
    setPassword("")
  }, [])

  // Show loading while checking authentication
  if (loading && !isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary/5 via-accent/5 to-primary/10 flex items-center justify-center p-4">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Vérification de l'authentification...</p>
        </div>
      </div>
    )
  }

  // Si l'utilisateur est déjà connecté, afficher un message au lieu de rediriger
  if (isAuthenticated && user && !loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary/5 via-accent/5 to-primary/10 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          <Card className="shadow-2xl border-0">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-green-600">✅ Déjà connecté</CardTitle>
              <CardDescription>
                Vous êtes déjà authentifié en tant que <strong>{user.email}</strong>
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              <p className="text-muted-foreground">
                Vous pouvez accéder directement au tableau de bord ou vous déconnecter pour vous reconnecter.
              </p>
              <div className="flex gap-3 justify-center">
                <Button onClick={() => router.push("/admin/dashboard")} className="flex-1">
                  Aller au Dashboard
                </Button>
                <Button 
                  variant="outline" 
                  onClick={() => {
                    // Déconnexion et rechargement de la page
                    localStorage.removeItem('auth_token')
                    window.location.reload()
                  }}
                  className="flex-1"
                >
                  Se déconnecter
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    if (!email || !password) {
      setError("Veuillez remplir tous les champs")
      return
    }

    try {
      console.log("Tentative de connexion...")
      await login(email, password)
      console.log("Connexion réussie, redirection vers dashboard...")
      
      // Utiliser router.push au lieu de window.location.href pour une navigation plus fluide
      router.push("/admin/dashboard")
    } catch (err) {
      console.error("Erreur de connexion:", err)
      setError(err instanceof Error ? err.message : "Erreur de connexion")
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 via-accent/5 to-primary/10 flex items-center justify-center p-4">
      <div className="w-full max-w-md">

        {/* Login Form */}
        <Card className="shadow-2xl border-0">
          <CardHeader className="space-y-1 pb-6">
            <CardTitle className="text-2xl text-center">Se connecter</CardTitle>
            <CardDescription className="text-center">
              Accès réservé aux administrateurs de la plateforme de dépistage
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4" autoComplete="off">
              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <div className="space-y-2">
                <Label htmlFor="email">Email professionnel</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="Entrez votre email professionnel"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={loading}
                  className="h-12"
                  autoComplete="off"
                  autoCorrect="off"
                  autoCapitalize="off"
                  spellCheck="false"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Mot de passe</Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    disabled={loading}
                    className="h-12 pr-10"
                    autoComplete="new-password"
                    autoCorrect="off"
                    autoCapitalize="off"
                    spellCheck="false"
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="absolute right-0 top-0 h-12 px-3 py-2 hover:bg-transparent"
                    onClick={() => setShowPassword(!showPassword)}
                    disabled={loading}
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4 text-muted-foreground" />
                    ) : (
                      <Eye className="h-4 w-4 text-muted-foreground" />
                    )}
                  </Button>
                </div>
              </div>

              <Button
                type="submit"
                className="w-full h-12 text-lg font-semibold"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Connexion en cours...
                  </>
                ) : (
                  "Se connecter"
                )}
              </Button>

            </form>

          </CardContent>
        </Card>

      </div>
    </div>
  )
}