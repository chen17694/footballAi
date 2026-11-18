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
import agents.D as D
from pathlib import Path
from config import OKOOO_RECENT_N, OKOOO_COOKIE, MATCHES, SELECTION_COUNT

MAX_ROUNDS = 6  # 最大轮次


# ===== 第一步：收集所有比赛的报告（并行，一次跑完）=====

REPORT_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / "output" / "roundtable"


def collect_reports():
    """收集所有比赛的数据，按 match_id 分组，返回 [{match_id, content}]。
    已缓存的比赛直接从本地读取，跳过 API 调用。
    """
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    missing = [m for m in MATCHES if not (REPORT_DIR / f"{m['OKOOO_MATCH_ID']}_report.md").exists()]

    intel_map = data_map = hand_map = handicap_rules = None
    if missing:
        intelligence = intelligence_app.invoke({"articles": []})
        xgscore = data_app.invoke({"xgscore": []})
        handicap = handicap_app.invoke({"handicap": []})
        handicap_rules = Path("handicap.md").read_text(encoding="utf-8")

        intel_map = {a["match_id"]: a["content"] for a in intelligence["articles"]}
        data_map = {d["match_id"]: d["content"] for d in xgscore["xgscore"]}
        hand_map = {h["match_id"]: h["content"] for h in handicap["handicap"]}

    reports = []
    for m in MATCHES:
        mid = m["OKOOO_MATCH_ID"]
        cache_path = REPORT_DIR / f"{mid}_report.md"

        if cache_path.exists():
            content = cache_path.read_text(encoding="utf-8")
        else:
            content = (
                f"## 情报\n{intel_map.get(mid, '')}\n\n"
                f"## 数据\n{data_map.get(mid, '')}\n\n"
                f"## 盘口\n{hand_map.get(mid, '')}\n\n"
                f"## 盘口规则\n{handicap_rules}"
            )
            cache_path.write_text(content, encoding="utf-8")

        reports.append({"match_id": mid, "content": content})
    return reports


# ===== 第二步：单场比赛的辩论图（每场比赛独立跑一遍）=====

class DebateState(TypedDict):
    report: str                            # 单场比赛的完整资料
    debate: Annotated[list, operator.add]  # 辩论记录
    round: int                              # 当前轮次
    verdict: str                            # C 的裁定


def debate_a(state: DebateState):
    round_num = state["round"] + 1
    content = A.speak(state["report"], state["debate"], round_num)
    return {
        "debate": [{"speaker": "A", "round": round_num, "content": content}],
        "round": round_num,
    }


def debate_b(state: DebateState):
    content = B.speak(state["report"], state["debate"], state["round"])
    return {
        "debate": [{"speaker": "B", "round": state["round"], "content": content}],
    }


def judge_c(state: DebateState):
    return {"verdict": C.judge(state["report"], state["debate"])}


def should_continue(state: DebateState):
    return "debate_a" if state["round"] < MAX_ROUNDS else "judge_c"


debate_workflow = StateGraph(DebateState)
debate_workflow.add_node("debate_a", debate_a)
debate_workflow.add_node("debate_b", debate_b)
debate_workflow.add_node("judge_c", judge_c)

debate_workflow.add_edge(START, "debate_a")
debate_workflow.add_edge("debate_a", "debate_b")
debate_workflow.add_conditional_edges("debate_b", should_continue, {
    "debate_a": "debate_a",
    "judge_c": "judge_c",
})
debate_workflow.add_edge("judge_c", END)

debate_app = debate_workflow.compile()


# ===== 第三步：逐场比赛跑辩论，各自存文件 =====

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "roundtable")
    os.makedirs(out_dir, exist_ok=True)

    reports = collect_reports()
    rprint(f"收集到 {len(reports)} 场比赛报告")

    verdicts = []  # 收集所有比赛的裁定，供 D 使用

    for r in reports:
        match_id = r["match_id"]
        rprint(f"\n{'='*50}\n开始辩论比赛 {match_id}\n{'='*50}")

        result = debate_app.invoke({
            "report": r["content"],
            "debate": [],
            "round": 0,
            "verdict": "",
        })

        # 保存 report
        with open(os.path.join(out_dir, f"{match_id}_report.md"), "w", encoding="utf-8") as f:
            f.write(r["content"])

        # 保存辩论记录 + 裁定
        lines = ["# 辩论记录\n"]
        for d in result["debate"]:
            lines.append(f"## 【{d['speaker']}·第{d['round']}轮】\n")
            lines.append(d["content"])
            lines.append("\n---\n")
        lines.append("# 最终裁定\n")
        lines.append(result["verdict"])
        with open(os.path.join(out_dir, f"{match_id}_debate.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        rprint(f"比赛 {match_id} 完成，已保存 {match_id}_report.md 和 {match_id}_debate.md")
        verdicts.append({"match_id": match_id, "verdict": result["verdict"]})

    # 所有比赛裁定完毕，D 选出精选推荐
    rprint(f"\n{'='*50}\nD 开始精选推荐\n{'='*50}")
    pick = D.pick(verdicts)
    with open(os.path.join(out_dir, "pick.md"), "w", encoding="utf-8") as f:
        f.write("# 精选推荐\n\n")
        f.write(pick)
    rprint("=== 精选推荐 ===")
    rprint(pick)
    rprint(f"\n全部完成，文件保存在 {out_dir}")
