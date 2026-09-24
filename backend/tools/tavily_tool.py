import os
from typing import Any, Dict, List, Optional

import requests


class TavilySearchTool:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.enabled = bool(self.api_key)

    def search(self, query: str, max_results: int = 3) -> Dict[str, Any]:
        if not self.enabled:
            return {
                "enabled": False,
                "message": "TAVILY_API_KEY is not set. Add it to .env to enable external web search.",
                "results": [],
            }

        try:
            response = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": self.api_key,
                    "query": query,
                    "max_results": 5,
                    "search_depth": "advanced",
                    "include_answer": True,
                    "include_raw_content": False,
                },
                timeout=20,
            )
            response.raise_for_status()
            payload = response.json()
            results = payload.get("results", [])
            answer = payload.get("answer")
            return {
                "enabled": True,
                "answer": answer,
                "results": results,
                "message": "Web search completed."
            }
        except Exception as exc:  # pragma: no cover - optional external dependency
            return {
                "enabled": False,
                "message": f"Tavily search unavailable: {exc}",
                "results": [],
            }


def get_tavily_tool() -> TavilySearchTool:
    return TavilySearchTool()
