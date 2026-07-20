import json
from pathlib import Path


def load_knowledge_base():

    base_path = Path(__file__).parent

    kb_path = base_path / "mental_health_indicators.json"

    with open(kb_path, "r", encoding="utf-8") as f:
        return json.load(f)