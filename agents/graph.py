from agents.analyze_logs import analyze_logs
from agents.developer_agent import generate_fix_plan
from agents.ingestion import ingest_logs
from agents.state import State


try:
    from langgraph.graph import StateGraph, START, END

    def run_pipeline(state: State, repo_path: str, log_path: str | None = None) -> State:
        state = ingest_logs(state, log_path)
        state = analyze_logs(state)
        state["fix_plan"] = generate_fix_plan(state)
        state["solution_markdown"] = state["fix_plan"]
        state["deployment_status"] = "ready_for_review"
        return state

    graph = StateGraph(State)
    graph.add_node("ingest", lambda state: ingest_logs(state, None))
    graph.add_node("analyze", analyze_logs)
    graph.add_node("plan", lambda state: {**state, "fix_plan": generate_fix_plan(state)})
    graph.add_node("done", lambda state: {**state, "deployment_status": "ready_for_review"})

    graph.add_edge(START, "ingest")
    graph.add_edge("ingest", "analyze")
    graph.add_edge("analyze", "plan")
    graph.add_edge("plan", "done")
    graph.add_edge("done", END)
except Exception:
    graph = None

