#!/usr/bin/env python
import os
import uvicorn
from fastapi import FastAPI
from langserve import add_routes
from agent import agent
from pydantic import BaseModel
from typing import List, Any, Dict

# Bypass introspection bug by defining explicit schemas
class Input(BaseModel):
    messages: List[Dict[str, Any]]

class Output(BaseModel):
    messages: List[Dict[str, Any]]

# Wrap the agent with explicit types
agent_runnable = agent.with_types(input_type=Input, output_type=Output)

app = FastAPI(
    title="Deep Research Agent",
    version="1.0",
    description="A multi-agent system for Equity Research (Financials + Strategy).",
)

add_routes(
    app,
    agent_runnable,
    path="/research",
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
