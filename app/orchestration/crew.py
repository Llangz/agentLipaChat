# app/orchestration/crew.py
import logging
from typing import Dict, Any, List, Optional
from crewai import Crew, Agent, Task, Process
from app.agents.customer_support_agent import CustomerSupportAgent
from app.agents.marketing_agent import MarketingAgent
from app.config import settings

logger = logging.getLogger(__name__)

class LipaChatCrew:
    """
    Orchestrates collaboration between different AI agents using CrewAI.
    """
    
    def __init__(self):
        """Initialize the LipaChat agent crew."""
        self.customer_support_agent = CustomerSupportAgent()
        self.marketing_agent = MarketingAgent()
        
        # Convert to CrewAI agents
        self.crew_customer_support = self._create_crew_agent(
            self.customer_support_agent,
            "Customer Support Specialist",
            "Expert in resolving customer issues and providing excellent support"
        )
        
        self.crew_marketing = self._create_crew_agent(
            self.marketing_agent, 
            "Marketing Specialist",
            "Expert in creating compelling marketing content and analyzing campaign performance"
        )
    
    def _create_crew_agent(self, base_agent, role: str, goal: str) -> Agent:
        """
        Create a CrewAI agent from a base agent.
        
        Args:
            base_agent: Base agent instance
            role: Role of the agent
            goal: Goal of the agent
            
        Returns:
            CrewAI Agent instance
        """
        tools = base_agent.get_tools()
        
        return Agent(
            role=role,
            goal=goal,
            backstory=f"You are an AI assistant working for LipaChat, a Kenyan software company.",
            verbose=settings.DEBUG,
            allow_delegation=True,
            tools=tools,
            llm=base_agent.llm
        )
    
    def handle_customer_feedback_campaign(
        self,
        feedback_data: List[Dict[str, Any]],
        campaign_id: str
    ) -> Dict[str, Any]:
        """
        Process customer feedback and create a marketing campaign response.
        
        Args:
            feedback_data: List of customer feedback items
            campaign_id: ID of the related marketing campaign
            
        Returns:
            Dictionary containing analysis and response plan
        """
        try:
            # Create tasks
            analyze_feedback_task = Task(
                description="Analyze customer feedback and identify key themes and opportunities",
                expected_output="Detailed analysis of customer feedback with key themes identified",
                agent=self.crew_customer_support,
                context={"feedback_data": feedback_data}
            )
            
            campaign_analysis_task = Task(
                description=f"Analyze the performance of campaign {campaign_id} and identify strengths and weaknesses",
                expected_output="Detailed campaign performance analysis",
                agent=self.crew_marketing,
                context={"campaign_id": campaign_id}
            )
            
            create_response_plan_task = Task(
                description="Create a response plan based on customer feedback analysis and campaign performance",
                expected_output="Strategic response plan with specific actions and content recommendations",
                agent=self.crew_marketing,
                context={"feedback_analysis": "Will be filled by analyze_feedback_task", 
                         "campaign_analysis": "Will be filled by campaign_analysis_task"}
            )
            
            # Create crew with tasks
            crew = Crew(
                agents=[self.crew_customer_support, self.crew_marketing],
                tasks=[analyze_feedback_task, campaign_analysis_task, create_response_plan_task],
                verbose=settings.DEBUG,
                process=Process.sequential  # Execute tasks in sequence
            )
            
            # Execute the crew's tasks
            result = crew.kickoff()
            
            # Parse and format the results
            return {
                "feedback_analysis": result[0],
                "campaign_analysis": result[1],
                "response_plan": result[2]
            }
            
        except Exception as e:
            logger.error(f"Error in handle_customer_feedback_campaign: {str(e)}")
            raise
    
    def create_marketing_campaign(
        self,
        campaign_brief: Dict[str, Any],
        target_audience: str,
        market_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a comprehensive marketing campaign.
        
        Args:
            campaign_brief: Brief description of the campaign
            target_audience: Description of the target audience
            market_data: Optional market research data
            
        Returns:
            Dictionary containing the campaign plan and content
        """
        try:
            # Create tasks
            if not market_data:
                market_research_task = Task(
                    description=f"Conduct market research for campaign targeting {target_audience}",
                    expected_output="Comprehensive market research report",
                    agent=self.crew_marketing,
                    context={"campaign_brief": campaign_brief, "target_audience": target_audience}
                )
                
                tasks = [market_research_task]
                context_for_planning = {"market_research": "Will be filled by market_research_task"}
            else:
                tasks = []
                context_for_planning = {"market_research": market_data}
            
            campaign_planning_task = Task(
                description="Create a strategic campaign plan based on the brief and market research",
                expected_output="Detailed campaign plan with strategy, channels, and timeline",
                agent=self.crew_marketing,
                context={**context_for_planning, "campaign_brief": campaign_brief, 
                         "target_audience": target_audience}
            )
            
            content_creation_task = Task(
                description="Create compelling marketing content for the campaign",
                expected_output="Various marketing content assets for different channels",
                agent=self.crew_marketing,
                context={"campaign_plan": "Will be filled by campaign_planning_task", 
                         "target_audience": target_audience}
            )
            
            support_preparation_task = Task(
                description="Prepare customer support responses for potential campaign questions",
                expected_output="FAQ document and support response templates",
                agent=self.crew_customer_support,
                context={"campaign_plan": "Will be filled by campaign_planning_task", 
                         "target_audience": target_audience}
            )
            
            tasks.extend([campaign_planning_task, content_creation_task, support_preparation_task])
            
            # Create crew with tasks
            crew = Crew(
                agents=[self.crew_customer_support, self.crew_marketing],
                tasks=tasks,
                verbose=settings.DEBUG,
                process=Process.sequential  # Execute tasks in sequence
            )
            
            # Execute the crew's tasks
            result = crew.kickoff()
            
            # Parse and format the results
            response = {}
            if not market_data:
                response["market_research"] = result[0]
                response["campaign_plan"] = result[1]
                response["campaign_content"] = result[2]
                response["support_materials"] = result[3]
            else:
                response["campaign_plan"] = result[0]
                response["campaign_content"] = result[1]
                response["support_materials"] = result[2]
            
            return response
            
        except Exception as e:
            logger.error(f"Error in create_marketing_campaign: {str(e)}")
            raise
    
    def handle_customer_issue(
        self,
        customer_id: str,
        issue_description: str,
        support_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Handle a complex customer issue that may require marketing input.
        
        Args:
            customer_id: ID of the customer
            issue_description: Description of the issue
            support_history: Optional support history
            
        Returns:
            Dictionary containing the resolution and any follow-up actions
        """
        try:
            # Create tasks
            troubleshoot_task = Task(
                description=f"Troubleshoot the customer issue: {issue_description}",
                expected_output="Detailed troubleshooting steps and solution",
                agent=self.crew_customer_support,
                context={"customer_id": customer_id, "issue_description": issue_description, 
                         "support_history": support_history or []}
            )
            
            customer_retention_task = Task(
                description="Create a customer retention plan based on the issue resolution",
                expected_output="Customer retention strategy with specific actions",
                agent=self.crew_marketing,
                context={"customer_id": customer_id, "issue_resolution": "Will be filled by troubleshoot_task"}
            )
            
            personalized_content_task = Task(
                description="Create personalized follow-up content for the customer",
                expected_output="Personalized email and in-app message templates",
                agent=self.crew_marketing,
                context={"customer_id": customer_id, "issue_resolution": "Will be filled by troubleshoot_task",
                         "retention_plan": "Will be filled by customer_retention_task"}
            )
            
            # Create crew with tasks
            crew = Crew(
                agents=[self.crew_customer_support, self.crew_marketing],
                tasks=[troubleshoot_task, customer_retention_task, personalized_content_task],
                verbose=settings.DEBUG,
                process=Process.sequential  # Execute tasks in sequence
            )
            
            # Execute the crew's tasks
            result = crew.kickoff()
            
            # Parse and format the results
            return {
                "issue_resolution": result[0],
                "retention_plan": result[1],
                "follow_up_content": result[2]
            }
            
        except Exception as e:
            logger.error(f"Error in handle_customer_issue: {str(e)}")
            raise