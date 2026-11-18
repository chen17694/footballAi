import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from typing import List
from agents._retry import call_with_retry
from agents._react import run_react

llm = ChatOpenAI(
    model_name="gemini-4-argon",
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


def _normalize_risks(items) -> list:
    """把模型给的 risks 数组统一成 List[str]。"""
    risks = []
    for item in items if isinstance(items, list) else []:
        if isinstance(item, dict):
            risk = str(item.get("risk", "")).strip()
            detail = str(item.get("detail", "")).strip()
            if risk and detail:
                risks.append(f"{risk}：{detail}")
            elif risk or detail:
                risks.append(risk or detail)
        elif isinstance(item, str) and item.strip():
            risks.append(item.strip())
    return risks


def _split_verdict_and_risks(text: str) -> tuple[list, str]:
    """从 C 的自由文本里拆出裁定正文与 risks 列表。

    兼容两种模型输出：``**risks：** [ ... ]``，以及结尾的 ```json {...} ``` 块里的
    ``"risks": [...]``。解析失败时视为“无待辩风险”，保证裁定一定返回 JudgeResult，
    不会因为结构不合法而让整个辩论中断。
    """
    text = (text or "").strip()

    # 形式一：**risks：** + JSON 数组
    m = re.search(r"\*{0,2}\s*risks\s*\*{0,2}\s*[：:]\s*", text, re.I)
    if m:
        head = text[:m.start()].rstrip().rstrip("*").rstrip()
        tail = text[m.end():].strip()
        start, end = tail.find("["), tail.rfind("]")
        if start != -1 and end > start:
            try:
                return _normalize_risks(json.loads(tail[start:end + 1])), head or text
            except Exception:  # noqa: BLE001
                pass
        return [], head or text

    # 形式二：结尾的 ```json {...} ``` 块
    for fm in re.finditer(r"```(?:json)?\s*([\s\S]*?)```", text, re.I):
        try:
            data = json.loads(fm.group(1).strip())
        except Exception:  # noqa: BLE001
            continue
        if isinstance(data, dict) and isinstance(data.get("risks"), list):
            head = text[:fm.start()].rstrip().rstrip("*").rstrip()
            return _normalize_risks(data["risks"]), head or text

    return [], text


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

    # 只调用一次 LLM（带联网搜索），risks 由本地解析，避免第二次调用拖慢裁定
    analysis_text = run_react(
        llm,
        messages,
        fallback_invoke=lambda msgs: call_with_retry(llm.invoke, msgs),
        response_format=JudgeResult
    )

    if not isinstance(analysis_text, str):
        analysis_text = str(analysis_text or "")

    risks, verdict = _split_verdict_and_risks(analysis_text)
    return JudgeResult(verdict=verdict or analysis_text, risks=risks)
