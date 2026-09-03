from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

#analyze the logs and provide a detailed solution to bring the system back up and running




def analyze_logs(logs: str) -> str:
    # have some GraphQL endpoint to stream the data

    agent = create_agent(
        model="google_genai:gemini-3.5-flash",
        system_prompt="You are a professional infrastructure engineer with 15+ YOE, who can take messy and even unclear "
                      "logs or messages and provide a clear, detailed structure and reason to why the system failed and enough reasoning to give to an experienced engineer to code "
                      "the solution ",
    )

    result = agent.invoke(
        {"message":[{
            "role":"user","content":"Provide the reason for downtime and provide a detailed solution to bring it back up"
        }]}
    )

    return result["messages"][-1].content

    # call on a tool and use Gemini to analyze and give feedback into what is going on


    # pass this onto the developer_agent

