# -*- coding: utf-8 -*-
"""ReAct 工具调用助手。A/B/C/D 共用。

用 langchain.agents.create_react_agent + AgentExecutor 实现。
工具用 @tool 装饰器自定义，底层调 tavily-python SDK。
若 tool calling 失败或 key 无效，自动降级为普通 invoke。
"""
import logging
from langchain.tools import tool

log = logging.getLogger(__name__)

_agent_cache: dict = {}  # 按 llm id 缓存，避免重复创建


@tool
def search_web(query: str) -> str:
    """搜索网络，获取足球赛事最新资讯（伤病、阵容、赔率、交锋记录等）。
    query: 搜索关键词，尽量具体，如"丹麦 vs 挪威 2026 伤病"
    """
    from config import TAVILY_API_KEY
    from tavily import TavilyClient
    client = TavilyClient(api_key=TAVILY_API_KEY)
    resp = client.search(query, max_results=3)
    results = resp.get("results", [])
    if not results:
        return "未找到相关结果。"
    return "\n\n".join(
        f"[{r.get('title', '')}]\n{r.get('content', '')}"
        for r in results
    )


def _get_agent(llm):
    key = id(llm)
    if key not in _agent_cache:
        from langgraph import create_agent, AgentExecutor
        from  langchain_core.prompts import PromptTemplate

        # ReAct prompt 模板（中文）
        template = """你是一名足球分析助手，可以使用以下工具：

{tools}

使用以下格式：
Thought: 我需要思考是否需要查询信息
Action: 工具名称（必须是 [{tool_names}] 之一）
Action Input: 传给工具的输入
Observation: 工具返回的结果
...（可重复多次 Thought/Action/Observation）
Thought: 我现在有足够信息了
Final Answer: 最终回答

{input}
{agent_scratchpad}"""

        prompt = PromptTemplate.from_template(template)
        agent = create_agent(llm, tools=[search_web], prompt=prompt)
        _agent_cache[key] = AgentExecutor(
            agent=agent,
            tools=[search_web],
            handle_parsing_errors=True,
            max_iterations=4,
            verbose=False,
        )
    return _agent_cache[key]


def run_react(llm, messages: list, fallback_invoke=None) -> str:
    """用 ReAct agent 运行，返回最终回答文本。
    messages: LangChain 消息列表（SystemMessage + HumanMessage）。
    失败时降级到 fallback_invoke(messages)，或直接 llm.invoke(messages)。
    """
    # 把消息列表拼成一段文本传给 AgentExecutor（它接受字符串 input）
    input_text = "\n".join(
        f"{'【系统】' if m.__class__.__name__ == 'SystemMessage' else '【用户】'}{m.content}"
        for m in messages
    )
    try:
        agent = _get_agent(llm)
        result = agent.invoke({"input": input_text})
        return result.get("output", "")
    except Exception as e:  # noqa: BLE001
        log.warning("ReAct agent 失败，降级为普通 invoke：%s", repr(e)[:200])
        if fallback_invoke:
            return fallback_invoke(messages).content
        return llm.invoke(messages).content
