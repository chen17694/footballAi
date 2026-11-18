from crawler.sportsmole import get_article
from langgraph.types import Send
from config import OKOOO_RECENT_N, OKOOO_COOKIE, MATCHES, SELECTION_COUNT
from typing import TypedDict, Annotated, Optional, Union
from langgraph.graph import StateGraph, START, END


class MatchState(TypedDict):
    match_id: str
    match_config: dict

def route_matches(state) -> list[Send]:
    return [
        Send("match", {
            "match_id":    m["OKOOO_MATCH_ID"],
            "match_config": m,
        })
        for m in MATCHES
    ]

def fetch_node(state: MatchState) -> MatchState:
    match = state["match_config"]
    if match["SPORTSMOLE_URL"]:
        article = get_article(match["SPORTSMOLE_URL"])
    else:
        article = ''
    Information = match.get("Information", "")
    if Information and Information.strip():
        article += f"\n\n#### Information\n{Information.strip()}"
  

    return {
        "article": article
    }


def build_match_graph() -> object:
    """构建单场比赛的子图（fetch → filter），所有比赛共用同一个子图定义。"""
    g = StateGraph(MatchState)
    g.add_node("fetch",  fetch_node)
    g.add_edge(START,    "fetch")
    g.add_edge("fetch",  END)
    return g.compile()

match_graph = build_match_graph()

def run_match(state: MatchState) -> dict:
    """主图里的 match 节点：调用子图跑完整的 fetch → filter 流程。"""
    match_id = state["match_id"]

    result = match_graph.invoke(state)
    return {"filter_results": [{"match_id": result["match_id"], "filter_result": result["filter_result"], "article": result["article"]}]}



workflow = StateGraph(MatchState)

workflow.add_node("match", run_match)
workflow.add_conditional_edges(START, route_matches, ["match"])