from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(
    model_name="claude-fable-5-1",
    api_key='sk-yFOTmuKp5mZee1kP6ZrS3FiCZqy63wvckE0fiAq0JLgu4fuZ',
    base_url='https://globalai.vip/v1',
    timeout=240
)

SYSTEM_PROMPT = """你是足球情报记者，负责收集关于球队的新闻动态。"""


def speak() -> str:

    prompt = f"""## 比赛资料
{report}

请以主队支持者的立场，进行第{round_num}轮发言。
- 若是首轮，陈述你的核心论点和关键证据
- 若非首轮，先针对B上一轮的观点逐一反驳，再补充己方新论据"""

    result = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ])
    return result.content