"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Activity, ArrowLeft, CheckCircle, Loader2 } from "lucide-react"
import { apiClient } from "@/lib/api"

export default function RequestAccessPage() {
  const router = useRouter()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSuccess, setIsSuccess] = useState(false)
  const [error, setError] = useState("")

  // Fonction pour réinitialiser le formulaire
  const resetForm = () => {
    setIsSubmitting(false)
    setIsSuccess(false)
    setError("")
    setFormData({
      full_name: "",
      email: "",
      phone_number: "",
      specialty: "",
      license_number: "",
      hospital_clinic: "",
      experience_years: "",
      password: "",
      confirm_password: "",
      motivation: "",
      additional_info: ""
    })
  }

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    phone_number: "",
    specialty: "",
    license_number: "",
    hospital_clinic: "",
    experience_years: "",
    password: "",
    confirm_password: "",
    motivation: "",
    additional_info: ""
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    console.log(`Changement de champ: ${name} = ${value}`)
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSelectChange = (value: string) => {
    setFormData(prev => ({ ...prev, specialty: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError("")

    // Validation du mot de passe
    if (formData.password !== formData.confirm_password) {
      setError("Les mots de passe ne correspondent pas")
      setIsSubmitting(false)
      return
    }

    if (formData.password.length < 6) {
      setError("Le mot de passe doit contenir au moins 6 caractères")
      setIsSubmitting(false)
      return
    }

    try {
      // Envoyer la demande d'accès à l'admin
      await apiClient.createAccessRequest(formData)
      
      setIsSuccess(true)
      // Rediriger vers la page de connexion après 3 secondes
      setTimeout(() => {
        router.push("/professional/login")
      }, 3000)
    } catch (err: any) {
      setError(err.message || "Erreur lors de l'envoi de la demande")
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isSuccess) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          <Card className="border-2">
            <CardContent className="pt-6">
              <div className="text-center">
                <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-green-600 mb-2">Demande envoyée !</h2>
                <p className="text-muted-foreground mb-4">
                  Votre demande d'accès a été transmise à l'administrateur. 
                  Vous recevrez un email de confirmation une fois votre demande traitée.
                </p>
                <p className="text-sm text-muted-foreground mb-4">
                  Redirection automatique vers la page de connexion...
                </p>
                <Button 
                  variant="outline" 
                  onClick={resetForm}
                  className="w-full"
                >
                  Faire une nouvelle demande
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        {/* Back Button */}
        <Button variant="ghost" asChild className="mb-4">
          <Link href="/professional/login">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour à la connexion
          </Link>
        </Button>

        {/* Request Access Card */}
        <Card className="border-2">
          <CardHeader className="text-center">
            <div className="flex items-center justify-center gap-2 mb-2">
              <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
                <Activity className="w-6 h-6 text-primary-foreground" />
              </div>
              <CardTitle className="text-2xl">Demande d'accès professionnel</CardTitle>
            </div>
            <CardDescription>
              Remplissez ce formulaire pour demander l'accès à la plateforme BreastCare Pro
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {/* Informations personnelles */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Informations personnelles</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="full_name">Nom complet *</Label>
                    <Input
                      id="full_name"
                      name="full_name"
                      value={formData.full_name}
                      onChange={handleInputChange}
                      placeholder="Dr. Jean Dupont"
                      required
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="email">Email professionnel *</Label>
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      placeholder="radiologue@centre-cancer.bj"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="phone_number">Numéro de téléphone</Label>
                    <Input
                      id="phone_number"
                      name="phone_number"
                      value={formData.phone_number}
                      onChange={handleInputChange}
                      placeholder="+229 97 12 34 56"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="license_number">Numéro de licence médicale *</Label>
                    <Input
                      id="license_number"
                      name="license_number"
                      value={formData.license_number}
                      onChange={handleInputChange}
                      placeholder="MED123456"
                      required
                    />
                  </div>
                </div>
              </div>

              {/* Informations professionnelles */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Informations professionnelles</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="specialty">Spécialité médicale *</Label>
                    <Select value={formData.specialty} onValueChange={handleSelectChange}>
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionnez votre spécialité" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="breast_radiology">Radiologie mammaire</SelectItem>
                        <SelectItem value="breast_oncology">Oncologie mammaire</SelectItem>
                        <SelectItem value="breast_surgery">Chirurgie mammaire</SelectItem>
                        <SelectItem value="breast_pathology">Anatomopathologie mammaire</SelectItem>
                        <SelectItem value="gynecology">Gynécologie</SelectItem>
                        <SelectItem value="medical_oncology">Oncologie médicale</SelectItem>
                        <SelectItem value="radiation_oncology">Radiothérapie</SelectItem>
                        <SelectItem value="nuclear_medicine">Médecine nucléaire</SelectItem>
                        <SelectItem value="general_radiology">Radiologie générale</SelectItem>
                        <SelectItem value="general_medicine">Médecine générale</SelectItem>
                        <SelectItem value="other">Autre spécialité</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="hospital_clinic">Hôpital/Clinique *</Label>
                    <Input
                      id="hospital_clinic"
                      name="hospital_clinic"
                      value={formData.hospital_clinic}
                      onChange={handleInputChange}
                      placeholder="Centre de lutte contre le cancer"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="experience_years">Années d'expérience *</Label>
                  <Select value={formData.experience_years} onValueChange={(value) => setFormData(prev => ({ ...prev, experience_years: value }))}>
                    <SelectTrigger>
                      <SelectValue placeholder="Sélectionnez votre expérience" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="0-2">0-2 ans</SelectItem>
                      <SelectItem value="3-5">3-5 ans</SelectItem>
                      <SelectItem value="6-10">6-10 ans</SelectItem>
                      <SelectItem value="11-15">11-15 ans</SelectItem>
                      <SelectItem value="16+">16+ ans</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Mot de passe */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Sécurité</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="password">Mot de passe *</Label>
                    <Input
                      id="password"
                      name="password"
                      type="password"
                      value={formData.password}
                      onChange={handleInputChange}
                      placeholder="Minimum 6 caractères"
                      required
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="confirm_password">Confirmer le mot de passe *</Label>
                    <Input
                      id="confirm_password"
                      name="confirm_password"
                      type="password"
                      value={formData.confirm_password}
                      onChange={handleInputChange}
                      placeholder="Répétez votre mot de passe"
                      required
                    />
                  </div>
                </div>
              </div>

              {/* Motivation */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Motivation</h3>
                
                <div className="space-y-2">
                  <Label htmlFor="motivation">Pourquoi souhaitez-vous accéder à cette plateforme ? *</Label>
                  <Textarea
                    id="motivation"
                    name="motivation"
                    value={formData.motivation}
                    onChange={handleInputChange}
                    placeholder="Décrivez votre motivation pour rejoindre la plateforme de dépistage du cancer du sein..."
                    className="min-h-[100px]"
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="additional_info">Informations complémentaires</Label>
                  <Textarea
                    id="additional_info"
                    name="additional_info"
                    value={formData.additional_info}
                    onChange={handleInputChange}
                    placeholder="Toute information supplémentaire que vous souhaitez partager..."
                    className="min-h-[80px]"
                  />
                </div>
              </div>

              <Button type="submit" className="w-full" size="lg" disabled={isSubmitting}>
                {isSubmitting ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Envoi en cours...
                  </>
                ) : (
                  "Envoyer la demande d'accès"
                )}
              </Button>
            </form>
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
