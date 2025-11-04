/**
 * API configuration and client for backend communication
 * Updated: 2025-01-27 - Improved error handling for 403 responses with fallback message
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

console.log('🌐 API_BASE_URL configuré:', API_BASE_URL);
console.log('🌐 NEXT_PUBLIC_API_URL depuis env:', process.env.NEXT_PUBLIC_API_URL);

export class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
    this.token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;
    console.log('🔧 ApiClient initialisé avec baseUrl:', this.baseUrl);
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    console.log('🔵 [REQUEST] Début de la méthode request')
    console.log('🔵 [REQUEST] endpoint:', endpoint)
    console.log('🔵 [REQUEST] options:', options)
    
    const url = `${this.baseUrl}${endpoint}`;
    console.log('🔵 [REQUEST] URL construite:', url)
    
    // Récupérer le token à chaque requête pour s'assurer qu'il est à jour
    const currentToken = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;
    
    console.log(`🌐 Requête API: ${url}`);
    console.log(`🔑 Token présent: ${!!currentToken}`);
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (currentToken) {
      (headers as any).Authorization = `Bearer ${currentToken}`;
    }

    try {
      console.log(`🚀 Début de la requête fetch vers: ${url}`);
      console.log(`📋 Options de requête:`, { method: options.method, body: options.body });
      console.log(`📋 Headers de requête:`, headers);
      
      // Pour les requêtes POST, s'assurer que le body est bien un string JSON
      const fetchOptions: RequestInit = {
        ...options,
        headers,
      };
      
      // Pour POST/PUT/PATCH, gérer le body
      // Si c'est déjà une string (JSON stringified), l'utiliser tel quel
      // Si c'est un objet, le convertir en JSON
      if (options.body) {
        if (typeof options.body === 'string') {
          // Déjà stringifié, utiliser tel quel
          fetchOptions.body = options.body;
        } else if (typeof options.body === 'object' && !(options.body instanceof FormData)) {
          // Objet à convertir en JSON
          fetchOptions.body = JSON.stringify(options.body);
        } else {
          // FormData ou autre, utiliser tel quel
          fetchOptions.body = options.body;
        }
      }
      
      // Ajouter un timeout de 5 minutes (300 secondes) pour les analyses de mammographie avec ML
      // Les analyses peuvent prendre du temps, surtout avec plusieurs images
      const timeoutDuration = endpoint.includes('/analyze') || endpoint.includes('/analysis') ? 300000 : 60000;
      const controller = new AbortController();
      const timeoutId = setTimeout(() => {
        console.error(`⏱️ TIMEOUT: La requête vers ${url} dépasse ${timeoutDuration / 1000} secondes`);
        controller.abort();
      }, timeoutDuration);
      
      console.log(`📤 Envoi de la requête...`);
      console.log(`📤 Body final:`, fetchOptions.body);
      console.log(`📤 Method:`, fetchOptions.method);
      
      let response;
      try {
        response = await fetch(url, {
          ...fetchOptions,
          signal: controller.signal,
        });
        console.log(`✅ Fetch complété, status: ${response.status}`);
      } catch (fetchError: any) {
        console.error(`❌ Erreur fetch:`, fetchError);
        clearTimeout(timeoutId);
        throw fetchError;
      }
      
      clearTimeout(timeoutId);
      
      console.log(`📡 Réponse reçue: ${response.status} ${response.statusText}`);
      console.log(`📡 Headers de réponse:`, Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        // NOUVEAU CODE - Lire d'abord le texte puis parser
        const statusCode = response.status;
        let errorDetail = `HTTP ${statusCode}`;
        let error: any = {};
        
        try {
          // Lire le texte brut de la réponse
          const responseText = await response.clone().text();
          console.log(`📄 Corps de la réponse brute (${statusCode}):`, responseText);
          console.log(`📄 Longueur du corps:`, responseText ? responseText.length : 0);
          
          if (responseText && responseText.trim()) {
            try {
              // Essayer de parser en JSON
              error = JSON.parse(responseText);
              console.log(`📋 Erreur parsée:`, error);
            } catch (parseError) {
              // Si ce n'est pas du JSON, utiliser le texte comme message
              console.log(`⚠️  Réponse n'est pas du JSON, utilisation du texte brut`);
              error = { detail: responseText };
            }
          } else {
            console.log(`⚠️  Réponse vide ou null pour le code ${statusCode}`);
          }
        } catch (readError) {
          console.error('❌ Erreur lors de la lecture de la réponse:', readError);
          error = { detail: 'Erreur lors de la lecture de la réponse du serveur' };
        }
        
        // Extraction du message d'erreur
        if (statusCode === 403) {
          // Pour les erreurs 403, utiliser le message du backend ou un message par défaut
          if (error.detail) {
            errorDetail = typeof error.detail === 'string' ? error.detail : JSON.stringify(error.detail);
          } else if (error.message) {
            errorDetail = error.message;
          } else {
            // Fallback pour les réponses vides
            errorDetail = 'Accès refusé. Les administrateurs doivent se connecter via la plateforme admin (/admin/login).';
          }
          
          // Pour les 403 (comportement attendu pour admin sur mobile), log moins verbeux
          console.log(`ℹ️  Accès refusé (comportement attendu pour admin sur mobile): ${errorDetail}`);
        } else if (error.detail) {
          errorDetail = typeof error.detail === 'string' ? error.detail : JSON.stringify(error.detail);
        } else if (error.message) {
          errorDetail = error.message;
        } else if (typeof error === 'string') {
          errorDetail = error;
        }
        
        // Seulement logger les vraies erreurs, pas les 403 attendus
        if (statusCode !== 403) {
          console.error(`❌ Erreur API (${statusCode}):`, error);
          console.log(`🔍 Message d'erreur final:`, errorDetail);
        }
        
        throw new Error(errorDetail);
      }

      const data = await response.json();
      console.log(`✅ Données reçues:`, data);
      return data;
    } catch (error: any) {
      console.error(`❌ Erreur de requête:`, error);
      console.error(`❌ Type d'erreur:`, error?.constructor?.name);
      console.error(`❌ Détails de l'erreur:`, {
        message: error?.message,
        stack: error?.stack,
        name: error?.name
      });
      
      // Gérer différents types d'erreurs
      if (error instanceof TypeError && (error.message.includes('fetch') || error.message.includes('Failed to fetch'))) {
        const networkError = 'Erreur de connexion au serveur. Impossible d\'établir la connexion.\n\n' +
          'Vérifications:\n' +
          '1. Le backend est-il démarré ? Ouvrez un terminal et exécutez:\n' +
          '   cd backend\n' +
          '   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000\n\n' +
          '2. Testez dans votre navigateur: http://localhost:8000/health\n' +
          '   Vous devriez voir: {"status": "healthy", "service": "breastcare-api"}\n\n' +
          '3. Vérifiez que le port 8000 n\'est pas utilisé par un autre programme';
        throw new Error(networkError);
      }
      
      // Gérer les erreurs de timeout (AbortError)
      if (error?.name === 'AbortError' || error?.message?.includes('aborted')) {
        const timeoutError = `Timeout: Le serveur ne répond pas après 60 secondes.\n\n` +
          `Vérifications à faire:\n` +
          `1. Le backend est-il démarré ? (cd backend && python -m uvicorn app.main:app --reload)\n` +
          `2. Le backend écoute-t-il sur http://localhost:8000 ?\n` +
          `3. Y a-t-il des erreurs dans les logs du backend ?\n` +
          `4. Le backend est-il en train de charger des modèles ML ? (première requête peut être lente)\n\n` +
          `Testez: http://localhost:8000/health dans votre navigateur`;
        throw new Error(timeoutError);
      }
      
      // Si c'est déjà une Error avec un message, la relancer
      if (error instanceof Error) {
        throw error;
      }
      
      // Sinon, wrapper dans une Error
      throw new Error(`Erreur inattendue: ${String(error)}`);
    }
  }

  // Authentication endpoints
  async login(email: string, password: string, source?: string) {
    try {
      console.log('🔵 [LOGIN] Début de la méthode login')
      const loginData = { email, password, ...(source && { source }) }
      console.log('📤 Envoi de la requête de connexion:', { email, password: '***', source })
      console.log('📤 Body JSON:', JSON.stringify(loginData))
      
      console.log('🔵 [LOGIN] Appel de this.request...')
      
      // Utiliser JSON.stringify explicitement pour garantir que le body est bien formaté
      const response = await this.request<{ access_token: string; token_type: string }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify(loginData), // Stringifier explicitement
      });
      
      console.log('🔵 [LOGIN] Réponse reçue:', response)
      
      if (!response || !response.access_token) {
        throw new Error('Réponse invalide du serveur: token manquant')
      }
      
      this.token = response.access_token;
      if (typeof window !== 'undefined') {
        localStorage.setItem('auth_token', response.access_token);
        console.log('✅ Token sauvegardé dans localStorage')
      }
      
      return response;
    } catch (error) {
      console.error('🔴 [LOGIN] Erreur dans login:', error)
      throw error
    }
  }

  async logout() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  async getCurrentUser() {
    return this.request('/auth/me');
  }

  // Admin endpoints
  async getDashboardStats() {
    return this.request('/admin/dashboard/stats');
  }

  async updateAccessRequest(requestId: string, status: string, rejectionReason?: string) {
    return this.request(`/admin/access-requests/${requestId}`, {
      method: 'PUT',
      body: JSON.stringify({ status, admin_notes: rejectionReason }),
    });
  }

  async getUsers(userType?: string, status?: string, skip = 0, limit = 100) {
    const params = new URLSearchParams();
    if (userType) params.append('user_type', userType);
    if (status) params.append('status', status);
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());
    
    return this.request(`/admin/users?${params}`);
  }

  async updateUserStatus(userId: string, isActive: boolean) {
    return this.request(`/admin/users/${userId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ is_active: isActive }),
    });
  }

  async getSystemStats(period = '30d') {
    return this.request(`/admin/system-stats?period=${period}`);
  }

  async getRecentActivity(limit = 50) {
    return this.request(`/admin/recent-activity?limit=${limit}`);
  }

  async getAnalysesSummary(startDate?: string, endDate?: string) {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    
    return this.request(`/admin/analyses/summary?${params}`);
  }

  // Mammography endpoints
  async analyzeMammography(files: File[], patientId?: string) {
    const formData = new FormData();
    files.forEach((file, index) => {
      formData.append('files', file);
    });
    if (patientId) {
      formData.append('patient_id', patientId);
    }

    const response = await fetch(`${this.baseUrl}/mammography/analyze`, {
      method: 'POST',
      headers: {
        Authorization: this.token ? `Bearer ${this.token}` : '',
      },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Network error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Professional endpoints
  async getProfessionals(skip = 0, limit = 100, specialty?: string) {
    const params = new URLSearchParams();
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());
    if (specialty) params.append('specialty', specialty);
    
    return this.request(`/professionals?${params}`);
  }

  async getProfessional(professionalId: string) {
    return this.request(`/professionals/${professionalId}`);
  }

  async createProfessional(professionalData: any) {
    return this.request('/professionals', {
      method: 'POST',
      body: JSON.stringify(professionalData),
    });
  }

  async updateProfessional(professionalId: string, professionalData: any) {
    return this.request(`/professionals/${professionalId}`, {
      method: 'PUT',
      body: JSON.stringify(professionalData),
    });
  }

  async deleteProfessional(professionalId: string) {
    return this.request(`/professionals/${professionalId}`, {
      method: 'DELETE',
    });
  }

  async getProfessionalsNearby(latitude: number, longitude: number, radius = 50, specialty = 'radiology') {
    return this.request(`/professionals/nearby?latitude=${latitude}&longitude=${longitude}&radius_km=${radius}&specialty=${specialty}`);
  }

  // Professional endpoints
  async getCurrentProfessional() {
    return this.request('/professionals/me');
  }

  // Professional dashboard endpoints
  async getProfessionalDashboardStats() {
    return this.request('/real-dashboard-stats');
  }

  async getRecentAnalyses(limit = 10) {
    return this.request(`/real-recent-analyses?limit=${limit}`);
  }

  async getProfessionalAlerts() {
    return this.request('/real-alerts');
  }

  // Professional reports endpoints
  async getProfessionalReports(skip = 0, limit = 50, search?: string, status?: string) {
    // Utiliser les vraies données des rapports depuis la DB
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (status) params.append('status', status);
    
    const queryString = params.toString();
    const url = queryString ? `/real-reports?${queryString}` : '/real-reports';
    return this.request(url);
  }

  // Patients endpoints
  async getRealPatients() {
    // Récupérer les vraies données des patients
    return this.request(`/real-patients`);
  }

  // Reports endpoints
  async getRealReports() {
    // Récupérer les vraies données des rapports depuis la DB
    return this.request(`/real-reports`);
  }

  async getProfessionalReport(reportId: string) {
    return this.request(`/professionals/reports/${reportId}`);
  }

  async downloadReport(reportId: string): Promise<Blob> {
    const url = `${this.baseUrl}/professionals/reports/${reportId}/download`;
    const currentToken = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;
    
    const headers: HeadersInit = {};
    if (currentToken) {
      headers['Authorization'] = `Bearer ${currentToken}`;
    }
    
    const response = await fetch(url, {
      method: 'POST',
      headers,
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Erreur lors du téléchargement du rapport' }));
      throw new Error(errorData.detail || `HTTP ${response.status}`);
    }
    
    return await response.blob();
  }

  // Patient endpoints
  async createPatient(patientData: any) {
    return this.request('/patients', {
      method: 'POST',
      body: JSON.stringify(patientData),
    });
  }

  async getPatients(skip = 0, limit = 100) {
    return this.request(`/patients?skip=${skip}&limit=${limit}`);
  }

  // Access request endpoints
  async createAccessRequest(requestData: any) {
    return this.request('/access-requests', {
      method: 'POST',
      body: JSON.stringify(requestData),
    });
  }

  async getAccessRequests(status?: string, skip = 0, limit = 100) {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());
    
    return this.request(`/access-requests?${params}`);
  }

  // Risk assessment endpoints - Modèle Gail
  async calculateRiskAssessment(riskData: {
    age: number;
    first_degree_relatives: number;
    previous_biopsies: number;
    atypical_hyperplasia: boolean;
    age_menarche: string;
    age_first_birth: string;
    weight_kg?: number;
    height_cm?: number;
    alcohol_consumption?: number;
    exercise_minutes_per_week?: number;
    smoking_status?: string;
    hormone_therapy?: boolean;
  }) {
    return this.request('/risk/calculate', {
      method: 'POST',
      body: JSON.stringify(riskData),
    });
  }

  async calculateAndSaveRiskAssessment(riskData: {
    age: number;
    first_degree_relatives: number;
    previous_biopsies: number;
    atypical_hyperplasia: boolean;
    age_menarche: string;
    age_first_birth: string;
    weight_kg?: number;
    height_cm?: number;
    alcohol_consumption?: number;
    exercise_minutes_per_week?: number;
    smoking_status?: string;
    hormone_therapy?: boolean;
  }) {
    return this.request('/risk/calculate-and-save', {
      method: 'POST',
      body: JSON.stringify(riskData),
    });
  }

  async getMyRiskAssessments(skip = 0, limit = 100) {
    const params = new URLSearchParams();
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());
    
    return this.request(`/risk/my-assessments?${params}`);
  }

  async getRiskAssessment(assessmentId: string) {
    return this.request(`/risk/assessments/${assessmentId}`);
  }

  // Healthcare Centers endpoints
  async getHealthcareCenters(params?: {
    skip?: number;
    limit?: number;
    city?: string;
    service?: string;
    latitude?: number;
    longitude?: number;
    radius_km?: number;
    is_available?: boolean;
    is_verified?: boolean;
  }) {
    const queryParams = new URLSearchParams();
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.city) queryParams.append('city', params.city);
    if (params?.service) queryParams.append('service', params.service);
    if (params?.latitude) queryParams.append('latitude', params.latitude.toString());
    if (params?.longitude) queryParams.append('longitude', params.longitude.toString());
    if (params?.radius_km) queryParams.append('radius_km', params.radius_km.toString());
    if (params?.is_available !== undefined) queryParams.append('is_available', params.is_available.toString());
    if (params?.is_verified !== undefined) queryParams.append('is_verified', params.is_verified.toString());
    
    return this.request<{ centers: HealthcareCenter[]; total: number; skip: number; limit: number }>(
      `/healthcare-centers/?${queryParams}`
    );
  }

  async getHealthcareCenter(centerId: string) {
    return this.request<HealthcareCenter>(`/healthcare-centers/${centerId}`);
  }

  async searchNearbyCenters(latitude: number, longitude: number, radius_km: number = 50, service?: string) {
    const queryParams = new URLSearchParams();
    queryParams.append('latitude', latitude.toString());
    queryParams.append('longitude', longitude.toString());
    queryParams.append('radius_km', radius_km.toString());
    if (service) queryParams.append('service', service);
    
    return this.request<{ centers: Array<{ center: HealthcareCenter; distance_km: number }>; total: number }>(
      `/healthcare-centers/nearby/search?${queryParams}`
    );
  }

  // Appointments API
  async createAppointment(appointment: {
    center_id: string;
    patient_name: string;
    patient_phone: string;
    patient_email?: string;
    appointment_date: string;
    appointment_time: string;
    notes?: string;
  }) {
    return this.request<Appointment>(`/appointments/`, {
      method: 'POST',
      body: JSON.stringify(appointment),
    });
  }

  async getAppointments(params?: {
    center_id?: string;
    status?: string;
    skip?: number;
    limit?: number;
  }) {
    const queryParams = new URLSearchParams();
    if (params?.center_id) queryParams.append('center_id', params.center_id);
    if (params?.status) queryParams.append('status', params.status);
    if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
    
    const queryString = queryParams.toString();
    const url = `/appointments/${queryString ? `?${queryString}` : ''}`;
    
    return this.request<{
      appointments: Appointment[];
      total: number;
      skip: number;
      limit: number;
    }>(url);
  }

  async getAppointment(appointmentId: string) {
    return this.request<Appointment>(`/appointments/${appointmentId}`);
  }

  // Mobile signup API
  async mobileSignup(userData: {
    name: string;
    email: string;
    phone: string;
    password: string;
  }) {
    return this.request<User>(`/auth/mobile-signup`, {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }
}

// Export singleton instance
export const apiClient = new ApiClient();

// Export types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login?: string;
  user_type?: string;
}

export interface DashboardStats {
  total_users: number;
  active_users: number;
  pending_users: number;
  total_professionals: number;
  active_professionals: number;
  pending_professionals: number;
  total_analyses: number;
  analyses_today: number;
  analyses_this_week: number;
  analyses_this_month: number;
  high_risk_cases: number;
  pending_access_requests: number;
  system_uptime: string;
  last_backup?: string;
}

export interface AccessRequest {
  id: string;
  full_name: string;
  email: string;
  phone_number?: string;
  license_number: string;
  specialty: string;
  hospital_clinic: string;
  experience_years: string;
  motivation: string;
  additional_info?: string;
  status: 'pending' | 'approved' | 'rejected';
  reviewed_by?: string;
  reviewed_at?: string;
  admin_notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface Professional {
  id: string;
  full_name: string;
  specialty: string;
  license_number: string;
  phone_number?: string;
  email?: string;
  address?: string;
  latitude?: number;
  longitude?: number;
  consultation_fee?: number;
  languages?: string[];
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at?: string;
}

export interface ProfessionalCreate {
  full_name: string;
  specialty: string;
  license_number: string;
  phone_number?: string;
  email?: string;
  address?: string;
  latitude?: number;
  longitude?: number;
  consultation_fee?: number;
  languages?: string[];
}

export interface ProfessionalUpdate {
  full_name?: string;
  specialty?: string;
  license_number?: string;
  phone_number?: string;
  email?: string;
  address?: string;
  latitude?: number;
  longitude?: number;
  consultation_fee?: number;
  languages?: string[];
}

export interface HealthcareCenter {
  id: string;
  name: string;
  type: string;
  address: string;
  city: string;
  department?: string;
  latitude: number;
  longitude: number;
  phone_number?: string;
  email?: string;
  website?: string;
  services?: string[];
  equipment?: string[];
  specialties?: string[];
  operating_hours?: Record<string, string>;
  description?: string;
  languages_spoken?: string[];
  rating: number;
  total_reviews: number;
  is_available: boolean;
  is_verified: boolean;
  accepts_appointments: boolean;
  max_appointments_per_day: number;
  created_at: string;
  updated_at?: string;
}

export interface Appointment {
  id: string;
  center_id: string;
  user_id?: string;
  patient_name: string;
  patient_phone: string;
  patient_email?: string;
  appointment_date: string;
  appointment_time: string;
  notes?: string;
  status: string;
  confirmation_code?: string;
  cancelled_at?: string;
  cancellation_reason?: string;
  created_at: string;
  updated_at?: string;
}
