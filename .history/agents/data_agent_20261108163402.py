import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler.sportsmole import get_article
from langgraph.types import Send
from config import OKOOO_RECENT_N, OKOOO_COOKIE, MATCHES, SELECTION_COUNT
from typing import TypedDict, Annotated, Optional, Union
from langgraph.graph import StateGraph, START, END
import operator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage