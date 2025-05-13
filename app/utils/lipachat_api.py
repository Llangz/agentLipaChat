# app/utils/lipachat_api.py
import logging
import httpx
import json
from typing import Dict, Any, List, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class LipaChatAPI:
    """
    Utility class to interact with the LipaChat API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LipaChat API client.
        
        Args:
            api_key: Optional API key. If not provided, it will be loaded from settings.
        """
        self.api_key = api_key or settings.LIPACHAT_API_KEY
        self.base_url = settings.LIPACHAT_API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to the LipaChat API.
        
        Args:
            method: HTTP method (get, post, put, delete)
            endpoint: API endpoint
            data: Request data
            
        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                if method.lower() == "get":
                    response = await client.get(url, headers=self.headers, params=data)
                elif method.lower() == "post":
                    response = await client.post(url, headers=self.headers, json=data)
                elif method.lower() == "put":
                    response = await client.put(url, headers=self.headers, json=data)
                elif method.lower() == "delete":
                    response = await client.delete(url, headers=self.headers, params=data)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
    
    # Customer data methods
    async def get_customer_data(self, customer_id: str) -> Dict[str, Any]:
        """Get customer data by ID."""
        endpoint = f"/customers/{customer_id}"
        return await self._make_request("get", endpoint)
    
    async def update_customer_data(self, customer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update customer data."""
        endpoint = f"/customers/{customer_id}"
        return await self._make_request("put", endpoint, data)
    
    async def get_customer_conversation_history(self, customer_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get conversation history for a customer."""
        endpoint = f"/customers/{customer_id}/conversations"
        data = {"limit": limit}
        response = await self._make_request("get", endpoint, data)
        return response.get("conversations", [])
    
    # Knowledge base methods
    async def search_knowledge_base(self, query: str, category: Optional[str] = None) -> Dict[str, Any]:
        """Search the knowledge base for articles matching a query."""
        endpoint = "/knowledge/search"
        data = {"query": query}
        if category:
            data["category"] = category
        return await self._make_request("get", endpoint, data)
    
    async def get_knowledge_article(self, article_id: str) -> Dict[str, Any]:
        """Get a specific knowledge base article by ID."""
        endpoint = f"/knowledge/articles/{article_id}"
        return await self._make_request("get", endpoint)
    
    # Analytics methods
    async def get_campaign_analytics(
        self, 
        campaign_id: str, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None,
        metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Get analytics for a specific marketing campaign."""
        endpoint = f"/analytics/campaigns/{campaign_id}"
        data = {}
        if start_date:
            data["start_date"] = start_date
        if end_date:
            data["end_date"] = end_date
        if metrics:
            data["metrics"] = ",".join(metrics)
        return await self._make_request("get", endpoint, data)
    
    async def get_customer_support_metrics(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        agent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get customer support metrics."""
        endpoint = "/analytics/support"
        data = {}
        if start_date:
            data["start_date"] = start_date
        if end_date:
            data["end_date"] = end_date
        if agent_id:
            data["agent_id"] = agent_id
        return await self._make_request("get", endpoint, data)
    
    # Market research methods
    async def get_competitor_data(self, competitor_name: str) -> Dict[str, Any]:
        """Get data about a competitor."""
        endpoint = f"/market-research/competitors/{competitor_name}"
        return await self._make_request("get", endpoint)
    
    async def get_market_trends(self, segment: Optional[str] = None, region: Optional[str] = None) -> Dict[str, Any]:
        """Get market trends data."""
        endpoint = "/market-research/trends"
        data = {}
        if segment:
            data["segment"] = segment
        if region:
            data["region"] = region
        return await self._make_request("get", endpoint, data)
    
    # Content methods
    async def submit_content(self, content_type: str, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Submit content to the LipaChat platform."""
        endpoint = "/content"
        data = {
            "type": content_type,
            "content": content,
            "metadata": metadata
        }
        return await self._make_request("post", endpoint, data)
    
    async def schedule_content(
        self, 
        content_id: str, 
        publish_date: str, 
        channels: List[str]
    ) -> Dict[str, Any]:
        """Schedule content for publishing."""
        endpoint = f"/content/{content_id}/schedule"
        data = {
            "publish_date": publish_date,
            "channels": channels
        }
        return await self._make_request("post", endpoint, data)