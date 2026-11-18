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
