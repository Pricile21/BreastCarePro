"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { ProfessionalSidebar } from "@/components/professional-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Upload, FileImage, X, Loader2 } from "lucide-react"

export default function UploadPage() {
  const router = useRouter()
  const [files, setFiles] = useState<File[]>([])
  const [isDragging, setIsDragging] = useState(false)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [patientInfo, setPatientInfo] = useState({
    name: "",
    age: "",
    id: "",
    notes: "",
  })

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const droppedFiles = Array.from(e.dataTransfer.files).filter((file) => file.type.startsWith("image/"))
    const remainingSlots = 4 - files.length
    if (remainingSlots > 0) {
      const filesToAdd = droppedFiles.slice(0, remainingSlots)
      setFiles((prev) => [...prev, ...filesToAdd])
      if (droppedFiles.length > remainingSlots) {
        alert(`Seulement ${remainingSlots} image(s) ajoutée(s). Vous devez uploader exactement 4 images.`)
      }
    } else {
      alert("Vous devez uploader exactement 4 images. Supprimez d'abord une image pour en ajouter une autre.")
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files)
      const remainingSlots = 4 - files.length
      if (remainingSlots > 0) {
        const filesToAdd = selectedFiles.slice(0, remainingSlots)
        setFiles((prev) => [...prev, ...filesToAdd])
        if (selectedFiles.length > remainingSlots) {
          alert(`Seulement ${remainingSlots} image(s) ajoutée(s). Vous devez uploader exactement 4 images.`)
        }
      } else {
        alert("Vous devez uploader exactement 4 images. Supprimez d'abord une image pour en ajouter une autre.")
      }
    }
    // Réinitialiser l'input pour permettre de sélectionner le même fichier à nouveau
    e.target.value = ''
  }

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index))
  }

  const handleAnalyze = async () => {
    // Valider qu'exactement 4 images sont sélectionnées
    if (files.length === 0) {
      alert("Veuillez sélectionner 4 images pour lancer l'analyse.")
      return
    }
    
    if (files.length !== 4) {
      alert(`Vous devez uploader exactement 4 images. Actuellement: ${files.length} image(s).`)
      return
    }

    setIsAnalyzing(true)
    
    try {
      // Créer FormData pour l'upload
      const formData = new FormData()
      
      // Ajouter les fichiers
      files.forEach((file) => {
        formData.append('files', file)
      })
      
      // Ajouter les informations patient
      if (patientInfo.id) {
        formData.append('patient_id', patientInfo.id)
      }
      if (patientInfo.name) {
        formData.append('patient_name', patientInfo.name)
      }
      if (patientInfo.age) {
        formData.append('patient_age', patientInfo.age)
      }
      if (patientInfo.notes) {
        formData.append('patient_notes', patientInfo.notes)
      }
      
      // Appeler l'API d'analyse (utiliser l'URL configurée)
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
      const response = await fetch(`${apiUrl}/mammography/analyze`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
        },
        body: formData
      })
      
      if (response.ok) {
        const result = await response.json()
        console.log('✅ Analyse terminée:', result)
        
        // Rediriger vers la page de résultats avec l'ID d'analyse
        router.push(`/professional/analysis/${result.id}`)
      } else {
        // Récupérer le message d'erreur
        let errorMessage = 'Erreur inconnue'
        try {
          const error = await response.json()
          errorMessage = error.detail || error.message || 'Erreur lors de l\'analyse'
          console.error('❌ Erreur d\'analyse:', error)
        } catch (e) {
          errorMessage = await response.text() || `Erreur ${response.status}: ${response.statusText}`
          console.error('❌ Erreur d\'analyse (réponse non-JSON):', errorMessage)
        }
        
        // Afficher le message d'erreur à l'utilisateur
        alert(`❌ ${errorMessage}`)
      }
    } catch (error) {
      console.error('❌ Erreur de connexion:', error)
      alert('Erreur de connexion. Vérifiez votre connexion internet.')
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="flex h-screen">
      <ProfessionalSidebar />

      <main className="flex-1 overflow-y-auto bg-background">
        <div className="container mx-auto p-8 max-w-5xl">
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">Nouvelle analyse</h1>
            <p className="text-muted-foreground">Téléchargez des mammographies pour analyse IA</p>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            {/* Upload Section */}
            <Card>
              <CardHeader>
                <CardTitle>Images mammographiques</CardTitle>
                <CardDescription>Formats acceptés: DICOM, PNG, JPEG</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Drop Zone */}
                <div
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                    isDragging ? "border-primary bg-primary/5" : "border-border"
                  }`}
                >
                  <Upload className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                  <p className="text-sm font-medium mb-2">
                    {files.length === 0 
                      ? "Glissez-déposez vos images ici (4 images requises)"
                      : files.length === 4
                      ? "✅ 4 images sélectionnées"
                      : `${files.length}/4 images sélectionnées`}
                  </p>
                  <p className="text-xs text-muted-foreground mb-4">
                    {files.length < 4 ? `Vous devez uploader exactement 4 images. ${4 - files.length} image(s) restante(s).` : "Toutes les images sont sélectionnées"}
                  </p>
                  {files.length < 4 && (
                    <Button variant="outline" asChild>
                      <label className="cursor-pointer">
                        Parcourir les fichiers
                        <input type="file" multiple accept="image/*" onChange={handleFileSelect} className="hidden" />
                      </label>
                    </Button>
                  )}
                </div>

                {/* File List */}
                {files.length > 0 && (
                  <div className="space-y-2">
                    <p className={`text-sm font-medium ${files.length === 4 ? 'text-green-600' : 'text-orange-600'}`}>
                      {files.length}/4 image(s) sélectionnée(s)
                      {files.length === 4 && <span className="ml-2">✅</span>}
                    </p>
                    {files.map((file, index) => (
                      <div key={index} className="flex items-center gap-3 p-3 rounded-lg border bg-card">
                        <FileImage className="w-5 h-5 text-primary flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium truncate">Image {index + 1}: {file.name}</p>
                          <p className="text-xs text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                        </div>
                        <Button variant="ghost" size="sm" onClick={() => removeFile(index)}>
                          <X className="w-4 h-4" />
                        </Button>
                      </div>
                    ))}
                    {files.length < 4 && (
                      <p className="text-xs text-orange-600 mt-2">
                        ⚠️ {4 - files.length} image(s) manquante(s) pour lancer l'analyse
                      </p>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Patient Info Section */}
            <Card>
              <CardHeader>
                <CardTitle>Informations patient</CardTitle>
                <CardDescription>Données nécessaires pour le rapport</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="patient-id">ID Patient</Label>
                  <Input
                    id="patient-id"
                    placeholder="P-2024-1248"
                    value={patientInfo.id}
                    onChange={(e) => setPatientInfo({ ...patientInfo, id: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="patient-name">Nom complet</Label>
                  <Input
                    id="patient-name"
                    placeholder="Nom du patient"
                    value={patientInfo.name}
                    onChange={(e) => setPatientInfo({ ...patientInfo, name: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="patient-age">Âge</Label>
                  <Input
                    id="patient-age"
                    type="number"
                    placeholder="45"
                    value={patientInfo.age}
                    onChange={(e) => setPatientInfo({ ...patientInfo, age: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="notes">Notes cliniques</Label>
                  <Textarea
                    id="notes"
                    placeholder="Antécédents, symptômes, observations..."
                    rows={4}
                    value={patientInfo.notes}
                    onChange={(e) => setPatientInfo({ ...patientInfo, notes: e.target.value })}
                  />
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Action Button */}
          <div className="mt-6 flex justify-end">
            <Button 
              size="lg" 
              onClick={handleAnalyze} 
              disabled={files.length !== 4 || isAnalyzing} 
              className="min-w-48"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Analyse en cours...
                </>
              ) : (
                <>
                  <Upload className="mr-2 h-4 w-4" />
                  {files.length === 4 ? "Lancer l'analyse IA" : `Lancer l'analyse IA (${files.length}/4)`}
                </>
              )}
            </Button>
          </div>
        </div>
      </main>
    </div>
  )
}
