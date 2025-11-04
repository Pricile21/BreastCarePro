"use client"

import { useEffect } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Heart, MapPin, Calendar, BookOpen, Shield, ArrowRight, User } from "lucide-react"
import Image from "next/image"
import { useAuth } from "@/contexts/auth-context"
import { useRouter } from "next/navigation"

export default function MobileHomePage() {
  const { isAuthenticated, user, checkAuth, loading } = useAuth()
  const router = useRouter()

  // Vérifier l'authentification au montage et lors du changement de route
  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
    if (token && !isAuthenticated && !loading) {
      checkAuth()
    }
  }, [isAuthenticated, loading, checkAuth])

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-white/95 backdrop-blur-lg sticky top-0 z-50 border-b border-border/50 shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between max-w-7xl">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-primary via-primary to-accent flex items-center justify-center shadow-lg">
              <Heart className="w-6 h-6 text-white fill-white" />
            </div>
            <div>
              <span className="font-bold text-xl bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent block leading-none">
                BreastCare
              </span>
              <span className="text-xs text-muted-foreground">Pro</span>
            </div>
          </div>
          {isAuthenticated ? (
            <Button
              variant="ghost"
              size="sm"
              className="text-primary hover:text-primary hover:bg-primary/10 font-medium"
              onClick={() => router.push('/mobile/dashboard')}
            >
              <User className="w-4 h-4 mr-2" />
              Profil
            </Button>
          ) : (
            <Button
              variant="ghost"
              size="sm"
              className="text-primary hover:text-primary hover:bg-primary/10 font-medium"
              asChild
            >
              <Link href="/mobile/login">Connexion</Link>
            </Button>
          )}
        </div>
      </header>

      <main>
        <section className="relative h-[90vh] min-h-[600px] overflow-hidden">
          <div className="absolute inset-0 bg-primary/60 z-10" />
          <div className="absolute inset-0 bg-black/10 z-10" />
          <Image 
            src="/african-woman-hero-empowered-confident.jpg" 
            alt="Hero" 
            fill 
            className="object-cover brightness-90 contrast-110 saturate-110" 
            priority 
          />
          <div className="relative z-20 container mx-auto px-4 h-full flex flex-col justify-center max-w-7xl">
            <div className="max-w-3xl">
              <h1 className="text-6xl md:text-7xl font-bold text-white mb-6 leading-[1.1] text-balance drop-shadow-2xl">
                Votre santé mammaire,
                <br />
                notre priorité
              </h1>
              <p className="text-2xl text-white/95 mb-10 leading-relaxed text-balance drop-shadow-lg max-w-2xl">
                Dépistage précoce, technologie avancée et accompagnement personnalisé pour toutes les femmes
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Button
                  size="lg"
                  className="bg-white text-primary hover:bg-white/90 shadow-2xl text-lg h-16 px-10 rounded-2xl font-semibold"
                  asChild
                >
                  <Link href="/mobile/assessment">
                    Évaluer mes risques
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Link>
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="border-2 border-white text-white hover:bg-white hover:text-primary text-lg h-16 px-10 rounded-2xl bg-white/10 backdrop-blur-sm font-semibold"
                  asChild
                >
                  <Link href="/mobile/providers">Trouver un centre</Link>
                </Button>
              </div>
            </div>
          </div>
        </section>

        <section className="py-24 container mx-auto px-4 max-w-7xl">
          <div className="text-center mb-20">
            <div className="inline-block px-4 py-2 bg-primary/10 rounded-full mb-4">
              <span className="text-primary font-semibold text-sm">COMMENT ÇA MARCHE</span>
            </div>
            <h2 className="text-5xl font-bold mb-6 text-balance">Trois étapes simples</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-balance leading-relaxed">
              Prenez soin de votre santé en quelques clics
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="overflow-hidden border-0 shadow-xl hover:shadow-2xl transition-all group bg-gradient-to-br from-white to-primary/5">
              <div className="relative h-64 overflow-hidden">
                <Image
                  src="/african-woman-mobile-health-app.jpg"
                  alt="Assessment"
                  fill
                  className="object-cover group-hover:scale-110 transition-transform duration-500 brightness-90 contrast-110 saturate-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />
                <div className="absolute bottom-4 left-4 right-4">
                  <div className="w-14 h-14 rounded-2xl bg-white shadow-lg flex items-center justify-center mb-3">
                    <Shield className="w-7 h-7 text-primary" />
                  </div>
                </div>
              </div>
              <CardContent className="p-8">
                <div className="text-primary font-bold text-sm mb-2">ÉTAPE 1</div>
                <h3 className="text-2xl font-bold mb-3">Évaluez vos risques</h3>
                <p className="text-muted-foreground mb-6 leading-relaxed">
                  Répondez à un questionnaire personnalisé pour connaître votre niveau de risque en quelques minutes
                </p>
                <Button variant="link" className="text-primary p-0 h-auto font-semibold group/btn" asChild>
                  <Link href="/mobile/assessment">
                    Commencer l'évaluation
                    <ArrowRight className="ml-2 h-4 w-4 group-hover/btn:translate-x-1 transition-transform" />
                  </Link>
                </Button>
              </CardContent>
            </Card>

            <Card className="overflow-hidden border-0 shadow-xl hover:shadow-2xl transition-all group bg-gradient-to-br from-white to-accent/5">
              <div className="relative h-64 overflow-hidden">
                <Image
                  src="/modern-medical-clinic-building-healthcare-center-a.jpg"
                  alt="Find Center"
                  fill
                  className="object-cover group-hover:scale-110 transition-transform duration-500 brightness-95 contrast-105"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />
                <div className="absolute bottom-4 left-4 right-4">
                  <div className="w-14 h-14 rounded-2xl bg-white shadow-lg flex items-center justify-center mb-3">
                    <MapPin className="w-7 h-7 text-accent" />
                  </div>
                </div>
              </div>
              <CardContent className="p-8">
                <div className="text-accent font-bold text-sm mb-2">ÉTAPE 2</div>
                <h3 className="text-2xl font-bold mb-3">Trouvez un centre</h3>
                <p className="text-muted-foreground mb-6 leading-relaxed">
                  Localisez les centres de dépistage certifiés près de chez vous avec notre carte interactive
                </p>
                <Button variant="link" className="text-primary p-0 h-auto font-semibold group/btn" asChild>
                  <Link href="/mobile/providers">
                    Voir la carte
                    <ArrowRight className="ml-2 h-4 w-4 group-hover/btn:translate-x-1 transition-transform" />
                  </Link>
                </Button>
              </CardContent>
            </Card>

            <Card className="overflow-hidden border-0 shadow-xl hover:shadow-2xl transition-all group bg-gradient-to-br from-white to-primary/5">
              <div className="relative h-64 overflow-hidden">
                <Image
                  src="/african-doctor-woman-consultation.jpg"
                  alt="Book Appointment"
                  fill
                  className="object-cover group-hover:scale-110 transition-transform duration-500 brightness-90 contrast-110 saturate-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />
                <div className="absolute bottom-4 left-4 right-4">
                  <div className="w-14 h-14 rounded-2xl bg-white shadow-lg flex items-center justify-center mb-3">
                    <Calendar className="w-7 h-7 text-primary" />
                  </div>
                </div>
              </div>
              <CardContent className="p-8">
                <div className="text-primary font-bold text-sm mb-2">ÉTAPE 3</div>
                <h3 className="text-2xl font-bold mb-3">Prenez rendez-vous</h3>
                <p className="text-muted-foreground mb-6 leading-relaxed">
                  Réservez votre consultation en ligne en quelques clics et recevez une confirmation immédiate
                </p>
                <Button variant="link" className="text-primary p-0 h-auto font-semibold group/btn" asChild>
                  <Link href="/mobile/booking">
                    Réserver maintenant
                    <ArrowRight className="ml-2 h-4 w-4 group-hover/btn:translate-x-1 transition-transform" />
                  </Link>
                </Button>
              </CardContent>
            </Card>
          </div>
        </section>

        <section className="py-24 bg-gradient-to-br from-primary via-primary to-accent relative overflow-hidden">
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-0 left-1/4 w-96 h-96 bg-white rounded-full blur-3xl animate-pulse" />
            <div
              className="absolute bottom-0 right-1/4 w-96 h-96 bg-white rounded-full blur-3xl animate-pulse"
              style={{ animationDelay: "1s" }}
            />
          </div>
          <div className="container mx-auto px-4 max-w-7xl relative z-10">
            <div className="text-center mb-16">
              <h2 className="text-5xl font-bold text-white mb-6">Le dépistage sauve des vies</h2>
              <p className="text-2xl text-white/90 max-w-3xl mx-auto">Des chiffres qui parlent d'eux-mêmes</p>
            </div>
            <div className="grid md:grid-cols-3 gap-12">
              <div className="text-center">
                <div className="text-7xl font-bold text-white mb-4 drop-shadow-lg">90%</div>
                <p className="text-white/95 text-xl font-medium">Taux de guérison avec détection précoce</p>
              </div>
              <div className="text-center">
                <div className="text-7xl font-bold text-white mb-4 drop-shadow-lg">50+</div>
                <p className="text-white/95 text-xl font-medium">Centres partenaires disponibles</p>
              </div>
              <div className="text-center">
                <div className="text-7xl font-bold text-white mb-4 drop-shadow-lg">24/7</div>
                <p className="text-white/95 text-xl font-medium">Plateforme accessible à tout moment</p>
              </div>
            </div>
          </div>
        </section>

        <section className="py-24 container mx-auto px-4 max-w-7xl">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div className="order-2 md:order-1">
              <div className="inline-flex items-center gap-2 bg-primary/10 px-4 py-2 rounded-full mb-6">
                <BookOpen className="w-4 h-4 text-primary" />
                <span className="text-primary text-sm font-semibold">RESSOURCES ÉDUCATIVES</span>
              </div>
              <h2 className="text-5xl font-bold mb-6 text-balance leading-tight">Informez-vous, protégez-vous</h2>
              <p className="text-xl text-muted-foreground mb-8 leading-relaxed">
                Accédez à une bibliothèque complète d'articles, vidéos et guides pratiques sur la santé mammaire, le
                dépistage et la prévention du cancer du sein.
              </p>
              <ul className="space-y-6 mb-10">
                <li className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <Heart className="w-6 h-6 text-primary fill-primary" />
                  </div>
                  <div>
                    <p className="font-bold text-lg mb-1">Auto-examen mensuel</p>
                    <p className="text-muted-foreground">Apprenez les gestes qui sauvent avec nos vidéos tutoriels</p>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <Heart className="w-6 h-6 text-primary fill-primary" />
                  </div>
                  <div>
                    <p className="font-bold text-lg mb-1">Facteurs de risque</p>
                    <p className="text-muted-foreground">Comprenez votre profil de santé personnalisé</p>
                  </div>
                </li>
                <li className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <Heart className="w-6 h-6 text-primary fill-primary" />
                  </div>
                  <div>
                    <p className="font-bold text-lg mb-1">Témoignages inspirants</p>
                    <p className="text-muted-foreground">Des histoires de courage et d'espoir de femmes africaines</p>
                  </div>
                </li>
              </ul>
              <Button
                size="lg"
                className="bg-primary hover:bg-primary/90 h-14 px-8 text-lg rounded-2xl shadow-lg"
                asChild
              >
                <Link href="/mobile/education">
                  Explorer les ressources
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
            </div>
            <div className="order-1 md:order-2 relative">
              <div className="relative h-[600px] rounded-3xl overflow-hidden shadow-2xl">
                <Image 
                  src="/african-women-community-support-group.jpg" 
                  alt="Education" 
                  fill 
                  className="object-cover brightness-90 contrast-110 saturate-110" 
                />
              </div>
              <div className="absolute -bottom-6 -left-6 w-32 h-32 bg-accent rounded-3xl opacity-20 blur-2xl" />
              <div className="absolute -top-6 -right-6 w-32 h-32 bg-primary rounded-3xl opacity-20 blur-2xl" />
            </div>
          </div>
        </section>

        <section className="py-24">
          <div className="container mx-auto px-4 max-w-7xl">
            <Card className="overflow-hidden border-0 shadow-2xl rounded-3xl">
              <div className="relative h-[700px] min-h-[700px]">
                <div className="absolute inset-0 bg-gradient-to-br from-primary/90 via-primary/85 to-accent/90 z-10" />
                <Image
                  src="/african-woman-confident-empowered-healthcare-welln.jpg"
                  alt="CTA"
                  fill
                  className="object-cover object-[center_top] brightness-90 contrast-110 saturate-110"
                  style={{ objectPosition: 'center top' }}
                />
                <CardContent className="relative z-20 p-16 text-left flex flex-col justify-center h-full max-w-2xl">
                <h2 className="text-5xl font-bold text-white mb-6 text-balance leading-tight">
                  Prenez votre santé en main dès aujourd'hui
                </h2>
                <p className="text-2xl text-white/95 mb-10 text-balance leading-relaxed">
                  Rejoignez des milliers de femmes qui ont fait le choix de la prévention
                </p>
                <div className="flex flex-col sm:flex-row gap-4">
                  <Button
                    size="lg"
                    className="bg-white text-primary hover:bg-white/90 text-lg h-16 px-10 rounded-2xl shadow-xl font-semibold"
                    asChild
                  >
                    <Link href="/mobile/assessment">Commencer maintenant</Link>
                  </Button>
                  {!isAuthenticated && (
                    <Button
                      size="lg"
                      variant="outline"
                      className="border-2 border-white text-white hover:bg-white hover:text-primary text-lg h-16 px-10 rounded-2xl bg-white/10 backdrop-blur-sm font-semibold"
                      asChild
                    >
                      <Link href="/mobile/signup">Créer un compte</Link>
                    </Button>
                  )}
                  {isAuthenticated && (
                    <Button
                      size="lg"
                      variant="outline"
                      className="border-2 border-white text-white hover:bg-white hover:text-primary text-lg h-16 px-10 rounded-2xl bg-white/10 backdrop-blur-sm font-semibold"
                      asChild
                    >
                      <Link href="/mobile/dashboard">Mon espace</Link>
                    </Button>
                  )}
                </div>
              </CardContent>
              </div>
            </Card>
          </div>
        </section>
      </main>

      <footer className="bg-gradient-to-br from-primary/25 via-accent/25 to-primary/30 border-t border-primary/30 py-16">
        <div className="container mx-auto px-4 max-w-7xl">
          <div className="grid md:grid-cols-4 gap-12 mb-12">
            <div>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg">
                  <Heart className="w-6 h-6 text-white fill-white" />
                </div>
                <div>
                  <span className="font-bold text-xl bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent block leading-none">
                    BreastCare
                  </span>
                  <span className="text-xs text-foreground/70">Pro</span>
                </div>
              </div>
              <p className="text-sm text-foreground/80 leading-relaxed">
                Plateforme de dépistage du cancer du sein
              </p>
            </div>
            <div>
              <h3 className="font-bold mb-4 text-lg text-foreground">Services</h3>
              <ul className="space-y-3 text-sm text-foreground/80">
                <li>
                  <Link href="/mobile/assessment" className="hover:text-primary transition-colors">
                    Évaluation des risques
                  </Link>
                </li>
                <li>
                  <Link href="/mobile/providers" className="hover:text-primary transition-colors">
                    Trouver un centre
                  </Link>
                </li>
                <li>
                  <Link href="/mobile/booking" className="hover:text-primary transition-colors">
                    Prendre rendez-vous
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-4 text-lg text-foreground">Ressources</h3>
              <ul className="space-y-3 text-sm text-foreground/80">
                <li>
                  <Link href="/mobile/education" className="hover:text-primary transition-colors">
                    Éducation
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-4 text-lg text-foreground">Contact</h3>
              <ul className="space-y-3 text-sm text-foreground/80">
                <li>Support disponible 24/7</li>
                <li>contact@breastcare.com</li>
                <li>Support téléphonique disponible</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-primary/20 pt-8 text-center text-sm text-foreground/70">
            <p>© 2025 BreastCare Pro. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
