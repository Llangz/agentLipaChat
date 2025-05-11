import logging
from typing import Dict, Any, List, Optional
from crewai.tools import BaseTool
import json

logger = logging.getLogger(__name__)

class KnowledgeBaseTool(BaseTool):
    """Tool for accessing LipaChat's knowledge base."""
    
    def __init__(self):
        """Initialize the knowledge base tool."""
        super().__init__(
            name="knowledge_base",
            description="Search LipaChat's knowledge base for product information, FAQs, and troubleshooting guides"
        )
        # In a real implementation, this would connect to a vector database
        # For this example, we'll use a simplified in-memory approach
        self._initialize_knowledge_base()
        
    def _initialize_knowledge_base(self):
        """Initialize the knowledge base with sample data."""
        self.knowledge_base = {
            "products": {
                "lipachat_messenger": {
                    "name": "LipaChat Messenger",
                    "description": "Secure messaging app with integrated payment features",
                    "features": [
                        "End-to-end encrypted messaging",
                        "Voice and video calls",
                        "Mobile money integration",
                        "Group chats up to 1000 members",
                        "File sharing up to 100MB"
                    ],
                    "pricing": {
                        "basic": "Free",
                        "premium": "Ksh 299/month",
                        "business": "Ksh 999/month"
                    },
                    "platforms": ["Android", "iOS", "Web"]
                },
                "lipapay": {
                    "name": "LipaPay",
                    "description": "Digital payment solution for businesses",
                    "features": [
                        "Payment processing",
                        "Invoice generation",
                        "Transaction reports",
                        "Multi-currency support",
                        "API integration"
                    ],
                    "pricing": {
                        "starter": "1.5% per transaction",
                        "growth": "1.2% per transaction + Ksh 1999/month",
                        "enterprise": "Custom pricing"
                    },
                    "platforms": ["Web Dashboard", "Android", "iOS", "API"]
                }
            },
            "faqs": [
                {
                    "question": "How do I reset my password?",
                    "answer": "You can reset your password by going to the login screen and clicking on 'Forgot Password'. Enter your registered email address, and we'll send you a password reset link."
                },
                {
                    "question": "How do I send money through LipaChat?",
                    "answer": "To send money, open a chat with the recipient, tap the + icon, select 'Send Money', enter the amount, select payment method, and confirm the transaction with your PIN."
                },
                {
                    "question": "Is LipaChat secure?",
                    "answer": "Yes, LipaChat uses end-to-end encryption for all messages and calls. For payments, we use bank-grade security protocols and do not store your payment details on our servers."
                },
                {
                    "question": "Which payment methods are supported?",
                    "answer": "LipaChat supports M-Pesa, Airtel Money, T-Kash, bank transfers, and major credit/debit cards including Visa and Mastercard."
                },
                {
                    "question": "How do I upgrade to Premium?",
                    "answer": "To upgrade to Premium, go to Settings > Account > Subscription, select the Premium plan, choose your payment method, and follow the prompts to complete your purchase."
                }
            ],
            "troubleshooting": [
                {
                    "issue": "Unable to send messages",
                    "solutions": [
                        "Check your internet connection",
                        "Ensure the app is updated to the latest version",
                        "Restart the app",
                        "Check if the recipient has blocked you",
                        "Try logging out and logging back in"
                    ]
                },
                {
                    "issue": "Payment failed",
                    "solutions": [
                        "Ensure you have sufficient funds",
                        "Check if your payment method is active and not expired",
                        "Verify that you entered the correct payment details",
                        "Try an alternative payment method",
                        "Wait a few minutes and try again"
                    ]
                },
                {
                    "issue": "App crashes on startup",
                    "solutions": [
                        "Update to the latest version",
                        "Clear the app cache",
                        "Restart your device",
                        "Uninstall and reinstall the app",
                        "Check device storage space"
                    ]
                }
            ]
        }
    
    def _run(self, query: str, category: Optional[str] = None) -> str:
        """Run the knowledge base search.
        
        Args:
            query: Search query
            category: Optional category to search (products, faqs, troubleshooting)
            
        Returns:
            Search results as a string
        """
        try:
            query = query.lower()
            results = {}
            
            # If category is specified, only search in that category
            if category:
                if category not in self.knowledge_base:
                    return f"Category '{category}' not found in knowledge base."
                categories_to_search = [category]
            else:
                categories_to_search = self.knowledge_base.keys()
            
            # Search in each category
            for cat in categories_to_search:
                if cat == "products":
                    product_results = self._search_products(query)
                    if product_results:
                        results["products"] = product_results
                        
                elif cat == "faqs":
                    faq_results = self._search_faqs(query)
                    if faq_results:
                        results["faqs"] = faq_results
                        
                elif cat == "troubleshooting":
                    troubleshooting_results = self._search_troubleshooting(query)
                    if troubleshooting_results:
                        results["troubleshooting"] = troubleshooting_results
            
            # Format and return results
            if not results:
                return "No matching information found in the knowledge base."
            
            return json.dumps(results, indent=2)
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
            return f"Error searching knowledge base: {str(e)}"
    
    def _search_products(self, query: str) -> List[Dict[str, Any]]:
        """Search product information."""
        results = []
        
        for product_id, product_info in self.knowledge_base["products"].items():
            # Check if query matches product name or description
            if (query in product_info["name"].lower() or 
                query in product_info["description"].lower() or
                any(query in feature.lower() for feature in product_info["features"])):
                results.append(product_info)
                
        return results
    
    def _search_faqs(self, query: str) -> List[Dict[str, Any]]:
        """Search FAQs."""
        results = []
        
        for faq in self.knowledge_base["faqs"]:
            # Check if query matches question or answer
            if query in faq["question"].lower() or query in faq["answer"].lower():
                results.append(faq)
                
        return results
    
    def _search_troubleshooting(self, query: str) -> List[Dict[str, Any]]:
        """Search troubleshooting guides."""
        results = []
        
        for guide in self.knowledge_base["troubleshooting"]:
            # Check if query matches issue or any solution
            if (query in guide["issue"].lower() or
                any(query in solution.lower() for solution in guide["solutions"])):
                results.append(guide)
                
        return results