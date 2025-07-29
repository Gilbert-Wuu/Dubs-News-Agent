from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from agent_tools import AGENT_TOOLS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SYSTEM_PROMPT = """
You are an NBA news assistant.
When scraping news, always try the full keyword first.
If you find no results with the full keyword, try again with a more general or shorter keyword (e.g., use 'Warriors' if 'Golden State Warriors' returns nothing).
Summarize the news and email the results.

When you need to perform multiple steps, always use the output of one tool as the input to the next tool, if applicable.

Example:
User: "Find NBA news about the Los Angeles Lakers, summarize them, and email me the summaries."

Step 1: Use the scrape_news tool with keyword "Lakers". Suppose it returns a list of articles.
Step 2: Pass the list of articles to the summarize_articles tool to generate summaries.
Step 3: Pass the summaries to the notify_email tool to send the email.

Remember: always pass the output from one tool to the next, instead of starting from scratch each time.
"""

# Define the system message
system_message = SystemMessage(content=SYSTEM_PROMPT)

# Choose your LLM
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

agent = initialize_agent(tools=AGENT_TOOLS, 
                         llm=llm, 
                         agent=AgentType.OPENAI_FUNCTIONS, 
                         verbose=True, 
                         agent_kwargs={"system_message": system_message})

result = agent.invoke({
    "input": "Find the latest NBA news about the Golden State Warriors, summarize them, and email me a summary."
})

print(result)