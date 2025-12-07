import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Load env vars from .env file explicitly
load_dotenv(override=True)

print("--- Checking Environment Variables ---")

# Method 1: Check your Environment Variable (Most common)
api_key = os.environ.get("AZURE_OPENAI_API_KEY")

if api_key:
    # Handle case where key might be shorter than 4 chars (unlikely but safe)
    suffix = api_key[-4:] if len(api_key) >= 4 else api_key
    print(f"✅ Method 1: Current API Key ends in: ...{suffix}")
else:
    print("❌ Method 1: No AZURE_OPENAI_API_KEY found in environment variables.")

# Method 2: Check the LangChain Object directly
print("\n--- Checking LangChain Object ---")
try:
    # Using the model specified in agent.py
    llm = AzureChatOpenAI(
        azure_deployment=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        temperature=0.0
    )
    
    # LangChain often stores api_key as a SecretStr
    if llm.openai_api_key:
        key_val = llm.openai_api_key.get_secret_value() if hasattr(llm.openai_api_key, 'get_secret_value') else str(llm.openai_api_key)
        suffix = key_val[-4:] if len(key_val) >= 4 else key_val
        print(f"✅ Method 2: LLM Object Key ends in: ...{suffix}")
    else:
        print("❌ Method 2: LLM Object has no openai_api_key set.")
except Exception as e:
    print(f"❌ Method 2 Error: Could not initialize LLM. {e}")
