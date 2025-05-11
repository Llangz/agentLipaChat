import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from anthropic import Anthropic
from crewai import Agent as CrewAgent, Task, Crew
from crewai.tools import Tool

from app.config import settings
from app.utils.anthropic_helpers import create_anthropic_client

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all LipaChat AI agents."""
    
    def __init__(self, agent_name: str, agent_role: str, agent_goal: str):
        """Initialize the base agent with common attributes.
        
        Args:
            agent_name: Name of the agent
            agent_role: Role description of the agent
            agent_goal: Primary goal of the agent
        """
        self.name = agent_name
        self.role = agent_role
        self.goal = agent_goal
        self.tools: List[Tool] = []
        self.anthropic_client: Anthropic = create_anthropic_client()
        
        # Set up the CrewAI agent
        self.crew_agent = CrewAgent(
            name=self.name,
            role=self.role,
            goal=self.goal,
            backstory=self._get_backstory(),
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self._configure_llm()
        )
    
    @abstractmethod
    def _get_backstory(self) -> str:
        """Return the backstory of the agent. To be implemented by subclasses."""
        pass
    
    @abstractmethod
    def register_tools(self) -> None:
        """Register tools for the agent. To be implemented by subclasses."""
        pass
    
    def _configure_llm(self) -> Any:
        """Configure the language model for the agent."""
        # Setup for Anthropic's Claude using CrewAI
        from crewai.llms import AnthropicLLM
        
        return AnthropicLLM(
            model=settings.CLAUDE_MODEL,
            anthropic_api_key=settings.ANTHROPIC_API_KEY
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def process_query(self, 
                     query: str, 
                     conversation_history: Optional[List[Dict[str, str]]] = None, 
                     language: str = "en",
                     metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a user query through the agent.
        
        Args:
            query: User's query text
            conversation_history: Previous conversation turns
            language: Language code for response (default "en" for English)
            metadata: Optional additional context information
            
        Returns:
            Dict containing the agent's response and additional metadata
        """
        if language not in settings.SUPPORTED_LANGUAGES:
            logger.warning(f"Unsupported language requested: {language}, falling back to {settings.DEFAULT_LANGUAGE}")
            language = settings.DEFAULT_LANGUAGE
        
        # Create a task for the agent
        task = Task(
            description=f"Process the following query in {language}: {query}",
            agent=self.crew_agent,
            context=self._prepare_context(conversation_history, metadata)
        )
        
        # Create a single-agent crew to execute the task
        crew = Crew(
            agents=[self.crew_agent],
            tasks=[task],
            verbose=True
        )
        
        # Execute the task
        result = crew.kickoff()
        
        return {
            "response": result,
            "agent": self.name,
            "language": language,
            "metadata": self._process_result_metadata(result, query)
        }
    
    def _prepare_context(self, 
                        conversation_history: Optional[List[Dict[str, str]]], 
                        metadata: Optional[Dict[str, Any]]) -> str:
        """Prepare context for the agent based on conversation history and metadata."""
        context = ""
        
        # Include conversation history if available
        if conversation_history:
            # Trim to the max history length
            trimmed_history = conversation_history[-settings.MAX_CONVERSATION_HISTORY:]
            
            context += "Conversation history:\n"
            for turn in trimmed_history:
                if "user" in turn:
                    context += f"User: {turn['user']}\n"
                if "assistant" in turn:
                    context += f"Assistant: {turn['assistant']}\n"
            context += "\n"
        
        # Include additional metadata if available
        if metadata:
            context += "Additional context:\n"
            for key, value in metadata.items():
                context += f"{key}: {value}\n"
        
        return context

    def _process_result_metadata(self, result: str, query: str) -> Dict[str, Any]:
        """Process result to extract and return useful metadata."""
        # Placeholder for extracting metadata from results
        # This could be expanded based on specific agent needs
        return {
            "query_length": len(query),
            "response_length": len(result),
            "timestamp": import_time().isoformat()
        }
        
# Helper function to avoid circular imports
def import_time():
    from datetime import datetime
    return datetime.now()