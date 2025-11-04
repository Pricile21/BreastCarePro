"use client"

import { ProfessionalSidebar } from "@/components/professional-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { FileText, Download, Eye, Search, AlertCircle } from "lucide-react"
import Link from "next/link"
import { useState, useEffect } from "react"
import { useProfessionalReports } from "@/hooks/use-api"
import { useSearchParams, useRouter } from "next/navigation"
import { apiClient } from "@/lib/api"

export default function ReportsPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState<string | undefined>(undefined)
  const [downloadingId, setDownloadingId] = useState<string | null>(null)
  const { reports, loading, error, refetch } = useProfessionalReports(searchTerm, statusFilter)
  
  // Vérifier si on a un analysis_id dans l'URL pour rediriger vers l'analyse
  useEffect(() => {
    const analysisId = searchParams.get('analysis_id')
    if (analysisId) {
      // Rediriger vers la page d'analyse
      router.replace(`/professional/analysis/${analysisId}`)
    }
  }, [searchParams, router])

  const handleSearch = (value: string) => {
    setSearchTerm(value)
  }

  const handleStatusFilter = (status: string | undefined) => {
    setStatusFilter(status)
  }

  const handleDownload = async (reportId: string) => {
    try {
      setDownloadingId(reportId)
      const blob = await apiClient.downloadReport(reportId)
      
      // Créer un lien de téléchargement
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `Rapport_${reportId.substring(0, 8)}.pdf`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error: any) {
      alert(`Erreur lors du téléchargement: ${error.message}`)
    } finally {
      setDownloadingId(null)
    }
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
            <Card className="mb-6">
              <CardContent className="pt-6">
                <Skeleton className="h-10 w-full" />
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <Skeleton className="h-6 w-32 mb-2" />
                <Skeleton className="h-4 w-24" />
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {[...Array(3)].map((_, i) => (
                    <div key={i} className="flex items-center gap-4 p-4 rounded-lg border">
                      <Skeleton className="w-10 h-10 rounded-lg" />
                      <div className="flex-1">
                        <Skeleton className="h-4 w-32 mb-2" />
                        <Skeleton className="h-3 w-48" />
                      </div>
                      <div className="flex gap-2">
                        <Skeleton className="h-6 w-16" />
                        <Skeleton className="h-8 w-8" />
                        <Skeleton className="h-8 w-8" />
                      </div>
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
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
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
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">Rapports médicaux</h1>
            <p className="text-muted-foreground">Historique et gestion des rapports d'analyse</p>
          </div>

          {/* Search and Filters */}
          <Card className="mb-6">
            <CardContent className="pt-6">
              <div className="flex gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input 
                    placeholder="Rechercher par ID patient ou rapport..." 
                    className="pl-9"
                    value={searchTerm}
                    onChange={(e) => handleSearch(e.target.value)}
                  />
                </div>
                <div className="flex gap-2">
                  <Button 
                    variant={statusFilter === undefined ? "default" : "outline"}
                    onClick={() => handleStatusFilter(undefined)}
                  >
                    Tous
                  </Button>
                  <Button 
                    variant={statusFilter === "pending" ? "default" : "outline"}
                    onClick={() => handleStatusFilter("pending")}
                  >
                    En attente
                  </Button>
                  <Button 
                    variant={statusFilter === "completed" ? "default" : "outline"}
                    onClick={() => handleStatusFilter("completed")}
                  >
                    Complétés
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Reports Table */}
          <Card>
            <CardHeader>
              <CardTitle>Tous les rapports</CardTitle>
              <CardDescription>{reports.length} rapports au total</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {reports && reports.length > 0 ? (
                  reports.map((report) => (
                    <div
                      key={report.id}
                      className="flex items-center gap-4 p-4 rounded-lg border hover:bg-accent/50 transition-colors"
                    >
                      <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                        <FileText className="w-5 h-5 text-primary" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <p className="font-medium">{report.id}</p>
                          <Badge variant="outline" className="text-xs">
                            {report.bi_rads_category}
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground">
                          Patient {report.patient_id} • {new Date(report.created_at).toLocaleDateString("fr-FR")}
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
                        <Button variant="ghost" size="sm" asChild>
                          <Link href={`/professional/analysis/${report.analysis_id || report.id}`}>
                            <Eye className="w-4 h-4" />
                          </Link>
                        </Button>
                        <Button 
                          variant="ghost" 
                          size="sm"
                          onClick={() => handleDownload(report.id)}
                          disabled={downloadingId === report.id}
                        >
                          <Download className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    <FileText className="h-8 w-8 mx-auto mb-2 opacity-50" />
                    <p>Aucun rapport trouvé</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
