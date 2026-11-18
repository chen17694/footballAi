from crawler.sportsmole import get_article
from langgraph.types import Send
from config import OKOOO_RECENT_N, OKOOO_COOKIE, MATCHES, SELECTION_COUNT
from typing import TypedDict, Annotated, Optional, Union

# article_data = get_article(MATCHES[0]["SPORTSMOLE_URL"])

class AgentState(TypedDict):
    match_id: str
    match_config: dict

def dispatch(state: AgentState):
    """
    路由函数：为每场比赛生成一个 Send，触发并行执行。
    Send("match", {...}) 表示：把这份数据发给 "match" 节点跑一次。
    """
    return [
        Send("match", {
            "match_id":    m["OKOOO_MATCH_ID"],
            "match_config": m,
        })
        for m in MATCHES
    ]