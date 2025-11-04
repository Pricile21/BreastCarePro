"""
Admin dashboard endpoints
"""

from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.professional import Professional
from app.models.patient import Patient
from app.models.mammography import MammographyAnalysis
from app.schemas.admin import (
    AdminDashboardStats,
    AccessRequestResponse,
    AccessRequestCreate,
    AccessRequestUpdate,
    UserManagementResponse,
    ProfessionalManagementResponse,
    SystemStatsResponse,
    RecentActivityResponse
)
from app.services.admin_service import AdminService

router = APIRouter()


@router.get("/dashboard/stats", response_model=AdminDashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get admin dashboard statistics
    """
    admin_service = AdminService(db)
    stats = admin_service.get_dashboard_stats()
    return stats


@router.get("/access-requests", response_model=List[AccessRequestResponse])
async def get_access_requests(
    status: Optional[str] = Query(None, description="Filter by status: pending, approved, rejected"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all access requests with optional filtering
    """
    admin_service = AdminService(db)
    requests = admin_service.get_access_requests(status=status, skip=skip, limit=limit)
    return requests


@router.post("/access-requests", response_model=AccessRequestResponse)
async def create_access_request(
    request_data: AccessRequestCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new access request (used by professionals)
    """
    admin_service = AdminService(db)
    request = admin_service.create_access_request(request_data)
    return request


@router.put("/access-requests/{request_id}", response_model=AccessRequestResponse)
async def update_access_request(
    request_id: str,
    request_update: AccessRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update access request status (approve/reject)
    """
    try:
        admin_service = AdminService(db)
        request = admin_service.update_access_request(request_id, request_update, current_user.id)
        
        if not request:
            raise HTTPException(status_code=404, detail="Access request not found")
        
        return request
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la demande: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")


@router.get("/users", response_model=List[UserManagementResponse])
async def get_users(
    user_type: Optional[str] = Query(None, description="Filter by user type: admin, professional, patient"),
    status: Optional[str] = Query(None, description="Filter by status: active, inactive, pending"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all users with management information
    """
    admin_service = AdminService(db)
    users = admin_service.get_users(user_type=user_type, status=status, skip=skip, limit=limit)
    return users


@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: str,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Activate/deactivate user account
    """
    admin_service = AdminService(db)
    success = admin_service.update_user_status(user_id, is_active, current_user.id)
    
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": f"User {'activated' if is_active else 'deactivated'} successfully"}


@router.get("/professionals", response_model=List[ProfessionalManagementResponse])
async def get_professionals_management(
    specialty: Optional[str] = Query(None, description="Filter by specialty"),
    status: Optional[str] = Query(None, description="Filter by status: active, inactive, pending"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all professionals with management information
    """
    admin_service = AdminService(db)
    professionals = admin_service.get_professionals_management(
        specialty=specialty, status=status, skip=skip, limit=limit
    )
    return professionals


@router.get("/system-stats", response_model=SystemStatsResponse)
async def get_system_stats(
    period: str = Query("30d", description="Time period: 7d, 30d, 90d, 1y"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get system-wide statistics
    """
    admin_service = AdminService(db)
    stats = admin_service.get_system_stats(period)
    return stats


@router.get("/recent-activity", response_model=List[RecentActivityResponse])
async def get_recent_activity(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get recent system activity
    """
    admin_service = AdminService(db)
    activities = admin_service.get_recent_activity(limit)
    return activities


@router.get("/analyses/summary")
async def get_analyses_summary(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get mammography analyses summary
    """
    admin_service = AdminService(db)
    summary = admin_service.get_analyses_summary(start_date, end_date)
    return summary


@router.get("/reports/export")
async def export_reports(
    report_type: str = Query("users", description="Report type: users, professionals, analyses"),
    format: str = Query("json", description="Export format: json, csv"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Export system reports
    """
    admin_service = AdminService(db)
    report_data = admin_service.export_reports(report_type, format, start_date, end_date)
    return report_data


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete user account (soft delete)
    """
    admin_service = AdminService(db)
    success = admin_service.delete_user(user_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}


@router.post("/users/{user_id}/reset-password")
async def reset_user_password(
    user_id: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Reset user password
    """
    admin_service = AdminService(db)
    success = admin_service.reset_user_password(user_id, new_password, current_user.id)
    
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "Password reset successfully"}


@router.get("/notifications")
async def get_admin_notifications(
    unread_only: bool = Query(False, description="Get only unread notifications"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get admin notifications
    """
    admin_service = AdminService(db)
    notifications = admin_service.get_admin_notifications(unread_only)
    return notifications


@router.put("/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark notification as read
    """
    admin_service = AdminService(db)
    success = admin_service.mark_notification_read(notification_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {"message": "Notification marked as read"}
