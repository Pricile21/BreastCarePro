import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Heart, ArrowLeft, MapPin, Phone, Clock, Star, Mail, Navigation, CheckCircle, Calendar } from "lucide-react"

export default function ProviderDetailPage() {
  // Mock data - would come from API based on [id]
  const provider = {
    id: 1,
    name: "Centre Hospitalier Universitaire de Cotonou",
    address: "Avenue Clozel, Cotonou",
    distance: "2.3 km",
    rating: 4.8,
    reviews: 124,
    phone: "+229 21 30 01 23",
    email: "contact@chu-cotonou.bj",
    hours: "Lundi-Vendredi: 8h-17h",
    services: ["Mammographie", "Échographie", "Biopsie", "Consultation spécialisée"],
    description:
      "Centre hospitalier universitaire équipé des dernières technologies de dépistage. Notre équipe de radiologues expérimentés utilise l'intelligence artificielle pour des diagnostics précis.",
    features: [
      "Équipement moderne",
      "Radiologues certifiés",
      "Analyse IA",
      "Résultats rapides",
      "Parking disponible",
      "Accessible PMR",
    ],
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-accent/5">
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/mobile/providers">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Retour
            </Link>
          </Button>
          <div className="flex items-center gap-2">
            <Heart className="w-5 h-5 text-accent" />
          </div>
          <div className="w-20" />
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-start justify-between mb-3">
            <div className="flex-1">
              <h1 className="text-2xl font-bold mb-2 text-balance">{provider.name}</h1>
              <div className="flex items-center gap-2 text-muted-foreground mb-2">
                <MapPin className="w-4 h-4" />
                <span className="text-sm">{provider.address}</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-1">
                  <Star className="w-4 h-4 fill-accent text-accent" />
                  <span className="font-medium">{provider.rating}</span>
                  <span className="text-sm text-muted-foreground">({provider.reviews} avis)</span>
                </div>
                <div className="flex items-center gap-1 text-muted-foreground">
                  <Navigation className="w-4 h-4" />
                  <span className="text-sm">{provider.distance}</span>
                </div>
              </div>
            </div>
            <Badge className="bg-primary text-primary-foreground">Disponible</Badge>
          </div>
        </div>

        {/* Map */}
        <Card className="mb-6 overflow-hidden">
          <div className="aspect-video bg-gradient-to-br from-primary/10 to-accent/10 relative flex items-center justify-center">
            <div className="text-center">
              <MapPin className="w-12 h-12 text-primary mx-auto mb-2" />
              <p className="text-sm text-muted-foreground">Localisation du centre</p>
            </div>
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-primary flex items-center justify-center animate-pulse">
              <MapPin className="w-7 h-7 text-primary-foreground" />
            </div>
          </div>
        </Card>

        {/* Description */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>À propos</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground leading-relaxed">{provider.description}</p>
          </CardContent>
        </Card>

        {/* Contact Info */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Informations de contact</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <Phone className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Téléphone</p>
                <p className="font-medium">{provider.phone}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <Mail className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Email</p>
                <p className="font-medium">{provider.email}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <Clock className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Horaires</p>
                <p className="font-medium">{provider.hours}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Services */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Services disponibles</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-3">
              {provider.services.map((service, index) => (
                <div key={index} className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-primary" />
                  <span className="text-sm">{service}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Features */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Équipements et services</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {provider.features.map((feature, index) => (
                <Badge key={index} variant="outline">
                  {feature}
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* CTA */}
        <div className="flex gap-4">
          <Button variant="outline" className="flex-1 bg-transparent">
            <Phone className="mr-2 h-4 w-4" />
            Appeler
          </Button>
          <Button asChild className="flex-1 bg-accent hover:bg-accent/90 text-accent-foreground">
            <Link href={`/mobile/booking?provider=${provider.id}`}>
              <Calendar className="mr-2 h-4 w-4" />
              Réserver
            </Link>
          </Button>
        </div>
      </main>
    </div>
  )
}
