import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(override=True)

def inspect_index_fields():
    print("\n--- Inspecting Vector Index Schema ---")
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    api_key = os.getenv("AZURE_SEARCH_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX", "external-documents")
    api_version = os.getenv("AZURE_API_VERSION", "2023-11-01")

    url = f"{endpoint}/indexes/{index_name}/docs/search?api-version={api_version}"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }
    
    # Request stats using facets if possible, or just fetch top 100 to sample
    body = {
        "search": "*",
        "top": 50,
        "select": "companhia_nome,companhia_ticker,tipo_secao,ano_fiscal"
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=10)
        if response.status_code == 200:
            data = response.json()
            docs = data.get("value", [])
            
            print(f"✅ Retrieved {len(docs)} sample documents.")
            
            tickers = set()
            sections = set()
            companies = set()
            years = set()

            for doc in docs:
                tickers.add(doc.get("companhia_ticker"))
                sections.add(doc.get("tipo_secao"))
                companies.add(doc.get("companhia_nome"))
                years.add(doc.get("ano_fiscal"))

            print("\n--- 📊 Index Content Analysis (Sample 50) ---")
            print(f"🏢 Companies found: {list(companies)}")
            print(f"🎫 Tickers found: {list(tickers)}")
            print(f"📅 Years found: {list(years)}")
            print(f"📑 Section Types found: {list(sections)}")
            
            if not docs:
                 print("⚠️ Index appears empty.")
        else:
            print(f"❌ Failed to inspect index. Status: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    inspect_index_fields()
