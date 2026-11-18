import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler.handicap import get_handicap
from langgraph.types import Send
from config import OKOOO_RECENT_N, OKOOO_COOKIE, MATCHES, SELECTION_COUNT
from typing import TypedDict, Annotated, Optional, Union
from langgraph.graph import StateGraph, START, END
import operator
from langchain_core.messages import HumanMessage, SystemMessage

class MatchState(TypedDict):
    match_id: str
    match_config: dict
    raw_handicap: str

class AgentState(TypedDict):
    handicap: Annotated[list, operator.add]


def route_matches(state) -> list[Send]:
    return [
        Send("match", {
            "match_id": m["OKOOO_MATCH_ID"],
            "match_config": m,
        })
        for m in MATCHES
    ]

def handicap_node(state: MatchState):
    match = state["match_config"]

    handicap = get_handicap(match["OKOOO_MATCH_ID"], OKOOO_COOKIE)


    return {
        "handicap": handicap
    }

def build_match_graph() -> object:
    g = StateGraph(MatchState)
    g.add_node("handicap",  handicap_node)
    g.add_edge(START,    "handicap")
    g.add_edge("handicap",  END)
    return g.compile()

match_graph = build_match_graph()

def run_match(state: MatchState) -> dict:
    result = match_graph.invoke(state)
   
    return {"handicap": [{"match_id": state["match_id"], "content": result['raw_handicap']}]}

workflow = StateGraph(AgentState)

workflow.add_node("match", run_match)
workflow.add_conditional_edges(START, route_matches, ["match"])
workflow.add_edge("match", END)

app = workflow.compile()

result = app.invoke({"handicap": []})
