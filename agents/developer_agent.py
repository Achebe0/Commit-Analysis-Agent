import f
from dotenv import load_dotenv
import os

load_dotenv()

def create_markdown_file(file, title):

    # create the markdown file by writing to a file
    with open("solution.md","w") as file:
        file.write("We now have something in the file")

    # some logic to rewrite the markdown file to get a different solution.
    # Not sure if we need to use some tool as memory or if LangGraph has that alreadu




def developer_agent():
    pass

