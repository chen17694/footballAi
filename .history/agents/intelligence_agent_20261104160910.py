from crawler.sportsmole import get_article
from langgraph.types import Send

# article_data = get_article(MATCHES[0]["SPORTSMOLE_URL"])

class IntelligenceState(TypedDict):
    pass


workflow = StateGraph(IntelligenceState)
