"use client"

import type React from "react"
import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Heart, ArrowLeft, Mail } from "lucide-react"

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [error, setError] = useState("")
  const [resetToken, setResetToken] = useState("")
  const [resetLink, setResetLink] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setIsLoading(true)

    try {
      const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
      const response = await fetch(`${API_BASE}/api/v1/auth/forgot-password`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || "Une erreur est survenue")
      }

      const data = await response.json()
      
      // Si le token est retourné (pas de service email configuré), l'afficher
      if (data.token) {
        setResetToken(data.token)
        setResetLink(data.reset_link || "")
      }
      
      setIsSubmitted(true)
    } catch (err: any) {
      console.error("Erreur:", err)
      setError(err.message || "Une erreur est survenue lors de l'envoi de l'email")
    } finally {
      setIsLoading(false)
    }
  }

  if (isSubmitted) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background to-accent/5 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          <Button variant="ghost" asChild className="mb-4">
            <Link href="/mobile/login">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Retour
            </Link>
          </Button>

          <Card className="border-2">
            <CardHeader className="text-center">
              <div className="flex items-center justify-center gap-2 mb-4">
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                  <Mail className="w-6 h-6 text-primary" />
                </div>
              </div>
              <CardTitle className="text-2xl">
                {resetToken ? "Lien de réinitialisation généré" : "Email envoyé"}
              </CardTitle>
              <CardDescription className="mt-4">
                {resetToken ? (
                  <>
                    Un lien de réinitialisation a été généré. {resetLink && "Cliquez sur le lien ci-dessous ou copiez le token."}
                  </>
                ) : (
                  <>
                    Si un compte existe avec l'adresse {email}, vous recevrez un email avec les instructions pour réinitialiser votre mot de passe.
                  </>
                )}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {resetToken && (
                <div className="space-y-3 p-4 bg-muted rounded-lg">
                  <div>
                    <Label className="text-sm font-semibold">Lien de réinitialisation :</Label>
                    {resetLink ? (
                      <Button asChild variant="outline" className="w-full mt-2">
                        <Link href={resetLink} target="_blank">
                          Cliquer pour réinitialiser
                        </Link>
                      </Button>
                    ) : null}
                  </div>
                  <div>
                    <Label className="text-sm font-semibold">Ou copiez le token :</Label>
                    <div className="mt-2 p-2 bg-background border rounded text-xs break-all font-mono">
                      {resetToken}
                    </div>
                    <p className="text-xs text-muted-foreground mt-2">
                      Utilisez ce token sur la page de réinitialisation.
                    </p>
                  </div>
                  <div className="p-2 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded text-xs text-yellow-800 dark:text-yellow-200">
                    ⚠️ Sans service email configuré, ce token est visible. Pour plus de sécurité, configurez un service d'envoi d'email.
                  </div>
                </div>
              )}
              <Button asChild className="w-full">
                <Link href={resetLink || "/mobile/login"}>
                  {resetLink ? "Réinitialiser le mot de passe" : "Retour à la connexion"}
                </Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-accent/5 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <Button variant="ghost" asChild className="mb-4">
          <Link href="/mobile/login">
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
            <CardDescription>Réinitialiser votre mot de passe</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
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
                <p className="text-xs text-muted-foreground">
                  Entrez votre adresse email et nous vous enverrons un lien pour réinitialiser votre mot de passe.
                </p>
              </div>
              
              {error && (
                <div className="text-sm text-red-500 bg-red-50 dark:bg-red-950/20 p-3 rounded-lg">
                  {error}
                </div>
              )}
              
              <Button
                type="submit"
                className="w-full bg-accent hover:bg-accent/90 text-accent-foreground"
                size="lg"
                disabled={isLoading}
              >
                {isLoading ? "Envoi en cours..." : "Envoyer le lien de réinitialisation"}
              </Button>
            </form>

            <div className="mt-6 text-center text-sm">
              <span className="text-muted-foreground">Vous vous souvenez de votre mot de passe? </span>
              <Link href="/mobile/login" className="text-accent hover:underline font-medium">
                Se connecter
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

