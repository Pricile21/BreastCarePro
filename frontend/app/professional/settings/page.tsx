import { ProfessionalSidebar } from "@/components/professional-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"

export default function SettingsPage() {
  return (
    <div className="flex h-screen">
      <ProfessionalSidebar />

      <main className="flex-1 overflow-y-auto bg-background">
        <div className="container mx-auto p-8 max-w-4xl">
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">Paramètres</h1>
            <p className="text-muted-foreground">Gérez vos préférences et configuration</p>
          </div>

          <div className="space-y-6">
            {/* Profile Settings */}
            <Card>
              <CardHeader>
                <CardTitle>Profil professionnel</CardTitle>
                <CardDescription>Informations de votre compte</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="name">Nom complet</Label>
                    <Input id="name" defaultValue="Dr. Marie Kouassi" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="specialty">Spécialité</Label>
                    <Input id="specialty" defaultValue="Radiologue" />
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email professionnel</Label>
                  <Input id="email" type="email" defaultValue="marie.kouassi@hopital.bj" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="license">Numéro de licence</Label>
                  <Input id="license" defaultValue="RAD-BJ-2024-0123" />
                </div>
                <Button>Enregistrer les modifications</Button>
              </CardContent>
            </Card>

            {/* Notification Settings */}
            <Card>
              <CardHeader>
                <CardTitle>Notifications</CardTitle>
                <CardDescription>Gérez vos préférences de notification</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Alertes BI-RADS élevé</p>
                    <p className="text-sm text-muted-foreground">Recevoir une notification pour les cas BI-RADS 4-5</p>
                  </div>
                  <Switch defaultChecked />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Rapports complétés</p>
                    <p className="text-sm text-muted-foreground">Notification quand un rapport est prêt</p>
                  </div>
                  <Switch defaultChecked />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Mises à jour système</p>
                    <p className="text-sm text-muted-foreground">Nouvelles versions et améliorations</p>
                  </div>
                  <Switch />
                </div>
              </CardContent>
            </Card>

            {/* AI Settings */}
            <Card>
              <CardHeader>
                <CardTitle>Paramètres IA</CardTitle>
                <CardDescription>Configuration du modèle d'analyse</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Seuil de confiance</p>
                    <p className="text-sm text-muted-foreground">Niveau minimum pour validation automatique</p>
                  </div>
                  <Input type="number" defaultValue="85" className="w-20" />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Détection automatique</p>
                    <p className="text-sm text-muted-foreground">Marquer automatiquement les zones suspectes</p>
                  </div>
                  <Switch defaultChecked />
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
