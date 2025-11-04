"""
Appointments endpoints for booking and managing appointments
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.api.deps import get_db
from app.models.appointment import Appointment
from app.models.healthcare_center import HealthcareCenter
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentListResponse
)

router = APIRouter()


@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new appointment booking
    """
    # Verify center exists
    center = db.query(HealthcareCenter).filter(HealthcareCenter.id == appointment.center_id).first()
    if not center:
        raise HTTPException(status_code=404, detail="Healthcare center not found")
    
    if not center.is_available or not center.accepts_appointments:
        raise HTTPException(status_code=400, detail="This center is not accepting appointments")
    
    # Parse appointment date
    try:
        appointment_datetime = datetime.fromisoformat(appointment.appointment_date.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    # Check if date is in the future
    if appointment_datetime < datetime.now():
        raise HTTPException(status_code=400, detail="Appointment date must be in the future")
    
    # Generate confirmation code
    confirmation_code = f"APT-{uuid.uuid4().hex[:8].upper()}"
    
    # Create appointment
    db_appointment = Appointment(
        id=f"appt-{uuid.uuid4()}",
        center_id=appointment.center_id,
        patient_name=appointment.patient_name,
        patient_phone=appointment.patient_phone,
        patient_email=appointment.patient_email,
        appointment_date=appointment_datetime,
        appointment_time=appointment.appointment_time,
        notes=appointment.notes,
        status="pending",
        confirmation_code=confirmation_code,
        user_id=None  # TODO: Get from authentication when implemented
    )
    
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    
    # Convert to response format with proper datetime serialization
    from app.schemas.appointment import AppointmentResponse
    return AppointmentResponse(
        id=db_appointment.id,
        center_id=db_appointment.center_id,
        user_id=db_appointment.user_id,
        patient_name=db_appointment.patient_name,
        patient_phone=db_appointment.patient_phone,
        patient_email=db_appointment.patient_email,
        appointment_date=appointment_datetime.isoformat(),
        appointment_time=db_appointment.appointment_time,
        notes=db_appointment.notes,
        status=db_appointment.status,
        confirmation_code=db_appointment.confirmation_code,
        cancelled_at=db_appointment.cancelled_at.isoformat() if db_appointment.cancelled_at else None,
        cancellation_reason=db_appointment.cancellation_reason,
        created_at=db_appointment.created_at,
        updated_at=db_appointment.updated_at
    )


@router.get("/", response_model=AppointmentListResponse)
async def list_appointments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    center_id: str = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """
    List appointments with optional filtering
    """
    query = db.query(Appointment)
    
    if center_id:
        query = query.filter(Appointment.center_id == center_id)
    
    if status:
        query = query.filter(Appointment.status == status)
    
    total = query.count()
    appointments = query.offset(skip).limit(limit).all()
    
    # Convert to response format
    from datetime import datetime
    appointments_list = []
    for appt in appointments:
        appointments_list.append(AppointmentResponse(
            id=appt.id,
            center_id=appt.center_id,
            user_id=appt.user_id,
            patient_name=appt.patient_name,
            patient_phone=appt.patient_phone,
            patient_email=appt.patient_email,
            appointment_date=appt.appointment_date.isoformat() if appt.appointment_date else None,
            appointment_time=appt.appointment_time,
            notes=appt.notes,
            status=appt.status,
            confirmation_code=appt.confirmation_code,
            cancelled_at=appt.cancelled_at.isoformat() if appt.cancelled_at else None,
            cancellation_reason=appt.cancellation_reason,
            created_at=appt.created_at,
            updated_at=appt.updated_at
        ))
    
    return AppointmentListResponse(
        appointments=appointments_list,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific appointment by ID
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Convert to response format
    from datetime import datetime
    return AppointmentResponse(
        id=appointment.id,
        center_id=appointment.center_id,
        user_id=appointment.user_id,
        patient_name=appointment.patient_name,
        patient_phone=appointment.patient_phone,
        patient_email=appointment.patient_email,
        appointment_date=appointment.appointment_date.isoformat() if appointment.appointment_date else None,
        appointment_time=appointment.appointment_time,
        notes=appointment.notes,
        status=appointment.status,
        confirmation_code=appointment.confirmation_code,
        cancelled_at=appointment.cancelled_at.isoformat() if appointment.cancelled_at else None,
        cancellation_reason=appointment.cancellation_reason,
        created_at=appointment.created_at,
        updated_at=appointment.updated_at
    )

