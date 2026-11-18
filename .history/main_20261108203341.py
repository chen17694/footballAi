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

def match_report(state):
    intelligence = intelligence_app.invoke({"articles": []})
    xgscore = data_app.invoke({"articles": []})
    return {"intelligence": intelligence["content"], "data": xgscore["content"]}


workflow = StateGraph(MainState)
workflow.add_node("match_report", match_report)
workflow.add_node("analyze_match", analyze_match)
workflow.add_edge(START, "match_report")
workflow.add_edge("match_report", "analyze_match")
workflow.add_edge("analyze_match", END)

app = workflow.compile()
if __name__ == "__main__":
    result = app.invoke({"intelligence": [], "data": []})
    print("intelligence:", result["intelligence"])
    print("data:", result["data"])