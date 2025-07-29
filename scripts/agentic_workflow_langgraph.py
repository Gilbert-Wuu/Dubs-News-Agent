from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from agent_tools import AGENT_TOOLS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SYSTEM_PROMPT = (
    "You are an NBA news assistant. "
    "When scraping news, always try the full keyword first. "
    "If you find no results with the full keyword, try again with a more general or shorter keyword (e.g., use 'Warriors' if 'Golden State Warriors' returns nothing). "
    "Summarize the news and email the results."
)

# prompt_template = ChatPromptTemplate.from_messages([
#     SystemMessage(content=SYSTEM_PROMPT),
#     HumanMessage(content="{input}"),
#     ("ai", "{agent_scratchpad}")
# ])

# Choose your LLM
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

# Create the LangGraph agent with a custom system prompt
agent = create_react_agent(
    model=llm,
    tools=AGENT_TOOLS,
    prompt=SYSTEM_PROMPT
)

result = agent.invoke({
    "input": "Find the latest NBA news about the Golden State Warriors, summarize them, and email me a summary."
})

for m in result["messages"]:
    m.pretty_print()

'''
workflow = StateGraph()
workflow.add_node("agent", agent)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)
graph = workflow.compile()

result = graph.invoke({
    "input": "Find the latest NBA news about the Golden State Warriors, summarize them, and email me a summary."
})
print(result)
'''
