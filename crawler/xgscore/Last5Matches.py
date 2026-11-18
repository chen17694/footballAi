# -*- coding: utf-8 -*-
"""
xgscore.io 比赛预览页的 Last 5 matches 抓取模块。

数据源是公开 API（免鉴权），比从 HTML 解析更干净、且包含比分：
    GET https://api.xgscore.io/games/{slug}?tournamentSlug={联赛}
        → 拿到两队 ID、比赛时间（本模块从这里取参数）
    GET https://api.xgscore.io/team-games/?beforeDate=MM-DD-YYYY&teamId={队ID}
        → 该队最近 5 场，每场含：对手、主客(side)、比分(goals)、赛果(result)、评分(rate)
    可选过滤参数：
        &side=h|a             → 只看主场/客场（对应 "Home / Away" 标签）
        &opponentId={队ID}    → 只看两队交锋（对应 "Head to head" 标签）

比分换算规则（goals 是"被查询队视角"）：
    side == "h"  →  主队得分 = goals.s，客队得分 = goals.c
    side == "a"  →  主队得分 = goals.c，客队得分 = goals.s
"""

import time
from datetime import datetime
from urllib.parse import urlparse

import requests

from .KeyStats import DEFAULT_HEADERS
from ._config import PREVIEW_URL

API_BASE = "https://api.xgscore.io"
DEFAULT_URL = PREVIEW_URL


class XgscoreError(RuntimeError):
    """抓取过程中的错误。"""


def fetch_json(url, headers=None, timeout=20, params=None):
    """GET 一个 JSON 接口并解析。"""
    resp = requests.get(url, headers=headers or DEFAULT_HEADERS,
                        params=params, timeout=timeout)
    resp.raise_for_status()
    try:
        return resp.json()
    except ValueError as exc:
        raise XgscoreError(f"接口返回的不是 JSON: {url}") from exc


def parse_preview_url(url):
    """
    从比赛预览页 URL 解析出 联赛 slug 和 比赛 slug。
    例：https://xgscore.io/norway-eliteserien/kfum-lillestrom/preview
        → ("norway-eliteserien", "kfum-lillestrom")
    """
    path = urlparse(url).path.strip("/").split("/")
    if len(path) < 2:
        raise XgscoreError(f"无法从 URL 解析比赛: {url}")
    return path[0], path[1]


def _before_date(datetime_iso):
    """把比赛的 datetime 转成接口要求的 beforeDate（MM-DD-YYYY，UTC 口径）。"""
    dt = datetime.fromisoformat(datetime_iso.replace("Z", "+00:00"))
    return dt.strftime("%m-%d-%Y")


def fetch_game(url, headers=None, timeout=20):
    """
    拉取比赛信息。返回 API 的 game 对象，含 teams.h / teams.a / datetime / id。
    """
    league, slug = parse_preview_url(url)
    game = fetch_json(f"{API_BASE}/games/{slug}?tournamentSlug={league}",
                      headers=headers, timeout=timeout)
    if "teams" not in game or "h" not in game.get("teams", {}):
        raise XgscoreError(f"game 接口缺少 teams 字段: {slug}")
    return game


def fetch_team_games(team_id, before_date, side=None, opponent_id=None,
                     headers=None, timeout=20):
    """
    拉取某队最近比赛列表。side=None 为全部；'h'/'a' 限主/客场；
    opponent_id 传另一队 ID 即 Head to head。
    """
    params = {"beforeDate": before_date, "teamId": team_id}
    if side in ("h", "a"):
        params["side"] = side
    if opponent_id:
        params["opponentId"] = opponent_id
    return fetch_json(f"{API_BASE}/team-games/", params=params,
                      headers=headers, timeout=timeout)


def normalize_team_games(raw_list, team_map):
    """
    把一队的 team-games 原始记录归一化成主客视角明确的记录。
    team_map: {teamId: 队名}，用于补齐被查询队自己的名字。
    """
    records = []
    for g in raw_list:
        side = g.get("side")
        t_id = g.get("teamId")
        t_name = team_map.get(t_id, t_id)
        opp = g.get("opponent", {})
        goals = g.get("goals", {})
        xg = g.get("xG", {})
        s, c = goals.get("s", 0), goals.get("c", 0)
        if side == "h":
            home, away = t_name, opp.get("name")
            home_g, away_g = s, c
        else:  # side == "a"
            home, away = opp.get("name"), t_name
            home_g, away_g = c, s
        records.append({
            "gameId": g.get("gameId"),
            "datetime": g.get("datetime"),
            # 对阵双方（主客已校正）
            "home": home,
            "away": away,
            # 比分（主客已校正）
            "homeGoals": home_g,
            "awayGoals": away_g,
            # 该队视角信息
            "side": side,              # 被查询队本场是主(h)还是客(a)
            "result": g.get("result"),  # 被查询队赛果: w/l/d
            "rate": g.get("rate"),      # 评分
            "xGRate": g.get("xGRate"),
            "goalsRate": g.get("goalsRate"),
            "xGFor": round(xg.get("s", 0), 2),
            "xGAgainst": round(xg.get("c", 0), 2),
            "opponentId": opp.get("id"),
        })
    return records


def get_last_matches(url=DEFAULT_URL, tab="all", sleep=0.3, headers=None, timeout=20):
    """
    抓取比赛预览页的 Last 5 matches。

    tab 可选：
        "all"  → 两队各最近 5 场（默认）
        "side" → 主队只看主场，客队只看客场（对应 Home / Away 标签）
        "h2h"  → 只看两队交锋（对应 Head to head 标签）

    返回：
        {
            "game": {gameId, datetime, home_team, away_team},
            "home_team": [归一化记录...],   # 从主队视角抓的
            "away_team": [归一化记录...],   # 从客队视角抓的
        }
    """
    if tab not in ("all", "side", "h2h"):
        raise ValueError(f"tab 只能是 all/side/h2h，收到: {tab}")

    game = fetch_game(url, headers=headers, timeout=timeout)
    home = game["teams"]["h"]
    away = game["teams"]["a"]
    before = _before_date(game["datetime"])
    team_map = {home["id"]: home["name"], away["id"]: away["name"]}

    def _query(team_id, opponent_id=None):
        side = None
        if tab == "side":
            side = "h" if team_id == home["id"] else "a"
        data = fetch_team_games(team_id, before, side=side,
                                opponent_id=opponent_id,
                                headers=headers, timeout=timeout)
        if sleep:
            time.sleep(sleep)  # 基本礼仪，避免高频请求
        return data

    home_raw = _query(home["id"], opponent_id=away["id"] if tab == "h2h" else None)
    away_raw = _query(away["id"], opponent_id=home["id"] if tab == "h2h" else None)

    return {
        "game": {
            "gameId": game.get("id"),
            "datetime": game.get("datetime"),
            "home_team": home["name"],
            "away_team": away["name"],
        },
        "home_team": normalize_team_games(home_raw, team_map),
        "away_team": normalize_team_games(away_raw, team_map),
    }


def get_last5(url=DEFAULT_URL, sleep=0.3, headers=None, timeout=20):
    """一次性抓 all / side / h2h 三种 tab，返回 {"all":.., "side":.., "h2h":..}。"""
    return {tab: get_last_matches(url, tab=tab, sleep=sleep,
                                  headers=headers, timeout=timeout)
            for tab in ("all", "side", "h2h")}


def _print_records(title, records):
    print(f"\n【{title}】共 {len(records)} 场")
    for r in records:
        score = f"{r['homeGoals']}-{r['awayGoals']}"
        result = {"w": "胜", "l": "负", "d": "平"}.get(r["result"], r["result"])
        print(
            f"  {r['datetime'][:10]}  {r['home']} {score} {r['away']}"
            f"  [{result}]  评分={r['rate']}"
        )


if __name__ == "__main__":
    import sys

    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    for tab in ("all", "side", "h2h"):
        print(f"\n===== tab={tab} =====")
        data = get_last_matches(tab=tab)
        _print_records(f"主队 {data['game']['home_team']}", data["home_team"])
        _print_records(f"客队 {data['game']['away_team']}", data["away_team"])
