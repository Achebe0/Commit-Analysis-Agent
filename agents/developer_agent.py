from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

from state import State
from dotenv import load_dotenv
from agents import ingestion
import os


load_dotenv()

#declaring the model
llm = init_chat_model(
    "google_genai:gemini-3.5-flash",
)

#giving the agent a system prompt and goal
agent = create_agent(
    model=llm,
    system_prompt="You are a senior engineer with 15 YOE, given an issue you can produce a detailed, implementation ready"
                  " solution with concrete steps, considering edge cases and code eligibility"
)

# the function takes the ingest file and passes the state and the output file
def developer_agent(state:State, issue_analysis, output_file:str):
    result = agent.invoke({
        "messages":[
            {
                "role":"user",
                "content":(
                    "Create a detailed solution for the issue analysis\n\n"
                    f"{issue_analysis}\n\n"
                )
            }
        ]
    })

    solution = result["messages"][-1].content
    return create_markdown_file(output_file, "Solution", solution)


def create_markdown_file(file, title, body:str):
    with open(file, "w") as f:
        f.write(f"# {title}\n\n{body}")
    return file





