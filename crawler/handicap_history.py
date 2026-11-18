# -*- coding: utf-8 -*-
"""
抓取本场比赛的让球方，在近 N 场同为让球方时的赢盘/输盘情况。

- 数据源：okooo.com 的比赛历史页（需要有效的 OKOOO_COOKIE，否则页面返回 405）
- 本模块只负责"抓数据 + 渲染 Markdown"，不再自己导出文件；
  由 ai/main.py 调用，作为报告第十五节。

说明：页面中每支球队的"近期比赛"表格包含历史比赛的亚盘终盘，
"盘口"列以主队为视角（带"受"表示主队受让、即客队让球），
盘口左右两列为主/客队水位；平手盘时水位低的一方视为让球方，
水位相同时主队视为让球方。统计时走盘计为0.5场赢盘。
最后一列为该队本场比赛的赢盘/输盘结果。
"""

import os
import re
import sys

import requests
from bs4 import BeautifulSoup

# 配置统一在上级目录 ai/config.py
_PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)
from config import OKOOO_COOKIE, OKOOO_RECENT_N

# Windows 控制台默认 GBK，强制 UTF-8 输出避免中文乱码
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 盘口常见单位，用于识别"盘口"列
HANDICAP_UNITS = ("平手", "半球", "一球", "球半", "两球", "两球半",
                  "三球", "三球半", "四球", "四球半", "五球")


def _headers(match_id, cookie=OKOOO_COOKIE):
    return {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"),
        "Referer": f"https://www.okooo.com/soccer/match/{match_id}/",
        "Cookie": cookie,
        "Accept-Language": "zh-CN,zh;q=0.9",
    }


def fetch(url, match_id, timeout=15, cookie=OKOOO_COOKIE):
    resp = requests.get(url, headers=_headers(match_id, cookie), timeout=timeout)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or "gbk"
    return resp.text


def is_handicap(s):
    """判断某单元格内容是否为盘口（如 半球 / 受平手/半球；"-" 不算）。"""
    s = (s or "").strip()
    if not s or s == "-":
        return False
    return any(u in s for u in HANDICAP_UNITS)


def is_friendly(league):
    """判断联赛名是否为友谊赛（含"友谊"，如 友谊赛/国际友谊/俱乐部友谊）。"""
    return "友谊" in (league or "")


def parse_team_tables(html):
    """返回 {球队名: 该队近期比赛 table}。"""
    soup = BeautifulSoup(html, "html.parser")
    tables = {}
    for t in soup.find_all("table"):
        first = t.find("tr")
        if not first:
            continue
        txt = first.get_text(strip=True)
        if "全赛事" in txt:
            team = txt.split("全赛事")[0].strip()
            if team and team != "两队交锋":
                tables[team] = t
    return tables


def parse_row(tr):
    """解析一行近期比赛，返回 dict；非数据行返回 None。"""
    cols = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
    if len(cols) < 12:
        return None
    hc_idx = next((i for i, c in enumerate(cols) if is_handicap(c)), None)
    if hc_idx is None:
        return None
    return {
        "league": cols[0],
        "time": cols[1],
        "home": cols[2],
        "score": cols[3],
        "away": cols[4],
        "handicap": cols[hc_idx],   # 主队视角：带"受"=主队受让
        "home_water": cols[hc_idx - 1] if hc_idx >= 1 else "-",             # 365 主队水位
        "away_water": cols[hc_idx + 1] if hc_idx + 1 < len(cols) else "-",  # 365 客队水位
        "result": cols[-1],         # 本表球队视角：赢 / 输 / 走 / -
    }


def parse_rows(table):
    return [r for r in (parse_row(tr) for tr in table.find_all("tr")) if r]


def lower_water_side(home_water, away_water):
    """平手盘时，水位低的一方为让球方；水位相同时主队为让球方。
    返回 'home'/'away'/None（水位缺失）。"""
    try:
        h, a = float(home_water), float(away_water)
    except (TypeError, ValueError):
        return None
    if h < a:
        return "home"
    if a < h:
        return "away"
    return "home"   # 水位相同 → 主队为让球方


def team_is_giver(r, team):
    """该场比赛里 team 是否作为让球方；平手盘时取水位低的一方。"""
    hc = r["handicap"]
    if not is_handicap(hc):
        return False
    if hc in ("平手", "受平手"):
        side = lower_water_side(r["home_water"], r["away_water"])
        if side == "home":
            return r["home"] == team
        if side == "away":
            return r["away"] == team
        return False
    if r["home"] == team:
        return not hc.startswith("受")
    if r["away"] == team:
        return hc.startswith("受")
    return False


def show_handicap(r, team):
    """把主队角度的盘口换算成 team 的角度（如 让半球 / 受平手/半球）。"""
    hc, home, away = r["handicap"], r["home"], r["away"]
    if hc in ("平手", "受平手"):
        side = lower_water_side(r["home_water"], r["away_water"])
        if side == "home":
            return "让平手" if team == home else "受平手"
        if side == "away":
            return "让平手" if team == away else "受平手"
        return "平手"
    if hc.startswith("受"):
        return f"{'让' if home != team else '受'}{hc[1:]}"
    return f"{'让' if home == team else '受'}{hc}"


def short_time(t):
    m = re.match(r"(\d{2}-\d{2}-\d{2})", t or "")
    return m.group(1) if m else (t or "")


def result_label(res):
    return {"赢": "赢盘", "输": "输盘", "走": "走盘"}.get(
        res, "无数据" if res == "-" else (res or "未赛"))


def get_handicap_history(match_id=None, recent_n=OKOOO_RECENT_N,
                         cookie=OKOOO_COOKIE):
    """
    获取指定比赛的让球方历史盘路，返回 Markdown 格式文本。
    Args:
        match_id (str): 比赛 ID。
        recent_n (int): 近 N 场比赛。
        cookie (str): 有效的 OKOOO_COOKIE。

    Returns:
        str: Markdown 格式文本，形如：
            ### 让球方盘路（近 N 场主/客场）
            本场：主队 vs 客队，终盘（主队视角）：盘口
            本场让球方：**球队名**（主/客场）
            | 日期 | 联赛 | 主队 | 比分 | 客队 | 让球方盘口 | 结果 |
            | ...（全部变化记录）... |
            合计：赢盘 + 走盘×0.5 = N 场 ，输盘 M 场

    Raises:
        RuntimeError: 页面结构变化或 Cookie 失效，导致无法抓取数据。
    """
    url = f"https://www.okooo.com/soccer/match/{match_id}/history/"
    html = fetch(url, match_id, cookie=cookie)
    tables = parse_team_tables(html)
    if not tables:
        raise RuntimeError("未找到球队近期比赛表（页面结构变化或 Cookie 失效）")

    team0 = next(iter(tables))
    rows0 = parse_rows(tables[team0])
    if not rows0:
        raise RuntimeError("未能解析到本场比赛数据")
    cur = rows0[0]
    home, away, cur_hc = cur["home"], cur["away"], cur["handicap"]

    data = {
        "match_id": match_id,
        "home": home, "away": away, "handicap": cur_hc,
        "recent_n": recent_n,
        "giver": None,
        "giver_side": None,  # 'home' 或 'away'
        "note": None,
        "matches": [],
        "summary": {"win": 0, "lose": 0, "push": 0},
    }

    if not is_handicap(cur_hc):
        data["note"] = "本场无有效盘口，无让球方"
        return data

    if cur_hc in ("平手", "受平手"):
        # 平手盘：水位低的一方为让球方；水位相同时主队为让球方
        side = lower_water_side(cur["home_water"], cur["away_water"])
        if not side:
            data["note"] = "本场为平手盘，缺少水位数据，无法判断让球方"
            return data
        giver = cur["home"] if side == "home" else cur["away"]
        giver_side = side
    else:
        if cur_hc.startswith("受"):
            giver = away
            giver_side = "away"
        else:
            giver = home
            giver_side = "home"

    data["giver"] = giver
    data["giver_side"] = giver_side

    giver_table = tables.get(giver)
    if not giver_table:
        data["note"] = f"未找到 {giver} 的近期比赛表"
        return data

    # 筛选条件：让球方作为让球方 + 指定主客场（主队→主场，客队→客场）
    for r in parse_rows(giver_table)[1:]:   # 跳过当前比赛行
        if not team_is_giver(r, giver):
            continue
        if is_friendly(r["league"]):
            continue
        # 新增：主客场限制
        if giver_side == "home" and r["home"] != giver:
            continue  # 让球方是主队，但这场比赛它是客队 → 跳过
        if giver_side == "away" and r["away"] != giver:
            continue  # 让球方是客队，但这场比赛它是主队 → 跳过

        data["matches"].append({
            "date": r["time"], "league": r["league"],
            "home": r["home"], "score": r["score"], "away": r["away"],
            "handicap": show_handicap(r, giver),
            "result": result_label(r["result"]),
        })
        if r["result"] == "走":
            data["summary"]["push"] += 1
            data["summary"]["win"] += 0.5   # 走盘计为0.5场赢盘
        elif r["result"] == "赢":
            data["summary"]["win"] += 1
        elif r["result"] == "输":
            data["summary"]["lose"] += 1
        if len(data["matches"]) >= recent_n:
            break

    if not data["matches"]:
        side_label = "主场" if giver_side == "home" else "客场"
        data["note"] = f"{giver} 近期没有作为让球方的{side_label}比赛记录"

    return format_handicap_history_report(data)

def format_handicap_history_report(data: dict) -> str:
    """
    本场比赛让球方的历史盘路信息
    输出：Markdown 字符串
    """
    side_label = "主场" if data.get("giver_side") == "home" else "客场"
    lines = [
        f"### 让球方盘路（近 {data['recent_n']} 场{side_label}）",
        "",
        f"本场：{data['home']} vs {data['away']}，终盘（主队视角）：{data['handicap']}",
    ]
    if data["note"]:
        lines += ["", data["note"]]
        return "\n".join(lines)

    lines += [f"本场让球方：**{data['giver']}**（{side_label}）", ""]
    lines += ["| 日期 | 联赛 | 主队 | 比分 | 客队 | 让球方盘口 | 结果 |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in data["matches"]:
        lines.append(
            f"| {short_time(r['date'])} | {r['league']} | {r['home']} | "
            f"{r['score']} | {r['away']} | {r['handicap']} | {r['result']} |"
        )
    s = data["summary"]
    lines += ["", f"合计：赢盘 + 走盘×0.5 = {s['win']} 场 ，输盘 {s['lose']} 场"]
    return "\n".join(lines)
