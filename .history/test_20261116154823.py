import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_tavily import TavilySearch

os.environ["TAVILY_API_KEY"] = "your_tavily_api_key_here"  # 替换为你的 Tavily API Key

llm = ChatOpenAI(
    model_name="qwen3.8-max",
    api_key='sk-yFOTmuKp5mZee1kP6ZrS3FiCZqy63wvckE0fiAq0JLgu4fuZ',
    base_url='https://globalai.vip/v1',
    timeout=240
)

SYSTEM_PROMPT = """你是足球情报记者，负责收集关于球队的新闻动态。"""

search = TavilySearch(max_results=5)


def speak() -> str:
    # 1. 用 Tavily 实时搜索新闻
    search_results = search.invoke("保加利亚媒体关于保加利亚男足国家队近期新闻动态")

    # 2. 将搜索结果注入 prompt，让 LLM 整理成报道
    prompt = f"""## 请收集关于保加利亚媒体关于保加利亚男足国家队近期的新闻动态

以下是通过搜索引擎获取的最新资料：
{search_results}

请根据以上资料，整理成一份简洁的新闻动态报告。"""

    result = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ])
    return result.content

if __name__ == "__main__":
    news = speak()
    print(news)