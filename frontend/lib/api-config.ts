/**
 * Configuration de l'API backend
 */

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
export const API_V1_BASE = `${API_BASE_URL}/api/v1`

export const API_ENDPOINTS = {
  articles: `${API_V1_BASE}/articles`,
  article: (id: string) => `${API_V1_BASE}/articles/${id}`,
  riskAssessment: `${API_V1_BASE}/risk/calculate`,
  mammography: `${API_V1_BASE}/mammography`,
  patients: `${API_V1_BASE}/patients`,
  professionals: `${API_V1_BASE}/professionals`,
} as const

