from langgraph.graph import StateGraph, START, END
from state import State

from investigator import stream_logs
from developer_agent import  create_markdown_file


graph = StateGraph(State)

