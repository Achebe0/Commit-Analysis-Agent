import os
import requests
from langchain.agents import create_agent


def get_render_logs(service_id: str) -> list[dict]:
    """Tool: pulls recent logs for the LLM Router service from Render's API"""
    headers = {"Authorization": f"Bearer {os.getenv('RENDER_API_KEY')}"}
    response = requests.get(
        f"https://api.render.com/v1/services/{service_id}/logs",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()



get_render_logs(service_id=os.getenv("RENDER_SERVICE_ID"))
# Commit Analysis Agent — Investigator
agent = create_agent(
    model="azure_ai:your-deployment-name",   # Azure = Commit Agent's reasoning engine
    tools=[get_render_logs, get_recent_commits, get_ci_status],  # Render = LLM Router's real logs
    system_prompt=(
        "You are an infrastructure investigator. The LLM Router prototype "
        "is hosted on Render. Use get_render_logs to check recent errors, "
        "cross-reference with recent commits and CI status, and diagnose "
        "the likely cause of the failure."
    ),
)