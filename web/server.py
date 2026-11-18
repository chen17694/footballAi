# -*- coding: utf-8 -*-
"""足球辩论室 - 本地 Web 可视化后端。

启动： python web/server.py   然后浏览器打开 http://127.0.0.1:8766
"""
import sys
import os
import json
import asyncio
import threading
from pathlib import Path

# 把 ai/ 目录加入 path，使其能 import main / config / agents
AI_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AI_DIR))

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from sse_starlette.sse import EventSourceResponse

from config import MATCHES
from main import debate_app, collect_reports

app = FastAPI(title="足球辩论室")

WEB_DIR = Path(__file__).resolve().parent
REPORT_DIR = AI_DIR / "output" / "roundtable"


def _match_label(m: dict) -> str:
    """从 PREVIEW_URL 里取一个可读的短标签，比如 denmark-norway。"""
    url = m.get("PREVIEW_URL", "")
    if url:
        parts = [p for p in url.rstrip("/").split("/") if p]
        # 倒数第二段通常是对阵，例如 .../nations-league/denmark-norway/preview
        if len(parts) >= 2:
            return parts[-2]
    return m.get("OKOOO_MATCH_ID", "")


def get_report(match_id: str) -> str:
    """优先读缓存报告，没有就现场收集（会跑情报 agent）。"""
    cache_path = REPORT_DIR / f"{match_id}_report.md"
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8")
    for r in collect_reports():
        if r["match_id"] == match_id:
            return r["content"]
    return ""


def transform_update(chunk: dict) -> dict:
    """把 LangGraph 的 updates chunk 整理成前端好用的事件结构。"""
    node = next(iter(chunk.keys()))
    delta = chunk[node] or {}
    event = {"node": node, "messages": [], "verdict": None, "risks": None, "round": None}
    for entry in delta.get("debate", []):
        event["messages"].append({
            "speaker": entry["speaker"],
            "round": entry["round"],
            "content": entry["content"],
        })
    if "verdict" in delta:
        event["verdict"] = delta["verdict"]
    if "risks" in delta:
        event["risks"] = delta["risks"]
    if "round" in delta:
        event["round"] = delta["round"]
    return event


@app.get("/")
def index():
    return FileResponse(WEB_DIR / "index.html")


@app.get("/api/matches")
def api_matches():
    out = []
    for m in MATCHES:
        mid = m["OKOOO_MATCH_ID"]
        out.append({
            "match_id": mid,
            "label": _match_label(m),
            "cached": (REPORT_DIR / f"{mid}_report.md").exists(),
        })
    return out


@app.get("/api/report")
def api_report(match_id: str = Query(...)):
    return {"match_id": match_id, "content": get_report(match_id)}


@app.get("/api/debate/stream")
async def debate_stream(match_id: str = Query(...)):
    """SSE 流：跑一场比赛的辩论，每个节点完成推一条 update 事件，结束推 done。"""

    async def event_generator():
        report_content = get_report(match_id)
        if not report_content:
            yield {"event": "error", "data": json.dumps({"message": "未找到该比赛报告"}, ensure_ascii=False)}
            return

        aq: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_running_loop()

        def runner():
            state = {
                "report": report_content,
                "debate": [],
                "round": 0,
                "verdict": "",
                "risks": [],
                "judge_count": 0,
            }
            try:
                for chunk in debate_app.stream(state, stream_mode="updates"):
                    event = transform_update(chunk)
                    loop.call_soon_threadsafe(aq.put_nowait, ("update", event))
                loop.call_soon_threadsafe(aq.put_nowait, ("done", None))
            except Exception as e:  # noqa: BLE001
                loop.call_soon_threadsafe(aq.put_nowait, ("error", repr(e)))

        threading.Thread(target=runner, daemon=True).start()

        while True:
            try:
                kind, payload = await asyncio.wait_for(aq.get(), timeout=20)
            except asyncio.TimeoutError:
                # 心跳，防止代理掐断空闲连接
                yield {"event": "ping", "data": ""}
                continue

            if kind == "update":
                yield {"event": "update", "data": json.dumps(payload, ensure_ascii=False)}
            elif kind == "done":
                yield {"event": "done", "data": "{}"}
                break
            elif kind == "error":
                yield {"event": "error", "data": json.dumps({"message": payload}, ensure_ascii=False)}
                break

    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8766)
