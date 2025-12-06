"""Equity Research Deep Agent."""

import os
from datetime import datetime

# from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
from deepagents import create_deep_agent

from research_agent.prompts import (
    DIRECTOR_INSTRUCTIONS,
    FORENSIC_ACCOUNTANT_INSTRUCTIONS,
    STRATEGY_ANALYST_INSTRUCTIONS,
    DATA_VIZ_SPECIALIST_INSTRUCTIONS,
    LEAD_ANALYST_INSTRUCTIONS,
    COMPLIANCE_OFFICER_INSTRUCTIONS,
)

# Import tools
from research_agent.tools import dummy_search, think_tool, read_local_document

# --- Sub-Agent Definitions ---

# Forensic Accountant gets native 'read_local_document' to fetch ITR/DFP
forensic_accountant_agent = {
    "name": "forensic_accountant",
    "description": "Extrai dados quantitativos (Hard Data) consolidados de ITR/DFP. Limpeza rigorosa de dados.",
    "system_prompt": FORENSIC_ACCOUNTANT_INSTRUCTIONS,
    "tools": [read_local_document, think_tool], 
}

# Strategy Analyst gets native 'read_local_document' to fetch FRE
strategy_analyst_agent = {
    "name": "strategy_analyst",
    "description": "Analisa aspectos qualitativos, notas explicativas, riscos e eventos específicos (Lava Jato, etc.).",
    "system_prompt": STRATEGY_ANALYST_INSTRUCTIONS,
    "tools": [read_local_document, think_tool],
}

data_viz_agent = {
    "name": "data_viz_specialist",
    "description": "Gera código Python para gráficos profissionais (Plotly/Matplotlib). Regras rígidas de design.",
    "system_prompt": DATA_VIZ_SPECIALIST_INSTRUCTIONS,
    "tools": [dummy_search, think_tool],
}

lead_analyst_agent = {
    "name": "lead_analyst",
    "description": "Revisor e Redator. Sintetiza inputs no relatório final. Pode solicitar revisões.",
    "system_prompt": LEAD_ANALYST_INSTRUCTIONS,
    "tools": [dummy_search, think_tool],
}

compliance_officer_agent = {
    "name": "compliance_officer",
    "description": "Auditor Final. Verifica alucinações, consistência e qualidade visual. Rejeita se necessário.",
    "system_prompt": COMPLIANCE_OFFICER_INSTRUCTIONS,
    "tools": [dummy_search, think_tool],
}

# --- Main Agent Setup ---

model = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)

# The 'Director' is the main orchestrator.
agent = create_deep_agent(
    model=model,
    tools=[], # Director has NO tools other than sub-agents. MUST Delegate.
    system_prompt=DIRECTOR_INSTRUCTIONS,
    subagents=[
        forensic_accountant_agent,
        strategy_analyst_agent,
        data_viz_agent,
        lead_analyst_agent,
        compliance_officer_agent,
    ],
)
