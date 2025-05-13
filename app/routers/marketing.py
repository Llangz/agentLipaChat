# app/routers/marketing.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from app.agents.marketing_agent import MarketingAgent
from app.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/marketing", tags=["Marketing"])

# Input models
class ContentRequest(BaseModel):
    content_type: str  # e.g., "blog", "social", "email", "ad"
    topic: str
    target_audience: Optional[str] = None
    tone: Optional[str] = None
    length: Optional[str] = None  # e.g., "short", "medium", "long"
    keywords: Optional[List[str]] = None
    additional_context: Optional[Dict[str, Any]] = None


class CampaignAnalysisRequest(BaseModel):
    campaign_id: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    metrics: Optional[List[str]] = None
    comparison_campaign_id: Optional[str] = None


class MarketResearchRequest(BaseModel):
    topic: str
    competitor_names: Optional[List[str]] = None
    market_segment: Optional[str] = None
    region: Optional[str] = None
    additional_params: Optional[Dict[str, Any]] = None


# Dependency to get the marketing agent
def get_marketing_agent():
    try:
        return MarketingAgent()
    except Exception as e:
        logger.error(f"Failed to initialize marketing agent: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize marketing agent",
        )


@router.post("/generate-content", response_model=Dict[str, Any])
async def generate_marketing_content(
    content_req: ContentRequest, agent: MarketingAgent = Depends(get_marketing_agent)
):
    """Generate marketing content based on specified parameters."""
    try:
        content = agent.generate_content(
            content_type=content_req.content_type,
            topic=content_req.topic,
            target_audience=content_req.target_audience,
            tone=content_req.tone,
            length=content_req.length,
            keywords=content_req.keywords or [],
            additional_context=content_req.additional_context or {},
        )
        return {"status": "success", "content": content}
    except Exception as e:
        logger.error(f"Error generating marketing content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate content: {str(e)}",
        )


@router.post("/analyze-campaign", response_model=Dict[str, Any])
async def analyze_marketing_campaign(
    analysis_req: CampaignAnalysisRequest, agent: MarketingAgent = Depends(get_marketing_agent)
):
    """Analyze the performance of a marketing campaign."""
    try:
        analysis = agent.analyze_campaign(
            campaign_id=analysis_req.campaign_id,
            start_date=analysis_req.start_date,
            end_date=analysis_req.end_date,
            metrics=analysis_req.metrics or ["impressions", "clicks", "conversions", "roi"],
            comparison_campaign_id=analysis_req.comparison_campaign_id,
        )
        return {"status": "success", "analysis": analysis}
    except Exception as e:
        logger.error(f"Error analyzing campaign: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze campaign: {str(e)}",
        )


@router.post("/market-research", response_model=Dict[str, Any])
async def conduct_market_research(
    research_req: MarketResearchRequest, agent: MarketingAgent = Depends(get_marketing_agent)
):
    """Conduct market research on specific topics or competitors."""
    try:
        research_data = agent.conduct_market_research(
            topic=research_req.topic,
            competitor_names=research_req.competitor_names or [],
            market_segment=research_req.market_segment,
            region=research_req.region,
            additional_params=research_req.additional_params or {},
        )
        return {"status": "success", "research_data": research_data}
    except Exception as e:
        logger.error(f"Error conducting market research: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to conduct market research: {str(e)}",
        )