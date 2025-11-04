"use client"
import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Heart, Calendar, FileText, MapPin, User, LogOut, Bell } from "lucide-react"
import { useAuth } from "@/contexts/auth-context"
import { apiClient } from "@/lib/api"

export default function MobileDashboardPage() {
  const { user, isAuthenticated, loading, checkAuth, logout } = useAuth()
  const router = useRouter()
  const [recentAssessments, setRecentAssessments] = useState<Array<{ id: string; date: string; score?: number; riskLevel?: string }>>([])
  const [assessmentsLoading, setAssessmentsLoading] = useState(true)
  const [upcomingAppointments, setUpcomingAppointments] = useState<Array<{ id: string; provider: string; date: string; time: string; type: string }>>([])
  const [appointmentsLoading, setAppointmentsLoading] = useState(true)

  // Vérifier l'authentification et bloquer les admins
  useEffect(() => {
    const verifyAccess = async () => {
      // Attendre que le contexte soit chargé
      if (loading) return
      
      // Vérifier si un token existe
      const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
      if (!token) {
        router.replace('/mobile/login?redirect=/mobile/dashboard')
        return
      }
      
      // Si l'utilisateur n'est pas encore chargé, forcer la vérification
      if (!isAuthenticated && !user) {
        await checkAuth()
        return
      }
      
      // Bloquer les admins et les professionnels
      if (user && user.user_type === 'admin') {
        console.log('🚫 Admin détecté sur dashboard mobile - Redirection vers admin')
        localStorage.removeItem('auth_token')
        window.location.href = '/admin/login'
        return
      }
      
      // Bloquer les professionnels de santé (ils doivent utiliser /professional/login)
      if (user && user.user_type === 'professional') {
        console.log('🚫 Professionnel détecté sur dashboard mobile - Redirection vers plateforme professionnelle')
        localStorage.removeItem('auth_token')
        window.location.href = '/professional/login'
        return
      }
      
      // Afficher les informations utilisateur dans la console pour debug
      if (user) {
        console.log('👤 Utilisateur actuel dans dashboard:', {
          email: user.email,
          name: user.full_name,
          id: user.id,
          type: user.user_type
        })
        
        // Charger les évaluations de risque et les rendez-vous
        loadAssessments()
        loadAppointments()
      }
    }
    
    verifyAccess()
  }, [user, isAuthenticated, loading, router, checkAuth])

  const loadAssessments = async () => {
    try {
      setAssessmentsLoading(true)
      const response: any = await apiClient.getMyRiskAssessments(0, 10)
      const assessments = response.assessments || []
      
      // Formater les données pour l'affichage
      const formattedAssessments = assessments.map((assessment: any) => ({
        id: assessment.id,
        date: new Date(assessment.date).toLocaleDateString('fr-FR', { 
          day: 'numeric', 
          month: 'long', 
          year: 'numeric' 
        }),
        score: Math.round(assessment.risk_5_years * 10) / 10,
        riskLevel: assessment.risk_level || assessment.risk_category
      }))
      
      setRecentAssessments(formattedAssessments)
      console.log('✅ Évaluations chargées:', formattedAssessments)
    } catch (err) {
      console.error('❌ Erreur lors du chargement des évaluations:', err)
    } finally {
      setAssessmentsLoading(false)
    }
  }

  const loadAppointments = async () => {
    if (!user) {
      setAppointmentsLoading(false)
      return
    }

    try {
      setAppointmentsLoading(true)
      // Récupérer tous les rendez-vous (on filtrera côté client par user_id et date)
      const response = await apiClient.getAppointments({
        limit: 100 // Récupérer assez pour filtrer
      })
      
      const appointments = response.appointments || []
      console.log('📅 Tous les rendez-vous reçus:', appointments.length)
      console.log('👤 User ID actuel:', user.id)
      
      // Récupérer les noms des centres en parallèle si nécessaire
      const centerIds = [...new Set(appointments.map((apt: any) => apt.center_id).filter(Boolean))]
      const centerNames: Record<string, string> = {}
      
      // Essayer de récupérer les noms des centres
      if (centerIds.length > 0) {
        try {
          const centersResponse = await apiClient.getHealthcareCenters({ limit: 100 })
          centersResponse.centers.forEach((center: any) => {
            if (center.id) {
              centerNames[center.id] = center.name
            }
          })
        } catch (err) {
          console.warn('⚠️ Impossible de récupérer les noms des centres:', err)
        }
      }
      
      // Formater les données pour l'affichage
      const now = new Date()
      now.setHours(0, 0, 0, 0) // Ignorer l'heure pour comparer seulement les dates
      
      const formattedAppointments = appointments
        .filter((apt: any) => {
          // Filtrer par user_id (email match si pas de user_id)
          const matchesUser = apt.user_id === user.id || 
                            apt.patient_email === user.email ||
                            !apt.user_id // Inclure les rendez-vous sans user_id pour compatibilité
          
          // Filtrer seulement les rendez-vous futurs et non annulés
          if (!matchesUser || apt.status === 'cancelled') return false
          
          if (!apt.appointment_date) return false
          const appointmentDate = new Date(apt.appointment_date)
          appointmentDate.setHours(0, 0, 0, 0)
          
          return appointmentDate >= now
        })
        .sort((a: any, b: any) => {
          // Trier par date croissante
          return new Date(a.appointment_date).getTime() - new Date(b.appointment_date).getTime()
        })
        .slice(0, 5) // Limiter à 5 prochains rendez-vous
        .map((apt: any) => {
          const appointmentDate = new Date(apt.appointment_date)
          return {
            id: apt.id || apt.appointment_id,
            provider: centerNames[apt.center_id] || apt.center_name || apt.healthcare_center_name || apt.provider_name || 'Centre de dépistage',
            date: appointmentDate.toLocaleDateString('fr-FR', { 
              day: 'numeric', 
              month: 'long', 
              year: 'numeric' 
            }),
            time: apt.appointment_time || appointmentDate.toLocaleTimeString('fr-FR', { 
              hour: '2-digit', 
              minute: '2-digit' 
            }),
            type: apt.service_type || apt.appointment_type || 'Consultation'
          }
        })
      
      setUpcomingAppointments(formattedAppointments)
      console.log('✅ Rendez-vous chargés:', formattedAppointments.length, formattedAppointments)
    } catch (err: any) {
      console.error('❌ Erreur lors du chargement des rendez-vous:', err)
      // Si l'endpoint n'existe pas ou retourne une erreur, on laisse le tableau vide
      setUpcomingAppointments([])
    } finally {
      setAppointmentsLoading(false)
    }
  }

  // Afficher un loading pendant la vérification
  if (loading || (!user && isAuthenticated)) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Chargement...</p>
      </div>
    )
  }

  // Si pas authentifié, ne rien afficher (redirection en cours)
  if (!isAuthenticated || !user) {
    return null
  }
  

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-accent/5">
      <header className="border-b bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center">
              <Heart className="w-5 h-5 text-accent-foreground" />
            </div>
            <span className="font-semibold">Mon espace</span>
          </div>
          <Button variant="ghost" size="sm">
            <Bell className="w-5 h-5" />
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* User Info */}
        <Card className="mb-6">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-full bg-accent/10 flex items-center justify-center">
                <User className="w-8 h-8 text-accent" />
              </div>
              <div className="flex-1">
                <h2 className="text-xl font-bold mb-1">{user?.full_name || user?.email || 'Utilisateur'}</h2>
                <p className="text-sm text-muted-foreground">{user?.email || ''}</p>
              </div>
              {!!user && (
                <Badge variant="outline" className="bg-accent/10">
                  Profil
                </Badge>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Upcoming Appointments */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Rendez-vous à venir</CardTitle>
            <CardDescription>Vos prochaines consultations</CardDescription>
          </CardHeader>
          <CardContent>
            {appointmentsLoading ? (
              <p className="text-sm text-muted-foreground text-center py-4">Chargement...</p>
            ) : upcomingAppointments.length > 0 ? (
              <div className="space-y-3">
                {upcomingAppointments.map((apt) => (
                  <div key={apt.id} className="p-4 rounded-lg border bg-card">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <p className="font-medium">{apt.provider}</p>
                        <p className="text-sm text-muted-foreground">{apt.type}</p>
                      </div>
                      <Badge className="bg-primary text-primary-foreground">Confirmé</Badge>
                    </div>
                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <div className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        <span>{apt.date}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <span>{apt.time}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground text-center py-4">Aucun rendez-vous prévu</p>
            )}
          </CardContent>
        </Card>

        {/* Recent Assessments */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Évaluations récentes</CardTitle>
            <CardDescription>Historique de vos évaluations de risque</CardDescription>
          </CardHeader>
          <CardContent>
            {assessmentsLoading ? (
              <p className="text-sm text-muted-foreground text-center py-4">Chargement...</p>
            ) : recentAssessments.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-4">Aucune évaluation disponible</p>
            ) : (
              recentAssessments.map((assessment) => (
                <div key={assessment.id} className="p-4 rounded-lg border bg-card">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium mb-1">Évaluation du {assessment.date}</p>
                      {assessment.score !== undefined && (
                        <p className="text-sm text-muted-foreground">Score: {assessment.score}%</p>
                      )}
                    </div>
                    {assessment.riskLevel && (
                      <Badge variant="outline" className="bg-accent/10">
                        Risque {assessment.riskLevel}
                      </Badge>
                    )}
                  </div>
                </div>
              ))
            )}
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <div className="grid gap-4 sm:grid-cols-2 mb-6">
          <Card className="hover:bg-accent/5 transition-colors">
            <CardContent className="pt-6">
              <Link href="/mobile/assessment" className="flex flex-col items-center text-center gap-3">
                <div className="w-12 h-12 rounded-full bg-accent/10 flex items-center justify-center">
                  <FileText className="w-6 h-6 text-accent" />
                </div>
                <div>
                  <p className="font-medium">Nouvelle évaluation</p>
                  <p className="text-xs text-muted-foreground">Évaluez votre risque</p>
                </div>
              </Link>
            </CardContent>
          </Card>

          <Card className="hover:bg-accent/5 transition-colors">
            <CardContent className="pt-6">
              <Link href="/mobile/providers" className="flex flex-col items-center text-center gap-3">
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                  <MapPin className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <p className="font-medium">Trouver un centre</p>
                  <p className="text-xs text-muted-foreground">Centres de dépistage</p>
                </div>
              </Link>
            </CardContent>
          </Card>
        </div>

        {/* Logout */}
        <Button 
          variant="outline" 
          className="w-full bg-transparent" 
          onClick={async () => {
            await logout()
            router.push('/mobile/login')
          }}
        >
          <LogOut className="mr-2 h-4 w-4" />
          Se déconnecter
        </Button>
      </main>
    </div>
  )
}
