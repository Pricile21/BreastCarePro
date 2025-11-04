"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, MapPin, Phone, Clock, Star, Navigation, Loader2 } from "lucide-react"
import { apiClient, HealthcareCenter } from "@/lib/api"
import dynamic from 'next/dynamic'

// Importer le composant de carte dynamiquement (SSR disabled pour Leaflet)
const MapComponent = dynamic(() => import('@/components/MapComponent'), { ssr: false })

interface ProviderDisplay extends HealthcareCenter {
  distance?: string;
  hours?: string;
}

export default function ProvidersPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [providers, setProviders] = useState<ProviderDisplay[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | undefined>(undefined)
  const [locationRequested, setLocationRequested] = useState(false)
  const [selectedCenterId, setSelectedCenterId] = useState<string | undefined>(undefined)

  useEffect(() => {
    // Demander la géolocalisation en premier
    requestGeolocation()
  }, [])

  // Charger les providers quand on a la position OU après un délai raisonnable
  useEffect(() => {
    // Attendre soit la géolocalisation soit 500ms
    const timer = setTimeout(() => {
      loadProviders()
    }, 500)
    
    return () => clearTimeout(timer)
  }, [userLocation]) // eslint-disable-line react-hooks/exhaustive-deps

  const requestGeolocation = async () => {
    if (typeof navigator !== 'undefined' && 'geolocation' in navigator && !locationRequested) {
      setLocationRequested(true)
        navigator.geolocation.getCurrentPosition(
        (position) => {
          console.log('📍 Position obtenue:', position.coords)
          console.log(`📍 Latitude: ${position.coords.latitude}, Longitude: ${position.coords.longitude}`)
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          })
        },
        (error) => {
          console.log('⚠️ Erreur géolocalisation:', error.message)
          console.log('⚠️ Code erreur:', error.code)
          // L'utilisateur a refusé ou erreur - continuer sans position
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 300000 // 5 minutes
        }
      )
    }
  }

  const loadProviders = async () => {
    try {
      setLoading(true)
      setError(null)
      
      // Attendre un peu si la géolocalisation est en cours
      await new Promise(resolve => setTimeout(resolve, 100))
      
      // Utiliser la position déjà obtenue par requestGeolocation si disponible
      const userLat = userLocation?.lat
      const userLng = userLocation?.lng
      
      console.log('🚀 loadProviders appelé avec userLocation:', { userLat, userLng })

      let response
      try {
        if (userLat && userLng) {
          // Recherche par proximité - SEULEMENT les 4 plus proches
          console.log('🔍 Recherche par proximité...', { lat: userLat, lng: userLng })
          response = await apiClient.searchNearbyCenters(userLat, userLng, 100)
          
          // Trier par distance et prendre les 4 premiers
          console.log(`📊 Réponse API: ${response.centers.length} centres reçus`)
          const sortedCenters = response.centers
            .sort((a, b) => a.distance_km - b.distance_km)
            .slice(0, 4)
            .map((item) => ({
              ...item.center,
              distance: `${item.distance_km.toFixed(1)} km`,
              distance_km: item.distance_km
            }))
          console.log(`✅ ${sortedCenters.length} centres les plus proches:`)
          sortedCenters.forEach((c, i) => {
            console.log(`   ${i + 1}. ${c.name}: ${c.distance} (${c.city})`)
          })
          setProviders(sortedCenters)
          
          // Sélectionner le premier centre par défaut
          if (sortedCenters.length > 0 && !selectedCenterId) {
            setSelectedCenterId(sortedCenters[0].id)
          }
        } else {
          // Liste normale - limiter à 4
          console.log('📋 Liste normale des centres...')
          response = await apiClient.getHealthcareCenters({ 
            limit: 100,  // Récupérer plus pour avoir des options
            is_available: true 
          })
          const centers = response.centers.slice(0, 4).map(center => ({
            ...center,
            distance: undefined, // Pas de distance sans GPS
          }))
          console.log(`📊 ${centers.length} centres affichés`)
          setProviders(centers)
          
          // Sélectionner le premier centre par défaut
          if (centers.length > 0 && !selectedCenterId) {
            setSelectedCenterId(centers[0].id)
          }
        }
      } catch (apiError: any) {
        console.error('❌ Erreur API centres:', apiError)
        throw apiError // Re-throw pour être capturé par le catch externe
      }
    } catch (err: any) {
      console.error('❌ Erreur lors du chargement des centres:', err)
      setError(err.message || 'Erreur lors du chargement des centres')
    } finally {
      setLoading(false)
    }
  }

  const formatOperatingHours = (hours: Record<string, string> | undefined): string => {
    if (!hours) return "Non disponible"
    
    const weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    const weekend = ['saturday', 'sunday']
    
    const weekdayHours = weekdays.map(day => hours[day]).filter(Boolean)
    const weekendHours = weekend.map(day => hours[day]).filter(Boolean)
    
    if (weekdayHours.length > 0 && weekdayHours.every(h => h === weekdayHours[0])) {
      const weekday = weekdayHours[0]
      if (weekendHours.length > 0 && weekendHours[0] === weekday && weekendHours[1] === weekday) {
        return `Tous les jours: ${weekday}`
      } else if (weekendHours[0] === weekday) {
        return `Lun-Sam: ${weekday}`
      } else {
        return `Lun-Ven: ${weekday}`
      }
    }
    
    // Format simple si les horaires sont différents
    return hours['monday'] || "Non disponible"
  }

  const filteredProviders = providers.filter(
    (provider) =>
      provider.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      provider.address.toLowerCase().includes(searchQuery.toLowerCase()) ||
      provider.city.toLowerCase().includes(searchQuery.toLowerCase()),
  )
  // Ne pas limiter ici car providers est déjà limité à 4 depuis l'API

  console.log(`🔍 ${providers.length} centres chargés, ${filteredProviders.length} après recherche`)

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-accent/5">
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/mobile">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Retour
            </Link>
          </Button>
          <div className="flex items-center gap-2">
            <MapPin className="w-5 h-5 text-primary" />
            <span className="font-semibold">Centres de dépistage</span>
          </div>
          <div className="w-20" />
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Carte Interactive */}
        <Card className="mb-6 overflow-hidden">
          <CardHeader className="pb-2">
            <CardTitle className="text-lg">Carte des centres</CardTitle>
            <CardDescription>
              {userLocation ? 'Position détectée - centres à proximité' : 'Carte interactive des centres de dépistage'}
            </CardDescription>
          </CardHeader>
          <CardContent className="p-0">
            <div className="h-[400px] w-full bg-muted">
              <MapComponent 
                centers={providers.map(p => ({
                  id: p.id,
                  name: p.name,
                  latitude: p.latitude || 6.3667,
                  longitude: p.longitude || 2.4167,
                  type: p.type,
                  distance_km: undefined // Retirer pour éviter conflit de type
                }))}
                userLocation={userLocation}
                selectedCenterId={selectedCenterId}
                onCenterClick={(id) => setSelectedCenterId(id)}
              />
            </div>
          </CardContent>
        </Card>

        {/* Search */}
        <div className="mb-6">
          <Input
            placeholder="Rechercher un centre..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full"
          />
        </div>

        {/* Results Count */}
        <div className="mb-4">
          {loading ? (
            <p className="text-sm text-muted-foreground">Chargement des centres...</p>
          ) : error ? (
            <p className="text-sm text-destructive">{error}</p>
          ) : (
            <p className="text-sm text-muted-foreground">
              {filteredProviders.length} centre(s) {searchQuery ? 'trouvé(s)' : 'disponible(s)'}
            </p>
          )}
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-primary" />
          </div>
        )}

        {/* Error State */}
        {error && !loading && (
          <Card className="p-6">
            <div className="text-center">
              <p className="text-destructive mb-4">{error}</p>
              <Button onClick={loadProviders} variant="outline">
                Réessayer
              </Button>
            </div>
          </Card>
        )}

        {/* Providers List */}
        {!loading && !error && (
        <div className="space-y-4">
            {filteredProviders.length === 0 ? (
              <Card className="p-6">
                <div className="text-center">
                  <p className="text-muted-foreground">
                    {searchQuery ? 'Aucun centre trouvé pour votre recherche.' : 'Aucun centre disponible pour le moment.'}
                  </p>
                </div>
              </Card>
            ) : (
              filteredProviders.map((provider) => (
            <Card 
              key={provider.id} 
              className={`hover:bg-accent/5 transition-colors cursor-pointer ${selectedCenterId === provider.id ? 'ring-2 ring-primary' : ''}`}
              onClick={() => setSelectedCenterId(provider.id)}
            >
              <CardHeader>
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <CardTitle className="text-lg mb-1 hover:text-primary">{provider.name}</CardTitle>
                    <CardDescription className="flex items-center gap-1 mb-2">
                      <MapPin className="w-3 h-3" />
                          {provider.address}, {provider.city}
                    </CardDescription>
                  </div>
                      <div className="flex flex-col gap-2 items-end">
                        {provider.is_verified && (
                          <Badge variant="outline" className="bg-green-50 border-green-200 text-green-700 text-xs">
                            Vérifié
                          </Badge>
                        )}
                        {provider.is_available ? (
                    <Badge className="bg-primary text-primary-foreground">Disponible</Badge>
                  ) : (
                    <Badge variant="outline">Complet</Badge>
                  )}
                      </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Info Grid */}
                <div className="grid grid-cols-2 gap-3 text-sm">
                      {provider.distance && (
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Navigation className="w-4 h-4" />
                    <span>{provider.distance}</span>
                  </div>
                      )}
                      {provider.phone_number && (
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Phone className="w-4 h-4" />
                          <span className="text-xs">{provider.phone_number}</span>
                  </div>
                      )}
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Clock className="w-4 h-4" />
                        <span className="text-xs">{formatOperatingHours(provider.operating_hours)}</span>
                  </div>
                </div>

                {/* Services */}
                    {provider.services && provider.services.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {provider.services.map((service, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {service}
                    </Badge>
                  ))}
                </div>
                    )}

                {/* Actions */}
                <div className="flex gap-2">
                  <Button
                    asChild
                    className="w-full bg-accent hover:bg-accent/90 text-accent-foreground"
                        disabled={!provider.is_available || !provider.accepts_appointments}
                  >
                    <Link href={`/mobile/booking?provider=${provider.id}`}>Réserver</Link>
                  </Button>
                </div>
              </CardContent>
            </Card>
              ))
            )}
        </div>
        )}
      </main>
    </div>
  )
}
