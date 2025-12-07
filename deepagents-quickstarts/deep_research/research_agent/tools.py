"""Tools for the Research Agent."""
import os
import requests
import psycopg2
from typing import Optional, List, Dict, Any
from langchain_core.tools import tool
from dotenv import load_dotenv

# Load env vars
load_dotenv(override=True)

def _get_db_connection():
    try:
        conn = psycopg2.connect(os.getenv("POSTGRES_CONNECTION_STRING"))
        return conn
    except Exception as e:
        raise ConnectionError(f"Failed to connect to database: {e}")

@tool(parse_docstring=True)
def query_financial_db(query: str) -> str:
    """Execute a raw SQL query against the Financial Database (PostgreSQL).
    
    Use this tool to retrieve precise quantitative data (Revenue, EBITDA, Debt, etc.)
    from structured tables.

    Args:
        query: Valid SQL query string (read-only).
    """
    # 🛡️ SECURITY CHECK: Enforce READ-ONLY access
    normalized_query = query.strip().upper()
    if not normalized_query.startswith("SELECT"):
        return "Security Error: Only SELECT queries are allowed to prevent data modification."

    conn = None
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchmany(50) # Limit to 50 rows to protect context window
            
            if not results:
                return "No results found."
            
            # Format Markdown table
            md_table = "| " + " | ".join(columns) + " |\n"
            md_table += "| " + " | ".join(["---"] * len(columns)) + " |\n"
            
            for row in results:
                row_str = [str(x) for x in row]
                md_table += "| " + " | ".join(row_str) + " |\n"
            
            if len(results) == 50:
                md_table += "\n*(Results truncated to 50 rows for safety based on context limits)*"
                
            return md_table
        else:
            conn.commit()
            return "Query executed successfully (no results returned)."
            
    except Exception as e:
        return f"SQL Error: {e}"
    finally:
        if conn:
            conn.close()

@tool(parse_docstring=True)
def inspect_database_tables() -> str:
    """Retrieve the list of tables and their schema in the database.
    
    Call this FIRST to understand the database structure before writing queries.
    """
    return query_financial_db.invoke("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")

@tool(parse_docstring=True)
def search_fre_vector(query: str, section_type: str = None) -> str:
    """Search the 'Corporate Memory' (Vector Store) for qualitative context.
    
    Use this to find 'Risk Factors', 'Strategy', 'Governance' details from 
    reference forms (FRE).

    Args:
        query: The semantic search query (e.g. "principais riscos operacionais").
        section_type: Optional filter. Common types: 'RISK_FACTORS', 'STRATEGY', 'GOVERNANCE', 'BUSINESS_OVERVIEW'.
    """
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    api_key = os.getenv("AZURE_SEARCH_KEY") or os.getenv("AZURE_SEARCH_ADMIN_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX", "external-documents")
    api_version = os.getenv("AZURE_API_VERSION", "2023-11-01")

    if not endpoint or not api_key:
        return "Error: Azure Search credentials not configured."

    url = f"{endpoint}/indexes/{index_name}/docs/search?api-version={api_version}"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }

    # Logging inputs
    print(f"🔎 [Vector Search] Query: '{query}' | Filter: {section_type}")

    # Construct Body
    # Schema Mapping:
    # title -> titulo
    # content -> conteudo
    # section_type -> tipo_secao
    # year -> ano_fiscal
    # company_name -> companhia_nome
    # source -> (Not present in index, will fallback)
    
    body = {
        "search": query,
        "top": 5,
        "select": "titulo,conteudo,ano_fiscal,tipo_secao,companhia_nome" 
    }

    if section_type:
        body["filter"] = f"tipo_secao eq '{section_type}'"

    try:
        response = requests.post(url, headers=headers, json=body, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        docs = data.get("value", [])
        print(f"✅ [Vector Search] Hit Count: {len(docs)}")
        
        # --- FALLBACK MECHANISM ---
        if not docs and section_type:
            print(f"⚠️ [Vector Search] No results with filter '{section_type}'. Retrying broad search...")
            # Remove filter and retry
            if "filter" in body:
                del body["filter"]
            
            response = requests.post(url, headers=headers, json=body, timeout=10)
            response.raise_for_status()
            data = response.json()
            docs = data.get("value", [])
            print(f"🔄 [Vector Search] Retry Hit Count: {len(docs)}")
        # --------------------------

        if not docs:
            return "No relevant documents found in vector store."
            
        formatted_results = ""
        for i, doc in enumerate(docs, 1):
            title = doc.get("titulo", "Unknown Doc")
            content = doc.get("conteudo", "")[:1000]
            year = doc.get("ano_fiscal", "N/A")
            company = doc.get("companhia_nome", "Unknown Company")
            section = doc.get("tipo_secao", "Unknown Section")
            
            formatted_results += f"Source [{i}]: {title} ({year}) - {company} [Section: {section}]\n"
            formatted_results += f"Content: {content}...\n"
            formatted_results += "-" * 40 + "\n"
        
        # Log snippet
        print(f"📄 [Vector Search] Result Snippet: {formatted_results[:200]}...")
        return formatted_results

    except Exception as e:
        print(f"❌ [Vector Search] Error: {e}")
        return f"Vector Search Error: {e}"

@tool(parse_docstring=True)
def dummy_search(query: str) -> str:
    """A dummy search tool that returns a placeholder.
    
    Args:
        query: The search query string.
    """
    return f"Search placeholder. Query: {query}"

@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection.
    
    Args:
        reflection: The thoughtful reflection or reasoning to record.
    """
    return f"Reflection recorded: {reflection}"
