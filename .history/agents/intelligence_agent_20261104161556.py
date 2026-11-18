from crawler.sportsmole import get_article
from langgraph.types import Send
from config import OKOOO_RECENT_N, OKOOO_COOKIE, MATCHES, SELECTION_COUNT
from typing import TypedDict, Annotated, Optional, Union
from langgraph.graph import StateGraph, START, END


class IntelligenceState(TypedDict):
    match_id: str
    match_config: dict

def route_matches(state) -> list[Send]:
    return [
        Send("analyze_one_match", {"match": match}) 
        for match in state["matches"]
    ]

def analyze_one_match(state: SingleMatchState) -> dict:
    match = state["match"]
    features = ai_main.analyze(
        preview_url=match["preview_url"],
        xgscore_url=match["xgscore_url"],
        clubelo_home_url=match.get("clubelo_home_url", ""),
        clubelo_away_url=match.get("clubelo_away_url", ""),
        sportsmole_url=match.get("sportsmole_url", ""),
        okooo_match_id=match["okooo_match_id"],
        okooo_recent_n=match.get("okooo_recent_n", OKOOO_RECENT_N),
        okooo_cookie=match.get("okooo_cookie", OKOOO_COOKIE),
    )
    return {"results": [{"match": match, "features": features}]}


workflow = StateGraph(IntelligenceState)
workflow.add_node()

workflow.add_edge(START, "route_matches", route_matches)