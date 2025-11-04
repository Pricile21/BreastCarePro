"""
Healthcare Centers endpoints for listing screening facilities
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
import math

from app.api.deps import get_db
from app.models.healthcare_center import HealthcareCenter
from app.schemas.healthcare_center import (
    HealthcareCenterResponse,
    HealthcareCenterListResponse,
    HealthcareCenterCreate,
    HealthcareCenterUpdate
)

router = APIRouter()


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates in kilometers (Haversine formula)"""
    R = 6371  # Earth radius in kilometers
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


@router.get("/", response_model=HealthcareCenterListResponse)
async def list_healthcare_centers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    city: Optional[str] = None,
    service: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_km: Optional[float] = Query(None, ge=0, le=100),
    is_available: Optional[bool] = None,
    is_verified: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    List healthcare centers with optional filtering and location-based search
    """
    try:
        print(f"📋 Liste des centres demandée. skip={skip}, limit={limit}, is_available={is_available}")
        query = db.query(HealthcareCenter)
        
        # Filters
        if city:
            query = query.filter(HealthcareCenter.city.ilike(f"%{city}%"))
        
        if service:
            # Filter by service (JSON array contains)
            query = query.filter(HealthcareCenter.services.contains([service]))
        
        if is_available is not None:
            query = query.filter(HealthcareCenter.is_available == is_available)
        
        if is_verified is not None:
            query = query.filter(HealthcareCenter.is_verified == is_verified)
        
        # Location-based filtering
        if latitude and longitude and radius_km:
            # For now, get all and filter in Python (can be optimized with PostGIS)
            centers = query.all()
            nearby_centers = []
            for center in centers:
                if center.latitude and center.longitude:
                    distance = calculate_distance(
                        latitude, longitude,
                        center.latitude, center.longitude
                    )
                    if distance <= radius_km:
                        nearby_centers.append(center)
            
            total = len(nearby_centers)
            centers_list = nearby_centers[skip:skip + limit]
            
            # Convert datetime to string manually
            from datetime import datetime
            centers_data = []
            for center in centers_list:
                center_dict = {
                    **center.__dict__,
                    'created_at': center.created_at.isoformat() if isinstance(center.created_at, datetime) else str(center.created_at),
                    'updated_at': center.updated_at.isoformat() if isinstance(center.updated_at, datetime) else (str(center.updated_at) if center.updated_at else None)
                }
                centers_data.append(HealthcareCenterResponse(**center_dict))
            
            return HealthcareCenterListResponse(
                centers=centers_data,
                total=total,
                skip=skip,
                limit=limit
            )
        else:
            # Standard pagination
            total = query.count()
            print(f"📊 Total centres dans la base: {total}")
            centers = query.offset(skip).limit(limit).all()
            print(f"✅ Retour de {len(centers)} centres")
            
            # Convert datetime to string manually
            from datetime import datetime
            centers_data = []
            for center in centers:
                center_dict = {
                    **center.__dict__,
                    'created_at': center.created_at.isoformat() if isinstance(center.created_at, datetime) else str(center.created_at),
                    'updated_at': center.updated_at.isoformat() if isinstance(center.updated_at, datetime) else (str(center.updated_at) if center.updated_at else None)
                }
                centers_data.append(HealthcareCenterResponse(**center_dict))
            
            return HealthcareCenterListResponse(
                centers=centers_data,
                total=total,
                skip=skip,
                limit=limit
            )
    except Exception as e:
        print(f"❌ Erreur dans list_healthcare_centers: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/{center_id}", response_model=HealthcareCenterResponse)
async def get_healthcare_center(
    center_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific healthcare center by ID"""
    center = db.query(HealthcareCenter).filter(HealthcareCenter.id == center_id).first()
    
    if not center:
        raise HTTPException(status_code=404, detail="Healthcare center not found")
    
    # Convert datetime to string manually
    from datetime import datetime
    center_dict = {
        **center.__dict__,
        'created_at': center.created_at.isoformat() if isinstance(center.created_at, datetime) else str(center.created_at),
        'updated_at': center.updated_at.isoformat() if isinstance(center.updated_at, datetime) else (str(center.updated_at) if center.updated_at else None)
    }
    
    return HealthcareCenterResponse(**center_dict)


@router.get("/nearby/search")
async def search_nearby_centers(
    latitude: float,
    longitude: float,
    radius_km: float = Query(50, ge=0, le=100),
    service: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Search for centers near a location with distance calculation
    Returns centers with distance in kilometers
    """
    centers = db.query(HealthcareCenter).filter(HealthcareCenter.is_available == True)
    
    if service:
        centers = centers.filter(HealthcareCenter.services.contains([service]))
    
    centers = centers.all()
    
    results = []
    for center in centers:
        if center.latitude and center.longitude:
            distance = calculate_distance(
                latitude, longitude,
                center.latitude, center.longitude
            )
            
            if distance <= radius_km:
                center_data = HealthcareCenterResponse.model_validate(center)
                results.append({
                    "center": center_data,
                    "distance_km": round(distance, 1)
                })
    
    # Sort by distance
    results.sort(key=lambda x: x["distance_km"])
    
    return {"centers": results, "total": len(results)}


@router.post("/", response_model=HealthcareCenterResponse)
async def create_healthcare_center(
    center_data: HealthcareCenterCreate,
    db: Session = Depends(get_db)
):
    """Create a new healthcare center (Admin only - add auth later)"""
    import uuid
    
    center = HealthcareCenter(
        id=str(uuid.uuid4()),
        **center_data.model_dump()
    )
    
    db.add(center)
    db.commit()
    db.refresh(center)
    
    return center


@router.put("/{center_id}", response_model=HealthcareCenterResponse)
async def update_healthcare_center(
    center_id: str,
    center_update: HealthcareCenterUpdate,
    db: Session = Depends(get_db)
):
    """Update healthcare center information (Admin only - add auth later)"""
    center = db.query(HealthcareCenter).filter(HealthcareCenter.id == center_id).first()
    
    if not center:
        raise HTTPException(status_code=404, detail="Healthcare center not found")
    
    update_data = center_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(center, key, value)
    
    db.commit()
    db.refresh(center)
    
    return center

