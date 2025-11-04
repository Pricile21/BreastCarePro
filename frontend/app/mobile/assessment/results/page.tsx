"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { AlertCircle, Calendar, MapPin, BookOpen, CheckCircle, Loader2, Shield, TrendingUp } from "lucide-react"
import { apiClient } from "@/lib/api"

function getRiskLevelInfo(riskCategory: string) {
  const categoryMap: Record<string, any> = {
    'Faible': {
      level: "faible",
      color: "text-green-600",
      bgColor: "bg-green-50",
      borderColor: "border-green-200",
    },
    'Modéré': {
      level: "modéré",
      color: "text-yellow-600",
      bgColor: "bg-yellow-50",
      borderColor: "border-yellow-200",
    },
    'Élevé': {
      level: "élevé",
      color: "text-orange-600",
      bgColor: "bg-orange-50",
      borderColor: "border-orange-200",
    },
    'Très élevé': {
      level: "très élevé",
      color: "text-red-600",
      bgColor: "bg-red-50",
      borderColor: "border-red-200",
    },
  }

  return categoryMap[riskCategory] || categoryMap['Faible']
}

export default function AssessmentResultsPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [riskData, setRiskData] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // Check if user is authenticated and has the right user type
  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
    if (!token) {
      router.push('/mobile/login?redirect=/mobile/assessment')
      return
    }
    
    // Vérifier le type d'utilisateur pour bloquer les admins et professionnels
    const checkUserType = async () => {
      try {
        const userData = await apiClient.getCurrentUser()
        
        // Bloquer les admins
        if (userData.user_type === 'admin') {
          console.log('🚫 Admin détecté sur page résultats mobile - Redirection')
          localStorage.removeItem('auth_token')
          window.location.href = '/admin/login'
          return
        }
        
        // Bloquer les professionnels
        if (userData.user_type === 'professional') {
          console.log('🚫 Professionnel détecté sur page résultats mobile - Redirection')
          localStorage.removeItem('auth_token')
          window.location.href = '/professional/login'
          return
        }
        
        // Si l'utilisateur est valide (patient ou aucun type spécifique), autoriser l'accès
        setIsAuthenticated(true)
      } catch (err) {
        console.error('Erreur lors de la vérification du type d\'utilisateur:', err)
        // En cas d'erreur, rediriger vers la page de login
        router.push('/mobile/login?redirect=/mobile/assessment')
      }
    }
    
    checkUserType()
  }, [router])

  useEffect(() => {
    if (!isAuthenticated) return
    
    const loadRiskAssessment = async () => {
      try {
        const storedData = sessionStorage.getItem('riskAssessmentData')
        if (!storedData) {
          router.push('/mobile/assessment')
          return
        }

        const riskDataInput = JSON.parse(storedData)
        // Utiliser calculateAndSaveRiskAssessment pour sauvegarder automatiquement
        const result = await apiClient.calculateAndSaveRiskAssessment(riskDataInput)
        setRiskData(result)
        // Nettoyer sessionStorage après sauvegarde
        sessionStorage.removeItem('riskAssessmentData')
        console.log('✅ Évaluation calculée et sauvegardée avec succès')
      } catch (err: any) {
        console.error('Erreur lors du calcul du risque:', err)
        // Améliorer l'affichage des erreurs
        let errorMessage = 'Une erreur est survenue lors du calcul du risque'
        if (err.message) {
          errorMessage = err.message
        } else if (typeof err === 'object' && err !== null) {
          errorMessage = JSON.stringify(err)
        }
        setError(errorMessage)
      } finally {
        setLoading(false)
      }
    }

    loadRiskAssessment()
  }, [router, isAuthenticated])

  if (!isAuthenticated) {
    return null
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4 text-primary" />
          <p className="text-muted-foreground">Calcul en cours...</p>
        </div>
      </div>
    )
  }

  if (error || !riskData) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="max-w-md p-6">
          <h2 className="text-xl font-bold mb-4">Erreur</h2>
          <p className="text-destructive mb-4">{error || 'Impossible de calculer le risque'}</p>
          <Button asChild className="w-full">
            <Link href="/mobile/assessment">Réessayer</Link>
          </Button>
        </div>
      </div>
    )
  }

  const riskInfo = getRiskLevelInfo(riskData.risk_category)

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-white/95 backdrop-blur-lg sticky top-0 z-50 border-b border-border/50 shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Shield className="w-6 h-6 text-primary" />
            <span className="font-bold text-lg">Résultats de l'évaluation</span>
          </div>
          <Button variant="ghost" size="sm" asChild>
            <Link href="/mobile">Retour</Link>
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 max-w-3xl">
        {/* Résultat principal */}
        <div className="text-center mb-8 p-8 bg-gradient-to-br from-primary/10 to-accent/10 rounded-2xl border border-primary/20">
          <Badge className={`${riskInfo.bgColor} ${riskInfo.color} border ${riskInfo.borderColor} mb-4 text-base px-4 py-2`}>
            Niveau de risque: {riskInfo.level}
          </Badge>
          <div className={`text-7xl font-bold ${riskInfo.color} mb-2`}>
            {riskData.risk_5_years?.toFixed(2)}%
          </div>
          <p className="text-muted-foreground text-lg">Risque de développer un cancer du sein dans les 5 prochaines années</p>
          
          {/* Comparaison au risque moyen */}
          {riskData.average_risk_for_age && riskData.risk_relative && (
            <div className="mt-6 p-4 bg-white/80 rounded-xl border border-primary/10">
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Risque moyen</p>
                  <p className="text-2xl font-bold text-foreground">{riskData.average_risk_for_age}%</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Votre position</p>
                  <p className="text-2xl font-bold text-primary flex items-center justify-center gap-1">
                    <TrendingUp className="w-6 h-6" />
                    {riskData.risk_relative}x
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Signification clinique */}
        {riskData.clinical_significance && riskData.significance_explanation && (
          <div className="mb-6 p-5 bg-primary/5 rounded-xl border-l-4 border-primary">
            <p className="font-bold text-primary text-lg mb-2">{riskData.clinical_significance}</p>
            <p className="text-sm text-foreground/80">{riskData.significance_explanation}</p>
          </div>
        )}

        {/* Avertissement génétique */}
        {riskData.warning_message && (
          <div className="mb-6 p-5 bg-orange-50 rounded-xl border-l-4 border-orange-500">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-6 h-6 text-orange-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-bold text-orange-900 mb-1">Avertissement</h3>
                <p className="text-sm text-orange-900">{riskData.warning_message}</p>
              </div>
            </div>
          </div>
        )}

        {/* Recommandations */}
        {riskData.recommendations && riskData.recommendations.length > 0 && (
          <div className="mb-6">
            <div className="flex items-center gap-2 mb-4">
              <CheckCircle className="w-6 h-6 text-primary" />
              <h3 className="font-bold text-xl">Recommandations personnalisées</h3>
            </div>
            <ul className="space-y-3">
              {riskData.recommendations.map((rec: string, index: number) => (
                <li key={index} className="flex items-start gap-3 p-4 bg-white rounded-xl border border-border shadow-sm">
                  <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-xs font-bold text-primary">{index + 1}</span>
                  </div>
                  <p className="text-sm text-foreground flex-1">{rec}</p>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Message éducatif */}
        {riskData.educational_message && riskData.educational_message.length > 0 && (
          <div className="mb-6 p-5 bg-muted/50 rounded-xl">
            <div className="flex items-center gap-2 mb-3">
              <BookOpen className="w-5 h-5 text-primary" />
              <h3 className="font-bold">Comprendre votre résultat</h3>
            </div>
            <div className="space-y-2">
              {riskData.educational_message.map((msg: string, index: number) => (
                <p key={index} className="text-sm text-foreground/80 leading-relaxed">{msg}</p>
              ))}
            </div>
          </div>
        )}

        {/* Avertissements critiques */}
        {riskData.critical_warnings && riskData.critical_warnings.length > 0 && (
          <div className="mb-6 p-5 bg-red-50 rounded-xl border-l-4 border-red-500">
            <div className="flex items-center gap-2 mb-3">
              <AlertCircle className="w-6 h-6 text-red-600" />
              <h3 className="font-bold text-red-900">Avertissements importants</h3>
            </div>
            <ul className="space-y-2">
              {riskData.critical_warnings.map((warning: string, index: number) => (
                <li key={index} className="text-sm text-red-900 flex items-start gap-2">
                  <span className="text-red-600 mt-1">•</span>
                  <span>{warning}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Informations techniques */}
        <div className="mb-6 p-4 bg-muted/30 rounded-xl text-sm text-muted-foreground">
          {riskData.model_used && <p><strong>Modèle utilisé:</strong> {riskData.model_used}</p>}
          {riskData.estimated_accuracy && <p className="mt-1"><strong>Précision estimée:</strong> {riskData.estimated_accuracy}</p>}
          {riskData.disclaimer && <p className="mt-3 pt-3 border-t border-border italic">{riskData.disclaimer}</p>}
        </div>

        {/* Actions rapides */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <Button variant="outline" className="h-auto p-6 flex-col gap-2" asChild>
            <Link href="/mobile/providers">
              <MapPin className="w-6 h-6 text-primary" />
              <div>
                <span className="block font-semibold">Centres</span>
                <span className="text-xs text-muted-foreground">de dépistage</span>
              </div>
            </Link>
          </Button>
          <Button variant="outline" className="h-auto p-6 flex-col gap-2" asChild>
            <Link href="/mobile/booking">
              <Calendar className="w-6 h-6 text-primary" />
              <div>
                <span className="block font-semibold">Rendez-vous</span>
                <span className="text-xs text-muted-foreground">Réserver en ligne</span>
              </div>
            </Link>
          </Button>
          <Button variant="outline" className="h-auto p-6 flex-col gap-2" asChild>
            <Link href="/mobile/education">
              <BookOpen className="w-6 h-6 text-primary" />
              <div>
                <span className="block font-semibold">Ressources</span>
                <span className="text-xs text-muted-foreground">En savoir plus</span>
              </div>
            </Link>
          </Button>
        </div>

        {/* Actions finales */}
        <div className="flex gap-4">
          <Button variant="outline" asChild className="flex-1">
            <Link href="/mobile/assessment">Refaire l'évaluation</Link>
          </Button>
          <Button asChild className="flex-1 bg-primary hover:bg-primary/90">
            <Link href="/mobile">Retour à l'accueil</Link>
          </Button>
        </div>
      </main>
    </div>
  )
}
