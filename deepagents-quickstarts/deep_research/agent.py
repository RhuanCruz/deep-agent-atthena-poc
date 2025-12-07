"""Equity Research Deep Agent."""

import os
from datetime import datetime

from langchain_openai import AzureChatOpenAI
from deepagents import create_deep_agent

from research_agent.prompts import (
    DIRECTOR_SYSTEM_PROMPT,
    FORENSIC_ACCOUNTANT_INSTRUCTIONS,
    STRATEGY_ANALYST_INSTRUCTIONS,
    DATA_VIZ_SPECIALIST_INSTRUCTIONS,
    LEAD_ANALYST_INSTRUCTIONS,
    COMPLIANCE_OFFICER_INSTRUCTIONS,
)

model = AzureChatOpenAI(
    azure_deployment=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    temperature=0.0
)

from research_agent.tools import (
    dummy_search, 
    think_tool, 
    query_financial_db,
    inspect_database_tables,
    search_fre_vector
)


from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

# --- SUB-AGENTS (MANUAL INSTANTIATION) ---

# 1. Forensic Accountant (Hard Data)
forensic_agent = create_deep_agent(
    model=model,
    tools=[query_financial_db, inspect_database_tables, think_tool],
    system_prompt=FORENSIC_ACCOUNTANT_INSTRUCTIONS,
)

@tool
def forensic_accountant(task: str) -> str:
    """Delegates a financial research task to the Forensic Accountant agent.
    
    Use this for fetching HARD DATA (Revenue, Income, Debt, etc.) from the SQL database.
    Pass a clear task description (e.g. "Get Revenue for AMER3 in 2024").
    """
    try:
        response = forensic_agent.invoke({"messages": [HumanMessage(content=task)]})
        return response["messages"][-1].content
    except Exception as e:
        return f"Forensic Agent Failed: {e}"

# 2. Strategy Analyst (Soft Data)
strategy_agent = create_deep_agent(
    model=model,
    tools=[search_fre_vector, think_tool],
    system_prompt=STRATEGY_ANALYST_INSTRUCTIONS,
)

@tool
def strategy_analyst(task: str) -> str:
    """Delegates a qualitative analysis task to the Strategy Analyst agent.
    
    Use this for researching RISKS, STRATEGY, and CONTEXT from unstructured text.
    Pass a clear question (e.g. "What are the strategic risks for Americanas?").
    """
    try:
        response = strategy_agent.invoke({"messages": [HumanMessage(content=task)]})
        return response["messages"][-1].content
    except Exception as e:
        return f"Strategy Agent Failed: {e}"

# --- MAIN DIRECTOR AGENT ---

agent = create_deep_agent(
    model=model,
    tools=[
        forensic_accountant, 
        strategy_analyst, 
        think_tool,
        dummy_search 
    ], 
    system_prompt=DIRECTOR_SYSTEM_PROMPT,
    subagents=[], 
)
