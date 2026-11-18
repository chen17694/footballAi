import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(
    model_name="gemini-4-carbon",
    api_key='sk-yFOTmuKp5mZee1kP6ZrS3FiCZqy63wvckE0fiAq0JLgu4fuZ',
    base_url='https://globalai.vip/v1',
    timeout=240
)

SYSTEM_PROMPT = """你是足球分析师B，站在最强反方立场，找出分析师A是否有遗漏或错误的事实、过度乐观的假设、不可逆成本、机会成本、最坏后果，以及情绪和个人偏好造成的判断偏差。
观点要有理有据，不可捏造数据，但可以对数据做有利于己方的解读。
控制在300字以内。"""


def speak(report: str, history: list, round_num: int) -> str:
    history_text = "\n\n".join(
        f"【{d['speaker']}·第{d['round']}轮】{d['content']}"
        for d in history
    ) if history else "（暂无辩论记录，请开始首轮发言）"

    prompt = f"""## 比赛资料
{report}

## 辩论记录
{history_text}

请以客队支持者的立场，进行第{round_num}轮发言。
- 若是首轮，陈述你的核心论点和关键证据
- 若非首轮，先针对A上一轮的观点逐一反驳，再补充己方新论据"""

    result = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ])
    return result.content
