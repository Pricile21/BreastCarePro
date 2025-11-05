"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { ProfessionalSidebar } from "@/components/professional-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { AlertCircle, CheckCircle, Download, FileText, ImageIcon, Loader2, X } from "lucide-react"
import Link from "next/link"
import { apiClient } from "@/lib/api"

export default function AnalysisResultPage() {
  const params = useParams()
  const router = useRouter()
  const analysisId = params.id as string
  const [analysis, setAnalysis] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [validating, setValidating] = useState(false)
  const [exporting, setExporting] = useState(false)
  const [generatingReport, setGeneratingReport] = useState(false)
  const [showImagesModal, setShowImagesModal] = useState(false)
  
  // Get API URL from environment
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        setLoading(true)
        const response = await fetch(`${apiUrl}/mammography/analysis/${analysisId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
          }
        })
        
        if (response.ok) {
          const data = await response.json()
          setAnalysis(data)
        } else {
          const errorData = await response.json().catch(() => ({}))
          console.error('❌ Erreur API:', response.status, errorData)
          setError(`Erreur ${response.status}: ${errorData.detail || 'Erreur lors du chargement des résultats'}`)
        }
      } catch (err) {
        setError('Erreur de connexion')
      } finally {
        setLoading(false)
      }
    }

    if (analysisId) {
      fetchAnalysis()
    }
  }, [analysisId])

  if (loading) {
    return (
      <div className="flex h-screen">
        <ProfessionalSidebar />
        <main className="flex-1 overflow-y-auto bg-background flex items-center justify-center">
          <div className="text-center">
            <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4" />
            <p>Chargement des résultats...</p>
          </div>
        </main>
      </div>
    )
  }

  if (error || !analysis) {
    return (
      <div className="flex h-screen">
        <ProfessionalSidebar />
        <main className="flex-1 overflow-y-auto bg-background flex items-center justify-center">
          <div className="text-center">
            <AlertCircle className="w-8 h-8 text-destructive mx-auto mb-4" />
            <p className="text-destructive">{error || 'Aucun résultat trouvé'}</p>
            <Button asChild className="mt-4">
              <Link href="/professional/upload">Nouvelle analyse</Link>
            </Button>
          </div>
        </main>
      </div>
    )
  }

  const getRiskLevel = (biRads: string) => {
    // Extraire le numéro de catégorie de différentes formats
    let category = 2 // Valeur par défaut
    
    if (biRads.includes('CATEGORY_')) {
      category = parseInt(biRads.split('CATEGORY_')[1]) || 2
    } else if (biRads.includes('_')) {
      category = parseInt(biRads.split('_')[1]) || 2
    } else if (!isNaN(parseInt(biRads))) {
      category = parseInt(biRads)
    }
    
    if (category <= 2) return { label: "Faible", color: "bg-primary text-primary-foreground" }
    if (category === 3) return { label: "Modéré", color: "bg-accent text-accent-foreground" }
    return { label: "Élevé", color: "bg-destructive text-destructive-foreground" }
  }

  // Fonction pour exporter les données de l'analyse en JSON
  const handleExport = async () => {
    if (!analysis) return
    try {
      setExporting(true)
      const dataToExport = {
        analysis_id: analysisId,
        patient_id: analysis.patient_id,
        bi_rads_category: analysis.bi_rads_category,
        confidence_score: analysis.confidence_score,
        findings: analysis.findings,
        recommendations: analysis.recommendations,
        breast_density: analysis.breast_density,
        model_version: analysis.model_version,
        processing_time: analysis.processing_time,
        status: analysis.status,
        created_at: analysis.created_at,
      }

      const blob = new Blob([JSON.stringify(dataToExport, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `analyse_${analysis.patient_id}_${analysisId}.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (err) {
      console.error('Erreur lors de l\'export:', err)
      alert('Erreur lors de l\'export des données')
    } finally {
      setExporting(false)
    }
  }

  // Fonction pour générer et télécharger un rapport PDF
  const handleGenerateReport = async () => {
    if (!analysis) return
    try {
      setGeneratingReport(true)
      
      // Utiliser directement l'analysis_id (UUID) - l'endpoint le supporte maintenant
      const blob = await apiClient.downloadReport(analysisId)
      
      // Créer un lien de téléchargement
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      
      // Générer le nom du fichier
      const patientId = analysis.patient_id?.replace(/[^a-zA-Z0-9]/g, '_') || 'report'
      const filename = `Rapport_Mammographie_${patientId}_${analysisId.slice(0, 8)}.pdf`
      link.download = filename
      
      // Déclencher le téléchargement
      document.body.appendChild(link)
      link.click()
      
      // Nettoyer
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (err: any) {
      console.error('Erreur lors de la génération du rapport:', err)
      alert(`Erreur lors de la génération du rapport: ${err.message || 'Erreur inconnue'}`)
    } finally {
      setGeneratingReport(false)
    }
  }

  // Fonction pour valider l'analyse
  const handleValidateAnalysis = async () => {
    if (!analysis) return
    try {
      setValidating(true)
      const response = await fetch(`${apiUrl}/mammography/analysis/${analysisId}/validate`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        // Récupérer les données mises à jour depuis la réponse
        const responseData = await response.json()
        
        if (responseData.analysis) {
          setAnalysis(responseData.analysis)
          alert('✅ Analyse validée avec succès')
        } else {
          // Si l'endpoint ne retourne pas l'analyse, recharger
          const updatedAnalysis = await fetch(`${apiUrl}/mammography/analysis/${analysisId}`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            }
          })
          
          if (updatedAnalysis.ok) {
            const data = await updatedAnalysis.json()
            setAnalysis(data)
            alert('✅ Analyse validée avec succès')
          }
        }
      } else {
        const errorData = await response.json().catch(() => ({}))
        alert(`Erreur lors de la validation: ${errorData.detail || 'Erreur inconnue'}`)
      }
    } catch (err) {
      console.error('Erreur lors de la validation:', err)
      alert('Erreur lors de la validation de l\'analyse')
    } finally {
      setValidating(false)
    }
  }

  // Fonction pour voir les images
  const handleViewImages = () => {
    if (!analysis) return
    setShowImagesModal(true)
  }

  const risk = analysis ? getRiskLevel(analysis.bi_rads_category || 'CATEGORY_2') : { label: "Faible", color: "bg-primary text-primary-foreground" }
  const biRadsNumber = analysis ? (() => {
    const category = analysis.bi_rads_category || 'CATEGORY_2'
    if (category.includes('CATEGORY_')) {
      return parseInt(category.split('CATEGORY_')[1]) || 2
    } else if (category.includes('_')) {
      return parseInt(category.split('_')[1]) || 2
    } else if (!isNaN(parseInt(category))) {
      return parseInt(category)
    }
    return 2
  })() : 2

  return (
    <div className="flex h-screen">
      <ProfessionalSidebar />

      <main className="flex-1 overflow-y-auto bg-background">
        <div className="container mx-auto p-8 max-w-6xl">
          {/* Header */}
          <div className="mb-8 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">Résultats d'analyse</h1>
              <p className="text-muted-foreground">
                Patient {analysis.patient_id} • {new Date(analysis.created_at).toLocaleDateString("fr-FR")}
              </p>
            </div>
            <div className="flex gap-3">
              <Button 
                variant="outline" 
                onClick={handleExport}
                disabled={exporting}
              >
                {exporting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Export...
                  </>
                ) : (
                  <>
                    <Download className="mr-2 h-4 w-4" />
                    Exporter
                  </>
                )}
              </Button>
              <Button 
                onClick={handleGenerateReport}
                disabled={generatingReport}
              >
                {generatingReport ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Génération...
                  </>
                ) : (
                  <>
                    <FileText className="mr-2 h-4 w-4" />
                    Générer rapport
                  </>
                )}
              </Button>
            </div>
          </div>

          {/* Main Results */}
          <div className="grid gap-6 lg:grid-cols-3 mb-6">
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle>Classification BI-RADS</CardTitle>
                <CardDescription>Résultat de l'analyse par intelligence artificielle</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-6 mb-6">
                  <div className="text-center">
                    <div className="text-6xl font-bold text-primary mb-2">BI-RADS {biRadsNumber}</div>
                    <Badge className={risk.color}>{risk.label}</Badge>
                  </div>
                  <div className="flex-1">
                    <div className="space-y-3">
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-muted-foreground">Confiance du modèle</span>
                          <span className="font-medium">{Math.round((analysis.confidence_score || 0) * 100)}%</span>
                        </div>
                        <div className="h-2 bg-secondary rounded-full overflow-hidden">
                          <div className="h-full bg-primary" style={{ width: `${(analysis.confidence_score || 0) * 100}%` }} />
                        </div>
                      </div>
                      <div className="flex items-start gap-2 p-3 rounded-lg bg-muted">
                        <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
                        <div>
                          <p className="text-sm font-medium">{analysis.findings || 'Analyse terminée'}</p>
                          <p className="text-xs text-muted-foreground mt-1">{analysis.recommendations || 'Consultez les recommandations ci-dessous'}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Findings */}
                <div className="space-y-3">
                  <h3 className="font-semibold">Observations détaillées</h3>
                  <div className="p-4 rounded-lg border bg-card">
                    <div className="space-y-2">
                      <div>
                        <span className="font-medium">Densité mammaire:</span> {analysis.breast_density || 'Non spécifiée'}
                      </div>
                      <div>
                        <span className="font-medium">Modèle utilisé:</span> {analysis.model_version || 'MedSigLIP'}
                      </div>
                      <div>
                        <span className="font-medium">Temps de traitement:</span> {analysis.processing_time || 0}s
                      </div>
                      <div>
                        <span className="font-medium">Statut:</span> {
                          analysis.status === 'validated' ? 'Validé' : 
                          analysis.status === 'completed' ? 'Terminé' :
                          analysis.status === 'pending' ? 'En attente' :
                          analysis.status === 'processing' ? 'En traitement' :
                          analysis.status === 'failed' ? 'Échoué' :
                          analysis.status || 'Terminé'
                        }
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Side Panel */}
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Informations patient</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3 text-sm">
                  <div>
                    <p className="text-muted-foreground">ID Patient</p>
                    <p className="font-medium">{analysis.patient_id}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Date d'analyse</p>
                    <p className="font-medium">{new Date(analysis.created_at).toLocaleDateString("fr-FR")}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Statut</p>
                    <Badge variant={analysis.status?.toLowerCase() === 'validated' ? 'default' : 'outline'}>
                      {analysis.status?.toLowerCase() === 'validated' ? 'Validé' : 'En attente de validation'}
                    </Badge>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Actions recommandées</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <Button 
                    variant="outline" 
                    className="w-full justify-start bg-transparent"
                    onClick={handleValidateAnalysis}
                    disabled={validating || analysis.status?.toLowerCase() === 'validated'}
                  >
                    {validating ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Validation...
                      </>
                    ) : (
                      <>
                        <CheckCircle className="mr-2 h-4 w-4" />
                        Valider l'analyse
                      </>
                    )}
                  </Button>
                  <Button 
                    variant="outline" 
                    className="w-full justify-start bg-transparent"
                    onClick={handleViewImages}
                  >
                    <ImageIcon className="mr-2 h-4 w-4" />
                    Voir les images
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Image Viewer */}
          <Card>
            <CardHeader>
              <CardTitle>Images mammographiques</CardTitle>
              <CardDescription>Visualisation avec zones d'intérêt détectées</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4">
                {analysis.original_files && analysis.original_files.length > 0 ? (
                  analysis.original_files.map((fileInfo: any, i: number) => {
                    // Parse view type to get view and side
                    const viewParts = fileInfo.view_type.split('_');
                    const view = viewParts[0] || 'UNKNOWN';
                    const side = viewParts[1] || '';
                    
                    return (
                      <div key={i} className="aspect-square bg-muted rounded-lg relative overflow-hidden">
                        <img 
                          src={`${apiUrl}/mammography/image/${fileInfo.path}`}
                          alt={`Mammographie ${fileInfo.view_type}`}
                          className="w-full h-full object-contain"
                          onError={(e) => {
                            const target = e.target as HTMLImageElement;
                            target.style.display = 'none';
                            const parent = target.parentElement;
                            if (parent) {
                              parent.innerHTML = `
                                <div class="flex items-center justify-center h-full">
                                  <div class="text-center">
                                    <svg class="w-16 h-16 text-muted-foreground mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                    </svg>
                                    <p class="text-sm text-muted-foreground">Image non disponible</p>
                                  </div>
                                </div>
                              `;
                            }
                          }}
                        />
                        <div className="absolute top-3 left-3">
                          <Badge variant={side === 'LEFT' ? 'default' : 'secondary'}>
                            {view} {side}
                          </Badge>
                        </div>
                        {/* Zone de détection simulée */}
                        <div className="absolute top-1/3 left-1/3 w-24 h-24 border-2 border-destructive rounded opacity-50" />
                      </div>
                    );
                  })
                ) : (
                  // Fallback for 4 standard views
                  [
                    { view: 'CC', side: 'LEFT' },
                    { view: 'CC', side: 'RIGHT' },
                    { view: 'MLO', side: 'LEFT' },
                    { view: 'MLO', side: 'RIGHT' }
                  ].map((viewInfo, i) => (
                    <div key={i} className="aspect-square bg-muted rounded-lg flex items-center justify-center relative">
                      <ImageIcon className="w-16 h-16 text-muted-foreground" />
                      <div className="absolute top-3 left-3">
                        <Badge variant={viewInfo.side === 'LEFT' ? 'default' : 'secondary'}>
                          {viewInfo.view} {viewInfo.side}
                        </Badge>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </main>

      {/* Modal pour voir les images */}
      {showImagesModal && (
        <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4">
          <div className="bg-background rounded-lg max-w-6xl w-full max-h-[90vh] overflow-auto">
            <div className="flex items-center justify-between p-4 border-b">
              <h2 className="text-xl font-bold">Images mammographiques</h2>
              <Button variant="ghost" size="sm" onClick={() => setShowImagesModal(false)}>
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-2 gap-4">
                {analysis.original_files && analysis.original_files.length > 0 ? (
                  analysis.original_files.map((fileInfo: any, i: number) => {
                    const viewParts = fileInfo.view_type.split('_');
                    const view = viewParts[0] || 'UNKNOWN';
                    const side = viewParts[1] || '';
                    
                    return (
                      <div key={i} className="aspect-square bg-muted rounded-lg relative overflow-hidden">
                        <img 
                          src={`${apiUrl}/mammography/image/${fileInfo.path}`}
                          alt={`Mammographie ${fileInfo.view_type}`}
                          className="w-full h-full object-contain cursor-pointer hover:scale-105 transition-transform"
                          onClick={() => window.open(`${apiUrl}/mammography/image/${fileInfo.path}`, '_blank')}
                          onError={(e) => {
                            const target = e.target as HTMLImageElement;
                            target.style.display = 'none';
                            const parent = target.parentElement;
                            if (parent) {
                              parent.innerHTML = `
                                <div class="flex items-center justify-center h-full">
                                  <div class="text-center">
                                    <svg class="w-16 h-16 text-muted-foreground mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                    </svg>
                                    <p class="text-sm text-muted-foreground">Image non disponible</p>
                                  </div>
                                </div>
                              `;
                            }
                          }}
                        />
                        <div className="absolute top-3 left-3">
                          <Badge variant={side === 'LEFT' ? 'default' : 'secondary'}>
                            {view} {side}
                          </Badge>
                        </div>
                      </div>
                    );
                  })
                ) : (
                  <div className="col-span-2 text-center text-muted-foreground p-8">
                    Aucune image disponible
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
