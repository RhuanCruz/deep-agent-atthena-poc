"""Research Tools.

This module provides search and content processing utilities for the research agent.
"""

import os
import httpx
from langchain_core.tools import tool
from markdownify import markdownify
from tavily import TavilyClient
from typing_extensions import Annotated, Literal

try:
    tavily_client = TavilyClient()
except Exception:
    tavily_client = None

# --- Local Document Tools (Mock RAG) ---
DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")

@tool(parse_docstring=True)
def read_local_document(
    doc_name: str,
    query: str = None
) -> str:
    """Read specific local documents (ITR, FRE, DFP) by name or list available ones.
    
    Use this tool to fetch the full text of a financial document to extract data.
    
    Args:
        doc_name: Exact filename or keywords like 'ITR', 'FRE', 'Petrobras'. If 'list', returns available files.
        query: Optional query to filter or focus (currently returns full text for simplicity).
    """
    if not os.path.exists(DOCS_DIR):
        return f"Erro: Diretório de documentos não encontrado em {DOCS_DIR}"
        
    files = os.listdir(DOCS_DIR)
    
    # 1. List files
    if doc_name.lower() == "list":
        return f"Documentos Disponíveis:\n" + "\n".join([f"- {f}" for f in files])
    
    # 2. Fuzzy match filename
    target_file = None
    for f in files:
        if doc_name.lower() in f.lower():
            target_file = f
            break
            
    if not target_file:
        return f"Documento '{doc_name}' não encontrado. Disponíveis: {files}"
        
    # 3. Read content
    try:
        path = os.path.join(DOCS_DIR, target_file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"## Documento: {target_file}\n\n{content}"
    except Exception as e:
        return f"Erro ao ler {target_file}: {e}"

# --- Search Tools ---
@tool(parse_docstring=True)
def dummy_search(query: str) -> str:
    """A dummy search tool that returns a placeholder.
    
    Args:
        query: Search query
    """
    return f"Search is currently disabled. Query: {query}"


def fetch_webpage_content(url: str, timeout: float = 10.0) -> str:
    """Fetch and convert webpage content to markdown.

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds

    Returns:
        Webpage content as markdown
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = httpx.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return markdownify(response.text)
    except Exception as e:
        return f"Error fetching content from {url}: {str(e)}"


@tool(parse_docstring=True)
def tavily_search(
    query: str,
    max_results: int = 1,
    topic: Literal["general", "news", "finance"] = "general",
) -> str:
    """Search the web for information on a given query.

    Uses Tavily to discover relevant URLs, then fetches and returns full webpage content as markdown.

    Args:
        query: Search query to execute
        max_results: Maximum number of results to return (default: 1)
        topic: Topic filter - 'general', 'news', or 'finance' (default: 'general')
    """
    if not tavily_client:
        return "Tavily Search not configured (missing API key)."

    # Use Tavily to discover URLs
    try:
        search_results = tavily_client.search(
            query,
            max_results=max_results,
            topic=topic,
        )

        # Fetch full content for each URL
        result_texts = []
        for result in search_results.get("results", []):
            url = result["url"]
            title = result["title"]

            # Fetch webpage content
            content = fetch_webpage_content(url)

            result_text = f"""## {title}
**URL:** {url}

{content}

---
"""
            result_texts.append(result_text)

        # Format final response
        response = f"""🔍 Found {len(result_texts)} result(s) for '{query}':

{chr(10).join(result_texts)}"""

        return response
    except Exception as e:
        return f"Error executing Tavily search: {e}"


@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on research progress and decision-making.

    Use this tool after each search to analyze results and plan next steps systematically.
    This creates a deliberate pause in the research workflow for quality decision-making.

    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?

    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?

    Args:
        reflection: Your detailed reflection on research progress, findings, gaps, and next steps
    """
    return f"Reflection recorded: {reflection}"
