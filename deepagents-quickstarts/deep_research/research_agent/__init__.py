"""Deep Research Agent Example.

This module demonstrates building a research agent using the deepagents package
with custom tools for web search and strategic thinking.
"""

from research_agent.prompts import (
    DIRECTOR_INSTRUCTIONS,
    FORENSIC_ACCOUNTANT_INSTRUCTIONS,
    STRATEGY_ANALYST_INSTRUCTIONS,
    DATA_VIZ_SPECIALIST_INSTRUCTIONS,
    LEAD_ANALYST_INSTRUCTIONS,
    COMPLIANCE_OFFICER_INSTRUCTIONS,
)
from research_agent.tools import tavily_search, dummy_search, think_tool

__all__ = [
    "tavily_search",
    "dummy_search",
    "think_tool",
    "DIRECTOR_INSTRUCTIONS",
    "FORENSIC_ACCOUNTANT_INSTRUCTIONS",
    "STRATEGY_ANALYST_INSTRUCTIONS",
    "DATA_VIZ_SPECIALIST_INSTRUCTIONS",
    "LEAD_ANALYST_INSTRUCTIONS",
    "COMPLIANCE_OFFICER_INSTRUCTIONS",
]
