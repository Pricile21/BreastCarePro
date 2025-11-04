"""
Access request endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.access_request_service import AccessRequestService
from app.schemas.access_request import AccessRequest, AccessRequestCreate, AccessRequestUpdate
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=AccessRequest, status_code=status.HTTP_201_CREATED)
async def create_access_request(
    request_data: AccessRequestCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new access request
    """
    try:
        service = AccessRequestService(db)
        access_request = service.create_access_request(request_data)
        return access_request
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating access request: {str(e)}"
        )


@router.get("/", response_model=List[AccessRequest])
async def get_access_requests(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get access requests (admin only)
    """
    try:
        service = AccessRequestService(db)
        requests = service.get_access_requests(skip=skip, limit=limit, status=status)
        return requests
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching access requests: {str(e)}"
        )


@router.get("/{request_id}", response_model=AccessRequest)
async def get_access_request(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific access request (admin only)
    """
    service = AccessRequestService(db)
    access_request = service.get_access_request(request_id)
    
    if not access_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access request not found"
        )
    
    return access_request


@router.put("/{request_id}", response_model=AccessRequest)
async def update_access_request(
    request_id: str,
    request_data: AccessRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an access request (admin only)
    """
    service = AccessRequestService(db)
    access_request = service.update_access_request(request_id, request_data)
    
    if not access_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access request not found"
        )
    
    return access_request


@router.post("/{request_id}/approve", response_model=AccessRequest)
async def approve_access_request(
    request_id: str,
    admin_notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Approve an access request (admin only)
    """
    service = AccessRequestService(db)
    access_request = service.approve_request(request_id, current_user.id, admin_notes)
    
    if not access_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access request not found"
        )
    
    return access_request


@router.post("/{request_id}/reject", response_model=AccessRequest)
async def reject_access_request(
    request_id: str,
    admin_notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Reject an access request (admin only)
    """
    service = AccessRequestService(db)
    access_request = service.reject_request(request_id, current_user.id, admin_notes)
    
    if not access_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access request not found"
        )
    
    return access_request
