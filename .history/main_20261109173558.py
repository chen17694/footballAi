import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.intelligence_agent import app as intelligence_app
from agents.data_agent import app as data_app
from agents.handicap_agent import app as handicap_app
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from rich import print as rprint
import agents.A as A
import agents.B as B
import agents.C as C

MAX_ROUNDS = 3  # 最大轮次

class MainState(TypedDict):
    intelligence: list
    data: list
    analysis: str
    handicap: list
    debate: Annotated[list, operator.add] # 辩论记录
    round: int # 当前轮次
    verdict: str # C 的裁定


llm = ChatOpenAI(
    model_name="claude-fable-5-1",
    temperature=0.4,
    api_key='sk-yFOTmuKp5mZee1kP6ZrS3FiCZqy63wvckE0fiAq0JLgu4fuZ',
    base_url='https://globalai.vip/v1',
    timeout=240
)

def debate_a(state):
    content = A.speak(report, state["debate"], state["round"] + 1)
    return {"debate": [{"speaker": "A", "round": state["round"]+1, "content": content}], "round": state["round"]+1}

def debate_b(state):
    content = B.speak(report, state["debate"], state["round"])
    return {"debate": [{"speaker": "B", "round": state["round"], "content": content}]}

def judge_c(state):
    return {"verdict": C.judge(report, state["debate"])}

def match_report(state: MainState):
    intelligence = intelligence_app.invoke({"articles": []})
    xgscore = data_app.invoke({"xgscore": []})
    handicap = handicap_app.invoke({"handicap": []})
    return {"intelligence": intelligence["articles"], "data": xgscore["xgscore"], "handicap": handicap["handicap"]}

def analyze_match(state: MainState):
    intelligence = state["intelligence"]
    data = state["data"]
    handicap = state["handicap"]
    # 在这里可以对 intelligence 和 data 进行进一步的分析和处理
    result = llm.invoke([
        SystemMessage(content="你是一个足球数据分析师。请根据提供的情报、数据和盘口进行分析。"),
        HumanMessage(content=f"情报: {intelligence}\n数据: {data}\n盘口: {handicap}")
    ])
    return {"analysis": result.content}

def roundtable_meeting():

    pass

def should_continue(state):
    return "debate_a" if state["round"] < MAX_ROUNDS else "judge_c"


workflow = StateGraph(MainState)
workflow.add_node("get_match_report", match_report)
workflow.add_node("start_the_roundtable_meeting", roundtable_meeting)
workflow.add_node("analyze_match", analyze_match)
workflow.add_edge(START, "get_match_report")
workflow.add_edge("get_match_report", "start_the_roundtable_meeting")
workflow.add_edge("start_the_roundtable_meeting", END)

app = workflow.compile()
if __name__ == "__main__":
    result = app.invoke({"intelligence": [], "data": [], "analysis": "", "handicap": [], "debate": [], "round": 0, "verdict": ""})
    rprint(result["analysis"])  
   
