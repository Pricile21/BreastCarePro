"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { CheckCircle, Calendar, MapPin, Clock, Phone, Download, Home, Loader2 } from "lucide-react"

interface BookingData {
  id: string
  confirmation_code?: string
  center_name: string
  center_address: string
  patient_name: string
  appointment_date: string
  appointment_time: string
}

export default function BookingConfirmationPage() {
  const router = useRouter()
  const [booking, setBooking] = useState<BookingData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Retrieve booking data from sessionStorage
    if (typeof window !== 'undefined') {
      const bookingData = sessionStorage.getItem('lastAppointment')
      if (bookingData) {
        try {
          setBooking(JSON.parse(bookingData))
        } catch (error) {
          console.error('Error parsing booking data:', error)
        }
      }
      setLoading(false)
    }
  }, [])

  // Format date
  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString)
      const options: Intl.DateTimeFormatOptions = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      }
      return date.toLocaleDateString('fr-FR', options)
    } catch {
      return dateString
    }
  }

  // Download confirmation as text file
  const handleDownload = () => {
    if (!booking) return
    
    const confirmationText = `
CONFIRMATION DE RÉSERVATION
===========================

Référence: ${booking.confirmation_code || booking.id}
Patient: ${booking.patient_name}

CENTRE DE SANTÉ
---------------
${booking.center_name}
${booking.center_address}

RENDEZ-VOUS
-----------
Date: ${formatDate(booking.appointment_date)}
Heure: ${booking.appointment_time}

INFORMATIONS IMPORTANTES
------------------------
• Arrivez 15 minutes avant l'heure du rendez-vous
• Apportez votre carte d'identité et votre carte d'assurance
• Un SMS de rappel vous sera envoyé 24h avant
• Pour annuler ou modifier, contactez le centre directement

---
Date d'émission: ${new Date().toLocaleDateString('fr-FR')}
    `.trim()

    // Create a blob and download it
    const blob = new Blob([confirmationText], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `confirmation-${booking.confirmation_code || booking.id}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background to-accent/5 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    )
  }

  if (!booking) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background to-accent/5">
        <main className="container mx-auto px-4 py-8 max-w-2xl">
          <Card>
            <CardContent className="pt-6 text-center">
              <p className="text-muted-foreground mb-4">Aucune réservation trouvée</p>
              <Button asChild>
                <Link href="/mobile">Retour à l'accueil</Link>
              </Button>
            </CardContent>
          </Card>
        </main>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-accent/5">
      <main className="container mx-auto px-4 py-8 max-w-2xl">
        {/* Success Message */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
            <CheckCircle className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-3xl font-bold mb-2">Réservation confirmée!</h1>
          <p className="text-muted-foreground">Votre rendez-vous a été enregistré avec succès</p>
        </div>

        {/* Booking Details */}
        <Card className="mb-6 border-2 border-primary/20">
          <CardHeader>
            <CardTitle>Détails du rendez-vous</CardTitle>
            <CardDescription>
              Référence: {booking.confirmation_code || booking.id}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-start gap-3 p-3 rounded-lg bg-muted">
              <MapPin className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-medium">{booking.center_name}</p>
                <p className="text-sm text-muted-foreground">{booking.center_address}</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 rounded-lg bg-muted">
              <Calendar className="w-5 h-5 text-primary flex-shrink-0" />
              <div>
                <p className="font-medium">{formatDate(booking.appointment_date)}</p>
                <p className="text-sm text-muted-foreground">Date du rendez-vous</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 rounded-lg bg-muted">
              <Clock className="w-5 h-5 text-primary flex-shrink-0" />
              <div>
                <p className="font-medium">{booking.appointment_time}</p>
                <p className="text-sm text-muted-foreground">Heure du rendez-vous</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Important Info */}
        <Card className="mb-6 bg-accent/5 border-accent/20">
          <CardHeader>
            <CardTitle className="text-base">Informations importantes</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm text-muted-foreground">
            <p>• Arrivez 15 minutes avant l'heure du rendez-vous</p>
            <p>• Apportez votre carte d'identité et votre carte d'assurance</p>
            <p>• Un SMS de rappel vous sera envoyé 24h avant</p>
            <p>• Pour annuler ou modifier, contactez le centre directement</p>
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="space-y-3">
          <Button variant="outline" className="w-full bg-transparent" onClick={handleDownload}>
            <Download className="mr-2 h-4 w-4" />
            Télécharger la confirmation
          </Button>
          <Button asChild className="w-full bg-accent hover:bg-accent/90 text-accent-foreground">
            <Link href="/mobile">
              <Home className="mr-2 h-4 w-4" />
              Retour à l'accueil
            </Link>
          </Button>
        </div>
      </main>
    </div>
  )
}
