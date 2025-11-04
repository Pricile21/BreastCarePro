"use client"

import { ProfessionalSidebar } from "@/components/professional-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Activity, FileText, TrendingUp, Users, Upload, AlertCircle } from "lucide-react"
import Link from "next/link"
import { useProfessionalDashboard } from "@/hooks/use-api"
import { ApiTestComponent } from "@/components/api-test"
import { useAuth } from "@/contexts/auth-context"

export default function ProfessionalDashboardPage() {
  const { user, isAuthenticated, loading: authLoading } = useAuth()
  const { stats, analyses, alerts, loading, error, refetch } = useProfessionalDashboard()
  
  // Attendre que l'authentification soit prête
  if (authLoading) {
    return (
      <div className="flex h-screen">
        <ProfessionalSidebar />
        <main className="flex-1 overflow-y-auto bg-background">
          <div className="container mx-auto p-8">
            <div className="mb-8">
              <Skeleton className="h-8 w-64 mb-2" />
              <Skeleton className="h-4 w-96" />
            </div>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
              {[...Array(4)].map((_, i) => (
                <Card key={i}>
                  <CardHeader className="flex flex-row items-center justify-between pb-2">
                    <Skeleton className="h-4 w-24" />
                    <Skeleton className="h-4 w-4" />
                  </CardHeader>
                  <CardContent>
                    <Skeleton className="h-8 w-16 mb-2" />
                    <Skeleton className="h-3 w-20" />
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </main>
      </div>
    )
  }
  
  // Si pas authentifié, ne pas afficher le dashboard
  if (!isAuthenticated || !user) {
    return (
      <div className="flex h-screen">
        <ProfessionalSidebar />
        <main className="flex-1 overflow-y-auto bg-background">
          <div className="container mx-auto p-8">
            <Alert variant="destructive" className="mb-6">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                Vous devez être connecté pour accéder au dashboard.
                <br />
                <Button 
                  onClick={() => window.location.href = '/professional/login'} 
                  className="mt-2"
                  size="sm"
                >
                  Se connecter
                </Button>
              </AlertDescription>
            </Alert>
            <ApiTestComponent />
          </div>
        </main>
      </div>
    )
  }
  
  if (loading) {
    return (
      <div className="flex h-screen">
        <ProfessionalSidebar />
        <main className="flex-1 overflow-y-auto bg-background">
          <div className="container mx-auto p-8">
            <div className="mb-8">
              <Skeleton className="h-8 w-64 mb-2" />
              <Skeleton className="h-4 w-96" />
            </div>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
              {[...Array(4)].map((_, i) => (
                <Card key={i}>
                  <CardHeader className="flex flex-row items-center justify-between pb-2">
                    <Skeleton className="h-4 w-24" />
                    <Skeleton className="h-4 w-4" />
                  </CardHeader>
                  <CardContent>
                    <Skeleton className="h-8 w-16 mb-2" />
                    <Skeleton className="h-3 w-20" />
                  </CardContent>
                </Card>
              ))}
            </div>
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
            <ApiTestComponent />
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
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">Tableau de bord</h1>
            <p className="text-muted-foreground">Vue d'ensemble de votre activité et analyses récentes</p>
          </div>

          {/* Stats Grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Analyses ce mois</CardTitle>
                <Activity className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats?.analyses_this_month || 0}</div>
                <p className="text-xs text-muted-foreground mt-1">
                  <span className={stats?.month_change_percent >= 0 ? "text-primary" : "text-destructive"}>
                    {stats?.month_change_percent >= 0 ? "+" : ""}{stats?.month_change_percent || 0}%
                  </span> vs mois dernier
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Patients actifs</CardTitle>
                <Users className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats?.active_patients || 0}</div>
                <p className="text-xs text-muted-foreground mt-1">
                  <span className="text-primary">+{stats?.new_patients_this_week || 0}</span> nouveaux cette semaine
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Rapports générés</CardTitle>
                <FileText className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats?.total_reports || 0}</div>
                <p className="text-xs text-muted-foreground mt-1">Total depuis le début</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Taux de détection</CardTitle>
                <TrendingUp className="h-4 w-4 text-accent" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats?.ai_accuracy || 0}%</div>
                <p className="text-xs text-muted-foreground mt-1">Précision de l'IA</p>
              </CardContent>
            </Card>
          </div>

          {/* Quick Actions */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Actions rapides</CardTitle>
              <CardDescription>Accédez rapidement aux fonctionnalités principales</CardDescription>
            </CardHeader>
            <CardContent className="flex flex-wrap gap-4">
              <Button asChild size="lg">
                <Link href="/professional/upload">
                  <Upload className="mr-2 h-4 w-4" />
                  Nouvelle analyse
                </Link>
              </Button>
              <Button variant="outline" asChild size="lg">
                <Link href="/professional/reports">
                  <FileText className="mr-2 h-4 w-4" />
                  Voir les rapports
                </Link>
              </Button>
              <Button variant="outline" asChild size="lg">
                <Link href="/professional/patients">
                  <Users className="mr-2 h-4 w-4" />
                  Gérer les patients
                </Link>
              </Button>
            </CardContent>
          </Card>

          {/* Recent Analyses */}
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Analyses récentes</CardTitle>
                <CardDescription>Dernières mammographies analysées</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {analyses && analyses.length > 0 ? (
                    analyses.map((analysis) => (
                      <div key={analysis.id} className="flex items-center justify-between p-3 rounded-lg border">
                        <div>
                          <p className="font-medium">Patient #{analysis.patient_id}</p>
                          <p className="text-sm text-muted-foreground">{analysis.time_ago}</p>
                        </div>
                        <div className="text-right">
                          <p
                            className={cn(
                              "text-sm font-medium",
                              analysis.risk_level === "high" && "text-destructive",
                              analysis.risk_level === "medium" && "text-accent",
                              analysis.risk_level === "low" && "text-primary",
                            )}
                          >
                            {analysis.bi_rads_category}
                          </p>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">
                      <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
                      <p>Aucune analyse récente</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Alertes et notifications</CardTitle>
                <CardDescription>Cas nécessitant votre attention</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {alerts && alerts.length > 0 ? (
                    alerts.map((alert) => {
                      const AlertContent = (
                        <div 
                          className={cn(
                            "flex gap-3 p-3 rounded-lg border",
                            alert.severity === "high" && "border-destructive/50 bg-destructive/5",
                            alert.severity === "medium" && "border-accent/50 bg-accent/5",
                            alert.severity === "low" && "border-primary/50 bg-primary/5"
                          )}
                        >
                          <AlertCircle className={cn(
                            "h-5 w-5 flex-shrink-0 mt-0.5",
                            alert.severity === "high" && "text-destructive",
                            alert.severity === "medium" && "text-accent",
                            alert.severity === "low" && "text-primary"
                          )} />
                          <div>
                            <p className="font-medium text-sm">{alert.title}</p>
                            <p className="text-sm text-muted-foreground">{alert.message}</p>
                          </div>
                        </div>
                      )
                      
                      // Rendre cliquable si c'est une alerte patient
                      if (alert.type === "high_risk" && alert.analysis_id) {
                        return (
                          <Link key={alert.id} href={`/professional/analysis/${alert.analysis_id}`}>
                            <div className="hover:opacity-80 transition-opacity cursor-pointer">
                              {AlertContent}
                            </div>
                          </Link>
                        )
                      } else if (alert.type === "pending_reports") {
                        return (
                          <Link key={alert.id} href="/professional/reports?status=completed">
                            <div className="hover:opacity-80 transition-opacity cursor-pointer">
                              {AlertContent}
                            </div>
                          </Link>
                        )
                      }
                      
                      return <div key={alert.id}>{AlertContent}</div>
                    })
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">
                      <AlertCircle className="h-8 w-8 mx-auto mb-2 opacity-50" />
                      <p>Aucune alerte</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}

function cn(...classes: (string | boolean | undefined)[]) {
  return classes.filter(Boolean).join(" ")
}
