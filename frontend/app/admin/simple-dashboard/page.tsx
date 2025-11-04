"use client"

import { useState, useEffect } from "react"

export default function SimpleDashboardPage() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('auth_token')
      if (!token) {
        window.location.href = "/admin/simple-login"
        return
      }

      try {
        const response = await fetch('http://localhost:8000/api/v1/auth/me', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.ok) {
          const userData = await response.json()
          setUser(userData)
        } else {
          localStorage.removeItem('auth_token')
          window.location.href = "/admin/simple-login"
        }
      } catch (err) {
        localStorage.removeItem('auth_token')
        window.location.href = "/admin/simple-login"
      } finally {
        setLoading(false)
      }
    }

    checkAuth()
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('auth_token')
    window.location.href = "/admin/simple-login"
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto mb-4"></div>
          <p>Chargement...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold">Dashboard Admin - SIMPLE</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span>Connecté: {user?.email}</span>
              <button
                onClick={handleLogout}
                className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
              >
                Déconnexion
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg p-8">
            <h2 className="text-2xl font-bold mb-4">🎉 CONNEXION RÉUSSIE !</h2>
            <p className="text-gray-600 mb-4">
              Bienvenue dans le dashboard admin simplifié !
            </p>
            
            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
              <strong>Utilisateur connecté :</strong> {user?.full_name} ({user?.email})
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
              <div className="bg-blue-100 p-4 rounded">
                <h3 className="font-semibold">Professionnels</h3>
                <p className="text-2xl font-bold">12</p>
              </div>
              <div className="bg-green-100 p-4 rounded">
                <h3 className="font-semibold">Utilisateurs</h3>
                <p className="text-2xl font-bold">156</p>
              </div>
              <div className="bg-yellow-100 p-4 rounded">
                <h3 className="font-semibold">Analyses</h3>
                <p className="text-2xl font-bold">342</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
