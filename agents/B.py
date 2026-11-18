import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from agents._retry import call_with_retry
from agents._react import run_react

llm = ChatOpenAI(
    model_name="gpt-6.2-astra",
    api_key='sk-yFOTmuKp5mZee1kP6ZrS3FiCZqy63wvckE0fiAq0JLgu4fuZ',
    base_url='https://globalai.vip/v1',
    timeout=240
)

SYSTEM_PROMPT = """你是足球分析师B，站在反方立场，找出分析师A是否有遗漏或错误的事实、过度乐观的假设、不可逆成本、机会成本、最坏后果，以及情绪和个人偏好造成的判断偏差。
观点要有理有据，不可捏造数据。
控制在300字以内。
你拥有联网搜索工具，当比赛资料或辩论中提到的信息不足、过时或存疑时，可主动搜索查证最新伤病、阵容、战绩、交锋记录等。"""


def speak(report: str, history: list, round_num: int, risks: list = None) -> str:
    history_text = "\n\n".join(
        f"【{d['speaker']}·第{d['round']}轮】{d['content']}"
        for d in history
    ) if history else "（暂无辩论记录，请开始首轮发言）"

    risks_instruction = ""
    if risks:
        risks_list = "\n".join(f"- {r}" for r in risks)
        risks_instruction = f"""
## 裁判C指定的待辩风险（本轮必须逐一回应）
{risks_list}
"""

    prompt = f"""## 比赛资料
{report}

## 辩论记录
{history_text}
{risks_instruction}
请以客队支持者的立场，进行第{round_num}轮发言。
- 若是首轮，陈述你的核心论点和关键证据
- 若非首轮，先针对A上一轮的观点逐一反驳，再补充己方新论据
- 若裁判C提出了待辩风险，必须逐一表明立场并给出论据"""

    result = run_react(
        llm,
        [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)],
        fallback_invoke=lambda msgs: call_with_retry(llm.invoke, msgs),
    )
    return result
