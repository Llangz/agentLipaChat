import logging
from typing import Dict, List, Any, Optional
from crewai.tools import Tool

from app.agents.base import BaseAgent
from app.tools.knowledge_base import KnowledgeBaseTool
from app.utils.lipachat_api import LipaChatAPIClient

logger = logging.getLogger(__name__)

class CustomerSupportAgent(BaseAgent):
    """Agent specialized in handling customer support inquiries."""
    
    def __init__(self):
        """Initialize the customer support agent."""
        super().__init__(
            agent_name="LipaChat Customer Support Assistant",
            agent_role="Customer Support Specialist",
            agent_goal="Provide exceptional customer support by accurately answering questions, troubleshooting issues, and ensuring customer satisfaction"
        )
        self.lipachat_client = LipaChatAPIClient()
        self.register_tools()
        
    def _get_backstory(self) -> str:
        """Return the backstory for the customer support agent."""
        return """
        You are an experienced customer support specialist at LipaChat, a leading Kenyan software company. 
        You have deep knowledge of all LipaChat products and services, and you're committed to providing 
        excellent customer service.
        
        You're known for your patience, clear communication, and ability to solve technical problems 
        efficiently. You understand the local Kenyan and broader East African market context, including 
        common payment systems, mobile networks, and cultural nuances.
        
        Your primary goal is to assist customers quickly and effectively, ensuring they have a positive 
        experience with LipaChat's services.
        """
    
    def register_tools(self) -> None:
        """Register tools for the customer support agent."""
        # Knowledge base tool for accessing product information and FAQs
        knowledge_base_tool = KnowledgeBaseTool()
        
        # Support ticket tool - wraps the LipaChat API for ticket operations
        support_ticket_tool = Tool(
            name="create_support_ticket",
            description="Creates a support ticket for issues that need escalation to the support team",
            func=self._create_support_ticket
        )
        
        # Account lookup tool
        account_lookup_tool = Tool(
            name="lookup_account",
            description="Looks up a customer's account information using their email or account ID",
            func=self._lookup_account
        )
        
        # Subscription management tool
        subscription_tool = Tool(
            name="manage_subscription",
            description="Checks or updates a customer's subscription status",
            func=self._manage_subscription
        )
        
        # Add tools to the agent
        self.tools = [
            knowledge_base_tool.as_tool(),
            support_ticket_tool,
            account_lookup_tool,
            subscription_tool
        ]
    
    def _create_support_ticket(self, issue_description: str, customer_email: str, priority: str = "medium") -> Dict[str, Any]:
        """Create a support ticket for escalation.
        
        Args:
            issue_description: Description of the customer's issue
            customer_email: Customer's email address
            priority: Ticket priority (low, medium, high, urgent)
            
        Returns:
            Dictionary with ticket information
        """
        try:
            # Call the LipaChat API to create a ticket
            ticket = self.lipachat_client.create_ticket(
                issue_description=issue_description,
                customer_email=customer_email,
                priority=priority
            )
            
            return {
                "status": "success",
                "ticket_id": ticket["id"],
                "estimated_response_time": ticket["estimated_response_time"]
            }
        except Exception as e:
            logger.error(f"Failed to create support ticket: {str(e)}")
            return {
                "status": "error",
                "message": "Unable to create support ticket. Please try again later."
            }
    
    def _lookup_account(self, identifier: str) -> Dict[str, Any]:
        """Look up customer account information.
        
        Args:
            identifier: Customer email or account ID
            
        Returns:
            Dictionary with account information or error
        """
        try:
            # Call the LipaChat API to look up account
            account_info = self.lipachat_client.get_account(identifier)
            
            # Filter sensitive information before returning
            return {
                "account_id": account_info["id"],
                "name": account_info["name"],
                "email": account_info["email"],
                "account_type": account_info["account_type"],
                "subscription_status": account_info["subscription_status"],
                "last_login": account_info["last_login"],
                "account_created": account_info["created_at"]
            }
        except Exception as e:
            logger.error(f"Failed to lookup account information: {str(e)}")
            return {
                "status": "error",
                "message": "Account not found or error in retrieval."
            }
    
    def _manage_subscription(self, account_id: str, action: str = "check", plan: str = None) -> Dict[str, Any]:
        """Manage customer subscription.
        
        Args:
            account_id: Customer's account ID
            action: Action to perform (check, upgrade, downgrade, cancel)
            plan: New plan name if upgrading or downgrading
            
        Returns:
            Dictionary with subscription information or confirmation
        """
        try:
            if action == "check":
                # Get current subscription details
                subscription = self.lipachat_client.get_subscription(account_id)
                return {
                    "status": "success",
                    "subscription_type": subscription["type"],
                    "subscription_status": subscription["status"],
                    "renewal_date": subscription["renewal_date"],
                    "features": subscription["features"]
                }
            elif action in ["upgrade", "downgrade"]:
                if not plan:
                    return {"status": "error", "message": "Plan name is required for upgrade/downgrade"}
                    
                # Update subscription
                result = self.lipachat_client.update_subscription(account_id, plan)
                return {
                    "status": "success",
                    "message": f"Subscription {action}d to {plan}",
                    "effective_date": result["effective_date"],
                    "next_billing_date": result["next_billing_date"]
                }
            elif action == "cancel":
                # Cancel subscription
                result = self.lipachat_client.cancel_subscription(account_id)
                return {
                    "status": "success",
                    "message": "Subscription canceled",
                    "effective_until": result["effective_until"]
                }
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"Failed to manage subscription: {str(e)}")
            return {
                "status": "error",
                "message": "Unable to process subscription request."
            }
            
    async def handle_support_query(self, 
                           query: str, 
                           user_id: Optional[str] = None,
                           conversation_history: Optional[List[Dict[str, str]]] = None,
                           language: str = "en") -> Dict[str, Any]:
        """Handle a customer support query.
        
        Args:
            query: User's support query
            user_id: Optional user ID for context
            conversation_history: Previous conversation turns
            language: Language code for response
            
        Returns:
            Dictionary with the agent's response and metadata
        """
        # Prepare additional metadata if user_id is provided
        metadata = {}
        if user_id:
            try:
                # Get user account information if available
                user_info = self.lipachat_client.get_user_info(user_id)
                metadata = {
                    "user_id": user_id,
                    "subscription_type": user_info.get("subscription_type", "unknown"),
                    "account_age_days": user_info.get("account_age_days", 0)
                }
            except Exception as e:
                logger.warning(f"Could not retrieve user info for {user_id}: {str(e)}")
        
        # Process the query through the base agent's method
        return await self.process_query(
            query=query,
            conversation_history=conversation_history,
            language=language,
            metadata=metadata
        )