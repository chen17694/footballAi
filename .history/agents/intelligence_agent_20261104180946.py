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


def run_match(state: MatchState) -> dict:
    """主图里的 match 节点：调用子图跑完整的 fetch → filter 流程。"""
    match_id = state["match_id"]
    output_path = Path(f"result_{match_id}.md")
    data_path = Path(f"data_{match_id}.md")

    # 如果结果文件已存在，直接读取
    if output_path.exists():
        rprint(f"  [yellow]比赛 {match_id} 结果已存在，跳过重复运行[/yellow]")
        filter_result = output_path.read_text(encoding="utf-8")
        # 从原始数据文件读取 article
        if data_path.exists():
            text = data_path.read_text(encoding="utf-8")
            parts = text.split("\n\n## ")
            article = parts[2].split("\n", 1)[1]
        else:
            article = ""
        return {"filter_results": [{"match_id": match_id, "filter_result": filter_result, "article": article}]}


    # 否则正常运行子图
    result = match_graph.invoke(state)
    rprint(f"[bold green]════ 比赛 {match_id} 处理完成 ════[/bold green]\n")
    # 子图 State 是 MatchState，filter_result 和 article 字段传递给主图
    return {"filter_results": [{"match_id": result["match_id"], "filter_result": result["filter_result"], "article": result["article"]}]}



workflow = StateGraph(MatchState)

workflow.add_node("match", run_match)
workflow.add_conditional_edges(START, route_matches, ["match"])