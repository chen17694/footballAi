# -*- coding: utf-8 -*-
"""
把 KeyStats、Last5Matches、/xgscore 比分预测页的抓取结果，
渲染成固定模板的 Markdown 报告。

模板结构（在合并报告里本节位于“一、比赛背景”（sportsmole）之后，故从 二 起编号）：
    1、关键指标对比 (Key Stats)          —— /preview 页
    2、All matches（胜平负 + 评分）       —— /preview 页
    3、Home / Away                       —— /preview 页
    4、HEAD TO HEAD                      —— /preview 页
    5、The Season's Matches              —— /xgscore 页
    6、Recent Matches                    —— /xgscore 页
    7、Home Matches / Away Matches       —— /xgscore 页
    8、Head to Head                      —— /xgscore 页
    9、Similar Opponents                 —— /xgscore 页
    10、Tables Results                  —— /xgscore 页
    11、Team Form                       —— /xgscore 页
    12、Teams Impact                    —— /xgscore 页
"""

import re

from ._config import PREVIEW_URL

# Key Stats：模板行中文名 → 抓取到的英文指标名
KEY_STATS_ROWS = [
    ("球队评级", "Team rating"),
    ("近期状态", "Team form"),
    ("xG运气指数", "xG Luckiness"),
    ("xG可预测性", "xG Predictability"),
]
# Key Stats 备注列（模板原文）
KEY_STATS_NOTES = {
    "球队评级": ("Team rankings of xGscore are based on a team's results, "
                "goals and xG, and level of tournament they perform."),
    "近期状态": ("This value is based on performances in the last few matches, "
                "results, goals and xG are taken into account."),
    "xG运气指数": ("A measure of how fair team's play (xG) compared to their results "
                 "(goals). Over-performing teams have positive value, "
                 "under-performing - negative. Calculation of the value is based on xG Fairness."),
    "xG可预测性": ("A measure of how close the post-match xG is to the pre-match "
                 "expected score prediction of xGscore. Determined by the average "
                 "percentage of all matches in the season."),
}

RESULT_CN = {"w": "胜", "l": "负", "d": "平"}


def _match_row(r):
    """把一个归一化比赛记录渲染成"对阵双方 | 比分 | 结果 | 评分"表格行。"""
    return (
        f"| {r['home']} vs {r['away']} | {r['homeGoals']}-{r['awayGoals']} "
        f"| {RESULT_CN.get(r['result'], r['result'])} | {r['rate']} |"
    )


def _render_key_stats(stats, home_name, away_name):
    lines = [
        "### 二、关键指标对比 (Key Stats)",
        "",
        f"| 指标 | {home_name} | {away_name} | 备注 |",
        "| --- | --- | --- | --- |",
    ]
    by_name = {s["name"]: s for s in stats}
    for cn, en in KEY_STATS_ROWS:
        s = by_name.get(en, {})
        lines.append(
            f"| **{cn}** | {s.get('home', '')} | {s.get('away', '')} | "
            f"{KEY_STATS_NOTES[cn]} |"
        )
    return lines


def _render_matches(title, records):
    lines = [
        f"#### {title}",
        "",
        "| 对阵双方 | 比分 | 结果 | 评分 |",
        "| --- | --- | --- | --- |",
    ]
    lines += [_match_row(r) for r in records]
    return lines


def _render_h2h(home_name, away_name, home_records, away_records):
    lines = [
        "### 五、HEAD TO HEAD",
        "",
        "| 球队 | 比分 | 战绩 | 各场评分 |",
        "| --- | --- | --- | --- |",
    ]
    for team, records in ((home_name, home_records), (away_name, away_records)):
        scores, results, rates = [], [], []
        for r in records:
            # 该队视角比分：该队进球 - 对手进球
            if r["home"] == team:
                scores.append(f"{r['homeGoals']}-{r['awayGoals']}")
            else:
                scores.append(f"{r['awayGoals']}-{r['homeGoals']}")
            results.append(r["result"])
            rates.append(str(r["rate"]))
        record = f"{results.count('w')}胜{results.count('d')}平{results.count('l')}负"
        lines.append(
            f"| **{team}** | {', '.join(scores)} | {record} | {', '.join(rates)} |"
        )
    return lines


_MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}


def _fmt_date(s):
    """把 "August 8, 2026" 转成 "2026-08-08"。转不了原样返回。"""
    if not s:
        return s
    m = re.match(r"(\w+)\s+(\d{1,2}),\s+(\d{4})", s)
    if not m:
        return s
    month, day, year = m.groups()
    return f"{year}-{_MONTHS.get(month, 0):02d}-{int(day):02d}"


def _rows_to_table(rows):
    """把比赛行渲染成"日期 | 对手 | 比分 | 进球xG | 失球xG"表格。"""
    lines = [
        "| 日期 | 对手 | 比分 | 进球 xG | 失球 xG |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append(
            f"| {_fmt_date(r['date'])} | {r['opponent']} | "
            f"{r['scored']['goals']}-{r['conceded']['goals']} | "
            f"{r['scored']['xg']} | {r['conceded']['xg']} |"
        )
    return lines


def _render_season_matches(block):
    """
    五、The Season's Matches：每个球队的所有赛季均值 + 整体 Factor。

    - 每个赛季前都输出赛季名（如 Season 2026/2027），即使只有一个赛季
    - Factor（综合预期进球/失球）是整队多赛季的综合预期，单独放在"球队综合预期"块里
    - 球队没有任何赛季数据时，输出"暂无数据"
    """
    sm = block["season_matches"]
    seasons = sm["seasons"]
    f = sm["factors"]

    if not seasons:
        return ["暂无数据"]

    lines = []
    for s in seasons:
        gs, gc = s.get("gs", {}), s.get("gc", {})
        lines.append(f"**Season {s.get('season', '')}**")
        lines.append(f"* **每场平均进球（GS）**：{gs.get('goals', '')}")
        lines.append(f"* **每场平均失球（GC）**：{gc.get('goals', '')}")
        lines.append(f"* **每场平均预期进球（xG Scored）**：{gs.get('xg', '')}")
        lines.append(f"* **每场平均预期失球（xG Conceded）**：{gc.get('xg', '')}")
        lines.append("")
    lines.append("**球队综合预期（多赛季）**")
    lines.append(f"* **综合预期进球能力（Scored Factor）**：{f.get('scored', '')}")
    lines.append(f"* **综合预期失球风险（Conceded Factor）**：{f.get('conceded', '')}")
    return lines


def _render_recent_matches(block):
    """六、Recent Matches：近期平均 + 具体场次。"""
    rm = block["recent_matches"]
    if not rm:
        return ["暂无数据"]
    avg = rm["average"]
    lines = [
        f"* **近期每场平均进球（GS）**：{avg['scored']}",
        f"* **近期每场平均失球（GC）**：{avg['conceded']}",
        "",
        "**具体场次数据：**",
        "",
    ]
    for r in rm["rows"]:
        lines.append(
            f"* **{r['opponent']} （{_fmt_date(r['date'])}）**："
            f"进球 {r['scored']['goals']} （xG {r['scored']['xg']}）| "
            f"失球 {r['conceded']['goals']} （xG {r['conceded']['xg']}）"
        )
    return lines


def _render_side_matches(block, side_key, side_title, side_label):
    """七、Home/Away Matches：主队主场或客队客场近况表格。"""
    t = block[side_key]
    if not t:
        return [f"**{side_title} ([{block['team']}] {side_label}近况)**", "", "暂无数据"]
    lines = [
        f"**{side_title} ([{block['team']}] {side_label}近况)**",
        "",
        *_rows_to_table(t["rows"]),
        "",
        f"* **{side_label}均场得分/失分**：{t['average']['scored']} / {t['average']['conceded']}",
    ]
    return lines


def _render_h2h_detail(block, opponent_name):
    """八、Head to Head：某队视角的交锋表。"""
    t = block["head_to_head"]
    if not t:
        return [f"**[{block['team']}] 视角 (对阵 [{opponent_name}])**", "", "两队暂无交锋记录"]
    return [
        f"**[{block['team']}] 视角 (对阵 [{opponent_name}])**",
        "",
        *_rows_to_table(t["rows"]),
        "",
        f"* **场均表现**：{t['average']['scored']} / {t['average']['conceded']}",
    ]


def _render_similar_opponents(block):
    """九、Similar Opponents：平均 + 各场。"""
    t = block["similar_opponents"]
    if not t:
        return ["暂无数据"]
    lines = [
        f"*平均每场：{t['average']['scored']} | {t['average']['conceded']}",
        "",
    ]
    for r in t["rows"]:
        lines.append(
            f"* **vs {r['opponent']} （{_fmt_date(r['date'])}）**："
            f"{r['scored']['goals']} - {r['conceded']['goals']} "
            f"（xG: {r['scored']['xg']} - {r['conceded']['xg']}）"
        )
    return lines


def _render_tables_results(block, is_home):
    """十、Tables Results：各口径平均进失球 + 综合加权。"""
    cats = block["tables_results"]["categories"]
    w = block["tables_results"]["weighted"]
    if is_home:
        items = [
            ("所有赛季比赛（All Season's Matches）", "All Season's Matches"),
            ("近期比赛（Recent Matches）", "Recent Matches"),
            ("主场比赛（Home Matches）", "Home Matches"),
            ("历史交锋（Head to Head）", "Head to Head"),
            ("相似对手（Similar Opponents）", "Similar Opponents"),
        ]
    else:
        items = [
            ("本赛季比赛（The Season's Matches）", "All Season's Matches"),
            ("近期比赛（Recent Matches）", "Recent Matches"),
            ("客场比赛（Away Matches）", "Away Matches"),
            ("历史交锋（Head to Head）", "Head to Head"),
            ("相似对手（Similar Opponents）", "Similar Opponents"),
        ]
    lines = [
        f"* **{label}**：{cats.get(key, {}).get('scored', '')} | "
        f"{cats.get(key, {}).get('conceded', '')}"
        for label, key in items
    ]
    lines.append(f"* **综合加权得分**：{w.get('scored', '')} | {w.get('conceded', '')}")
    return lines


_TEAM_FORM_INTRO = [
    "- **Attack condition**：This indicator is affected by injuries, suspensions, transfers of attacking players and significant increase or decrease scored goals in recent matches.",
    "- **Defence condition**：This indicator is affected by injuries, suspensions, transfers of defense players and significant increase or decrease conceded goals in recent matches.",
    "- **Overall form**：This indicator is affected by the physical condition and the current form of the team (streaks of wins or loses).",
    "- **Motivation**：This indicator is affected by the atmosphere in the club, motivation of the players and need to improve table position.",
]


def _render_team_form(block):
    """十一、Team Form：四个条件 + 修正后预估进失球。"""
    conds = block["team_form"]["conditions"]
    adj = block["team_form"]["adjusted"]
    return [
        f"* **Attack condition**：{conds.get('Attack condition', '')}",
        f"* **Defence condition**：{conds.get('Defence condition', '')}",
        f"* **Overall form**：{conds.get('Overall form', '')}",
        f"* **Motivation**：{conds.get('Motivation', '')}",
        f"* **修正后预估进失球**：{adj.get('scored', '')} | {adj.get('conceded', '')}",
    ]


def _render_xgscore_sections(xg, elo_golo=None):
    """渲染 /xgscore 页的六~十四节。"""
    home, away = xg["home"], xg["away"]
    hn, an = xg["teams"]["home"], xg["teams"]["away"]
    ti = xg.get("teams_impact", {})

    lines = []
    lines += ["### 六、The Season's Matches", "", f"#### {hn}", ""]
    lines += _render_season_matches(home)
    lines += ["", f"#### {an}", ""]
    lines += _render_season_matches(away)
    lines += ["", "---", ""]

    lines += ["### 七、Recent Matches", "", f"#### {hn}", ""]
    lines += _render_recent_matches(home)
    lines += ["", f"#### {an}", ""]
    lines += _render_recent_matches(away)
    lines += ["", "---", ""]

    lines += ["### 八、Home Matches/Away Matches", ""]
    lines += _render_side_matches(home, "home_matches", "Home Matches", "主场")
    lines += ["", "---", ""]
    lines += _render_side_matches(away, "away_matches", "Away Matches", "客场")
    lines += ["", "---", ""]

    lines += ["### 九、Head to Head", ""]
    lines += _render_h2h_detail(home, an)
    lines += ["", "---", ""]
    lines += _render_h2h_detail(away, hn)
    lines += ["", "---", ""]

    lines += ["### 十、Similar Opponents", "", f"#### {hn}", ""]
    lines += _render_similar_opponents(home)
    lines += ["", f"#### {an}", ""]
    lines += _render_similar_opponents(away)
    lines += ["", "---", ""]

    lines += ["### 十一、Tables Results", "", f"#### {hn}", ""]
    lines += _render_tables_results(home, is_home=True)
    lines += ["", f"#### {an}", ""]
    lines += _render_tables_results(away, is_home=False)
    lines += ["", "---", ""]

    lines += ["### 十二、Team Form", "", *_TEAM_FORM_INTRO, "", f"#### {hn}", ""]
    lines += _render_team_form(home)
    lines += ["", f"#### {an}", ""]
    lines += _render_team_form(away)
    lines += ["", "---", ""]

    lines += ["### 十三、Teams Impact", ""]
    lines += [f"* **{hn}**：{ti.get(hn, '')}", f"* **{an}**：{ti.get(an, '')}"]
    lines += ["", "---", ""]

    lines += ["### 十四、球队 Elo / Golo", ""]
    lines += [
        "> Elo：球队实力评分　Golo：球队进球表现/进球基准",
        "",
        "| 球队 | Elo | Golo |",
        "| --- | --- | --- |",
        f"| {hn} | {elo_golo.get('home_elo', '')} | {elo_golo.get('home_golo', '')} |",
        f"| {an} | {elo_golo.get('away_elo', '')} | {elo_golo.get('away_golo', '')} |",
    ]

    return lines


def render_report(stats, last5, xgscore_data, elo_golo=None, url=PREVIEW_URL):
    """把三个模块整理好的数据渲染成完整 Markdown 报告，返回字符串。

    参数：
        stats        —— KeyStats.get_key_stats() 的结果
        last5        —— {"all":.., "side":.., "h2h":..}（Last5Matches.get_last5() 的结果）
        xgscore_data —— xgscore.get_xgscore_data() 的结果
        url          —— 仅用于报告头部的"来源"标注
    """
    g_all = last5["all"]
    g_side = last5["side"]
    g_h2h = last5["h2h"]

    home = g_all["game"]["home_team"]
    away = g_all["game"]["away_team"]
    game_date = (g_all["game"]["datetime"] or "")[:10]

    lines = [
        f"# {home} vs {away}",
        "",
        f"> ### 一、比赛时间：{game_date}　来源：{url}",
        "",
    ]
    lines += _render_key_stats(stats, home, away)
    lines += ["", "---", ""]
    lines += ["### 三、All matches（胜平负 + 评分）", ""]
    lines += _render_matches(home, g_all["home_team"])
    lines += ["", ""]
    lines += _render_matches(away, g_all["away_team"])
    lines += ["", "---", ""]
    lines += ["### 四、Home / Away", ""]
    lines += _render_matches(f"{home}（主场）", g_side["home_team"])
    lines += ["", ""]
    lines += _render_matches(f"{away}（客场）", g_side["away_team"])
    lines += ["", "---", ""]
    lines += _render_h2h(home, away, g_h2h["home_team"], g_h2h["away_team"])
    lines += ["", "---", ""]
    lines += _render_xgscore_sections(xgscore_data, elo_golo=elo_golo or {})
    return "\n".join(lines)
