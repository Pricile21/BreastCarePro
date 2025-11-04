/**
 * React hooks for API communication
 */

import { useState, useEffect, useCallback } from 'react';
import { apiClient, type DashboardStats, type AccessRequest, type User } from '@/lib/api';

// Hook for authentication
export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const login = useCallback(async (username: string, password: string) => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.login(username, password);
      const userData = await apiClient.getCurrentUser();
      setUser(userData);
      return userData;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Login failed';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    await apiClient.logout();
    setUser(null);
  }, []);

  const checkAuth = useCallback(async () => {
    try {
      setLoading(true);
      // Vérifier d'abord si un token existe dans le localStorage
      const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;
      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }
      
      const userData = await apiClient.getCurrentUser();
      setUser(userData);
    } catch (err) {
      console.error("Erreur de vérification auth:", err);
      setUser(null);
      // Nettoyer le token invalide
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token');
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated: !!user,
  };
}

// Hook for admin dashboard
export function useAdminDashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.getDashboardStats();
      setStats(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch stats';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  return {
    stats,
    loading,
    error,
    refetch: fetchStats,
  };
}

// Hook for access requests
export function useAccessRequests(status?: string) {
  const [requests, setRequests] = useState<AccessRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRequests = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.getAccessRequests(status);
      setRequests(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch requests';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [status]);

  const updateRequest = useCallback(async (requestId: string, status: string, rejectionReason?: string) => {
    try {
      console.log(`Mise à jour demande ${requestId} vers statut: ${status}`);
      await apiClient.updateAccessRequest(requestId, status, rejectionReason);
      console.log(`Demande ${requestId} mise à jour avec succès`);
      await fetchRequests(); // Refresh the list
    } catch (err) {
      console.error(`Erreur lors de la mise à jour de la demande ${requestId}:`, err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to update request';
      setError(errorMessage);
      throw err;
    }
  }, [fetchRequests]);

  useEffect(() => {
    fetchRequests();
  }, [fetchRequests]);

  return {
    requests,
    loading,
    error,
    updateRequest,
    refetch: fetchRequests,
  };
}

// Hook for users management
export function useUsers(userType?: string, status?: string) {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchUsers = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.getUsers(userType, status);
      setUsers(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch users';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [userType, status]);

  const updateUserStatus = useCallback(async (userId: string, isActive: boolean) => {
    try {
      await apiClient.updateUserStatus(userId, isActive);
      await fetchUsers(); // Refresh the list
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update user';
      setError(errorMessage);
      throw err;
    }
  }, [fetchUsers]);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  return {
    users,
    loading,
    error,
    updateUserStatus,
    refetch: fetchUsers,
  };
}

// Hook for professionals management
export function useProfessionals(specialty?: string, status?: string) {
  const [professionals, setProfessionals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProfessionals = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.getProfessionals(specialty, status);
      setProfessionals(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch professionals';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [specialty, status]);

  useEffect(() => {
    fetchProfessionals();
  }, [fetchProfessionals]);

  return {
    professionals,
    loading,
    error,
    refetch: fetchProfessionals,
  };
}

// Hook for system statistics
export function useSystemStats(period = '30d') {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.getSystemStats(period);
      setStats(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch system stats';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [period]);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  return {
    stats,
    loading,
    error,
    refetch: fetchStats,
  };
}

// Hook for recent activity
export function useRecentActivity(limit = 50) {
  const [activities, setActivities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchActivities = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.getRecentActivity(limit);
      setActivities(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch activities';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [limit]);

  useEffect(() => {
    fetchActivities();
  }, [fetchActivities]);

  return {
    activities,
    loading,
    error,
    refetch: fetchActivities,
  };
}

// Hook for professional dashboard - VERSION SIMPLIFIÉE
export function useProfessionalDashboard() {
  const [stats, setStats] = useState<any>(null);
  const [analyses, setAnalyses] = useState<any[]>([]);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      console.log("🔄 Chargement des données du dashboard professionnel...");
      
      // Test des endpoints un par un pour identifier le problème
      console.log("📊 Test endpoint test...");
      try {
        const testData = await apiClient.request('/professionals/dashboard/test');
        console.log("✅ Test endpoint fonctionne:", testData);
      } catch (err) {
        console.error("❌ Erreur test endpoint:", err);
      }
      
      console.log("📊 Test endpoint stats...");
      const statsData = await apiClient.getProfessionalDashboardStats();
      console.log("✅ Stats chargées:", statsData);
      setStats(statsData);
      
      console.log("📊 Test endpoint analyses...");
      try {
        const analysesData = await apiClient.getRecentAnalyses(10);
        console.log("✅ Analyses chargées:", analysesData);
        setAnalyses(analysesData);
      } catch (err) {
        console.error("❌ Erreur analyses:", err);
        setAnalyses([]); // Valeur par défaut
      }
      
      console.log("📊 Test endpoint alerts...");
      try {
        const alertsData = await apiClient.getProfessionalAlerts();
        console.log("✅ Alerts chargées:", alertsData);
        setAlerts(alertsData);
      } catch (err) {
        console.error("❌ Erreur alerts:", err);
        setAlerts([]); // Valeur par défaut
      }
      
    } catch (err) {
      console.error("❌ Erreur lors du chargement du dashboard:", err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch dashboard data';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // Démarrer le chargement après un court délai
    const timer = setTimeout(() => {
      fetchDashboardData();
    }, 500);
    
    return () => clearTimeout(timer);
  }, [fetchDashboardData]);

  return {
    stats,
    analyses,
    alerts,
    loading,
    error,
    refetch: fetchDashboardData,
  };
}

// Hook for professional reports
export function useProfessionalReports(search?: string, status?: string) {
  const [reports, setReports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchReports = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.getProfessionalReports(0, 50, search, status);
      setReports(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch reports';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [search, status]);

  useEffect(() => {
    fetchReports();
  }, [fetchReports]);

  return {
    reports,
    loading,
    error,
    refetch: fetchReports,
  };
}

// Hook for real patients data
export function useRealPatients() {
  const [patients, setPatients] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPatients = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.getRealPatients();
      setPatients(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch patients';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchPatients();
  }, [fetchPatients]);

  return {
    patients,
    loading,
    error,
    refetch: fetchPatients,
  };
}

// Hook for current professional info
export function useCurrentProfessional() {
  const [professional, setProfessional] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProfessional = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Récupérer les vraies données du professionnel
      const professionalData = await apiClient.request('/real-professional');
      setProfessional(professionalData);
    } catch (err) {
      console.log("Erreur API, utilisation des données factices");
      // Fallback avec les bonnes données
      const mockProfessional = {
        id: "prof-123",
        full_name: "Dr GANGBE Pricile",
        specialty: "Nuclear Medicine",
        license_number: "MED123454",
        phone_number: "+2290161802144",
        email: "pricilegangbe@gmail.com",
        address: "CHU",
        is_active: true
      };
      setProfessional(mockProfessional);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProfessional();
  }, [fetchProfessional]);

  return {
    professional,
    loading,
    error,
    refetch: fetchProfessional,
  };
}
