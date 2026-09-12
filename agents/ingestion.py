import json
import os
import subprocess
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from agents.state import State

load_dotenv()


def normalize_log_entry(entry: Any, source: str = "unknown") -> dict[str, Any]:
    if isinstance(entry, dict):
        message = (
            entry.get("message")
            or entry.get("msg")
            or entry.get("error")
            or entry.get("detail")
            or json.dumps(entry, default=str)
        )
        timestamp = entry.get("timestamp") or entry.get("time") or entry.get("ts")
        level = entry.get("level") or entry.get("severity") or "INFO"
    else:
        message = str(entry)
        timestamp = None
        level = "INFO"

    return {
        "timestamp": timestamp,
        "level": str(level).upper(),
        "source": source,
        "message": str(message),
        "raw": entry,
    }


def parse_json_logs(text: str, source: str = "json") -> list[dict[str, Any]]:
    data = json.loads(text)
    if isinstance(data, list):
        return [normalize_log_entry(item, source) for item in data]
    if isinstance(data, dict):
        return [normalize_log_entry(data, source)]
    return [normalize_log_entry(data, source)]


def parse_text_logs(text: str, source: str = "text") -> list[dict[str, Any]]:
    logs = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        logs.append({
            "timestamp": None,
            "level": "INFO",
            "source": source,
            "message": line,
            "raw": line,
        })
    return logs


def read_log_file(path: str) -> list[dict[str, Any]]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    text = file_path.read_text(encoding="utf-8")
    if not text.strip():
        return []

    try:
        return parse_json_logs(text, file_path.name)
    except json.JSONDecodeError:
        return parse_text_logs(text, file_path.name)


def run_command(command: str) -> list[dict[str, Any]]:
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    error = result.stderr.strip()

    if output:
        try:
            return parse_json_logs(output, "command")
        except json.JSONDecodeError:
            return parse_text_logs(output, "command")

    if error:
        return parse_text_logs(error, "command")

    raise RuntimeError(f"Command returned no logs: {command}")


def ingest_logs(state: State, log_path: str | None = None) -> State:
    load_dotenv()

    if log_path:
        logs = read_log_file(log_path)
    else:
        configured_path = os.getenv("LOG_PATH")
        if configured_path:
            logs = read_log_file(configured_path)
        else:
            command = os.getenv("COMMAND")
            if not command:
                raise RuntimeError("No log source configured. Set LOG_PATH or COMMAND in .env.")
            logs = run_command(command)

    state["raw_logs"] = logs
    state["parsed_logs"] = logs
    return state


def get_render_logs(state: State, log_path: str | None = None) -> State:
    return ingest_logs(state, log_path)

