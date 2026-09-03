import f
from dotenv import load_dotenv
import os

from state import State
load_dotenv()


def developer(state:State):
    pass


#develop a solution that accurately solves the problem the analyze_logs agent provided and put it into a markdown file
def create_markdown_file(file, title):

    # create the markdown file by writing to a file
    with open("solution.md","w") as file:
        file.write("We now have something in the file")

    # some logic to rewrite the markdown file to get a different solution.
    # Not sure if we need to use some tool as memory or if LangGraph has that already






