# app/routers/crew.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

from app.orchestration.crew import LipaChatCrew
from app.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/crew", tags=["Agent Crew"])

# Input models
class CustomerFeedbackCampaignRequest(BaseModel):
    feedback_data: List[Dict[str, Any]]
    campaign_id: str


class MarketingCampaignRequest(BaseModel):
    campaign_brief: Dict[str, Any]
    target_audience: str
    market_data: Optional[Dict[str, Any]] = None


class CustomerIssueRequest(BaseModel):
    customer_id: str
    issue_description: str
    support_history: Optional[List[Dict[str, Any]]] = None


# Dependency to get the LipaChat crew
def get_lipachat_crew():
    try:
        return LipaChatCrew()
    except Exception as e:
        logger.error(f"Failed to initialize LipaChat crew: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize agent crew",
        )


@router.post("/customer-feedback-campaign", response_model=Dict[str, Any])
async def handle_customer_feedback_campaign(
    request: CustomerFeedbackCampaignRequest, 
    crew: LipaChatCrew = Depends(get_lipachat_crew)
):
    """
    Process customer feedback and create a marketing campaign response.
    """
    try:
        result = crew.handle_customer_feedback_campaign(
            feedback_data=request.feedback_data,
            campaign_id=request.campaign_id
        )
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error handling customer feedback campaign: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process customer feedback campaign: {str(e)}",
        )


@router.post("/marketing-campaign", response_model=Dict[str, Any])
async def create_marketing_campaign(
    request: MarketingCampaignRequest, 
    crew: LipaChatCrew = Depends(get_lipachat_crew)
):
    """
    Create a comprehensive marketing campaign.
    """
    try:
        result = crew.create_marketing_campaign(
            campaign_brief=request.campaign_brief,
            target_audience=request.target_audience,
            market_data=request.market_data
        )
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error creating marketing campaign: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create marketing campaign: {str(e)}",
        )


@router.post("/customer-issue", response_model=Dict[str, Any])
async def handle_customer_issue(
    request: CustomerIssueRequest, 
    crew: LipaChatCrew = Depends(get_lipachat_crew)
):
    """
    Handle a complex customer issue that may require marketing input.
    """
    try:
        result = crew.handle_customer_issue(
            customer_id=request.customer_id,
            issue_description=request.issue_description,
            support_history=request.support_history
        )
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error handling customer issue: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to handle customer issue: {str(e)}",
        )