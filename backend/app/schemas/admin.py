"""
Admin dashboard schemas
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class AdminDashboardStats(BaseModel):
    """Admin dashboard statistics"""
    total_users: int
    active_users: int
    pending_users: int
    total_professionals: int
    active_professionals: int
    pending_professionals: int
    total_analyses: int
    analyses_today: int
    analyses_this_week: int
    analyses_this_month: int
    high_risk_cases: int
    pending_access_requests: int
    system_uptime: str
    last_backup: Optional[datetime] = None


class AccessRequestResponse(BaseModel):
    """Access request response"""
    id: str
    professional_name: str
    email: str
    specialty: str
    license_number: str
    phone_number: str
    address: str
    status: str  # pending, approved, rejected
    requested_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None
    rejection_reason: Optional[str] = None
    documents: List[str] = []


class AccessRequestCreate(BaseModel):
    """Create access request"""
    professional_name: str
    email: str
    specialty: str
    license_number: str
    phone_number: str
    address: str
    documents: List[str] = []


class AccessRequestUpdate(BaseModel):
    """Update access request"""
    status: str  # approved, rejected
    admin_notes: Optional[str] = None


class UserManagementResponse(BaseModel):
    """User management response"""
    id: str
    email: str
    full_name: str
    user_type: str  # admin, professional, patient
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    total_analyses: Optional[int] = 0
    specialty: Optional[str] = None


class ProfessionalManagementResponse(BaseModel):
    """Professional management response"""
    id: str
    full_name: str
    email: str
    specialty: str
    license_number: str
    phone_number: str
    address: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    total_analyses: int
    consultation_fee: float
    languages: List[str] = []


class SystemStatsResponse(BaseModel):
    """System statistics response"""
    period: str
    total_users: int
    new_users: int
    total_analyses: int
    new_analyses: int
    high_risk_detections: int
    system_performance: Dict[str, Any]
    storage_usage: Dict[str, Any]
    api_usage: Dict[str, Any]


class RecentActivityResponse(BaseModel):
    """Recent activity response"""
    id: str
    activity_type: str  # user_registration, analysis_completed, access_request, etc.
    description: str
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    timestamp: datetime
    metadata: Dict[str, Any] = {}


class NotificationResponse(BaseModel):
    """Notification response"""
    id: str
    title: str
    message: str
    notification_type: str  # info, warning, error, success
    is_read: bool
    created_at: datetime
    metadata: Dict[str, Any] = {}


class ReportExportResponse(BaseModel):
    """Report export response"""
    report_type: str
    format: str
    data: List[Dict[str, Any]]
    generated_at: datetime
    total_records: int


class AnalysisSummaryResponse(BaseModel):
    """Analysis summary response"""
    total_analyses: int
    high_risk_cases: int
    medium_risk_cases: int
    low_risk_cases: int
    bi_rads_distribution: Dict[str, int]
    density_distribution: Dict[str, int]
    average_confidence: float
    top_findings: List[Dict[str, Any]]
    period: str
