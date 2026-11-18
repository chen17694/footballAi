import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler.sportsmole import get_article
from langgraph.types import Send
from config import OKOOO_RECENT_N, OKOOO_COOKIE, MATCHES, SELECTION_COUNT
from typing import TypedDict, Annotated, Optional, Union
from langgraph.graph import StateGraph, START, END
import operator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class MatchState(TypedDict):
    match_id: str
    match_config: dict
    article: str


class OuterState(TypedDict):
    articles: Annotated[list, operator.add]

llm = ChatOpenAI(
    model_name="claude-fable-5-1",
    temperature=0.4,
    api_key='sk-yFOTmuKp5mZee1kP6ZrS3FiCZqy63wvckE0fiAq0JLgu4fuZ',
    base_url='https://globalai.vip/v1',
    timeout=240
)

def route_matches(state) -> list[Send]:
    return [
        Send("match", {
            "match_id": m["OKOOO_MATCH_ID"],
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
    result = match_graph.invoke(state)
    articles = llm.invoke([
        SystemMessage(content="你是足球情报分析师，整理并提炼原始情报，不输出投注建议。"),
        HumanMessage(content=result['article'])
    ])
    return {"articles": [articles.content]}


workflow = StateGraph(OuterState)

workflow.add_node("match", run_match)

workflow.add_conditional_edges(START, route_matches, ["match"])
workflow.add_edge("match", END)

app = workflow.compile()

if __name__ == "__main__":
    result = app.invoke({"articles": []})
    print(result)
   