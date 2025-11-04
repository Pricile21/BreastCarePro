"use client"

import { useEffect, useRef } from 'react'
import L from 'leaflet'
import 'leaflet-routing-machine'
import 'leaflet-routing-machine/dist/leaflet-routing-machine.css'

interface MapComponentProps {
  centers: Array<{
    id?: string
    name: string
    latitude: number
    longitude: number
    type?: string
    distance_km?: number
  }>
  userLocation?: {
    lat: number
    lng: number
  }
  selectedCenterId?: string
  onCenterClick?: (centerId: string) => void
}

// Fix pour les icônes Leaflet dans Next.js
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

export default function MapComponent({ centers, userLocation, selectedCenterId, onCenterClick }: MapComponentProps) {
  const mapRef = useRef<L.Map | null>(null)
  const mapContainerRef = useRef<HTMLDivElement | null>(null)
  const markersRef = useRef<L.Marker[]>([])
  const routingRef = useRef<any>(null)

  useEffect(() => {
    if (!mapContainerRef.current) return

    // Initialiser la carte avec contrôle de scroll activé
    const map = L.map(mapContainerRef.current, {
      scrollWheelZoom: true,
      zoomControl: true,
      dragging: true,
      touchZoom: true,
      doubleClickZoom: true,
      boxZoom: true,
      keyboard: true
    }).setView([6.3667, 2.4167], 9) // Cotonou par défaut
    
             // Ajouter les tuiles OpenStreetMap
             L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
               attribution: '© OpenStreetMap contributors',
               maxZoom: 20,
             }).addTo(map)

    mapRef.current = map

    return () => {
      // Nettoyer proprement
      try {
        // Nettoyer les marqueurs d'abord
        if (markersRef.current) {
          markersRef.current.forEach(marker => {
            if (marker && mapRef.current) {
              try {
                mapRef.current.removeLayer(marker)
              } catch (e) {
                // Ignorer les erreurs de nettoyage
              }
            }
          })
          markersRef.current = []
        }
        
        // Nettoyer le routage
        if (routingRef.current && mapRef.current) {
          try {
            mapRef.current.removeControl(routingRef.current)
          } catch (e) {
            // Ignorer les erreurs de nettoyage
          }
          routingRef.current = null
        }
        
        // Détruire la carte
        if (mapRef.current) {
          mapRef.current.remove()
          mapRef.current = null
        }
      } catch (error) {
        console.warn('⚠️ Erreur lors du nettoyage de la carte:', error)
      }
    }
  }, [])

  // Initialiser les marqueurs une seule fois
  useEffect(() => {
    if (!mapRef.current) return
    const map = mapRef.current

    // Vérifier que la carte est toujours valide
    if (!map || !(map as any)._container) return

    console.log('🗺️ useEffect marqueurs déclenché. Nombre de centres:', centers.length)

    // Nettoyer les marqueurs précédents
    try {
      markersRef.current.forEach(m => {
        if (m && map && map.hasLayer && map.hasLayer(m)) {
          map.removeLayer(m)
        }
      })
      markersRef.current = []
    } catch (error) {
      console.warn('⚠️ Erreur lors du nettoyage des marqueurs:', error)
      markersRef.current = []
    }

    // Ajouter un marqueur pour la position de l'utilisateur si disponible
    if (userLocation) {
      const userIcon = L.icon({
        iconUrl: 'data:image/svg+xml;base64,' + btoa(`
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
            <circle cx="16" cy="16" r="12" fill="#3b82f6" stroke="white" stroke-width="2"/>
            <circle cx="16" cy="16" r="6" fill="white"/>
          </svg>
        `),
        iconSize: [32, 32],
        iconAnchor: [16, 16],
      })
      
      L.marker([userLocation.lat, userLocation.lng], { icon: userIcon })
        .addTo(map)
        .bindPopup('Votre position')
    }

    // Ajouter des marqueurs pour chaque centre avec interactivité
    centers.forEach((center, index) => {
      const isSelected = selectedCenterId && center.id === selectedCenterId
      console.log(`📍 Ajout marqueur ${index + 1}/${centers.length}: ${center.name}`)
      
      const centerIcon = L.icon({
        iconUrl: 'data:image/svg+xml;base64,' + btoa(`
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
            <path d="M16 0C9.373 0 4 5.373 4 12c0 8 12 20 12 20s12-12 12-20c0-6.627-5.373-12-12-12z" fill="${isSelected ? '#f97316' : '#ef4444'}" stroke="white" stroke-width="2"/>
            <circle cx="16" cy="12" r="6" fill="white"/>
          </svg>
        `),
        iconSize: [32, 32],
        iconAnchor: [16, 32],
      })
      
      const marker = L.marker([center.latitude, center.longitude], { icon: centerIcon })
        .addTo(map)
        .bindPopup(center.name)
      
      // Ajouter événement de clic personnalisé qui ne bloque pas le popup
      if (onCenterClick && center.id) {
        marker.on('click', (e) => {
          console.log(`🖱️  Clic sur marqueur: ${center.name}`)
          // Ouvrir le popup manuellement
          e.target.openPopup()
          // Mettre à jour la sélection
          onCenterClick(center.id!)
        })
      }
      
      markersRef.current.push(marker)
    })
    
    console.log(`✅ ${markersRef.current.length} marqueurs ajoutés au total`)

    // Adapter la vue pour afficher tous les marqueurs si pas de position utilisateur
    if (!userLocation && centers.length > 0) {
      const group = new L.FeatureGroup(centers.map(c => L.marker([c.latitude, c.longitude])))
      map.fitBounds(group.getBounds().pad(0.1))
    }

  }, [centers, userLocation, onCenterClick])

  // Mettre à jour les couleurs des marqueurs quand la sélection change
  useEffect(() => {
    if (!mapRef.current) return
    const map = mapRef.current

    // Vérifier que la carte est toujours valide
    if (!map || !(map as any)._container) return

    console.log('🎨 Mise à jour des couleurs des marqueurs. Nombre de marqueurs:', markersRef.current.length)

    // Mettre à jour les icônes selon la sélection
    try {
      markersRef.current.forEach((marker, index) => {
        if (!marker) return
        const center = centers[index]
        if (center && marker.setIcon) {
          const isSelected = selectedCenterId && center.id === selectedCenterId
          
          const centerIcon = L.icon({
            iconUrl: 'data:image/svg+xml;base64,' + btoa(`
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
                <path d="M16 0C9.373 0 4 5.373 4 12c0 8 12 20 12 20s12-12 12-20c0-6.627-5.373-12-12-12z" fill="${isSelected ? '#f97316' : '#ef4444'}" stroke="white" stroke-width="2"/>
                <circle cx="16" cy="12" r="6" fill="white"/>
              </svg>
            `),
            iconSize: [32, 32],
            iconAnchor: [16, 32],
          })
          
          marker.setIcon(centerIcon)
        }
      })
    } catch (error) {
      console.warn('⚠️ Erreur lors de la mise à jour des icônes:', error)
    }
  }, [selectedCenterId, centers])

  // Gérer le routage séparément
  useEffect(() => {
    if (!mapRef.current) return
    const map = mapRef.current

    // Vérifier que la carte est toujours valide
    if (!map || !(map as any)._container) return

    console.log('🗺️  useEffect routage déclenché, selectedCenterId:', selectedCenterId)

    // Nettoyer l'itinéraire précédent
    if (routingRef.current) {
      console.log('🧹 Nettoyage itinéraire précédent')
      try {
        if (map && map.removeControl) {
          map.removeControl(routingRef.current)
        }
      } catch (error) {
        console.warn('⚠️ Erreur lors du nettoyage de l\'itinéraire:', error)
      }
      routingRef.current = null
    }

    // Afficher l'itinéraire si un centre est sélectionné
    if (selectedCenterId && userLocation) {
      const selectedCenter = centers.find(c => c.id === selectedCenterId)
      if (selectedCenter && map) {
        try {
          console.log('🔀 Calcul itinéraire entre:', userLocation, 'et', selectedCenter)
          
          // Utiliser exactement la même config que dans votre projet
          const routingControl = (L as any).Routing.control({
            waypoints: [
              L.latLng(userLocation.lat, userLocation.lng),
              L.latLng(selectedCenter.latitude, selectedCenter.longitude)
            ],
            routeWhileDragging: false,
            draggableWaypoints: false,
            addWaypoints: false,
            show: false
          }).addTo(map)
          
          routingRef.current = routingControl
        } catch (error) {
          console.warn('⚠️ Erreur lors de l\'ajout de l\'itinéraire:', error)
        }
      }
    }

  }, [selectedCenterId, userLocation, centers])

  // Masquer le panneau d'instructions en CSS
  useEffect(() => {
    const style = document.createElement('style')
    style.textContent = `
      .leaflet-routing-container {
        display: none !important;
      }
    `
    document.head.appendChild(style)
    return () => {
      document.head.removeChild(style)
    }
  }, [])

  return <div ref={mapContainerRef} className="w-full h-full min-h-[400px]" />
}

