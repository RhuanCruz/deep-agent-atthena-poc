
import os
import time
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Load env vars
load_dotenv(override=True)

try:
    from agent import agent
    print("Agent imported successfully.")
except Exception as e:
    print(f"Failed to import agent: {e}")
    exit(1)

input_message = "Qual foi o lucro líquido da Petrobras no 3T25 e quais os riscos operacionais?"
print(f"\nInvoking agent with: '{input_message}'")
print("-" * 50)

try:
    # Stream events to observe the flow
    # 'values' mode returns the state at each step
    for event in agent.stream({"messages": [HumanMessage(content=input_message)]}, stream_mode="values"):
        # We look for the last message in the state
        messages = event.get("messages", [])
        if messages:
            last_msg = messages[-1]
            print(f"\n[{last_msg.type.upper()}]: {last_msg.content[:200]}...") 
            # Print only start of message to avoid spam, unless it's the final answer
            
            if last_msg.type == "ai" and not last_msg.tool_calls:
                 print("\n>>> POTENTIAL FINAL ANSWER (Content Preview):")
                 print(last_msg.content)

    print("\nExecution complete.")

except Exception as e:
    print(f"\nERROR during execution: {e}")
