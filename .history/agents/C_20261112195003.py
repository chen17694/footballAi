import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(
    model_name="gpt-6-astra",
    temperature=0.4,
    api_key='sk-yFOTmuKp5mZee1kP6ZrS3FiCZqy63wvckE0fiAq0JLgu4fuZ',
    base_url='https://globalai.vip/v1',
    timeout=240
)

SYSTEM_PROMPT = """你是足球分析裁定官C，没有立场，客观公正。
读完A和B的全部辩论后，权衡双方论据的质量和可信度，给出最终裁定。"""


def judge(report: str, history: list) -> str:
    history_text = "\n\n".join(
        f"【{d['speaker']}·第{d['round']}轮】{d['content']}"
        for d in history
    )

    prompt = f"""## 比赛资料
{report}

## 完整辩论记录
{history_text}

请给出最终裁定，包含以下内容：
1. 哪方论据更有说服力，理由是什么
2. 最终结论和推荐方向（让球方/受让方/观望）
3. 主要风险提示
"""

    result = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ])
    return result.content
