from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

from state import State
from dotenv import load_dotenv
from agents import ingestion
import os


load_dotenv()


llm = init_chat_model(
    "google_genai:gemini-3.5-flash",
)

agent = create_agent(
    model=llm,

    system_prompt="You are an engineer with 15 YOE, diagnose the issues in the txt file and give a detailed solution"
                  "for an engineer to implement the solution. The solution should be detailed enough for an experienced engineer to implement the solution. ",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": f"Analyze the logs and propose a solution:  {logs}"}]}
)
print(result["messages"][-1].content_blocks)

def developer_agent(state:State, output_file:str):
    log_file = ingestion.get_render_logs(state,output_file)

    with open(log_file,"r") as f:
        logs = f.read()

    result = agent.invoke({
        "messages":[
            {"role":"user","content":f"Analyze the logs and propose a detailed solution: \n\n {logs}"}
        ]
    })

    analysis = result["messages"][-1].content

    create_markdown_file("analysis.md", "Analysis of System Logs", analysis)
    return state.analysis_file

def create_markdown_file(file, title, body:str):
    with open(file, "w") as f:
        f.write(f"# {title}\n\n{body}")
    return file





