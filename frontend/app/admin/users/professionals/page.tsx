"use client"

import { useState, useEffect } from "react"
import { AdminSidebar } from "@/components/admin-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Search, MoreVertical, Mail, Phone, Users, UserCheck, UserX, TrendingUp, Plus, X, Edit, Trash2 } from "lucide-react"
import { apiClient, Professional, ProfessionalCreate } from "@/lib/api"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

export default function ProfessionalsPage() {
  const [professionals, setProfessionals] = useState<Professional[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState("")
  const [showAddForm, setShowAddForm] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [editingProfessional, setEditingProfessional] = useState<Professional | null>(null)

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    phone_number: "",
    specialty: "",
    license_number: "",
    address: "",
    consultation_fee: "",
    languages: ""
  })

  const handleAddProfessional = () => {
    setEditingProfessional(null)
    setFormData({
      full_name: "",
      email: "",
      phone_number: "",
      specialty: "",
      license_number: "",
      address: "",
      consultation_fee: "",
      languages: ""
    })
    setShowAddForm(true)
  }

  const handleCancelForm = () => {
    setShowAddForm(false)
    setEditingProfessional(null)
    setFormData({
      full_name: "",
      email: "",
      phone_number: "",
      specialty: "",
      license_number: "",
      address: "",
      consultation_fee: "",
      languages: ""
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    
    try {
      // Préparer les données pour l'API
      const professionalData: ProfessionalCreate = {
        full_name: formData.full_name,
        email: formData.email || undefined,
        phone_number: formData.phone_number || undefined,
        specialty: formData.specialty,
        license_number: formData.license_number,
        address: formData.address || undefined,
        consultation_fee: formData.consultation_fee ? parseFloat(formData.consultation_fee) : undefined,
        languages: formData.languages ? formData.languages.split(',').map(lang => lang.trim()) : undefined
      }

      if (editingProfessional) {
        // Mode édition
        const updatedProfessional = await apiClient.updateProfessional(editingProfessional.id, professionalData)
        setProfessionals(prev => prev.map(p => p.id === editingProfessional.id ? updatedProfessional : p))
        alert("Professionnel modifié avec succès !")
      } else {
        // Mode création
        const newProfessional = await apiClient.createProfessional(professionalData)
        setProfessionals(prev => [...prev, newProfessional])
        alert("Professionnel ajouté avec succès !")
      }
      
      // Fermer le formulaire et réinitialiser
      setShowAddForm(false)
      setEditingProfessional(null)
      setFormData({
        full_name: "",
        email: "",
        phone_number: "",
        specialty: "",
        license_number: "",
        address: "",
        consultation_fee: "",
        languages: ""
      })
      
    } catch (error: any) {
      console.error("Erreur lors de la sauvegarde du professionnel:", error)
      alert(`Erreur lors de la sauvegarde: ${error.message}`)
    } finally {
      setSubmitting(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleDeleteProfessional = async (professionalId: string) => {
    if (!confirm("Êtes-vous sûr de vouloir supprimer ce professionnel ?")) {
      return
    }

    try {
      await apiClient.deleteProfessional(professionalId)
      setProfessionals(prev => prev.filter(p => p.id !== professionalId))
      alert("Professionnel supprimé avec succès !")
    } catch (error: any) {
      console.error("Erreur lors de la suppression:", error)
      alert(`Erreur lors de la suppression: ${error.message}`)
    }
  }

  const handleEditProfessional = (professional: Professional) => {
    setEditingProfessional(professional)
    setFormData({
      full_name: professional.full_name,
      email: professional.email || "",
      phone_number: professional.phone_number || "",
      specialty: professional.specialty,
      license_number: professional.license_number,
      address: professional.address || "",
      consultation_fee: professional.consultation_fee?.toString() || "",
      languages: professional.languages?.join(", ") || ""
    })
    setShowAddForm(true)
  }

  useEffect(() => {
    const fetchProfessionals = async () => {
      try {
        setLoading(true)
        setError(null)
        const data = await apiClient.getProfessionals()
        setProfessionals(data)
      } catch (err) {
        setError(err.message || 'Failed to fetch professionals')
        setProfessionals([])
      } finally {
        setLoading(false)
      }
    }
    
    fetchProfessionals()
  }, [])

  // Calculer les statistiques basées sur les vraies données
  const totalProfessionals = professionals.length
  const activeProfessionals = professionals.filter(p => p.is_active).length
  const inactiveProfessionals = professionals.filter(p => !p.is_active).length
  
  // Filtrer les professionnels selon le terme de recherche
  const filteredProfessionals = professionals.filter(prof =>
    prof.full_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    prof.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    prof.specialty?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-slate-950">
      <AdminSidebar />
      <main className="flex-1 md:ml-64 p-8">
        <div className="max-w-7xl mx-auto space-y-6">
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Professionnels de santé</h1>
              <p className="text-slate-600 dark:text-slate-400 mt-1">Gestion des radiologues et médecins</p>
            </div>
            <Dialog open={showAddForm} onOpenChange={setShowAddForm}>
              <DialogTrigger asChild>
            <Button className="bg-slate-900 hover:bg-slate-800 dark:bg-slate-100 dark:hover:bg-slate-200">
                  <Plus className="h-4 w-4 mr-2" />
              Ajouter un professionnel
            </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle>
                    {editingProfessional ? "Modifier le professionnel" : "Ajouter un nouveau professionnel"}
                  </DialogTitle>
                  <DialogDescription>
                    {editingProfessional 
                      ? "Modifiez les informations du professionnel de santé"
                      : "Remplissez les informations du professionnel de santé"
                    }
                  </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="full_name">Nom complet *</Label>
                      <Input
                        id="full_name"
                        name="full_name"
                        value={formData.full_name}
                        onChange={handleInputChange}
                        placeholder="Dr. Jean Dupont"
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="email">Email *</Label>
                      <Input
                        id="email"
                        name="email"
                        type="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        placeholder="jean.dupont@hospital.bj"
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="phone_number">Téléphone</Label>
                      <Input
                        id="phone_number"
                        name="phone_number"
                        value={formData.phone_number}
                        onChange={handleInputChange}
                        placeholder="+229 97 12 34 56"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="specialty">Spécialité *</Label>
                      <Input
                        id="specialty"
                        name="specialty"
                        value={formData.specialty}
                        onChange={handleInputChange}
                        placeholder="Radiologie"
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="license_number">Numéro de licence *</Label>
                      <Input
                        id="license_number"
                        name="license_number"
                        value={formData.license_number}
                        onChange={handleInputChange}
                        placeholder="RAD001"
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="consultation_fee">Frais de consultation (FCFA)</Label>
                      <Input
                        id="consultation_fee"
                        name="consultation_fee"
                        type="number"
                        value={formData.consultation_fee}
                        onChange={handleInputChange}
                        placeholder="15000"
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="address">Adresse</Label>
                    <Textarea
                      id="address"
                      name="address"
                      value={formData.address}
                      onChange={handleInputChange}
                      placeholder="Ville, Pays"
                      rows={3}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="languages">Langues parlées</Label>
                    <Input
                      id="languages"
                      name="languages"
                      value={formData.languages}
                      onChange={handleInputChange}
                      placeholder="Français, Anglais"
                    />
                  </div>
                  <div className="flex justify-end gap-2 pt-4">
                    <Button type="button" variant="outline" onClick={handleCancelForm}>
                      Annuler
                    </Button>
                    <Button 
                      type="submit" 
                      className="bg-slate-900 hover:bg-slate-800"
                      disabled={submitting}
                    >
                      {submitting 
                        ? (editingProfessional ? "Modification..." : "Ajout...") 
                        : (editingProfessional ? "Modifier le professionnel" : "Ajouter le professionnel")
                      }
                    </Button>
                  </div>
                </form>
              </DialogContent>
            </Dialog>
          </div>

          {/* Search */}
          <Card>
            <CardContent className="pt-6">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input 
                  placeholder="Rechercher par nom, email, spécialité..." 
                  className="pl-10"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </CardContent>
          </Card>

          {/* Stats */}
          <div className="grid gap-4 md:grid-cols-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                  <Users className="h-4 w-4" />
                  Total
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{totalProfessionals}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                  <UserCheck className="h-4 w-4" />
                  Actifs
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600">{activeProfessionals}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                  <UserX className="h-4 w-4" />
                  Inactifs
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-orange-600">{inactiveProfessionals}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                  <TrendingUp className="h-4 w-4" />
                  Ce mois
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-600">0</div>
              </CardContent>
            </Card>
          </div>

          {/* Professionals List */}
          <Card>
            <CardHeader>
              <CardTitle>Liste des professionnels</CardTitle>
              <CardDescription>Tous les professionnels inscrits sur la plateforme</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-slate-900 mx-auto mb-4"></div>
                  <p className="text-slate-500">Chargement des professionnels...</p>
                </div>
              ) : error ? (
                <div className="text-center py-8">
                  <div className="text-red-500 mb-4">⚠️</div>
                  <p className="text-red-600 mb-2">Erreur lors du chargement</p>
                  <p className="text-sm text-slate-500">{error}</p>
                </div>
              ) : filteredProfessionals.length === 0 ? (
                <div className="text-center py-12">
                  <Users className="h-16 w-16 text-slate-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-2">
                    Aucun professionnel trouvé
                  </h3>
                  <p className="text-slate-500 mb-6">
                    {searchTerm ? "Aucun professionnel ne correspond à votre recherche." : "Aucun professionnel n'est encore inscrit sur la plateforme."}
                  </p>
                </div>
              ) : (
              <div className="space-y-4">
                  {filteredProfessionals.map((prof) => (
                  <div
                    key={prof.id}
                    className="flex flex-col sm:flex-row sm:items-center gap-4 p-4 rounded-lg border bg-card hover:bg-accent/5 transition-colors"
                  >
                    <div className="flex-1 space-y-2">
                      <div className="flex items-center gap-3">
                          <h3 className="font-semibold text-slate-900 dark:text-slate-100">{prof.full_name}</h3>
                          <Badge variant={prof.is_active ? "default" : "secondary"}>
                            {prof.is_active ? "Actif" : "Inactif"}
                        </Badge>
                      </div>
                      <div className="grid gap-2 sm:grid-cols-2 text-sm text-muted-foreground">
                        <div className="flex items-center gap-2">
                          <Mail className="h-4 w-4" />
                          {prof.email}
                        </div>
                        <div className="flex items-center gap-2">
                          <Phone className="h-4 w-4" />
                            {prof.phone_number}
                          </div>
                      </div>
                      <div className="flex flex-wrap gap-4 text-sm">
                        <span className="text-slate-600 dark:text-slate-400">
                          <strong>Spécialité:</strong> {prof.specialty}
                        </span>
                        <span className="text-slate-600 dark:text-slate-400">
                            <strong>Adresse:</strong> {prof.address}
                        </span>
                        <span className="text-slate-600 dark:text-slate-400">
                            <strong>Analyses:</strong> {prof.total_analyses || 0}
                        </span>
                      </div>
                    </div>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon">
                      <MoreVertical className="h-4 w-4" />
                    </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem onClick={() => handleEditProfessional(prof)}>
                            <Edit className="h-4 w-4 mr-2" />
                            Modifier
                          </DropdownMenuItem>
                          <DropdownMenuItem 
                            onClick={() => handleDeleteProfessional(prof.id)}
                            className="text-red-600"
                          >
                            <Trash2 className="h-4 w-4 mr-2" />
                            Supprimer
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                  </div>
                ))}
              </div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
