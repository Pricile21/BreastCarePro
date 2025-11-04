"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Heart, ArrowLeft, BookOpen, Video, FileText, Play, Clock } from "lucide-react"
import Image from "next/image"
import { useState } from "react"
import { VideoPlayerModal } from "@/components/video-player-modal"

export default function EducationPage() {
  const [selectedVideo, setSelectedVideo] = useState<{ url: string; title: string } | null>(null)

  const resources = [
    {
      title: "Qu'est-ce que le cancer du sein?",
      description: "Comprendre les bases du cancer du sein, ses différentes formes et comment il se développe",
      type: "article",
      duration: "5 min",
      image: "/african-woman-self-examination-education.jpg",
    },
    {
      title: "Facteurs de risque du cancer du sein",
      description: "Les facteurs qui augmentent le risque de cancer du sein et comment les gérer",
      type: "article",
      duration: "6 min",
      image: "/african-doctor-woman-consultation.jpg",
    },
    {
      title: "Importance du dépistage précoce",
      description: "Pourquoi la détection précoce sauve des vies - statistiques et témoignages",
      type: "video",
      duration: "10 min",
      image: "/african-women-community-support-group.jpg",
      videoUrl: "https://www.youtube.com/embed/OUbVI0460PQ",
    },
    {
      title: "Témoignages de survivantes africaines",
      description: "Histoires inspirantes de femmes africaines qui ont vaincu le cancer du sein",
      type: "video",
      duration: "12 min",
      image: "/african-women-community-support-group.jpg",
      videoUrl: "https://www.youtube.com/embed/XIPJtwYjtzo",
    },
    {
      title: "Nutrition et prévention",
      description: "L'alimentation et le mode de vie pour réduire les risques de cancer du sein",
      type: "article",
      duration: "7 min",
      image: "/african-women-wellness-yoga-exercise.jpg",
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-primary/5 to-background">
      <VideoPlayerModal
        isOpen={!!selectedVideo && !!selectedVideo.url}
        onClose={() => setSelectedVideo(null)}
        videoUrl={selectedVideo?.url || ""}
        title={selectedVideo?.title || "Vidéo"}
      />

      <header className="border-b bg-white/80 backdrop-blur-lg sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between max-w-7xl">
          <Button variant="ghost" size="sm" className="hover:bg-primary/10" asChild>
            <Link href="/mobile">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Retour
            </Link>
          </Button>
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-primary" />
            <span className="font-bold text-lg">Éducation</span>
          </div>
          <div className="w-20" />
        </div>
      </header>

      <main className="container mx-auto px-4 py-12 max-w-7xl">
        <div className="mb-16 relative">
          <div className="relative h-80 rounded-3xl overflow-hidden mb-8 shadow-2xl">
            <div className="absolute inset-0 bg-gradient-to-br from-primary/90 to-accent/90 z-10" />
            <Image
              src="/african-women-community-support-group.jpg"
              alt="Education Hero"
              fill
              className="object-cover"
            />
            <div className="relative z-20 h-full flex flex-col justify-center items-center text-center px-4">
              <div className="inline-flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full mb-4">
                <BookOpen className="w-4 h-4 text-white" />
                <span className="text-white text-sm font-semibold">RESSOURCES ÉDUCATIVES</span>
              </div>
              <h1 className="text-5xl font-bold text-white mb-4 text-balance">Informez-vous, protégez-vous</h1>
              <p className="text-xl text-white/90 max-w-2xl text-balance">
                Articles, vidéos et guides pratiques sur la santé mammaire
              </p>
            </div>
          </div>
        </div>

        <Card className="mb-12 border-0 shadow-2xl overflow-hidden rounded-3xl bg-gradient-to-br from-primary/5 to-accent/5">
          <div className="grid md:grid-cols-2 gap-0">
            <div className="relative h-80 md:h-auto">
              <div
                className="absolute inset-0 bg-black/40 z-10 flex items-center justify-center group cursor-pointer hover:bg-black/30 transition-colors"
                onClick={() =>
                  setSelectedVideo({
                    url: "https://www.youtube.com/embed/l9k_7bKwrvg",
                    title: "Guide complet de l'auto-examen",
                  })
                }
              >
                <div className="w-20 h-20 rounded-full bg-white/90 flex items-center justify-center group-hover:scale-110 transition-transform shadow-2xl">
                  <Play className="w-10 h-10 text-primary ml-1" fill="currentColor" />
                </div>
              </div>
              <Image
                src="/african-woman-self-examination-education.jpg"
                alt="Featured Video"
                fill
                className="object-cover"
              />
            </div>
            <CardContent className="p-10 flex flex-col justify-center">
              <div className="inline-flex items-center gap-2 bg-primary/10 px-3 py-1.5 rounded-full mb-4 w-fit">
                <Video className="w-4 h-4 text-primary" />
                <span className="text-primary text-sm font-semibold">VIDÉO RECOMMANDÉE</span>
              </div>
              <h2 className="text-3xl font-bold mb-4">Guide complet de l'auto-examen</h2>
              <p className="text-lg text-muted-foreground mb-6 leading-relaxed">
                Apprenez les techniques essentielles d'auto-examen des seins avec notre tutoriel vidéo détaillé présenté
                par des professionnels de santé africains.
              </p>
              <div className="flex items-center gap-4 text-sm text-muted-foreground mb-6">
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4" />
                  <span>12 minutes</span>
                </div>
                <span>•</span>
                <span>Français</span>
              </div>
              <Button
                size="lg"
                className="bg-primary hover:bg-primary/90 w-fit rounded-2xl h-12 px-8"
                onClick={() =>
                  setSelectedVideo({
                    url: "https://www.youtube.com/embed/l9k_7bKwrvg",
                    title: "Guide complet de l'auto-examen",
                  })
                }
              >
                Regarder maintenant
              </Button>
            </CardContent>
          </div>
        </Card>

        <div className="mb-12">
          <h2 className="text-3xl font-bold mb-8">Toutes les ressources</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {resources.map((resource, index) => (
              <Link
                key={index}
                href={resource.type === "article" ? `/mobile/education/article/${encodeURIComponent(resource.title)}` : "#"}
                onClick={(e) => {
                  if (resource.type === "video" && resource.videoUrl) {
                    e.preventDefault()
                    setSelectedVideo({ url: resource.videoUrl, title: resource.title })
                  }
                }}
              >
              <Card
                className="overflow-hidden border-0 shadow-lg hover:shadow-2xl transition-all group rounded-2xl cursor-pointer h-full"
              >
                <div className="relative h-56 overflow-hidden">
                  {resource.type === "video" && (
                    <div className="absolute inset-0 bg-black/40 z-10 flex items-center justify-center group-hover:bg-black/30 transition-colors">
                      <div className="w-16 h-16 rounded-full bg-white/90 flex items-center justify-center group-hover:scale-110 transition-transform shadow-xl">
                        <Play className="w-8 h-8 text-primary ml-1" fill="currentColor" />
                      </div>
                    </div>
                  )}
                  <Image
                    src={resource.image || "/placeholder.svg"}
                    alt={resource.title}
                    fill
                    className="object-cover group-hover:scale-110 transition-transform duration-500"
                  />
                </div>
                <CardContent className="p-6">
                  <div className="flex items-center gap-2 mb-3">
                    <div
                      className={`w-8 h-8 rounded-lg ${resource.type === "video" ? "bg-primary/10" : "bg-accent/10"} flex items-center justify-center`}
                    >
                      {resource.type === "video" ? (
                        <Video className="w-4 h-4 text-primary" />
                      ) : (
                        <FileText className="w-4 h-4 text-accent" />
                      )}
                    </div>
                    <span className="text-xs font-semibold text-muted-foreground uppercase">{resource.type}</span>
                    <span className="text-xs text-muted-foreground">• {resource.duration}</span>
                  </div>
                  <h3 className="font-bold text-lg mb-2 leading-tight">{resource.title}</h3>
                  <p className="text-sm text-muted-foreground mb-4 leading-relaxed">{resource.description}</p>
                  <div className="flex items-center text-primary font-semibold group/btn">
                    <span>{resource.type === "video" ? "Regarder" : "Lire l'article"}</span>
                    <ArrowLeft className="ml-2 h-4 w-4 rotate-180 group-hover/btn:translate-x-1 transition-transform" />
                  </div>
                </CardContent>
              </Card>
              </Link>
            ))}
          </div>
        </div>

        <Card className="border-0 shadow-2xl rounded-3xl overflow-hidden bg-gradient-to-br from-primary to-accent">
          <CardContent className="p-12 text-center">
            <Heart className="w-16 h-16 text-white fill-white mx-auto mb-6" />
            <h2 className="text-4xl font-bold text-white mb-4">Besoin d'aide personnalisée?</h2>
            <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
              Nos experts sont là pour répondre à vos questions et vous accompagner
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                size="lg"
                className="bg-white text-primary hover:bg-white/90 h-14 px-8 rounded-2xl font-semibold"
                asChild
              >
                <Link href="/mobile/providers">Trouver un centre</Link>
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="border-2 border-white text-white hover:bg-white hover:text-primary h-14 px-8 rounded-2xl bg-white/10 backdrop-blur-sm font-semibold"
                asChild
              >
                <Link href="/mobile/assessment">Évaluer mes risques</Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
