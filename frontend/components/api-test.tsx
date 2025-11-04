"use client"

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { apiClient } from '@/lib/api'

export function ApiTestComponent() {
  const [testResults, setTestResults] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const testApiConnection = async () => {
    setLoading(true)
    setTestResults(null)
    
    try {
      console.log("🧪 Test de connexion API...")
      
      // Test 1: Health check
      const healthResponse = await fetch('http://localhost:8000/health')
      const healthData = await healthResponse.json()
      
      // Test 2: Auth check
      const token = localStorage.getItem('auth_token')
      
      // Test 3: Auth me endpoint
      let authData = null
      if (token) {
        try {
          const authResponse = await fetch('http://localhost:8000/api/v1/auth/me', {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          })
          if (authResponse.ok) {
            authData = await authResponse.json()
          } else {
            authData = { error: `HTTP ${authResponse.status}: ${authResponse.statusText}` }
          }
        } catch (error) {
          authData = { error: error instanceof Error ? error.message : 'Unknown error' }
        }
      }
      
      // Test 4: Professional dashboard stats
      let dashboardData = null
      if (token) {
        try {
          dashboardData = await apiClient.getProfessionalDashboardStats()
        } catch (error) {
          console.error("Erreur dashboard:", error)
          dashboardData = { error: error instanceof Error ? error.message : 'Unknown error' }
        }
      }
      
      setTestResults({
        health: healthData,
        token: !!token,
        tokenValue: token ? token.substring(0, 20) + '...' : null,
        auth: authData,
        dashboard: dashboardData,
        timestamp: new Date().toISOString()
      })
      
    } catch (error) {
      setTestResults({
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Test de Connexion API</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex gap-2">
          <Button 
            onClick={testApiConnection} 
            disabled={loading}
            className="flex-1"
          >
            {loading ? "Test en cours..." : "Tester la connexion API"}
          </Button>
          <Button 
            onClick={() => window.location.reload()} 
            variant="outline"
            className="flex-1"
          >
            Recharger la page
          </Button>
        </div>
        
        {testResults && (
          <div className="mt-4 p-4 bg-gray-100 rounded-lg">
            <h3 className="font-semibold mb-2">Résultats du test :</h3>
            <pre className="text-xs overflow-auto">
              {JSON.stringify(testResults, null, 2)}
            </pre>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
