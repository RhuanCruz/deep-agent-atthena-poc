"""Deep Research Agent Example.

This module demonstrates building a research agent using the deepagents package
with custom tools for web search and strategic thinking.
"""

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

__all__ = [
    "dummy_search",
    "think_tool",
    "query_financial_db",
    "inspect_database_tables",
    "search_fre_vector",
    "DIRECTOR_SYSTEM_PROMPT",
    "FORENSIC_ACCOUNTANT_INSTRUCTIONS",
    "STRATEGY_ANALYST_INSTRUCTIONS",
    "DATA_VIZ_SPECIALIST_INSTRUCTIONS",
    "LEAD_ANALYST_INSTRUCTIONS",
    "COMPLIANCE_OFFICER_INSTRUCTIONS",
]
