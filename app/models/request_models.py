from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class CustomerSupportRequest(BaseModel):
    query: str = Field(..., description="Customer query or issue description")
    customer_id: Optional[str] = Field(None, description="Unique identifier for the customer")
    conversation_history: Optional[List[Dict[str, str]]] = Field(None, description="Previous messages in the conversation")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional context about the customer or issue")

class ContentGenerationRequest(BaseModel):
    content_type: str = Field(..., description="Type of content to generate (blog, social, email, etc.)")
    topic: str = Field(..., description="Main topic for the content")
    target_audience: Optional[str] = Field(None, description="Target audience for the content")
    tone: Optional[str] = Field(None, description="Desired tone for the content")
    length: Optional[int] = Field(None, description="Approximate word count")
    keywords: Optional[List[str]] = Field(None, description="Keywords to include in the content")
