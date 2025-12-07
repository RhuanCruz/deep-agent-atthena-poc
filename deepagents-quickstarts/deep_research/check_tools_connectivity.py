import os
import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

def debug_env_file():
    print("\n--- DEBUG: Environment Variables Loaded (os.getenv) ---")
    keys_to_check = [
        "POSTGRES_CONNECTION_STRING", 
        "AZURE_SEARCH_ENDPOINT", 
        "AZURE_SEARCH_KEY", 
        "AZURE_SEARCH_ADMIN_KEY",
        "AZURE_OPENAI_API_KEY"
    ]
    for k in keys_to_check:
        val = os.getenv(k)
        status = "✅ Present" if val else "❌ Missing"
        length = len(val) if val else 0
        print(f"{k}: {status} (Length: {length})")

    print("\n--- DEBUG: Inspecting .env file raw content ---")
    try:
        with open(".env", "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                # Check for trailing space in key
                key_clean = key.strip()
                if key != key_clean:
                    print(f"Line {i}: ⚠️ WARNING: Key has trailing whitespace! '{key}' -> '{key_clean}'")
                print(f"Line {i}: Key='{key_clean}' (Len: {len(key_clean)}) | Value_Len={len(val)}")
            else:
                print(f"Line {i}: [WARNING] No '=' found: {line}")
    except Exception as e:
        print(f"Could not read .env file: {e}")

def check_postgres():
    print("\n--- Checking PostgreSQL Connection ---")
    conn_str = os.getenv("POSTGRES_CONNECTION_STRING")
    if not conn_str:
        print("❌ POSTGRES_CONNECTION_STRING not found in env.")
        return

    try:
        # Attempt minimal connection
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        print(f"✅ PostgreSQL Connected! Check result: {result}")
        conn.close()
    except Exception as e:
        print(f"❌ PostgreSQL Connection Failed: {e}")

def check_azure_search():
    print("\n--- Checking Azure AI Search Connection ---")
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    api_key = os.getenv("AZURE_SEARCH_KEY") or os.getenv("AZURE_SEARCH_ADMIN_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX", "external-documents")
    api_version = os.getenv("AZURE_API_VERSION", "2023-11-01")

    if not endpoint or not api_key:
        print("❌ AZURE_SEARCH credentials missing.")
        return

    url = f"{endpoint}/indexes/{index_name}/docs/search?api-version={api_version}"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }
    # Simple query to check connectivity
    body = {"search": "*", "top": 1, "select": "title"}

    try:
        response = requests.post(url, headers=headers, json=body, timeout=10)
        if response.status_code == 200:
            print(f"✅ Azure Search Connected! Status: {response.status_code}")
        else:
            print(f"❌ Azure Search Failed. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"❌ Azure Search Connection Error: {e}")

if __name__ == "__main__":
    debug_env_file()
    check_postgres()
    check_azure_search()
