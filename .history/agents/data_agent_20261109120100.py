import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler.xgscore.build import build_report as get_xgscore
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
    xgscore: str
    raw_xgscore: str
    xgscore_json: dict

class AgentState(TypedDict):
    xgscore: Annotated[list, operator.add]

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

def xgscore_node(state: MatchState):
    match = state["match_config"]
    elo_golo = {
        "home_elo":  match["CLUBELO_HOME_ELO"],
        "away_elo":  match["CLUBELO_AWAY_ELO"],
        "home_golo": match["CLUBELO_HOME_GOLO"],
        "away_golo": match["CLUBELO_AWAY_GOLO"],
    }

    xgscore = get_xgscore(
        preview_url=match["PREVIEW_URL"],
        xgscore_url=match["XGSCORE_URL"],
        elo_golo=elo_golo,
    )

    print(xgscore)


    result = llm.invoke([
        SystemMessage(
            content="你是一个足球数据提取器。请把输入的XGSCORE报告转换为标准的 JSON 格式数据。"
        ),
        HumanMessage(content=xgscore)
    ])

    return {
        "raw_xgscore": xgscore,
        "xgscore_json": result.model_dump()
    }

def build_match_graph() -> object:
    g = StateGraph(MatchState)
    g.add_node("xgscore",  xgscore_node)
    g.add_edge(START,    "xgscore")
    g.add_edge("xgscore",  END)
    return g.compile()

match_graph = build_match_graph()

def run_match(state: MatchState) -> dict:
    print("Running match:", state["match_id"])
    result = match_graph.invoke(state)
    xgscore = llm.invoke([
        SystemMessage(content="你是足球情报分析师，整理并提炼数据，不输出投注建议。"),
        HumanMessage(content=result['raw_xgscore'])
    ])
    print(xgscore.content)
    return {"xgscore": [{"match_id": state["match_id"], "content": xgscore.content}]}

workflow = StateGraph(AgentState)

if __name__ == "__main__":
    workflow.add_node("match", run_match)
    workflow.add_conditional_edges(START, route_matches, ["match"])
    workflow.add_edge("match", END)

    app = workflow.compile()

