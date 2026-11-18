from crawler.sportsmole import get_article
from langgraph.types import Send
from config import OKOOO_RECENT_N, OKOOO_COOKIE, MATCHES, SELECTION_COUNT
from typing import TypedDict, Annotated, Optional, Union
from langgraph.graph import StateGraph, START, END


class IntelligenceState(TypedDict):
    pass

def route_matches(state) -> list[Send]:
    return [Send("analyze_one_match", {"match": match}) for match in state["matches"]]



workflow = StateGraph(IntelligenceState)
