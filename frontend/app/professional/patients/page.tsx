"use client"

import { ProfessionalSidebar } from "@/components/professional-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Users, Search, Plus, Eye, AlertCircle } from "lucide-react"
import { useRealPatients } from "@/hooks/use-api"
import Link from "next/link"

export default function PatientsPage() {
  const { patients, loading, error, refetch } = useRealPatients()

  if (loading) {
    return (
      <div className="flex h-screen">
        <ProfessionalSidebar />
        <main className="flex-1 overflow-y-auto bg-background">
          <div className="container mx-auto p-8">
            <div className="mb-8 flex items-center justify-between">
              <div>
                <Skeleton className="h-8 w-64 mb-2" />
                <Skeleton className="h-4 w-96" />
              </div>
              <Skeleton className="h-10 w-32" />
            </div>
            <Card className="mb-6">
              <CardContent className="pt-6">
                <Skeleton className="h-10 w-full" />
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <Skeleton className="h-6 w-32 mb-2" />
                <Skeleton className="h-4 w-48" />
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {[...Array(5)].map((_, i) => (
                    <div key={i} className="flex items-center gap-4 p-4 rounded-lg border">
                      <Skeleton className="w-10 h-10 rounded-full" />
                      <div className="flex-1">
                        <Skeleton className="h-4 w-32 mb-2" />
                        <Skeleton className="h-3 w-64" />
                      </div>
                      <Skeleton className="w-8 h-8" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex h-screen">
        <ProfessionalSidebar />
        <main className="flex-1 overflow-y-auto bg-background">
          <div className="container mx-auto p-8">
            <Alert variant="destructive" className="mb-6">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                {error}
                <br />
                <Button 
                  onClick={refetch} 
                  className="mt-2"
                  size="sm"
                  variant="outline"
                >
                  Réessayer
                </Button>
              </AlertDescription>
            </Alert>
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
          <div className="mb-8 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">Gestion des patients</h1>
              <p className="text-muted-foreground">Base de données et historique des patients</p>
            </div>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Nouveau patient
            </Button>
          </div>

          {/* Search */}
          <Card className="mb-6">
            <CardContent className="pt-6">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input placeholder="Rechercher un patient par ID ou nom..." className="pl-9" />
              </div>
            </CardContent>
          </Card>

          {/* Patients List */}
          <Card>
            <CardHeader>
              <CardTitle>Tous les patients</CardTitle>
              <CardDescription>{patients.length} patients enregistrés</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {patients.map((patient) => (
                  <div
                    key={patient.id}
                    className="flex items-center gap-4 p-4 rounded-lg border hover:bg-accent/50 transition-colors"
                  >
                    <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <Users className="w-5 h-5 text-primary" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <p className="font-medium">{patient.name}</p>
                        <Badge
                          variant="outline"
                          className={
                            patient.risk === "high"
                              ? "bg-destructive/10 text-destructive"
                              : patient.risk === "medium"
                                ? "bg-accent/10 text-accent"
                                : "bg-primary/10 text-primary"
                          }
                        >
                          {patient.risk === "high"
                            ? "Risque élevé"
                            : patient.risk === "medium"
                              ? "Risque modéré"
                              : "Risque faible"}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {patient.id} • {patient.age ? `${patient.age} ans •` : ''} {patient.analyses} analyses • Dernière visite:{" "}
                        {new Date(patient.lastVisit).toLocaleDateString("fr-FR")}
                      </p>
                      {patient.address || patient.phone ? (
                        <p className="text-xs text-muted-foreground mt-1">
                          {patient.address && <>📍 {patient.address}</>}
                          {patient.address && patient.phone && ' • '}
                          {patient.phone && <>📞 {patient.phone}</>}
                        </p>
                      ) : null}
                    </div>
                    <Button 
                      variant="ghost" 
                      size="sm"
                      asChild
                    >
                      <Link href={`/professional/patients/${patient.id}`}>
                        <Eye className="w-4 h-4" />
                      </Link>
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
