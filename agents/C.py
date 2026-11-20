import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from typing import List
from agents._retry import call_with_retry
from agents._react import run_react

llm = ChatOpenAI(
    model_name="gpt-6.2-astra",
    api_key='sk-yFOTmuKp5mZee1kP6ZrS3FiCZqy63wvckE0fiAq0JLgu4fuZ',
    base_url='https://globalai.vip/v1',
    timeout=240
)

class JudgeResult(BaseModel):
    verdict: str = Field(description="完整裁定文本，包含哪方论据更有说服力、最终结论和推荐方向")
    risks: List[str] = Field(
        default_factory=list,
        description="A和B尚未充分辩论的重要风险点列表（每条简明扼要）。若已无需继续辩论，返回空列表。"
    )


SYSTEM_PROMPT = """你是足球分析裁定官C，没有立场，客观公正。
读完A和B的全部辩论后，权衡双方论据的质量和可信度，给出裁定。
若发现A和B尚未充分讨论的重要风险，在risks中列出，供他们继续辩论；若无需继续辩论，risks返回空列表。
你拥有联网搜索工具，裁定前可主动搜索核实双方论据中的关键事实（伤病、阵容、赔率变化等）。"""



def judge(report: str, history: list) -> JudgeResult:
    history_text = "\n\n".join(
        f"【{d['speaker']}·第{d['round']}轮】{d['content']}"
        for d in history
    )

    prompt = f"""## 比赛资料
{report}

## 完整辩论记录
{history_text}

请给出裁定：
1. 哪方论据更有说服力，理由是什么
2. 最终结论和推荐方向（主队/客队）
3. 若存在A和B尚未辩论过的风险，在risks字段中列出；若无，risks返回空列表
"""
    messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)]

    # 第一步：带联网搜索的 ReAct agent 生成裁定分析文本
    analysis_text = run_react(
        llm,
        messages,
        fallback_invoke=lambda msgs: call_with_retry(llm.invoke, msgs),
    )

    if not isinstance(analysis_text, str):
        analysis_text = str(analysis_text or "")

    # 第二步：用结构化输出从分析文本中提取 verdict 和 risks，彻底避免正则解析
    extract_messages = [
        SystemMessage(content="你是一个信息提取助手，严格按照指定格式提取内容，不添加任何额外内容。"),
        HumanMessage(content=f"""请从以下裁定分析文本中提取信息：

{analysis_text}

提取规则：
- verdict：裁定的完整正文，保留所有分析内容，去除risks相关的JSON/代码块部分
- risks：列出文中提到的"待辩风险"或"尚未充分讨论的风险"，每条一个字符串；若无则返回空列表"""),
    ]

    try:
        structured_llm = llm.with_structured_output(JudgeResult)
        result = structured_llm.invoke(extract_messages)
        return result
    except Exception:  # noqa: BLE001
        # 结构化提取失败时降级：verdict 用原始文本，risks 为空
        return JudgeResult(verdict=analysis_text, risks=[])
