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
from pathlib import Path
from config import OKOOO_RECENT_N, OKOOO_COOKIE, MATCHES, SELECTION_COUNT

MAX_ROUNDS = 6  # 最大轮次

class MainState(TypedDict):
    intelligence: list
    data: list
    handicap: list
    report: str                             # 拼合后的完整比赛资料
    debate: Annotated[list, operator.add]   # 辩论记录
    round: int                              # 当前轮次
    verdict: str                            # C 的裁定


llm = ChatOpenAI(
    model_name="claude-fable-5-1",
    temperature=0.4,
    api_key='sk-yFOTmuKp5mZee1kP6ZrS3FiCZqy63wvckE0fiAq0JLgu4fuZ',
    base_url='https://globalai.vip/v1',
    timeout=240
)

def match_report(state: MainState):
    intelligence = intelligence_app.invoke({"articles": []})
    xgscore = data_app.invoke({"xgscore": []})
    handicap = handicap_app.invoke({"handicap": []})
    # 拼合成完整比赛资料字符串，供 A/B/C 使用
    intel_text = "\n".join(a["content"] for a in intelligence["articles"])
    data_text = "\n".join(d["content"] for d in xgscore["xgscore"])
    handicap_text = "\n".join(h["content"] for h in handicap["handicap"])
    report = f"## 情报\n{intel_text}\n\n## 数据\n{data_text}\n\n## 盘口\n{handicap_text}"
    return {
        "intelligence": intelligence["articles"],
        "data": xgscore["xgscore"],
        "handicap": handicap["handicap"],
        "report": report,
    }


def debate_a(state: MainState):
    round_num = state["round"] + 1
    handicap_rules = Path("handicap.md").read_text(encoding="utf-8")
    content = A.speak(state["report"], state["debate"], round_num)
    return {
        "debate": [{"speaker": "A", "round": round_num, "content": content}],
        "round": round_num,
    }


def debate_b(state: MainState):
    content = B.speak(state["report"], state["debate"], state["round"])
    return {
        "debate": [{"speaker": "B", "round": state["round"], "content": content}],
    }


def judge_c(state: MainState):
    return {"verdict": C.judge(state["report"], state["debate"])}


def should_continue(state: MainState):
    return "debate_a" if state["round"] < MAX_ROUNDS else "judge_c"

workflow = StateGraph(MainState)
workflow.add_node("match_report", match_report)
workflow.add_node("debate_a", debate_a)
workflow.add_node("debate_b", debate_b)
workflow.add_node("judge_c", judge_c)

workflow.add_edge(START, "match_report")
workflow.add_edge("match_report", "debate_a")
workflow.add_edge("debate_a", "debate_b")
workflow.add_conditional_edges("debate_b", should_continue, {
    "debate_a": "debate_a",
    "judge_c": "judge_c",
})
workflow.add_edge("judge_c", END)

app = workflow.compile()
if __name__ == "__main__":
    result = app.invoke({"intelligence": [], "data": [], "handicap": [], "report": "", "debate": [], "round": 0, "verdict": ""})
    rprint("=== 最终裁定 ===")
    rprint(result["verdict"])
