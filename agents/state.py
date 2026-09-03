from typing import TypedDict, Optional

class State(TypedDict):

    service_id: str
    owner_id: str
    raw_logs: list[dict]
    parsed_json_logs : list[dict]
    issue_analysis: Optional[str]
    solution_markdown: Optional[str]