"""
Mammography analysis schemas
"""

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.models.mammography import BI_RADS_Category, AnalysisStatus


class MammographyUploadRequest(BaseModel):
    """
    Request schema for mammography upload
    """
    patient_id: Optional[str] = None
    notes: Optional[str] = None


class MammographyAnalysisResponse(BaseModel):
    """
    Response schema for mammography analysis
    """
    id: str
    analysis_id: str
    patient_id: Optional[str]
    bi_rads_category: BI_RADS_Category
    confidence_score: float
    breast_density: Optional[str]
    findings: Optional[str]
    recommendations: Optional[str]
    processing_time: float
    status: AnalysisStatus
    created_at: datetime
    
    class Config:
        from_attributes = True


class MammographyHistoryItem(BaseModel):
    """
    Schema for mammography history item
    """
    analysis_id: str
    bi_rads_category: BI_RADS_Category
    confidence_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True
