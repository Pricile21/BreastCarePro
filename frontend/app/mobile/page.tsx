"use client"

import { useEffect } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Heart, MapPin, Calendar, BookOpen, Shield, ArrowRight, User } from "lucide-react"
import Image from "next/image"
import { useAuth } from "@/contexts/auth-context"
import { useRouter } from "next/navigation"
import { AnimateInView } from "@/components/animate-in-view"

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
    <div className="min-h-screen bg-gradient-to-b from-primary/[0.06] via-background to-accent/[0.06]">
      <header className="bg-background/95 backdrop-blur-xl sticky top-0 z-50 border-b border-border/50 shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between max-w-7xl">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-primary via-primary to-accent flex items-center justify-center shadow-lg transition-transform duration-300 hover:scale-105 hover:rotate-3">
              <Heart className="w-6 h-6 text-white fill-white" />
            </div>
            <div>
              <span className="font-bold text-xl text-foreground block leading-none">BreastCare</span>
              <span className="text-xs text-muted-foreground">Pro</span>
            </div>
          </div>
          {isAuthenticated ? (
            <Button
              variant="ghost"
              size="sm"
              className="text-primary hover:bg-primary/10 font-medium"
              onClick={() => router.push('/mobile/dashboard')}
            >
              <User className="w-4 h-4 mr-2" />
              Profil
            </Button>
          ) : (
            <Button
              variant="ghost"
              size="sm"
              className="text-primary hover:bg-primary/10 font-medium"
              asChild
            >
              <Link href="/mobile/login">Connexion</Link>
            </Button>
          )}
        </div>
      </header>

      <main>
        <section className="relative h-[90vh] min-h-[600px] overflow-hidden">
          <Image 
            src="/african-woman-hero-empowered-confident.jpg" 
            alt="Hero" 
            fill 
            className="object-cover brightness-90 contrast-110 saturate-110 transition-transform duration-[20s] ease-out hover:scale-105" 
            priority 
          />
          <div className="absolute inset-0 bg-gradient-to-r from-black/50 via-black/25 to-transparent z-10" />
          <div className="absolute inset-0 bg-gradient-to-r from-primary/55 via-primary/35 to-accent/40 z-10" />
          <div className="absolute bottom-10 right-10 w-72 h-72 bg-white/10 rounded-full blur-3xl animate-float pointer-events-none z-10" />
          <div className="relative z-20 container mx-auto px-4 h-full flex flex-col justify-center max-w-7xl">
            <div className="max-w-3xl">
              <h1 className="text-6xl md:text-7xl font-bold text-white mb-6 leading-[1.1] text-balance drop-shadow-2xl opacity-0 animate-fade-in-up delay-100">
                Votre santé mammaire,
                <br />
                notre priorité
              </h1>
              <p className="text-2xl text-white/95 mb-10 leading-relaxed text-balance drop-shadow-lg max-w-2xl opacity-0 animate-fade-in-up delay-300">
                Dépistage précoce, technologie avancée et accompagnement personnalisé pour toutes les femmes
              </p>
              <div className="flex flex-col sm:flex-row gap-4 opacity-0 animate-fade-in-up delay-500">
                <Button
                  size="lg"
                  className="group bg-gradient-to-r from-primary to-accent text-white hover:opacity-95 shadow-2xl text-lg h-14 px-8 rounded-2xl font-semibold transition-all duration-300 hover:scale-105 hover:shadow-[0_20px_40px_rgba(0,0,0,0.25)] active:scale-100 border-0"
                  asChild
                >
                  <Link href="/mobile/assessment">
                    Évaluer mes risques
                    <ArrowRight className="ml-2 h-5 w-5 inline-block transition-transform duration-200 group-hover:translate-x-1" />
                  </Link>
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="border-2 border-white text-white hover:bg-white/20 text-lg h-14 px-8 rounded-2xl bg-transparent backdrop-blur-sm font-semibold transition-all duration-300 hover:scale-105 active:scale-100"
                  asChild
                >
                  <Link href="/mobile/providers">Trouver un centre</Link>
                </Button>
              </div>
            </div>
          </div>
        </section>

        <section className="py-14 md:py-20 container mx-auto px-4 max-w-7xl relative overflow-hidden">
          {/* Fond coloré et formes décoratives */}
          <div className="absolute inset-0 bg-gradient-to-br from-primary/15 via-primary/5 to-accent/15 pointer-events-none" />
          <div className="absolute top-0 left-1/4 w-80 h-80 bg-primary/20 rounded-full blur-[100px] animate-float pointer-events-none" />
          <div className="absolute bottom-0 right-1/4 w-72 h-72 bg-accent/20 rounded-full blur-[80px] animate-float pointer-events-none" style={{ animationDelay: "1.5s" }} />
          <div className="relative z-10">
          <AnimateInView>
            <div className="text-center mb-10">
              <h2 className="text-4xl md:text-5xl font-bold mb-3 text-balance bg-gradient-to-r from-primary via-primary to-accent bg-clip-text text-transparent animate-gradient-text">
                Trois étapes simples
              </h2>
              <p className="text-lg text-foreground/80 max-w-2xl mx-auto text-balance leading-relaxed font-medium">
                Prenez soin de votre santé en quelques clics
              </p>
            </div>
          </AnimateInView>

          <div className="grid md:grid-cols-3 gap-5 md:gap-6">
            <AnimateInView delay={0}>
              <Card className="overflow-hidden border-0 rounded-2xl border-l-4 border-l-primary shadow-lg shadow-primary/15 hover:shadow-xl hover:shadow-primary/25 hover:-translate-y-1.5 hover:scale-[1.02] transition-all duration-300 group ring-2 ring-primary/10 hover:ring-primary/25">
              <div className="relative h-44 md:h-48 overflow-hidden">
                <Image
                  src="/african-woman-mobile-health-app.jpg"
                  alt="Assessment"
                  fill
                  className="object-cover group-hover:scale-105 transition-transform duration-500 brightness-90 contrast-110 saturate-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />
                <div className="absolute top-3 left-3">
                  <span className="inline-flex items-center rounded-full bg-primary px-2.5 py-0.5 text-[10px] font-bold text-primary-foreground shadow-md">ÉTAPE 1</span>
                </div>
                <div className="absolute bottom-3 left-3">
                  <div className="w-10 h-10 rounded-xl bg-white/95 shadow-md flex items-center justify-center">
                    <Shield className="w-5 h-5 text-primary" />
                  </div>
                </div>
              </div>
              <CardContent className="p-5 bg-gradient-to-br from-primary/15 via-primary/8 to-accent/10 border-t border-primary/20">
                <div className="text-primary font-bold text-sm mb-2 opacity-0 pointer-events-none">ÉTAPE 1</div>
                <h3 className="text-lg font-bold mb-2 text-foreground">Évaluez vos risques</h3>
                <p className="text-sm text-foreground/80 mb-4 leading-snug">
                  Questionnaire personnalisé pour connaître votre niveau de risque en quelques minutes
                </p>
                <Button variant="link" className="text-primary p-0 h-auto text-sm font-semibold group/btn" asChild>
                  <Link href="/mobile/assessment">
                    Commencer l'évaluation
                    <ArrowRight className="ml-1.5 h-3.5 w-3.5 group-hover/btn:translate-x-1 transition-transform" />
                  </Link>
                </Button>
              </CardContent>
            </Card>
            </AnimateInView>

            <AnimateInView delay={150}>
              <Card className="overflow-hidden border-0 rounded-2xl border-l-4 border-l-accent shadow-lg shadow-accent/15 hover:shadow-xl hover:shadow-accent/25 hover:-translate-y-1.5 hover:scale-[1.02] transition-all duration-300 group ring-2 ring-accent/10 hover:ring-accent/25">
              <div className="relative h-44 md:h-48 overflow-hidden">
                <Image
                  src="/modern-medical-clinic-building-healthcare-center-a.jpg"
                  alt="Find Center"
                  fill
                  className="object-cover group-hover:scale-105 transition-transform duration-500 brightness-95 contrast-105"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />
                <div className="absolute top-3 left-3">
                  <span className="inline-flex items-center rounded-full bg-accent px-2.5 py-0.5 text-[10px] font-bold text-accent-foreground shadow-md">ÉTAPE 2</span>
                </div>
                <div className="absolute bottom-3 left-3">
                  <div className="w-10 h-10 rounded-xl bg-white/95 shadow-md flex items-center justify-center">
                    <MapPin className="w-5 h-5 text-accent" />
                  </div>
                </div>
              </div>
              <CardContent className="p-5 bg-gradient-to-br from-accent/15 via-accent/8 to-primary/10 border-t border-accent/20">
                <div className="text-accent font-bold text-sm mb-2 opacity-0 pointer-events-none">ÉTAPE 2</div>
                <h3 className="text-lg font-bold mb-2 text-foreground">Trouvez un centre</h3>
                <p className="text-sm text-foreground/80 mb-4 leading-snug">
                  Centres de dépistage certifiés près de chez vous avec notre carte interactive
                </p>
                <Button variant="link" className="text-primary p-0 h-auto text-sm font-semibold group/btn" asChild>
                  <Link href="/mobile/providers">
                    Voir la carte
                    <ArrowRight className="ml-1.5 h-3.5 w-3.5 group-hover/btn:translate-x-1 transition-transform" />
                  </Link>
                </Button>
              </CardContent>
            </Card>
            </AnimateInView>

            <AnimateInView delay={300}>
              <Card className="overflow-hidden border-0 rounded-2xl border-l-4 border-l-primary shadow-lg shadow-primary/15 hover:shadow-xl hover:shadow-primary/25 hover:-translate-y-1.5 hover:scale-[1.02] transition-all duration-300 group ring-2 ring-primary/10 hover:ring-primary/25">
              <div className="relative h-44 md:h-48 overflow-hidden">
                <Image
                  src="/african-doctor-woman-consultation.jpg"
                  alt="Book Appointment"
                  fill
                  className="object-cover group-hover:scale-105 transition-transform duration-500 brightness-90 contrast-110 saturate-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />
                <div className="absolute top-3 left-3">
                  <span className="inline-flex items-center rounded-full bg-primary px-2.5 py-0.5 text-[10px] font-bold text-primary-foreground shadow-md">ÉTAPE 3</span>
                </div>
                <div className="absolute bottom-3 left-3">
                  <div className="w-10 h-10 rounded-xl bg-white/95 shadow-md flex items-center justify-center">
                    <Calendar className="w-5 h-5 text-primary" />
                  </div>
                </div>
              </div>
              <CardContent className="p-5 bg-gradient-to-br from-primary/15 via-primary/8 to-accent/10 border-t border-primary/20">
                <div className="text-primary font-bold text-sm mb-2 opacity-0 pointer-events-none">ÉTAPE 3</div>
                <h3 className="text-lg font-bold mb-2 text-foreground">Prenez rendez-vous</h3>
                <p className="text-sm text-foreground/80 mb-4 leading-snug">
                  Réservez en ligne en quelques clics et recevez une confirmation immédiate
                </p>
                <Button variant="link" className="text-primary p-0 h-auto text-sm font-semibold group/btn" asChild>
                  <Link href="/mobile/booking">
                    Réserver maintenant
                    <ArrowRight className="ml-1.5 h-3.5 w-3.5 group-hover/btn:translate-x-1 transition-transform" />
                  </Link>
                </Button>
              </CardContent>
            </Card>
            </AnimateInView>
          </div>
          </div>
        </section>

        <section className="py-12 md:py-16 bg-gradient-to-br from-primary via-primary to-accent relative overflow-hidden">
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-0 left-1/4 w-96 h-96 bg-white rounded-full blur-3xl animate-float" />
            <div
              className="absolute bottom-0 right-1/4 w-96 h-96 bg-white rounded-full blur-3xl animate-float"
              style={{ animationDelay: "2s" }}
            />
          </div>
          <div className="container mx-auto px-4 max-w-7xl relative z-10">
            <AnimateInView>
              <div className="text-center mb-8">
                <h2 className="text-3xl md:text-4xl font-bold text-white mb-3">Le dépistage sauve des vies</h2>
                <p className="text-lg text-white/90 max-w-2xl mx-auto">Des chiffres qui parlent d'eux-mêmes</p>
              </div>
            </AnimateInView>
            <div className="grid md:grid-cols-3 gap-6 md:gap-8">
              <AnimateInView delay={0}>
                <div className="text-center p-6 rounded-3xl bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-all duration-500 hover:scale-105">
                  <div className="text-7xl font-bold text-white mb-4 drop-shadow-lg">90%</div>
                  <p className="text-white/95 text-xl font-medium">Taux de guérison avec détection précoce</p>
                </div>
              </AnimateInView>
              <AnimateInView delay={100}>
                <div className="text-center p-6 rounded-3xl bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-all duration-500 hover:scale-105">
                  <div className="text-7xl font-bold text-white mb-4 drop-shadow-lg">50+</div>
                  <p className="text-white/95 text-xl font-medium">Centres partenaires disponibles</p>
                </div>
              </AnimateInView>
              <AnimateInView delay={200}>
                <div className="text-center p-6 rounded-3xl bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-all duration-500 hover:scale-105">
                  <div className="text-7xl font-bold text-white mb-4 drop-shadow-lg">24/7</div>
                  <p className="text-white/95 text-xl font-medium">Plateforme accessible à tout moment</p>
                </div>
              </AnimateInView>
            </div>
          </div>
        </section>

        <section className="pt-14 md:pt-20 pb-4 md:pb-6 relative overflow-hidden bg-gradient-to-b from-accent/[0.08] via-background to-primary/[0.08]">
          <div className="container mx-auto px-4 max-w-7xl relative z-10">
          <div className="grid md:grid-cols-2 gap-8 md:gap-10 items-start">
            <AnimateInView className="order-2 md:order-1">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-3 text-balance leading-tight bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">Informez-vous, protégez-vous</h2>
              <p className="text-foreground/80 mb-5 leading-relaxed">
                Accédez à une bibliothèque complète d'articles, vidéos et guides pratiques sur la santé mammaire, le
                dépistage et la prévention du cancer du sein.
              </p>
              <ul className="space-y-3 mb-6">
                <li className="flex items-start gap-3 p-3 rounded-xl transition-colors duration-300 hover:bg-primary/5">
                  <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <Heart className="w-5 h-5 text-primary fill-primary" />
                  </div>
                  <div>
                    <p className="font-bold mb-0.5">Auto-examen mensuel</p>
                    <p className="text-sm text-muted-foreground">Apprenez les gestes qui sauvent avec nos vidéos tutoriels</p>
                  </div>
                </li>
                <li className="flex items-start gap-3 p-3 rounded-xl transition-colors duration-300 hover:bg-primary/5">
                  <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <Heart className="w-5 h-5 text-primary fill-primary" />
                  </div>
                  <div>
                    <p className="font-bold mb-0.5">Facteurs de risque</p>
                    <p className="text-sm text-muted-foreground">Comprenez votre profil de santé personnalisé</p>
                  </div>
                </li>
                <li className="flex items-start gap-3 p-3 rounded-xl transition-colors duration-300 hover:bg-primary/5">
                  <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <Heart className="w-5 h-5 text-primary fill-primary" />
                  </div>
                  <div>
                    <p className="font-bold mb-0.5">Témoignages inspirants</p>
                    <p className="text-sm text-muted-foreground">Des histoires de courage et d'espoir de femmes africaines</p>
                  </div>
                </li>
              </ul>
              <Button
                size="lg"
                className="bg-primary hover:bg-primary/90 h-12 px-6 text-base rounded-xl shadow-lg transition-all duration-300 hover:scale-105 hover:shadow-xl active:scale-100"
                asChild
              >
                <Link href="/mobile/education">
                  Explorer les ressources
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              {/* Bande d’atouts pour combler le vide et donner envie */}
              <div className="mt-8 flex flex-wrap gap-4 sm:gap-6">
                <div className="flex items-center gap-2 rounded-full bg-primary/15 px-4 py-2.5 border border-primary/20">
                  <span className="text-lg">✓</span>
                  <span className="text-sm font-semibold text-foreground">Gratuit</span>
                </div>
                <div className="flex items-center gap-2 rounded-full bg-accent/15 px-4 py-2.5 border border-accent/20">
                  <span className="text-lg">✓</span>
                  <span className="text-sm font-semibold text-foreground">Sécurisé</span>
                </div>
                <div className="flex items-center gap-2 rounded-full bg-primary/15 px-4 py-2.5 border border-primary/20">
                  <span className="text-lg">✓</span>
                  <span className="text-sm font-semibold text-foreground">En français</span>
                </div>
              </div>
            </div>
            </AnimateInView>
            <AnimateInView className="order-1 md:order-2 relative" delay={150}>
              <div className="relative h-[320px] md:h-[380px] rounded-2xl overflow-hidden shadow-xl group">
                <Image 
                  src="/african-women-community-support-group.jpg" 
                  alt="Education" 
                  fill 
                  className="object-cover brightness-90 contrast-110 saturate-110 transition-transform duration-700 group-hover:scale-105" 
                />
              </div>
              <div className="absolute -bottom-6 -left-6 w-32 h-32 bg-accent rounded-3xl opacity-20 blur-2xl animate-float" />
              <div className="absolute -top-6 -right-6 w-32 h-32 bg-primary rounded-3xl opacity-20 blur-2xl animate-float" style={{ animationDelay: "1s" }} />
            </AnimateInView>
          </div>
          </div>
        </section>

        <section className="pt-4 md:pt-6 pb-10 md:pb-14">
          <div className="container mx-auto px-4 max-w-7xl">
            <AnimateInView>
            <div className="relative rounded-2xl overflow-hidden shadow-2xl ring-2 ring-primary/20 min-h-[320px] h-[340px] md:h-[380px]">
              <Image
                src="/african-woman-confident-empowered-healthcare-welln.jpg"
                alt="CTA"
                fill
                className="object-cover object-[center_top] brightness-75 contrast-110 saturate-110"
                style={{ objectPosition: 'center top' }}
              />
              <div className="absolute inset-0 bg-gradient-to-r from-primary/95 via-primary/80 to-accent/60 z-10" />
              <div className="absolute inset-0 z-20 p-6 md:p-10 flex flex-col justify-center max-w-xl">
                <h2 className="text-2xl md:text-4xl font-bold text-white mb-2 md:mb-3 leading-tight text-balance drop-shadow-lg">
                  Prenez votre santé en main dès aujourd'hui
                </h2>
                <p className="text-base md:text-lg text-white/95 mb-5 md:mb-6 text-balance leading-relaxed drop-shadow-md">
                  Rejoignez des milliers de femmes qui ont fait le choix de la prévention
                </p>
                <div className="flex flex-col sm:flex-row gap-3">
                  <Button
                    size="lg"
                    className="bg-gradient-to-r from-accent to-primary text-white hover:opacity-95 h-11 px-5 rounded-xl shadow-xl font-semibold border-0"
                    asChild
                  >
                    <Link href="/mobile/assessment">Commencer maintenant</Link>
                  </Button>
                  {!isAuthenticated && (
                    <Button
                      size="lg"
                      variant="outline"
                      className="border-2 border-white text-white hover:bg-white/20 h-11 px-5 rounded-xl bg-transparent font-semibold"
                      asChild
                    >
                      <Link href="/mobile/signup">Créer un compte</Link>
                    </Button>
                  )}
                  {isAuthenticated && (
                    <Button
                      size="lg"
                      variant="outline"
                      className="border-2 border-white text-white hover:bg-white/20 h-11 px-5 rounded-xl bg-transparent font-semibold"
                      asChild
                    >
                      <Link href="/mobile/dashboard">Mon espace</Link>
                    </Button>
                  )}
                </div>
              </div>
            </div>
            </AnimateInView>
          </div>
        </section>
      </main>

      <footer className="bg-gradient-to-br from-primary/25 via-primary/15 to-accent/25 border-t border-primary/20 py-8">
        <div className="container mx-auto px-4 max-w-7xl">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8 mb-6">
            <div className="col-span-2 md:col-span-1">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-9 h-9 rounded-xl bg-primary flex items-center justify-center shadow-md">
                  <Heart className="w-4 h-4 text-white fill-white" />
                </div>
                <div>
                  <span className="font-bold text-base text-foreground block leading-none">BreastCare</span>
                  <span className="text-xs text-foreground/70">Pro</span>
                </div>
              </div>
              <p className="text-xs text-foreground/80 leading-snug">
                Plateforme de dépistage du cancer du sein
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2 text-sm text-foreground">Services</h3>
              <ul className="space-y-1.5 text-xs text-foreground/80">
                <li><Link href="/mobile/assessment" className="hover:text-primary transition-colors">Évaluation des risques</Link></li>
                <li><Link href="/mobile/providers" className="hover:text-primary transition-colors">Trouver un centre</Link></li>
                <li><Link href="/mobile/booking" className="hover:text-primary transition-colors">Prendre rendez-vous</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-2 text-sm text-foreground">Ressources</h3>
              <ul className="space-y-1.5 text-xs text-foreground/80">
                <li><Link href="/mobile/education" className="hover:text-primary transition-colors">Éducation</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-2 text-sm text-foreground">Contact</h3>
              <ul className="space-y-1.5 text-xs text-foreground/80">
                <li>Support 24/7</li>
                <li>contact@breastcare.com</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-primary/20 pt-4 text-center text-xs text-foreground/75">
            <p>© 2025 BreastCare Pro. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
