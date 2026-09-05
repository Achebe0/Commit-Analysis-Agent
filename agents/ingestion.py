import os
import requests
import subprocess
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

def get_render_logs(filename, title) -> int:
    with open(filename, "w") as f:
        return f.write(subprocess.run( r".\render logs --resources srv-d60or8juibrs73dtcveg --output json > logs_from_render.txt",
        shell=True))

