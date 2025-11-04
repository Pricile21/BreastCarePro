"use client"

import { useState } from "react"
import { AdminSidebar } from "@/components/admin-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { AuthGuard } from "@/components/auth-guard"
import { useAccessRequests } from "@/hooks/use-api"
import { Skeleton } from "@/components/ui/skeleton"
import { CheckCircle, XCircle, Clock, Search, Filter, User, Mail, Phone, MapPin, FileText } from "lucide-react"

export default function AdminRequestsPage() {
  const [statusFilter, setStatusFilter] = useState<string>("all")
  const [searchTerm, setSearchTerm] = useState("")
  const { requests, loading, error, updateRequest } = useAccessRequests(statusFilter === "all" ? "" : statusFilter)

  const filteredRequests = requests.filter(request =>
    request.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    request.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    request.specialty.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleApprove = async (requestId: string) => {
    try {
      console.log(`Tentative d'approbation de la demande ${requestId}`);
      await updateRequest(requestId, "approved");
      console.log(`Demande ${requestId} approuvée avec succès`);
    } catch (err) {
      console.error("Erreur lors de l'approbation:", err);
      // Afficher une notification d'erreur à l'utilisateur
      alert(`Erreur lors de l'approbation: ${err instanceof Error ? err.message : 'Erreur inconnue'}`);
    }
  }

  const handleReject = async (requestId: string) => {
    try {
      console.log(`Tentative de rejet de la demande ${requestId}`);
      await updateRequest(requestId, "rejected", "Demande rejetée par l'administrateur");
      console.log(`Demande ${requestId} rejetée avec succès`);
    } catch (err) {
      console.error("Erreur lors du rejet:", err);
      // Afficher une notification d'erreur à l'utilisateur
      alert(`Erreur lors du rejet: ${err instanceof Error ? err.message : 'Erreur inconnue'}`);
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "pending":
        return <Badge variant="outline" className="text-orange-600 border-orange-200"><Clock className="w-3 h-3 mr-1" />En attente</Badge>
      case "approved":
        return <Badge variant="outline" className="text-green-600 border-green-200"><CheckCircle className="w-3 h-3 mr-1" />Approuvé</Badge>
      case "rejected":
        return <Badge variant="outline" className="text-red-600 border-red-200"><XCircle className="w-3 h-3 mr-1" />Rejeté</Badge>
      default:
        return <Badge variant="outline">{status}</Badge>
    }
  }

  return (
    <AuthGuard>
      <div className="flex min-h-screen bg-slate-50 dark:bg-slate-950">
        <AdminSidebar />
        <main className="flex-1 md:ml-64 p-8">
          <div className="max-w-7xl mx-auto space-y-8">
            {/* Header */}
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Demandes d'accès</h1>
                <p className="text-slate-600 dark:text-slate-400">Gérez les demandes d'accès des professionnels</p>
              </div>
              <Button 
                onClick={() => window.location.reload()} 
                variant="outline"
                className="flex items-center gap-2"
              >
                <Search className="w-4 h-4" />
                Recharger les données
              </Button>
            </div>

            {/* Filters */}
            <Card>
              <CardHeader>
                <CardTitle>Filtres et recherche</CardTitle>
                <CardDescription>Filtrez les demandes par statut et recherchez par nom ou spécialité</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col sm:flex-row gap-4">
                  <div className="flex-1">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
                      <Input
                        placeholder="Rechercher par nom, email ou spécialité..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-10"
                      />
                    </div>
                  </div>
                  <div className="sm:w-48">
                    <Select value={statusFilter} onValueChange={setStatusFilter}>
                      <SelectTrigger>
                        <Filter className="w-4 h-4 mr-2" />
                        <SelectValue placeholder="Filtrer par statut" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Tous les statuts</SelectItem>
                        <SelectItem value="pending">En attente</SelectItem>
                        <SelectItem value="approved">Approuvés</SelectItem>
                        <SelectItem value="rejected">Rejetés</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Error State */}
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {/* Loading State */}
            {loading && (
              <div className="space-y-4">
                {[...Array(3)].map((_, i) => (
                  <Card key={i}>
                    <CardContent className="p-6">
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <Skeleton className="h-6 w-48" />
                          <Skeleton className="h-6 w-20" />
                        </div>
                        <div className="space-y-2">
                          <Skeleton className="h-4 w-full" />
                          <Skeleton className="h-4 w-3/4" />
                        </div>
                        <div className="flex gap-2">
                          <Skeleton className="h-8 w-20" />
                          <Skeleton className="h-8 w-20" />
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}


            {/* Requests List */}
            {!loading && (
              <div className="space-y-4">
                {filteredRequests.length === 0 ? (
                  <Card>
                    <CardContent className="p-8 text-center">
                      <User className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                      <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-2">
                        Aucune demande trouvée
                      </h3>
                      <p className="text-slate-600 dark:text-slate-400">
                        {searchTerm || statusFilter
                          ? "Aucune demande ne correspond à vos critères de recherche."
                          : "Il n'y a actuellement aucune demande d'accès."}
                      </p>
                    </CardContent>
                  </Card>
                ) : (
                  filteredRequests.map((request) => (
                    <Card key={request.id} className="hover:shadow-lg transition-shadow">
                      <CardContent className="p-6">
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-center gap-3">
                            <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                              <User className="w-6 h-6 text-primary" />
                            </div>
                            <div>
                              <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
                                {request.full_name}
                              </h3>
                              <p className="text-slate-600 dark:text-slate-400">{request.specialty}</p>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            {getStatusBadge(request.status)}
                          </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                          <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
                            <Mail className="w-4 h-4" />
                            <span>{request.email}</span>
                          </div>
                          <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
                            <Phone className="w-4 h-4" />
                            <span>{request.phone_number}</span>
                          </div>
                          <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
                            <MapPin className="w-4 h-4" />
                            <span>{request.hospital_clinic}</span>
                          </div>
                          <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
                            <FileText className="w-4 h-4" />
                            <span>Licence: {request.license_number}</span>
                          </div>
                        </div>

                        <div className="text-sm text-slate-500 dark:text-slate-500 mb-4">
                          Demande reçue le {new Date(request.created_at).toLocaleDateString('fr-FR', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </div>

                        {request.status === "pending" && (
                          <div className="flex gap-3">
                            <Button
                              onClick={() => handleApprove(request.id)}
                              className="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-3 text-lg"
                            >
                              <CheckCircle className="w-5 h-5 mr-2" />
                              Approuver
                            </Button>
                            <Button
                              onClick={() => handleReject(request.id)}
                              variant="outline"
                              className="flex-1 border-red-200 text-red-600 hover:bg-red-50 py-3"
                            >
                              <XCircle className="w-4 h-4 mr-2" />
                              Rejeter
                            </Button>
                          </div>
                        )}

                        {request.status === "approved" && (
                          <div className="w-full bg-green-50 dark:bg-green-950/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
                            <div className="flex items-center gap-2 text-green-700 dark:text-green-300">
                              <CheckCircle className="w-5 h-5" />
                              <span className="font-semibold">Demande approuvée</span>
                            </div>
                            <p className="text-sm text-green-600 dark:text-green-400 mt-1">
                              Cette demande a été approuvée et le professionnel peut maintenant accéder à la plateforme.
                            </p>
                          </div>
                        )}

                        {request.status === "rejected" && request.admin_notes && (
                          <div className="mt-4 p-3 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800 rounded-lg">
                            <p className="text-sm text-red-700 dark:text-red-300">
                              <strong>Raison du rejet :</strong> {request.admin_notes}
                            </p>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  ))
                )}
              </div>
            )}
          </div>
        </main>
      </div>
    </AuthGuard>
  )
}