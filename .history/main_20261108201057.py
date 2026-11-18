import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.intelligence_agent import app as intelligence_app
from agents.data_agent import app as data_app
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator

class MainState(TypedDict):
    intelligence: list
    data: list

def run_intelligence(state):
    r = intelligence_app.invoke({"articles": []})
    return {"intelligence": r["articles"]}

def run_data(state):
    r = data_app.invoke({"articles": []})
    return {"data": r["articles"]}

workflow = StateGraph(MainState)
workflow.add_node("intelligence", run_intelligence)
workflow.add_node("data", run_data)
workflow.add_edge(START, "intelligence")
workflow.add_edge(START, "data")        # 两个 agent 并行
workflow.add_edge("intelligence", END)
workflow.add_edge("data", END)

app = workflow.compile()
result = app.invoke({"intelligence": [], "data": []})