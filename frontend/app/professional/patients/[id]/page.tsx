"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { ProfessionalSidebar } from "@/components/professional-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { AlertCircle, Loader2, FileText, User, Calendar, Phone, MapPin, ArrowLeft } from "lucide-react"
import Link from "next/link"
import { apiClient } from "@/lib/api"

export default function PatientDetailsPage() {
  const params = useParams()
  const router = useRouter()
  const patientId = params.id as string
  const [patient, setPatient] = useState<any>(null)
  const [reports, setReports] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchPatientData = async () => {
      try {
        setLoading(true)
        setError(null)

        // Récupérer directement les informations du patient depuis l'endpoint /api/v1/patients/{patient_id}
        const token = localStorage.getItem('auth_token')
        console.log('🔍 Fetching patient data for ID:', patientId)
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
        const patientResponse = await fetch(`${apiUrl}/patients/${patientId}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        console.log('📡 Patient response status:', patientResponse.status)
        if (patientResponse.ok) {
          const patientData = await patientResponse.json()
          console.log('✅ Patient data received:', patientData)
          console.log('📋 patient_id:', patientData.patient_id)
          console.log('📋 id:', patientData.id)
          console.log('📋 full_name:', patientData.full_name)
          
          // Vérifier que patient_id est bien présent
          if (!patientData.patient_id) {
            console.error('❌ ERREUR: patient_id est manquant dans la réponse du backend!')
            console.error('Réponse complète:', JSON.stringify(patientData, null, 2))
          } else {
            console.log('✅ patient_id trouvé:', patientData.patient_id)
          }
          
          setPatient(patientData)
        } else {
          const errorData = await patientResponse.json().catch(() => ({}))
          console.error('❌ Erreur récupération patient:', patientResponse.status, errorData)
          setError(`Erreur ${patientResponse.status}: ${errorData.detail || 'Patient non trouvé'}`)
        }

        // Récupérer les rapports du patient
        const reportsData = await apiClient.getProfessionalReports(0, 100, patientId)
        setReports(reportsData || [])

      } catch (err: any) {
        console.error('❌ Erreur:', err)
        setError('Erreur lors du chargement des données du patient')
      } finally {
        setLoading(false)
      }
    }

    if (patientId) {
      fetchPatientData()
    }
  }, [patientId])

  const getRiskBadge = (riskLevel: string) => {
    if (riskLevel === "high") {
      return <Badge variant="outline" className="bg-destructive/10 text-destructive">Risque élevé</Badge>
    } else if (riskLevel === "medium") {
      return <Badge variant="outline" className="bg-accent/10 text-accent">Risque modéré</Badge>
    } else {
      return <Badge variant="outline" className="bg-primary/10 text-primary">Risque faible</Badge>
    }
  }

  if (loading) {
    return (
      <div className="flex h-screen">
        <ProfessionalSidebar />
        <main className="flex-1 overflow-y-auto bg-background flex items-center justify-center">
          <div className="text-center">
            <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4" />
            <p>Chargement des informations...</p>
          </div>
        </main>
      </div>
    )
  }

  if (error || !patient) {
    return (
      <div className="flex h-screen">
        <ProfessionalSidebar />
        <main className="flex-1 overflow-y-auto bg-background flex items-center justify-center">
          <div className="text-center">
            <AlertCircle className="w-8 h-8 text-destructive mx-auto mb-4" />
            <p className="text-destructive">{error || 'Aucune information trouvée'}</p>
            <Button asChild className="mt-4">
              <Link href="/professional/patients">Retour aux patients</Link>
            </Button>
          </div>
        </main>
      </div>
    )
  }

  return (
    <div className="flex h-screen">
      <ProfessionalSidebar />
      <main className="flex-1 overflow-y-auto bg-background">
        <div className="container mx-auto p-8">
          <Button variant="ghost" className="mb-6" asChild>
            <Link href="/professional/patients">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Retour aux patients
            </Link>
          </Button>

          <div className="grid gap-6 lg:grid-cols-3">
            {/* Informations Patient */}
            <div className="lg:col-span-1">
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-4 mb-4">
                    <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
                      <User className="w-8 h-8 text-primary" />
                    </div>
                    <div className="flex-1">
                      <CardTitle className="text-xl">
                        {patient.full_name || `Patient ${patient.patient_id || 'N/A'}`}
                      </CardTitle>
                      <CardDescription>
                        ID: {(() => {
                          console.log('🔍 Rendering ID - patient.patient_id:', patient.patient_id);
                          console.log('🔍 Rendering ID - patient.id:', patient.id);
                          return patient.patient_id || 'N/A (patient_id manquant)';
                        })()}
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h3 className="font-semibold mb-3">Informations générales</h3>
                    <div className="space-y-2">
                      {patient.full_name && (
                        <div className="flex items-center gap-2 text-sm">
                          <User className="w-4 h-4 text-muted-foreground" />
                          <span>{patient.full_name}</span>
                        </div>
                      )}
                      {patient.age && (
                        <div className="flex items-center gap-2 text-sm">
                          <Calendar className="w-4 h-4 text-muted-foreground" />
                          <span>{patient.age} ans</span>
                        </div>
                      )}
                      {patient.phone_number && (
                        <div className="flex items-center gap-2 text-sm">
                          <Phone className="w-4 h-4 text-muted-foreground" />
                          <span>{patient.phone_number}</span>
                        </div>
                      )}
                      {patient.address && (
                        <div className="flex items-center gap-2 text-sm">
                          <MapPin className="w-4 h-4 text-muted-foreground" />
                          <span>{patient.address}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <h3 className="font-semibold mb-2">Évaluation du risque</h3>
                    {getRiskBadge(patient.riskLevel || "low")}
                  </div>

                  <div className="border-t pt-4">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Total d'analyses</span>
                      <span className="font-semibold">{reports.length}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Historique des rapports */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle>Historique des analyses</CardTitle>
                  <CardDescription>Liste de toutes les analyses mammographiques</CardDescription>
                </CardHeader>
                <CardContent>
                  {reports && reports.length > 0 ? (
                    <div className="space-y-3">
                      {reports.map((report) => (
                        <Link
                          key={report.id}
                          href={`/professional/analysis/${report.analysis_id || report.id}`}
                          className="block"
                        >
                          <div className="flex items-center gap-4 p-4 rounded-lg border hover:bg-accent/50 transition-colors">
                            <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                              <FileText className="w-5 h-5 text-primary" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-1">
                                <p className="font-medium">Analyse {report.analysis_id?.substring(0, 8) || report.id?.substring(0, 8)}</p>
                                <Badge variant="outline" className="text-xs">
                                  {report.bi_rads_category}
                                </Badge>
                              </div>
                              <p className="text-sm text-muted-foreground">
                                {new Date(report.created_at).toLocaleDateString("fr-FR")} • Confiance: {Math.round(report.confidence_score * 100)}%
                              </p>
                            </div>
                            <div className="flex items-center gap-2">
                              {report.status === "pending" ? (
                                <Badge variant="outline" className="bg-accent/10">
                                  En attente
                                </Badge>
                              ) : (
                                <Badge variant="outline" className="bg-primary/10">
                                  Complété
                                </Badge>
                              )}
                            </div>
                          </div>
                        </Link>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">
                      <FileText className="h-8 w-8 mx-auto mb-2 opacity-50" />
                      <p>Aucune analyse trouvée pour ce patient</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

