# LipaChat AI Agents

## Overview
LipaChat AI Agents is an intelligent customer engagement platform built specifically for the East African market. The system employs multiple AI agents powered by Anthropic's Claude and LipaChat API to handle customer support and marketing tasks over WhatsApp, providing businesses with scalable, culturally relevant automated services.


## Features

### Customer Support Agent
- **Capabilities:**
  - Answer product questions with context-aware responses
  - Troubleshoot technical issues through guided diagnostics
  - Process customer complaints with appropriate escalation paths
  - Handle subscription inquiries and account management
  - Escalate complex issues to human support when necessary
- **Key Features:**
  - Context awareness through conversation history
  - Access to knowledge base and documentation
  - Sentiment analysis for customer satisfaction monitoring
  - Multi-language support for Kenyan and regional customers

### Marketing Agent
- **Capabilities:**
  - Content generation (social media, email campaigns)
  - Market trend analysis and reporting
  - Campaign performance analytics
  - Customer segmentation recommendations
  - Competitive analysis and differentiation strategies
- **Key Features:**
  - Brand voice consistency across all generated content
  - Culturally relevant content for East African market
  - Data-driven insights using analytics integration
  - A/B testing recommendation engine

## Technical Stack

- **FastAPI**: API framework for endpoints, validation, and documentation
- **CrewAI**: Agent orchestration, role definition, and task allocation
- **Anthropic Claude API**: Large language model for natural language understanding and generation
- **LipaChat API**: Company-specific APIs and integrations for chat functionality
- **Data Stores**: Vector database for knowledge retrieval, PostgreSQL for structured data

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Anthropic API key
- CrewAI library

### Setup Instructions
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/lipachat-ai-agents.git
   cd lipachat-ai-agents
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file with your API keys and database connection details.
   
   ```


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, contact:
- Email: langatlangs@gmail.com