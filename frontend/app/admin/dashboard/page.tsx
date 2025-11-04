"use client"

import { useState, useEffect } from "react"
import { AdminSidebar } from "@/components/admin-sidebar"
import { AdminHeader } from "@/components/admin-header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Users, Smartphone, UserCheck, Activity, TrendingUp, AlertCircle } from "lucide-react"
import { useAuth } from "@/contexts/auth-context"
import { Skeleton } from "@/components/ui/skeleton"
import { AuthGuard } from "@/components/auth-guard"
import { apiClient } from "@/lib/api"

export default function AdminDashboardPage() {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true)
        setError(null)
        const data = await apiClient.getDashboardStats()
        setStats(data)
      } catch (err) {
        setError(err.message || 'Failed to fetch stats')
      } finally {
        setLoading(false)
      }
    }
    
    if (user) {
      fetchStats()
    }
  }, [user])

  if (loading) {
    return (
      <div className="flex min-h-screen">
        <AdminSidebar />
        <div className="flex-1 p-8">
          <div className="space-y-6">
            <div>
              <h1 className="text-3xl font-bold">Tableau de bord</h1>
              <p className="text-muted-foreground">Vue d'ensemble de la plateforme</p>
            </div>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
              {[...Array(4)].map((_, i) => (
                <Card key={i}>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
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
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex min-h-screen">
        <AdminSidebar />
        <div className="flex-1 p-8">
          <div className="text-center">
            <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-red-600 mb-2">Erreur de connexion</h2>
            <p className="text-muted-foreground">{error}</p>
          </div>
        </div>
      </div>
    )
  }

  // Utiliser les vraies données du backend
  const statsData = stats ? [
    {
      title: "Professionnels",
      value: stats.total_professionals?.toString() || "0",
      change: `${stats.active_professionals || 0} actifs`,
      icon: Users,
      color: "text-blue-600",
      bgColor: "bg-blue-100 dark:bg-blue-950",
    },
    {
      title: "Utilisateurs Mobile",
      value: stats.total_users?.toString() || "0",
      change: `${stats.active_users || 0} actifs`,
      icon: Smartphone,
      color: "text-pink-600",
      bgColor: "bg-pink-100 dark:bg-pink-950",
    },
    {
      title: "Demandes en attente",
      value: stats.pending_access_requests?.toString() || "0",
      change: "À traiter",
      icon: UserCheck,
      color: "text-orange-600",
      bgColor: "bg-orange-100 dark:bg-orange-950",
    },
    {
      title: "Analyses ce mois",
      value: stats.analyses_this_month?.toString() || "0",
      change: `${stats.analyses_today || 0} aujourd'hui`,
      icon: Activity,
      color: "text-green-600",
      bgColor: "bg-green-100 dark:bg-green-950",
    },
  ] : []

  // Supprimer les données fictives - sera remplacé par des données réelles du backend
  const recentActivity: any[] = []

  // Supprimer les alertes fictives - sera remplacé par des alertes réelles du backend
  const alerts: any[] = []

  return (
    <AuthGuard>
      <div className="flex min-h-screen bg-slate-50 dark:bg-slate-950">
        <AdminSidebar />
        <div className="flex-1 md:ml-64">
          <AdminHeader />
          <main className="p-8">
        <div className="max-w-7xl mx-auto space-y-8">
          {/* Header */}
          <div>
            <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Tableau de bord</h1>
            <p className="text-slate-600 dark:text-slate-400 mt-1">
              Vue d'ensemble de la plateforme BreastCare Pro
            </p>
          </div>

          {/* Stats Grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {statsData.map((stat) => (
              <Card key={stat.title}>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">{stat.title}</CardTitle>
                  <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                    <stat.icon className={`h-4 w-4 ${stat.color}`} />
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <p className="text-xs text-muted-foreground mt-1">{stat.change}</p>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            {/* Recent Activity */}
            <Card>
              <CardHeader>
                <CardTitle>Activité récente</CardTitle>
                <CardDescription>Dernières actions sur la plateforme</CardDescription>
              </CardHeader>
              <CardContent>
                {recentActivity.length > 0 ? (
                  <div className="space-y-4">
                    {recentActivity.map((activity, index) => (
                      <div key={index} className="flex items-center gap-4">
                        <div
                          className={`w-2 h-2 rounded-full ${
                            activity.status === "success" ? "bg-green-500" : "bg-orange-500"
                          }`}
                        />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-slate-900 dark:text-slate-100 truncate">
                            {activity.type}
                          </p>
                          <p className="text-sm text-slate-600 dark:text-slate-400 truncate">{activity.user}</p>
                        </div>
                        <span className="text-xs text-slate-500">{activity.time}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Activity className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                    <p className="text-slate-500">Aucune activité récente</p>
                    <p className="text-sm text-slate-400">Les nouvelles activités apparaîtront ici</p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Alerts */}
            <Card>
              <CardHeader>
                <CardTitle>Alertes système</CardTitle>
                <CardDescription>Notifications importantes</CardDescription>
              </CardHeader>
              <CardContent>
                {alerts.length > 0 ? (
                  <div className="space-y-4">
                    {alerts.map((alert, index) => (
                      <div
                        key={index}
                        className={`flex items-start gap-3 p-3 rounded-lg ${
                          alert.severity === "warning"
                            ? "bg-orange-50 dark:bg-orange-950/20"
                            : alert.severity === "info"
                              ? "bg-blue-50 dark:bg-blue-950/20"
                              : "bg-green-50 dark:bg-green-950/20"
                        }`}
                      >
                        <AlertCircle
                          className={`h-5 w-5 mt-0.5 ${
                            alert.severity === "warning"
                              ? "text-orange-600"
                              : alert.severity === "info"
                                ? "text-blue-600"
                                : "text-green-600"
                          }`}
                        />
                        <p className="text-sm text-slate-700 dark:text-slate-300">{alert.message}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <AlertCircle className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                    <p className="text-slate-500">Aucune alerte système</p>
                    <p className="text-sm text-slate-400">Tout fonctionne normalement</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Quick Stats */}
          <Card>
            <CardHeader>
              <CardTitle>Statistiques rapides</CardTitle>
              <CardDescription>Aperçu des performances du système</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-3">
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <TrendingUp className="h-4 w-4 text-green-600" />
                    <span className="text-sm font-medium">Taux d'adoption</span>
                  </div>
                  <p className="text-2xl font-bold">{stats ? `${Math.round((stats.active_users / Math.max(stats.total_users, 1)) * 100)}%` : "0%"}</p>
                  <p className="text-xs text-muted-foreground">Utilisateurs actifs</p>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Activity className="h-4 w-4 text-blue-600" />
                    <span className="text-sm font-medium">Analyses/jour</span>
                  </div>
                  <p className="text-2xl font-bold">{stats?.analyses_today || 0}</p>
                  <p className="text-xs text-muted-foreground">Aujourd'hui</p>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Users className="h-4 w-4 text-purple-600" />
                    <span className="text-sm font-medium">Utilisateurs actifs</span>
                  </div>
                  <p className="text-2xl font-bold">{stats?.active_users || 0}</p>
                  <p className="text-xs text-muted-foreground">Total: {stats?.total_users || 0}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
          </main>
        </div>
      </div>
    </AuthGuard>
  )
}
