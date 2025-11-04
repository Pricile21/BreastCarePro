"use client"

import { useState, useEffect } from "react"
import { AdminSidebar } from "@/components/admin-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, Users, Activity, Smartphone, Clock, Star, Calendar } from "lucide-react"
import { apiClient } from "@/lib/api"

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true)
        setError(null)
        // Pour l'instant, on utilise des données vides
        // Plus tard, on pourra implémenter des endpoints d'analytics
        setAnalytics({
          userGrowth: 0,
          engagementRate: 0,
          completedAnalyses: 0,
          appDownloads: 0,
          avgAnalysisTime: 0,
          satisfactionRate: 0,
          appointmentsBooked: 0
        })
      } catch (err: any) {
        setError(err.message || 'Failed to fetch analytics')
        setAnalytics(null)
      } finally {
        setLoading(false)
      }
    }
    
    fetchAnalytics()
  }, [])
  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-slate-950">
      <AdminSidebar />
      <main className="flex-1 md:ml-64 p-8">
        <div className="max-w-7xl mx-auto space-y-6">
          {/* Header */}
          <div>
            <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Analytiques</h1>
            <p className="text-slate-600 dark:text-slate-400 mt-1">
              Statistiques et métriques de performance de la plateforme
            </p>
          </div>

          {/* Key Metrics */}
          {loading ? (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
              {[...Array(4)].map((_, i) => (
                <Card key={i}>
                  <CardHeader className="flex flex-row items-center justify-between pb-2">
                    <div className="h-4 w-24 bg-slate-200 dark:bg-slate-700 rounded animate-pulse"></div>
                    <div className="h-4 w-4 bg-slate-200 dark:bg-slate-700 rounded animate-pulse"></div>
                  </CardHeader>
                  <CardContent>
                    <div className="h-8 w-16 bg-slate-200 dark:bg-slate-700 rounded animate-pulse mb-2"></div>
                    <div className="h-3 w-20 bg-slate-200 dark:bg-slate-700 rounded animate-pulse"></div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : error ? (
            <Card>
              <CardContent className="p-8 text-center">
                <div className="text-red-500 mb-4">⚠️</div>
                <p className="text-red-600 mb-2">Erreur lors du chargement des analytiques</p>
                <p className="text-sm text-slate-500">{error}</p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">Croissance utilisateurs</CardTitle>
                  <TrendingUp className="h-4 w-4 text-green-600" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{analytics?.userGrowth || 0}%</div>
                  <p className="text-xs text-muted-foreground mt-1">vs mois dernier</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">Taux d'engagement</CardTitle>
                  <Users className="h-4 w-4 text-blue-600" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{analytics?.engagementRate || 0}%</div>
                  <p className="text-xs text-muted-foreground mt-1">Utilisateurs actifs</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">Analyses complétées</CardTitle>
                  <Activity className="h-4 w-4 text-purple-600" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{analytics?.completedAnalyses || 0}</div>
                  <p className="text-xs text-muted-foreground mt-1">Ce mois</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">Téléchargements app</CardTitle>
                  <Smartphone className="h-4 w-4 text-pink-600" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{analytics?.appDownloads || 0}</div>
                  <p className="text-xs text-muted-foreground mt-1">Total</p>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Charts Section */}
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Analyses par mois</CardTitle>
                <CardDescription>Évolution du nombre d'analyses</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64 flex items-center justify-center bg-slate-50 dark:bg-slate-900 rounded-lg border-2 border-dashed border-slate-200 dark:border-slate-700">
                  <div className="text-center">
                    <Activity className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                    <p className="text-slate-500 mb-2">Aucune donnée d'analyse disponible</p>
                    <p className="text-sm text-slate-400">Les graphiques apparaîtront quand des analyses seront effectuées</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Répartition des utilisateurs</CardTitle>
                <CardDescription>Par ville et région</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64 flex items-center justify-center bg-slate-50 dark:bg-slate-900 rounded-lg border-2 border-dashed border-slate-200 dark:border-slate-700">
                  <div className="text-center">
                    <Users className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                    <p className="text-slate-500 mb-2">Aucune donnée d'utilisateur disponible</p>
                    <p className="text-sm text-slate-400">Les graphiques apparaîtront quand des utilisateurs s'inscriront</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Additional Stats */}
          <Card>
            <CardHeader>
              <CardTitle>Statistiques détaillées</CardTitle>
              <CardDescription>Métriques de performance du système</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="space-y-4">
                  {[...Array(3)].map((_, i) => (
                    <div key={i} className="flex items-center justify-between p-4 rounded-lg bg-slate-100 dark:bg-slate-900">
                      <div className="space-y-2">
                        <div className="h-4 w-32 bg-slate-200 dark:bg-slate-700 rounded animate-pulse"></div>
                        <div className="h-3 w-24 bg-slate-200 dark:bg-slate-700 rounded animate-pulse"></div>
                      </div>
                      <div className="h-8 w-16 bg-slate-200 dark:bg-slate-700 rounded animate-pulse"></div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 rounded-lg bg-slate-50 dark:bg-slate-900">
                    <div className="flex items-center gap-3">
                      <Clock className="h-5 w-5 text-blue-600" />
                      <div>
                        <p className="font-medium">Temps moyen d'analyse</p>
                        <p className="text-sm text-muted-foreground">Par mammographie</p>
                      </div>
                    </div>
                    <span className="text-2xl font-bold">{analytics?.avgAnalysisTime || 0}s</span>
                  </div>
                  <div className="flex items-center justify-between p-4 rounded-lg bg-slate-50 dark:bg-slate-900">
                    <div className="flex items-center gap-3">
                      <Star className="h-5 w-5 text-yellow-600" />
                      <div>
                        <p className="font-medium">Taux de satisfaction</p>
                        <p className="text-sm text-muted-foreground">Professionnels</p>
                      </div>
                    </div>
                    <span className="text-2xl font-bold">{analytics?.satisfactionRate || 0}%</span>
                  </div>
                  <div className="flex items-center justify-between p-4 rounded-lg bg-slate-50 dark:bg-slate-900">
                    <div className="flex items-center gap-3">
                      <Calendar className="h-5 w-5 text-green-600" />
                      <div>
                        <p className="font-medium">Rendez-vous pris</p>
                        <p className="text-sm text-muted-foreground">Via l'application mobile</p>
                      </div>
                    </div>
                    <span className="text-2xl font-bold">{analytics?.appointmentsBooked || 0}</span>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
