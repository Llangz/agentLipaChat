# app/utils/anthropic_helpers.py
import logging
from typing import Dict, Any, List, Optional
from anthropic import Anthropic, AnthropicError
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings

logger = logging.getLogger(__name__)

def create_anthropic_client() -> Anthropic:
    """
    Create and return an Anthropic client instance.
    
    Returns:
        Anthropic client instance
    """
    try:
        return Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    except Exception as e:
        logger.error(f"Failed to create Anthropic client: {str(e)}")
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=lambda e: isinstance(e, (AnthropicError, ConnectionError, TimeoutError)),
    reraise=True
)
def generate_response(
    client: Anthropic,
    system_prompt: str,
    user_message: str,
    model: Optional[str] = None,
    max_tokens: int = 1000,
    temperature: float = 0.7
) -> str:
    """
    Generate a response using Anthropic's Claude.
    
    Args:
        client: Anthropic client instance
        system_prompt: System prompt to set context
        user_message: User's message/query
        model: Model to use (defaults to setting in config)
        max_tokens: Maximum number of tokens to generate
        temperature: Sampling temperature (0.0-1.0)
        
    Returns:
        Generated response text
    """
    try:
        response = client.messages.create(
            model=model or settings.ANTHROPIC_MODEL,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.content[0].text
    except AnthropicError as e:
        logger.error(f"Anthropic API error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while generating response: {str(e)}")
        raise

def create_customer_support_prompt(
    query: str,
    customer_info: Optional[Dict[str, Any]] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    product_info: Optional[Dict[str, Any]] = None
) -> str:
    """
    Create a tailored prompt for the customer support agent.
    
    Args:
        query: Customer's query
        customer_info: Information about the customer
        conversation_history: Previous conversation history
        product_info: Information about relevant products
        
    Returns:
        Formatted prompt for Claude
    """
    prompt_parts = [
        "You are LipaChat's expert customer support AI assistant. Respond to the customer's query professionally, accurately, and helpfully.",
        "Customer query: " + query
    ]
    
    if customer_info:
        customer_info_str = "Customer information:\n"
        for key, value in customer_info.items():
            customer_info_str += f"- {key}: {value}\n"
        prompt_parts.append(customer_info_str)
    
    if conversation_history:
        history_str = "Previous conversation:\n"
        for message in conversation_history:
            role = message.get("role", "Unknown")
            content = message.get("content", "")
            history_str += f"{role}: {content}\n"
        prompt_parts.append(history_str)
    
    if product_info:
        product_info_str = "Product information:\n"
        for key, value in product_info.items():
            product_info_str += f"- {key}: {value}\n"
        prompt_parts.append(product_info_str)
    
    return "\n\n".join(prompt_parts)

def create_marketing_prompt(
    content_type: str,
    topic: str,
    target_audience: Optional[str] = None,
    tone: Optional[str] = None,
    keywords: Optional[List[str]] = None,
    brand_guidelines: Optional[Dict[str, Any]] = None
) -> str:
    """
    Create a tailored prompt for the marketing content generation.
    
    Args:
        content_type: Type of content to generate
        topic: Topic of the content
        target_audience: Target audience description
        tone: Desired tone of the content
        keywords: Keywords to include
        brand_guidelines: Brand guidelines to follow
        
    Returns:
        Formatted prompt for Claude
    """
    prompt_parts = [
        f"You are LipaChat's expert marketing content creator. Create compelling {content_type} content about {topic}."
    ]
    
    if target_audience:
        prompt_parts.append(f"Target audience: {target_audience}")
    
    if tone:
        prompt_parts.append(f"Tone: {tone}")
    
    if keywords:
        prompt_parts.append(f"Keywords to include: {', '.join(keywords)}")
    
    if brand_guidelines:
        guidelines_str = "Brand guidelines:\n"
        for key, value in brand_guidelines.items():
            guidelines_str += f"- {key}: {value}\n"
        prompt_parts.append(guidelines_str)
    
    prompt_parts.append(f"Please create a high-quality {content_type} about {topic} that will resonate with our audience and drive engagement.")
    
    return "\n\n".join(prompt_parts)

def create_market_research_prompt(
    topic: str,
    competitor_names: Optional[List[str]] = None,
    market_segment: Optional[str] = None,
    region: Optional[str] = None
) -> str:
    """
    Create a prompt for market research analysis.
    
    Args:
        topic: Topic to research
        competitor_names: List of competitor names
        market_segment: Market segment to focus on
        region: Geographic region to focus on
        
    Returns:
        Formatted prompt for Claude
    """
    prompt_parts = [
        f"You are LipaChat's expert market researcher. Conduct a thorough analysis on {topic}."
    ]
    
    if competitor_names:
        prompt_parts.append(f"Focus on these competitors: {', '.join(competitor_names)}")
    
    if market_segment:
        prompt_parts.append(f"Market segment: {market_segment}")
    
    if region:
        prompt_parts.append(f"Region: {region}")
    
    prompt_parts.append(f"Please provide a comprehensive market analysis on {topic} that includes strengths, weaknesses, opportunities, and threats. Include market trends, competitor positioning, and strategic recommendations.")
    
    return "\n\n".join(prompt_parts)