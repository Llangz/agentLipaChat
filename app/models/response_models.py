from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class CustomerSupportResponse(BaseModel):
    response: str = Field(..., description="Agent response to the customer query")
    suggested_actions: Optional[List[str]] = Field(None, description="Recommended next actions")
    confidence_score: float = Field(..., description="Confidence level in the response (0-1)")
    requires_human: bool = Field(False, description="Whether human intervention is recommended")
    reference_ids: Optional[List[str]] = Field(None, description="IDs of knowledge base articles referenced")

class ContentResponse(BaseModel):
    content: str = Field(..., description="Generated content")
    metadata: Dict[str, Any] = Field(..., description="Information about the generated content")
    alternative_versions: Optional[List[str]] = Field(None, description="Alternative content versions")

class AnalysisResponse(BaseModel):
    insights: List[Dict[str, Any]] = Field(..., description="Key insights from the campaign analysis")
    recommendations: List[str] = Field(..., description="Strategic recommendations based on analysis")
    performance_metrics: Dict[str, float] = Field(..., description="Calculated performance metrics")

class StrategicRecommendationsResponse(BaseModel):
    recommendations: List[Dict[str, Any]] = Field(..., description="Strategic marketing recommendations")
    rationale: Dict[str, str] = Field(..., description="Rationale behind each recommendation")
    expected_outcomes: Dict[str, Any] = Field(..., description="Expected outcomes if recommendations are implemented")
    implementation_timeline: Optional[Dict[str, Any]] = Field(None, description="Suggested implementation timeline")

class FeedbackResponse(BaseModel):
    status: str = Field(..., description="Status of the feedback submission")
    feedback_id: str = Field(..., description="Unique ID for the feedback submission")

class KnowledgeArticle(BaseModel):
    article_id: str = Field(..., description="Unique identifier for the article")
    title: str = Field(..., description="Article title")
    content: str = Field(..., description="Article content")
    relevance_score: float = Field(..., description="Relevance score (0-1)")
    last_updated: str = Field(..., description="Last updated timestamp")
    category: str = Field(..., description="Article category")

class KnowledgeSearchResponse(BaseModel):
    results: List[KnowledgeArticle] = Field(..., description="List of matching knowledge articles")
    query_expansion: Optional[List[str]] = Field(None, description="Suggested related queries")
    total_matches: int = Field(..., description="Total number of matches found")