import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from agents._retry import call_with_retry
from agents._react import run_react

llm = ChatOpenAI(
    model_name="claude-fable-5-2",
    api_key='sk-yFOTmuKp5mZee1kP6ZrS3FiCZqy63wvckE0fiAq0JLgu4fuZ',
    base_url='https://globalai.vip/v1',
    timeout=240
)

SYSTEM_PROMPT = """你是足球精选分析师D，负责从多场比赛的裁定结果中，选出最值得投注的一场。
选择标准：裁定结论清晰、论据最充分、风险最低、赔率最合理。
只选一场，给出明确理由。
你拥有联网搜索工具，选择前可主动搜索各场比赛的最新赔率、阵容确认、伤停情况等，以提升精选质量。"""


def pick(verdicts: list[dict]) -> str:
    """
    从所有比赛的裁定结果中选出精选推荐。
    verdicts: [{"match_id": str, "verdict": str}, ...]
    """
    verdicts_text = "\n\n".join(
        f"### 比赛 {v['match_id']}\n{v['verdict']}"
        for v in verdicts
    )

    prompt = f"""以下是今日全部比赛的裁定结果：

{verdicts_text}

请从中选出最值得投注的一场，给出：
1. 选择哪场比赛（match_id）
2. 推荐方向（让球方/受让方/大球/小球）
3. 选择理由（与其他比赛横向比较后的核心依据）
4. 主要风险提示"""

    result = run_react(
        llm,
        [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)],
        fallback_invoke=lambda msgs: call_with_retry(llm.invoke, msgs),
    )
    return result
