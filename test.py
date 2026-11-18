import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_tavily import TavilySearch

os.environ["TAVILY_API_KEY"] = "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"  # 在这里填入你的 Tavily API Key

llm = ChatOpenAI(
    model_name="qwen3.8-max",
    api_key='sk-yFOTmuKp5mZee1kP6ZrS3FiCZqy63wvckE0fiAq0JLgu4fuZ',
    base_url='https://globalai.vip/v1',
    timeout=240
)

SYSTEM_PROMPT = """你是足球情报记者，负责收集关于球队的新闻动态。"""

search = TavilySearch(
    max_results=10,
    country="bulgaria",            # 搜索地区设为保加利亚
    search_depth="advanced",      # 深度搜索，内容更全
    include_domains=[             # 只搜保加利亚本地媒体
        "sportal.bg",
        "gong.bg",
        "topsport.bg",
        "btvnovinite.bg",
        "dnevnik.bg",
        "marica.bg",
        "24chasa.bg",
    ],
)


def speak() -> str:
    # 1. 用保加利亚语搜索本地媒体（西里尔字母）
    queries = [
        "Български национален отбор по футбол новини",   # 保加利亚男足国家队新闻
        "България футбол последни резултати",              # 保加利亚足球最新赛果
    ]

    all_results = []
    for q in queries:
        all_results.append(search.invoke(q))

    combined = "\n\n".join(str(r) for r in all_results)

    # 2. 将搜索结果注入 prompt，让 LLM 整理成报道
    prompt = f"""## 请收集关于保加利亚媒体关于保加利亚男足国家队近期的新闻动态

以下是通过搜索引擎获取的最新资料：
{combined}

请根据以上资料，整理成一份简洁的新闻动态报告。"""

    result = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ])
    return result.content

if __name__ == "__main__":
    news = speak()
    print(news)