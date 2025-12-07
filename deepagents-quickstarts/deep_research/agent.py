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

from research_agent.tools import (
    dummy_search, 
    think_tool, 
    query_financial_db,
    inspect_database_tables,
    search_fre_vector
)


forensic_accountant_agent = {
    "name": "forensic_accountant",
    "description": "Extrai dados quantitativos (Hard Data) estruturados via SQL.",
    "system_prompt": FORENSIC_ACCOUNTANT_INSTRUCTIONS,
    "tools": [query_financial_db, inspect_database_tables, think_tool], 
}

strategy_analyst_agent = {
    "name": "strategy_analyst",
    "description": "Analisa aspectos qualitativos e riscos via busca vetorial.",
    "system_prompt": STRATEGY_ANALYST_INSTRUCTIONS,
    "tools": [search_fre_vector, think_tool],
}

data_viz_agent = {
    "name": "data_viz_specialist",
    "description": "Gera código Python para gráficos profissionais.",
    "system_prompt": DATA_VIZ_SPECIALIST_INSTRUCTIONS,
    "tools": [dummy_search, think_tool],
}

lead_analyst_agent = {
    "name": "lead_analyst",
    "description": "Revisor e Redator. Sintetiza inputs no relatório final. Pode solicitar revisões.",
    "system_prompt": LEAD_ANALYST_INSTRUCTIONS,
    "tools": [think_tool],
}

compliance_officer_agent = {
    "name": "compliance_officer",
    "description": "Auditor Final. Verifica alucinações, consistência e qualidade visual. Rejeita se necessário.",
    "system_prompt": COMPLIANCE_OFFICER_INSTRUCTIONS,
    "tools": [think_tool],
}

model = AzureChatOpenAI(
    azure_deployment=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    temperature=0.0
)

agent = create_deep_agent(
    model=model,
    tools=[], 
    system_prompt=DIRECTOR_SYSTEM_PROMPT,
    subagents=[
        forensic_accountant_agent,
        strategy_analyst_agent,
        data_viz_agent,
        lead_analyst_agent,
        compliance_officer_agent,
    ],
)
