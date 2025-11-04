"use client"

import { useState, useEffect } from "react"

export default function WorkingDashboardPage() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('auth_token')
      if (!token) {
        window.location.href = "/admin/working-login"
        return
      }

      try {
        const response = await fetch('http://localhost:8000/api/v1/auth/me', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.ok) {
          const userData = await response.json()
          setUser(userData)
        } else {
          localStorage.removeItem('auth_token')
          window.location.href = "/admin/working-login"
        }
      } catch (err) {
        localStorage.removeItem('auth_token')
        window.location.href = "/admin/working-login"
      } finally {
        setLoading(false)
      }
    }

    checkAuth()
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('auth_token')
    window.location.href = "/admin/working-login"
  }

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f3f4f6'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{
            width: '40px',
            height: '40px',
            border: '4px solid #e5e7eb',
            borderTop: '4px solid #3b82f6',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 1rem'
          }}></div>
          <p>Chargement...</p>
        </div>
      </div>
    )
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f3f4f6' }}>
      {/* Header */}
      <div style={{
        backgroundColor: 'white',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
        marginBottom: '2rem'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          padding: '1rem 2rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1f2937' }}>
            🎉 Dashboard Admin - FONCTIONNEL
          </h1>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <span style={{ color: '#6b7280' }}>
              Connecté: {user?.email}
            </span>
            <button
              onClick={handleLogout}
              style={{
                backgroundColor: '#dc2626',
                color: 'white',
                padding: '0.5rem 1rem',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Déconnexion
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 2rem' }}>
        <div style={{
          backgroundColor: 'white',
          borderRadius: '8px',
          padding: '2rem',
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
        }}>
          <h2 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '1rem', color: '#1f2937' }}>
            ✅ CONNEXION RÉUSSIE !
          </h2>
          <p style={{ color: '#6b7280', marginBottom: '2rem' }}>
            Bienvenue dans le dashboard admin qui fonctionne parfaitement !
          </p>
          
          <div style={{
            backgroundColor: '#dcfce7',
            border: '1px solid #bbf7d0',
            color: '#166534',
            padding: '1rem',
            borderRadius: '4px',
            marginBottom: '2rem'
          }}>
            <strong>Utilisateur connecté :</strong> {user?.full_name} ({user?.email})
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '1rem'
          }}>
            <div style={{
              backgroundColor: '#dbeafe',
              padding: '1.5rem',
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <h3 style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>Professionnels</h3>
              <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1d4ed8' }}>12</p>
            </div>
            
            <div style={{
              backgroundColor: '#dcfce7',
              padding: '1.5rem',
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <h3 style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>Utilisateurs</h3>
              <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#16a34a' }}>156</p>
            </div>
            
            <div style={{
              backgroundColor: '#fef3c7',
              padding: '1.5rem',
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <h3 style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>Analyses</h3>
              <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#d97706' }}>342</p>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}
