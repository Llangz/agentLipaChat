import logging
from typing import Dict, List, Any, Optional
from crewai.tools import BaseTool
from anthropic import Anthropic

from app.config import settings
from app.utils.anthropic_helpers import create_anthropic_client

logger = logging.getLogger(__name__)

class ContentGeneratorTool(BaseTool):
    """Tool for generating marketing content."""
    
    def __init__(self):
        """Initialize the content generator tool."""
        super().__init__(
            name="content_generator",
            description="Generate marketing content including social media posts, email copy, blog posts, and ad copy"
        )
        self.anthropic_client = create_anthropic_client()
        
    def _run(self,
           content_type: str,
           target_audience: str,
           goal: str,
           tone: str = "professional",
           length: str = "medium",
           keywords: Optional[List[str]] = None,
           brand_guidelines: Optional[Dict[str, Any]] = None) -> str:
        """Generate marketing content.
        
        Args:
            content_type: Type of content (social_post, email, blog_post, ad_copy)
            target_audience: Target audience description
            goal: Marketing goal
            tone: Tone of voice (professional, casual, enthusiastic, etc.)
            length: Content length (short, medium, long)
            keywords: Optional list of keywords to include
            brand_guidelines: Optional brand guidelines
            
        Returns:
            Generated content as a string
        """
        try:
            # Define length parameters based on content type and requested length
            length_params = self._get_length_params(content_type, length)
            
            # Set up keywords string if provided
            keywords_str = ""
            if keywords:
                keywords_str = f"Include these keywords naturally in the content: {', '.join(keywords)}."
            
            # Set up brand guidelines if provided, otherwise use defaults
            brand_info = brand_guidelines if brand_guidelines else self._get_default_brand_guidelines()
            brand_str = f"""
            Brand voice: {brand_info.get('voice', 'Professional yet approachable')}
            Key values: {brand_info.get('values', 'Reliability, Security, Innovation, Local Expertise')}
            Unique selling points: {', '.join(brand_info.get('unique_selling_points', ['Made in Kenya for East African users']))}
            """
            
            # Create the prompt
            prompt = f"""
            Generate {content_type} content for LipaChat, a leading Kenyan software company that offers secure messaging with integrated payment features.
            
            Content details:
            - Type: {content_type}
            - Target audience: {target_audience}
            - Goal: {goal}
            - Tone: {tone}
            - Length: Approximately {length_params['target_words']} words
            {keywords_str}
            
            Brand information:
            {brand_str}
            
            The content should be culturally relevant for the East African market, particularly Kenya.
            For any payment-related features, mention integration with M-Pesa and other local payment methods.
            """
            
            # Call Anthropic's Claude to generate content
            response = self.anthropic_client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=length_params['max_tokens'],
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            return f"Error generating content: {str(e)}"
    
    def _get_length_params(self, content_type: str, length: str) -> Dict[str, int]:
        """Get word count and token parameters based on content type and length."""
        params = {
            "social_post": {
                "short": {"target_words": 30, "max_tokens": 200},
                "medium": {"target_words": 80, "max_tokens": 400},
                "long": {"target_words": 150, "max_tokens": 600}
            },
            "email": {
                "short": {"target_words": 100, "max_tokens": 500},
                "medium": {"target_words": 250, "max_tokens": 1000},
                "long": {"target_words": 500, "max_tokens": 2000}
            },
            "blog_post": {
                "short": {"target_words": 300, "max_tokens": 1500},
                "medium": {"target_words": 600, "max_tokens": 3000},
                "long": {"target_words": 1200, "max_tokens": 6000}
            },
            "ad_copy": {
                "short": {"target_words": 25, "max_tokens": 150},
                "medium": {"target_words": 50, "max_tokens": 250},
                "long": {"target_words": 100, "max_tokens": 500}
            }
        }
        
        content_params = params.get(content_type, params["social_post"])
        return content_params.get(length, content_params["medium"])
    
    def _get_default_brand_guidelines(self) -> Dict[str, Any]:
        """Get default LipaChat brand guidelines."""
        return {
            "voice": "Professional yet approachable, highlighting LipaChat's Kenyan roots and innovation",
            "values": "Reliability, Security, Innovation, Local Expertise",
            "unique_selling_points": [
                "Made in Kenya for East African users",
                "Secure messaging with integrated payment features",
                "Seamless mobile money integration",
                "Local customer support"
            ],
            "dos": [
                "Emphasize security and reliability",
                "Highlight local expertise and understanding",
                "Focus on convenience and integration with local payment systems",
                "Use positive, solution-oriented language"
            ],
            "donts": [
                "Use technical jargon that might confuse users",
                "Make unrealistic promises",
                "Ignore cultural context",
                "Use generic marketing language"
            ]
        }