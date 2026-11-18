# -*- coding: utf-8 -*-
"""ReAct 工具调用助手。A/B/C/D 共用。

调用 run_react(llm, messages) 让模型自主决定是否联网搜索。
若代理不支持 tool calling 或 Tavily key 无效，自动降级为普通 invoke。
"""
from langchain.tools import tool
from tavily import TavilyClient
from config import TAVILY_API_KEY
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

import logging

log = logging.getLogger(__name__)

_agent_cache: dict = {}  # 按 llm id 缓存，避免重复创建

@tool
def search_web(query: str) -> str:
    """搜索网络获取最新足球赛事信息，包括伤病、阵容、赔率变化、交锋记录等。
    query 应为简洁的英文或中文搜索关键词。"""
    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        result = client.search(query, max_results=3)
        snippets = [r.get("content", "") for r in result.get("results", [])]
        return "\n\n".join(snippets) if snippets else "未找到相关结果"
    except Exception as e:  # noqa: BLE001
        return f"搜索失败：{repr(e)[:200]}"

def _get_agent(llm, response_format: str = "text") -> object:
    key = id(llm)
    if key not in _agent_cache:

        # 使用 system_prompt 配置提示词与角色
        system_prompt = """你是一名足球分析助手，可以使用提供的工具来查询和分析信息。"""

        _agent_cache[key] = create_agent(
            model=llm,
            tools=[search_web],
            system_prompt=system_prompt,
            response_format=ToolStrategy(response_format),
        )
    return _agent_cache[key]


def run_react(llm, messages: list, fallback_invoke=None, response_format: str = "text") -> str:
    """用 ReAct agent 运行，返回最终回答文本。
    失败时降级到 fallback_invoke(messages)，或直接 llm.invoke(messages)。
    """
    try:
        agent = _get_agent(llm, response_format=response_format)
        print('agent-------------------------')
        print(response_format)
        result = agent.invoke({"messages": messages})
        # 取最后一条 AIMessage 的内容
        final = result["messages"][-1].content
        if isinstance(final, list):
            # 部分模型返回 content blocks 列表
            final = " ".join(
                b.get("text", "") if isinstance(b, dict) else str(b)
                for b in final
            )
        return final
    except Exception as e:  # noqa: BLE001
        print(e)
        if fallback_invoke:
            return fallback_invoke(messages).content
        return llm.invoke(messages).content
