# -*- coding: utf-8 -*-
"""
FastAPI 服务：把 ai/main.py 的分析流程包成 HTTP API。

启动（在 ai/ 目录下）：
    uvicorn api:app --host 0.0.0.0 --port 5000

接口文档：http://localhost:5000/docs

请求 POST /api/analyze，body 为 JSON：
{
    "preview_url":      "https://xgscore.io/epl/xxx/preview",
    "xgscore_url":      "https://xgscore.io/epl/xxx/xgscore",
    "clubelo_home_url": "https://clubelo.com/HomeTeam",
    "clubelo_away_url": "https://clubelo.com/AwayTeam",
    "sportsmole_url":   "https://www.sportsmole.co.uk/.../xxx.html",
    "okooo_match_id":   "1331772",
    "okooo_recent_n":   6,
    "okooo_cookie":     "xxx"
}

响应：
{
    "success": true,
    "data": [
        {"feature": "稳胆筛选", "viewpoint": "主胜，比分 2-1、1-0", "reason": "……"},
        ...
    ]
}
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

import main as ai_main  # noqa: E402  （复用 analyze()）
from config import AI_API_KEY  # noqa: E402

app = FastAPI(
    title="赛事扫描分析 API",
    description="传入比赛 URL 与 okooo 配置，返回特征分析 JSON（feature / viewpoint / reason）",
    version="1.0.0",
)

# 跨域：浏览器不再直连本服务（由 Node 服务端转发），
# 故关闭 credentials（"*" + credentials=True 是非法组合）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 鉴权：Bearer <AI_API_KEY>（密钥由 Node 转发时携带，浏览器拿不到）
_bearer = HTTPBearer(auto_error=False)


def require_api_key(credentials: HTTPAuthorizationCredentials = Depends(_bearer)):
    if not credentials or credentials.credentials != AI_API_KEY:
        raise HTTPException(status_code=401, detail="无效的 API Key")
    return credentials


class AnalyzeRequest(BaseModel):
    preview_url: str
    xgscore_url: str
    clubelo_home_url: str
    clubelo_away_url: str
    sportsmole_url: str
    okooo_match_id: str
    okooo_cookie: str
    okooo_recent_n: int = Field(default=6, ge=1, le=30)
    # 手动 elo/golo（clubelo url 未填时用于十三节）
    home_elo: str = ""
    home_golo: str = ""
    away_elo: str = ""
    away_golo: str = ""


# ===== 每日精选：对比当天所有已分析比赛，选唯一一场 =====

class DailyAnalysis(BaseModel):
    feature: str = ""
    viewpoint: str = ""
    reason: str = ""
    handicap: str = ""


class DailyPickEvaluation(BaseModel):
    match_id: int
    score: int = Field(ge=0, le=100)
    grade: str
    opportunity_type: str
    direction: str
    evidence_summary: str
    risk_summary: str
    eligible: bool


class DailyPickCandidate(BaseModel):
    match_id: int
    rank: int
    score: int = Field(ge=0, le=100)
    grade: str
    opportunity_type: str
    direction: str
    supporting_evidence: str
    risk: str
    selection_note: str
    home_team: str
    away_team: str
    league: str
    match_time: str
    analyses: list[DailyAnalysis]


class DailyPick(BaseModel):
    match_id: int
    rec_type: str
    rec_direction: str
    reference_content: str
    reason: str
    main_risk: str


class DailyPickResult(BaseModel):
    evaluations: list[DailyPickEvaluation]
    candidates: list[DailyPickCandidate]
    pick: DailyPick


class DailyMatch(BaseModel):
    match_id: int
    home_team: str
    away_team: str
    league: str
    match_time: str
    analyses: list[DailyAnalysis] = []


class DailyPickRequest(BaseModel):
    date: str
    matches: list[DailyMatch]


@app.get("/")
def root():
    return {"service": "赛事扫描分析 API", "docs": "/docs", "endpoint": "/api/analyze"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/analyze")
def analyze(req: AnalyzeRequest, _auth=Depends(require_api_key)):
    """
    完整分析流程：抓取各站数据 → 组报告 → 调 LLM → 返回特征数组。
    整个流程耗时较长（分钟级），请合理设置客户端超时。
    需携带 Authorization: Bearer <AI_API_KEY>。
    """
    try:
        features = ai_main.analyze(
            preview_url=req.preview_url,
            xgscore_url=req.xgscore_url,
            clubelo_home_url=req.clubelo_home_url,
            clubelo_away_url=req.clubelo_away_url,
            sportsmole_url=req.sportsmole_url,
            okooo_match_id=req.okooo_match_id,
            okooo_recent_n=req.okooo_recent_n,
            okooo_cookie=req.okooo_cookie,
            home_elo=req.home_elo,
            home_golo=req.home_golo,
            away_elo=req.away_elo,
            away_golo=req.away_golo,
        )
        return {"success": True, "data": features}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        )


@app.post("/api/analyze-daily-pick")
def analyze_daily_pick(req: DailyPickRequest, _auth=Depends(require_api_key)):
    """
    每日精选：先由 AI 对全部未开赛比赛逐场评估，再由程序筛选少数候选，最后由 AI 选择唯一重点。
    matches 为全部未开赛且已完成分析的比赛及其已保存的特征分析。

    返回：
        { "success": true, "data": { "evaluations": [...], "candidates": [...], "pick": {
            "match_id", "rec_type", "rec_direction",
            "reference_content", "reason", "main_risk" } } }
    """
    print(req.matches)
    try:
        result = ai_main.analyze_daily_pick(
            pick_date=req.date,
            matches=[m.model_dump() for m in req.matches],
        )
        return {"success": True, "data": result}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        )
