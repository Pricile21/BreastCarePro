"""
Article schemas for educational content
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ArticleSection(BaseModel):
    """A section within an article"""
    title: str
    content: Optional[str] = None  # Some sections may only have subsections or lists
    image_url: Optional[str] = None  # URL or path to illustration for this section
    image_alt: Optional[str] = None  # Alt text for the image
    subsections: Optional[List["ArticleSection"]] = None
    bullet_points: Optional[List[str]] = None
    ordered_list: Optional[List[str]] = None


class ArticleMetadata(BaseModel):
    """Metadata about an article"""
    category: str = Field(..., description="Article category (e.g., 'education', 'prevention')")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    author: Optional[str] = None
    publish_date: Optional[str] = None
    last_updated: Optional[str] = None


class ArticleSummary(BaseModel):
    """Summary of an article for listing"""
    id: str
    title: str
    description: str
    thumbnail_url: Optional[str] = None
    reading_time: int
    category: str
    publish_date: Optional[str] = None


class ArticleContent(BaseModel):
    """Full article content formatted for mobile"""
    id: str
    title: str
    description: str
    reading_time: int
    metadata: ArticleMetadata
    introduction: str
    sections: List[ArticleSection]
    conclusion: Optional[str] = None
    disclaimer: Optional[str] = None
    sources: Optional[List[str]] = None
    html_content: Optional[str] = Field(None, description="Full HTML content for mobile rendering")
    markdown_content: Optional[str] = Field(None, description="Full markdown content")


class ArticleResponse(BaseModel):
    """Response model for article endpoints"""
    success: bool = True
    article: ArticleContent


class ArticleListResponse(BaseModel):
    """Response model for article list endpoint"""
    success: bool = True
    total: int
    articles: List[ArticleSummary]


# Allow forward references
ArticleSection.model_rebuild()

