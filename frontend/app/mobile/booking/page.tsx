"use client"

// Force dynamic rendering to prevent build-time prerendering errors
export const dynamic = 'force-dynamic'
export const revalidate = 0
export const dynamicParams = true

import type React from "react"

import { useState, useEffect, Suspense } from "react"
import Link from "next/link"
import { useRouter, useSearchParams } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { CalendarIcon, ArrowLeft, MapPin, Loader2 } from "lucide-react"
import { apiClient, HealthcareCenter } from "@/lib/api"

// Internal component that uses useSearchParams (must be wrapped in Suspense)
function BookingPageContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const providerId = searchParams.get('provider')
  
  const [provider, setProvider] = useState<HealthcareCenter | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    email: "",
    date: "",
    time: "",
    notes: "",
  })
  
  // Check if user is authenticated
  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
    if (token) {
      setIsAuthenticated(true)
    } else {
      // Redirect to login if not authenticated
      router.push('/mobile/login?redirect=/mobile/booking' + (providerId ? `?provider=${providerId}` : ''))
    }
  }, [router, providerId])

  // Charger les données du centre de santé
  useEffect(() => {
    if (!isAuthenticated) return
    
    const loadProvider = async () => {
      if (!providerId) {
        setLoading(false)
        return
      }
      
      try {
        setLoading(true)
        setError(null)
        const data = await apiClient.getHealthcareCenter(providerId)
        setProvider(data)
      } catch (err: any) {
        console.error('Erreur lors du chargement du centre:', err)
        setError(err.message || 'Erreur lors du chargement du centre de santé')
      } finally {
        setLoading(false)
      }
    }
    
    loadProvider()
  }, [providerId, isAuthenticated])

  // Generate available dates for the next 30 days (excluding weekends for now)
  const generateAvailableDates = () => {
    const dates: string[] = []
    const today = new Date()
    let daysAhead = 0
    
    while (dates.length < 10) {
      const date = new Date(today)
      date.setDate(today.getDate() + daysAhead)
      
      const dayOfWeek = date.getDay()
      // Exclude Saturday (6) and Sunday (0)
      if (dayOfWeek !== 0 && dayOfWeek !== 6) {
        dates.push(date.toISOString().split('T')[0])
      }
      daysAhead++
    }
    
    return dates
  }

  const availableDates = generateAvailableDates()
  const availableTimes = ["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!provider) {
      setError('Centre de santé non disponible')
      return
    }
    
    setIsSubmitting(true)
    setError(null)

    try {
      // Call the API to create the appointment
      const appointment = await apiClient.createAppointment({
        center_id: provider.id,
        patient_name: formData.name,
        patient_phone: formData.phone,
        patient_email: formData.email || undefined,
        appointment_date: formData.date,
        appointment_time: formData.time,
        notes: formData.notes || undefined
      })
      
      // Store appointment details in sessionStorage for confirmation page
      if (typeof window !== 'undefined') {
        sessionStorage.setItem('lastAppointment', JSON.stringify({
          id: appointment.id,
          confirmation_code: appointment.confirmation_code,
          center_name: provider.name,
          center_address: `${provider.address}, ${provider.city}`,
          patient_name: appointment.patient_name,
          appointment_date: appointment.appointment_date,
          appointment_time: appointment.appointment_time
        }))
      }
      
      router.push("/mobile/booking/confirmation")
    } catch (err: any) {
      console.error('Erreur lors de la réservation:', err)
      setError(err.message || 'Erreur lors de la réservation')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-accent/5">
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/mobile/providers">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Retour
            </Link>
          </Button>
          <div className="flex items-center gap-2">
            <CalendarIcon className="w-5 h-5 text-accent" />
            <span className="font-semibold">Réservation</span>
          </div>
          <div className="w-20" />
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-2xl">
        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-primary" />
          </div>
        )}
        
        {/* Error State */}
        {error && !loading && (
          <Card className="mb-6">
            <CardContent className="pt-6">
              <p className="text-destructive text-center">{error}</p>
            </CardContent>
          </Card>
        )}
        
        {/* No Provider Selected State */}
        {!provider && !loading && !error && (
          <Card className="mb-6 border-2 border-orange-200 bg-orange-50/50">
            <CardContent className="pt-6 text-center">
              <div className="space-y-4">
                <div className="w-16 h-16 rounded-full bg-orange-100 flex items-center justify-center mx-auto">
                  <MapPin className="w-8 h-8 text-orange-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-2">Aucun centre sélectionné</h3>
                  <p className="text-muted-foreground mb-4">
                    Veuillez sélectionner un centre de santé dans la liste pour réserver un rendez-vous.
                  </p>
                </div>
                <Button asChild className="bg-accent hover:bg-accent/90 text-accent-foreground">
                  <Link href="/mobile/providers">
                    Voir les centres disponibles
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
        
        {/* Provider Info */}
        {provider && !loading && (
          <Card className="mb-6 border-2 border-accent/20">
            <CardContent className="pt-6">
              <div className="flex items-start gap-3">
                <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center flex-shrink-0">
                  <MapPin className="w-6 h-6 text-accent" />
                </div>
                <div>
                  <p className="font-medium mb-1">{provider.name}</p>
                  <p className="text-sm text-muted-foreground">{provider.address}, {provider.city}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Booking Form */}
        {provider && !loading && (
          <form onSubmit={handleSubmit} className="space-y-6">
          {/* Error Message */}
          {error && (
            <Card className="border-red-200 bg-red-50/50">
              <CardContent className="pt-6">
                <p className="text-sm text-red-900">{error}</p>
              </CardContent>
            </Card>
          )}
          
          {/* Personal Info */}
          <Card>
            <CardHeader>
              <CardTitle>Vos informations</CardTitle>
              <CardDescription>Renseignez vos coordonnées pour la réservation</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Nom complet *</Label>
                <Input
                  id="name"
                  placeholder="Votre nom"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="phone">Téléphone *</Label>
                <Input
                  id="phone"
                  type="tel"
                  placeholder="+229 XX XX XX XX"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="votre@email.com"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                />
              </div>
            </CardContent>
          </Card>

          {/* Date & Time Selection */}
          <Card>
            <CardHeader>
              <CardTitle>Date et heure</CardTitle>
              <CardDescription>Choisissez votre créneau de rendez-vous</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="date">Date *</Label>
                <select
                  id="date"
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  value={formData.date}
                  onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                  required
                >
                  <option value="">Sélectionnez une date</option>
                  {availableDates.map((date) => (
                    <option key={date} value={date}>
                      {new Date(date).toLocaleDateString("fr-FR", {
                        weekday: "long",
                        year: "numeric",
                        month: "long",
                        day: "numeric",
                      })}
                    </option>
                  ))}
                </select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="time">Heure *</Label>
                <div className="grid grid-cols-4 gap-2">
                  {availableTimes.map((time) => (
                    <button
                      key={time}
                      type="button"
                      onClick={() => setFormData({ ...formData, time })}
                      className={`p-2 text-sm rounded-md border transition-colors ${
                        formData.time === time
                          ? "bg-accent text-accent-foreground border-accent"
                          : "bg-background hover:bg-accent/10"
                      }`}
                    >
                      {time}
                    </button>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Additional Notes */}
          <Card>
            <CardHeader>
              <CardTitle>Notes additionnelles</CardTitle>
              <CardDescription>Informations complémentaires (optionnel)</CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                placeholder="Précisez toute information utile pour votre rendez-vous..."
                rows={4}
                value={formData.notes}
                onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              />
            </CardContent>
          </Card>

          {/* Submit */}
          <Button
            type="submit"
            className="w-full bg-accent hover:bg-accent/90 text-accent-foreground"
            size="lg"
            disabled={isSubmitting || !formData.name || !formData.phone || !formData.date || !formData.time}
          >
            {isSubmitting ? "Confirmation en cours..." : "Confirmer la réservation"}
          </Button>
          </form>
        )}
      </main>
    </div>
  )
}

// Main component with Suspense wrapper for useSearchParams
export default function BookingPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-to-b from-background to-accent/5 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    }>
      <BookingPageContent />
    </Suspense>
  )
}
