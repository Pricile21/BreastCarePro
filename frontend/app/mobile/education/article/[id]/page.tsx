"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { ArrowLeft, Clock, FileText } from "lucide-react"
import { use, useEffect, useState } from "react"
import styles from "./page.module.css"

interface Article {
  id: string
  title: string
  description: string
  reading_time: number
  metadata: {
    category: string
    tags: string[]
    author?: string
    publish_date?: string
  }
  introduction: string
  sections: Array<{
    title: string
    content?: string
    bullet_points?: string[]
    ordered_list?: string[]
    subsections?: Array<{
      title: string
      content?: string
      bullet_points?: string[]
      ordered_list?: string[]
    }>
  }>
  conclusion?: string
  disclaimer?: string
  sources?: string[]
}

export default function ArticlePage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params)
  const [article, setArticle] = useState<Article | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        setLoading(true)
        setError(null)
        
        // Mapper les titres vers les IDs d'articles depuis le backend
        const articleIdMap: Record<string, string> = {
          "Qu'est-ce que le cancer du sein?": "quest-ce-que-le-cancer-du-sein",
          "Facteurs de risque du cancer du sein": "facteurs-de-risque",
          "Nutrition et prévention": "nutrition-prevention",
        }

        // Décoder l'ID si c'est un titre encodé
        const decodedId = decodeURIComponent(resolvedParams.id)
        console.log("Original ID:", resolvedParams.id)
        console.log("Decoded ID:", decodedId)
        
        const articleId = articleIdMap[decodedId] || articleIdMap[resolvedParams.id] || decodedId
        console.log("Mapped Article ID:", articleId)

        // Utiliser la configuration API
        const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"
        // API_BASE contient déjà /api/v1, ne pas le rajouter
        const apiUrl = API_BASE.includes('/api/v1') 
          ? `${API_BASE}/articles/${articleId}`
          : `${API_BASE}/api/v1/articles/${articleId}`
        console.log("Fetching from:", apiUrl)
        
        const response = await fetch(apiUrl)
        
        console.log("Response status:", response.status)
        
        if (!response.ok) {
          const errorText = await response.text()
          console.error("API Error:", errorText)
          throw new Error(`Article non trouvé (${response.status}): ${errorText.substring(0, 100)}`)
        }

        const data = await response.json()
        console.log("Article data received:", data)
        
        if (!data.article) {
          throw new Error("Format de réponse API invalide")
        }
        
        setArticle(data.article)
        setError(null)
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : "Erreur lors du chargement"
        setError(errorMessage)
        console.error("Error fetching article:", err)
      } finally {
        setLoading(false)
      }
    }

    fetchArticle()
  }, [resolvedParams.id])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background via-primary/5 to-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Chargement de l'article...</p>
        </div>
      </div>
    )
  }

  if (error || !article) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background via-primary/5 to-background">
        <header className="border-b bg-white/80 backdrop-blur-lg sticky top-0 z-50 shadow-sm">
          <div className="container mx-auto px-4 py-4 flex items-center justify-between max-w-7xl">
            <Button variant="ghost" size="sm" className="hover:bg-primary/10" asChild>
              <Link href="/mobile/education">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Retour
              </Link>
            </Button>
          </div>
        </header>
        <main className="container mx-auto px-4 py-12 max-w-4xl">
          <Card className="p-8 text-center">
            <h2 className="text-2xl font-bold mb-4">Article non trouvé</h2>
            <p className="text-muted-foreground mb-6">{error || "L'article demandé n'existe pas."}</p>
            <Button asChild>
              <Link href="/mobile/education">Retour aux articles</Link>
            </Button>
          </Card>
        </main>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-primary/5 to-background">
      <header className="border-b bg-white/80 backdrop-blur-lg sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between max-w-7xl">
          <Button variant="ghost" size="sm" className="hover:bg-primary/10" asChild>
            <Link href="/mobile/education">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Retour
            </Link>
          </Button>
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-primary" />
            <span className="font-bold text-lg">Article</span>
          </div>
          <div className="w-20" />
        </div>
      </header>

      <main className={`container mx-auto px-4 py-12 max-w-4xl ${styles.noCheckmarks}`}>
        {/* Header de l'article */}
        <div className="mb-12">
          <div className="flex items-center gap-2 text-sm text-muted-foreground mb-4">
            <span className="uppercase font-semibold">{article.metadata.category}</span>
            <span>•</span>
            <div className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              <span>{article.reading_time} min</span>
            </div>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{article.title}</h1>
          <p className="text-xl text-muted-foreground leading-relaxed">{article.description}</p>
        </div>

        {/* Introduction */}
        <Card className="mb-8 p-8 bg-gradient-to-br from-primary/5 to-accent/5 border-0 shadow-lg">
          <p className="text-lg leading-relaxed">{article.introduction}</p>
        </Card>

        {/* Sections */}
        <div className="space-y-8">
          {article.sections.map((section, sectionIndex) => (
            <Card key={sectionIndex} className="border-0 shadow-lg overflow-hidden">
              <CardContent className="p-8">
                <h2 className="text-2xl font-bold mb-6 text-primary">{section.title}</h2>
                
                {section.content && section.content.trim() && (
                  <p className="text-base leading-relaxed mb-6 text-foreground whitespace-pre-line">
                    {section.content}
                  </p>
                )}

                {section.bullet_points && (
                  <ul className="space-y-3 mb-6" style={{ listStyle: 'none', paddingLeft: 0, marginLeft: 0 }}>
                    {section.bullet_points.map((point, idx) => (
                      <li key={idx} className="text-base leading-relaxed" style={{ 
                        listStyle: 'none', 
                        paddingLeft: 0,
                        marginLeft: 0,
                        position: 'relative',
                        display: 'flex',
                        alignItems: 'flex-start'
                      }}>
                        <span className="mr-2" style={{ color: 'inherit' }}>-</span>
                        <span>{point.replace(/^[-•✓✅]\s*/, '').trim()}</span>
                      </li>
                    ))}
                  </ul>
                )}

                {section.ordered_list && (
                  <ol className="space-y-3 mb-6 list-decimal list-inside">
                    {section.ordered_list.map((item, idx) => (
                      <li key={idx} className="text-base leading-relaxed pl-2">
                        {item}
                      </li>
                    ))}
                  </ol>
                )}

                {section.subsections && section.subsections.length > 0 && (
                  <div className="space-y-6 mt-6">
                    {section.subsections.map((subsection, subIndex) => (
                      <div key={subIndex} className="ml-4 border-l-2 border-primary/20 pl-6">
                        <h3 className="text-xl font-semibold mb-4">{subsection.title}</h3>
                        
                        {subsection.content && (
                          <p className="text-base leading-relaxed mb-4 text-muted-foreground whitespace-pre-line">
                            {subsection.content}
                          </p>
                        )}

                        {subsection.bullet_points && (
                          <ul className="space-y-2 mb-4" style={{ listStyle: 'none', paddingLeft: 0, marginLeft: 0 }}>
                            {subsection.bullet_points.map((point, idx) => (
                              <li key={idx} className="text-sm leading-relaxed" style={{ 
                                listStyle: 'none', 
                                paddingLeft: 0,
                                marginLeft: 0,
                                position: 'relative',
                                display: 'flex',
                                alignItems: 'flex-start'
                              }}>
                                <span className="mr-2" style={{ color: 'inherit' }}>-</span>
                                <span>{point.replace(/^[-•✓✅]\s*/, '').trim()}</span>
                              </li>
                            ))}
                          </ul>
                        )}

                        {subsection.ordered_list && (
                          <ol className="space-y-2 mb-4 list-decimal list-inside">
                            {subsection.ordered_list.map((item, idx) => (
                              <li key={idx} className="text-sm leading-relaxed pl-2">
                                {item}
                              </li>
                            ))}
                          </ol>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Conclusion */}
        {article.conclusion && (
          <Card className="mt-8 p-8 bg-gradient-to-br from-primary/10 to-accent/10 border-0 shadow-lg">
            <h2 className="text-2xl font-bold mb-4">Conclusion</h2>
            <div className="text-base leading-relaxed whitespace-pre-line">{article.conclusion}</div>
          </Card>
        )}

        {/* Disclaimer */}
        {article.disclaimer && (
          <Card className="mt-8 p-6 bg-yellow-50 border border-yellow-200">
            <p className="text-sm text-yellow-900 leading-relaxed">{article.disclaimer}</p>
          </Card>
        )}

        {/* Sources */}
        {article.sources && article.sources.length > 0 && (
          <Card className="mt-8 p-6 border-0 shadow-md">
            <h3 className="font-semibold mb-3">Sources</h3>
            <ul className="space-y-1 text-sm text-muted-foreground">
              {article.sources.map((source, idx) => (
                <li key={idx}>• {source}</li>
              ))}
            </ul>
          </Card>
        )}

        {/* Bouton retour */}
        <div className="mt-12 flex justify-center">
          <Button size="lg" className="rounded-2xl px-8" asChild>
            <Link href="/mobile/education">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Retour aux articles
            </Link>
          </Button>
        </div>
      </main>
    </div>
  )
}

