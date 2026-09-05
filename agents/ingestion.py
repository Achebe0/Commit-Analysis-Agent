import os
import subprocess
from dotenv import load_dotenv
from state import State

load_dotenv()
# ingesting the logs from the system
def get_render_logs(state:State):
    with open("filename", "w") as f:
        return f.write(subprocess.run(os.getenv("COMMAND"),
        shell=True))

