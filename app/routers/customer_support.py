# app/routers/customer_support.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from app.agents.customer_support_agent import CustomerSupportAgent
from app.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/customer-support", tags=["Customer Support"])

# Input models
class CustomerQuery(BaseModel):
    query: str
    customer_id: Optional[str] = None
    conversation_history: Optional[List[Dict[str, str]]] = None
    metadata: Optional[Dict[str, Any]] = None


class TroubleshootRequest(BaseModel):
    issue_description: str
    customer_id: str
    device_info: Optional[Dict[str, str]] = None
    steps_tried: Optional[List[str]] = None
    error_messages: Optional[List[str]] = None


class FeedbackRequest(BaseModel):
    feedback_text: str
    customer_id: str
    satisfaction_rating: Optional[int] = None
    product_id: Optional[str] = None
    interaction_id: Optional[str] = None


# Dependency to get the customer support agent
def get_customer_support_agent():
    try:
        return CustomerSupportAgent()
    except Exception as e:
        logger.error(f"Failed to initialize customer support agent: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize customer support agent",
        )


@router.post("/query", response_model=Dict[str, Any])
async def handle_customer_query(
    query_data: CustomerQuery, agent: CustomerSupportAgent = Depends(get_customer_support_agent)
):
    """Handle a customer support query."""
    try:
        response = agent.handle_query(
            query=query_data.query,
            customer_id=query_data.customer_id,
            conversation_history=query_data.conversation_history or [],
            metadata=query_data.metadata or {},
        )
        return {"status": "success", "response": response}
    except Exception as e:
        logger.error(f"Error handling customer query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process customer query: {str(e)}",
        )


@router.post("/troubleshoot", response_model=Dict[str, Any])
async def troubleshoot_issue(
    troubleshoot_data: TroubleshootRequest,
    agent: CustomerSupportAgent = Depends(get_customer_support_agent),
):
    """Troubleshoot a technical issue reported by a customer."""
    try:
        solution = agent.troubleshoot_issue(
            issue_description=troubleshoot_data.issue_description,
            customer_id=troubleshoot_data.customer_id,
            device_info=troubleshoot_data.device_info or {},
            steps_tried=troubleshoot_data.steps_tried or [],
            error_messages=troubleshoot_data.error_messages or [],
        )
        return {"status": "success", "solution": solution}
    except Exception as e:
        logger.error(f"Error troubleshooting issue: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to troubleshoot issue: {str(e)}",
        )


@router.post("/feedback", response_model=Dict[str, Any])
async def process_feedback(
    feedback_data: FeedbackRequest,
    agent: CustomerSupportAgent = Depends(get_customer_support_agent),
):
    """Process customer feedback."""
    try:
        result = agent.process_feedback(
            feedback_text=feedback_data.feedback_text,
            customer_id=feedback_data.customer_id,
            satisfaction_rating=feedback_data.satisfaction_rating,
            product_id=feedback_data.product_id,
            interaction_id=feedback_data.interaction_id,
        )
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error processing feedback: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process feedback: {str(e)}",
        )