import { AdminSidebar } from "@/components/admin-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"

export default function SettingsPage() {
  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-slate-950">
      <AdminSidebar />
      <main className="flex-1 md:ml-64 p-8">
        <div className="max-w-4xl mx-auto space-y-6">
          {/* Header */}
          <div>
            <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Paramètres</h1>
            <p className="text-slate-600 dark:text-slate-400 mt-1">Configuration générale de la plateforme</p>
          </div>

          {/* Platform Settings */}
          <Card>
            <CardHeader>
              <CardTitle>Paramètres de la plateforme</CardTitle>
              <CardDescription>Configuration générale du système</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="platform-name">Nom de la plateforme</Label>
                <Input id="platform-name" defaultValue="BreastCare Pro" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="support-email">Email de support</Label>
                <Input id="support-email" type="email" defaultValue="support@breastcare.com" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="max-upload">Taille max des fichiers (MB)</Label>
                <Input id="max-upload" type="number" defaultValue="50" />
              </div>
            </CardContent>
          </Card>

          {/* Access Control */}
          <Card>
            <CardHeader>
              <CardTitle>Contrôle d'accès</CardTitle>
              <CardDescription>Gestion des permissions et accès</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Validation manuelle des professionnels</Label>
                  <p className="text-sm text-muted-foreground">
                    Nécessite une approbation admin pour chaque inscription
                  </p>
                </div>
                <Switch defaultChecked />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Inscription ouverte (mobile)</Label>
                  <p className="text-sm text-muted-foreground">Permet aux utilisateurs de s'inscrire librement</p>
                </div>
                <Switch defaultChecked />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Mode maintenance</Label>
                  <p className="text-sm text-muted-foreground">Désactive temporairement l'accès à la plateforme</p>
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
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="model-version">Version du modèle</Label>
                <Input id="model-version" defaultValue="ResNet50-v2.1" disabled />
              </div>
              <div className="space-y-2">
                <Label htmlFor="confidence-threshold">Seuil de confiance (%)</Label>
                <Input id="confidence-threshold" type="number" defaultValue="85" />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Analyse automatique</Label>
                  <p className="text-sm text-muted-foreground">Lance l'analyse IA immédiatement après l'upload</p>
                </div>
                <Switch defaultChecked />
              </div>
            </CardContent>
          </Card>

          {/* Notifications */}
          <Card>
            <CardHeader>
              <CardTitle>Notifications</CardTitle>
              <CardDescription>Configuration des alertes système</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Alertes nouvelles demandes</Label>
                  <p className="text-sm text-muted-foreground">Notification pour chaque nouvelle demande d'accès</p>
                </div>
                <Switch defaultChecked />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Rapport quotidien</Label>
                  <p className="text-sm text-muted-foreground">Résumé des activités envoyé chaque jour</p>
                </div>
                <Switch defaultChecked />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Alertes système</Label>
                  <p className="text-sm text-muted-foreground">
                    Notifications pour les erreurs et problèmes techniques
                  </p>
                </div>
                <Switch defaultChecked />
              </div>
            </CardContent>
          </Card>

          {/* Save Button */}
          <div className="flex justify-end">
            <Button size="lg" className="bg-slate-900 hover:bg-slate-800 dark:bg-slate-100 dark:hover:bg-slate-200">
              Enregistrer les modifications
            </Button>
          </div>
        </div>
      </main>
    </div>
  )
}
