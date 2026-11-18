# -*- coding: utf-8 -*-
"""
xgscore.io 比赛的 /xgscore（比分预测）页面抓取模块。

页面是 Angular SSR + 客户端水合，所有数据其实已渲染在 DOM 里；
部分区块（Home/Away/Similar）默认隐藏部分行，带 "Show all N matches" 按钮。
本模块用 Playwright 渲染页面、展开所有 SHOW ALL，再按区块提取：

    - All Season's Matches    每队：各赛季平均 GS/GC（含 xG）+ Scored/Conceded Factor
    - Recent Matches          每队：最近比赛明细 + 平均
    - Home / Away Matches     主队只看主场、客队只看客场
    - Head to Head            两队交锋（各队视角一份）
    - Similar Opponents       相似对手比赛明细 + 平均
    - Tables Results          各口径平均进失球 + 综合加权
    - Team Form               进攻/防守/整体状态/动机 + 修正后预估进失球
    - Teams Impact            两队影响力占比
"""

import sys

from playwright.sync_api import sync_playwright

from ._config import XGSCORE_URL

# 默认页：直接用 config 里显式配置的 /xgscore 页 URL
DEFAULT_URL = XGSCORE_URL

# Windows 控制台默认 GBK，强制 UTF-8 输出避免中文乱码
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

NAV_TIMEOUT = 60000
SHOW_ALL_MAX_CLICKS = 30


def _txt(locator):
    """取元素文本（textContent，不受 CSS 隐藏影响），清理空白。"""
    if locator.count() == 0:
        return None
    try:
        t = locator.evaluate("(e) => e.textContent")
    except Exception:
        return None
    return " ".join(t.split()) if t else None


def _list_texts(locator):
    """批量取元素的文本列表。"""
    return [_txt(l) for l in locator.all()]


def _expand_show_all(page):
    """
    展开所有 "Show all N matches" 按钮。
    按钮点击后会从 DOM 移除，所以循环里每次都重新查找第一个。
    """
    for _ in range(SHOW_ALL_MAX_CLICKS):
        buttons = page.locator("button:has-text('Show all')")
        if buttons.count() == 0:
            return
        try:
            buttons.first.click(timeout=3000)
            page.wait_for_timeout(200)
        except Exception:
            return


def _parse_team_names(page):
    """从比赛头部提取 主队/客队 名。"""
    names = page.locator("xgs-game-header .xgs-game-header_team-name")
    if names.count() < 2:
        raise RuntimeError("页面没有找到两队名字（xgs-game-header）")
    return {"home": _txt(names.nth(0)), "away": _txt(names.nth(1))}


def _parse_goals_block(block):
    """解析一个 xgs-team-goals 块：{goals, xg}。"""
    return {
        "goals": _txt(block.locator("mark")),
        "xg": _txt(block.locator(".xgs-team-goals_xg")),
    }


def _parse_match_rows(table):
    """
    解析 game-table 的比赛行。每行：对手、主/客(side)、日期、进/失球+对应 xG。
    跳过没有 logo 的空模板占位行（某些表末位会有）。
    """
    rows = []
    for row in table.locator("div.xgs-team-table-row").all():
        img = row.locator("img.xgs-team-table-row_logo")
        if img.count() == 0:
            continue  # 非比赛行（空模板占位）
        goals = row.locator("div.xgs-team-goals")
        rows.append({
            "opponent": img.get_attribute("alt", timeout=3000),
            "side": row.locator("mat-icon[data-mat-icon-name]")
                        .get_attribute("data-mat-icon-name", timeout=3000),  # home/away
            "date": _txt(row.locator(".xgs-team-table-row_secondary span")),
            "scored": _parse_goals_block(goals.nth(0)),
            "conceded": _parse_goals_block(goals.nth(1)),
        })
    return rows


def _parse_widget_footer(widget):
    """解析 widget 底部的 Scored / Conceded（两个 mark 依次为 进球、失球）。"""
    marks = widget.locator(".xgs-widget_footer .xgs-team-table-score mark strong")
    return {
        "scored": _txt(marks.nth(0)),
        "conceded": _txt(marks.nth(1)),
    }


def _parse_game_table(table):
    """解析一个 game-table：标题 + 比赛行 + 平均进失球。"""
    title = _txt(table.locator(".xgs-widget_header span").first)
    return {
        "title": title,
        "rows": _parse_match_rows(table),
        "average": _parse_widget_footer(table),
    }


def _parse_game_table_blocks(page):
    """
    页面按球队分两大块：主队块、客队块，各自包含
    [Recent, Home/Away, Head to Head, Similar Opponents] 四个 game-table。
    按标题 keyed，避免依赖硬编码的表格数量。
    """
    tables = page.locator("xgs-game-table")
    n = tables.count()
    if n == 0:
        raise RuntimeError("页面没有找到 game-table")

    half = n // 2  # 前一半属主队，后一半属客队

    def _block(start, end):
        out = {}
        for i in range(start, end):
            t = _parse_game_table(tables.nth(i))
            if t["title"]:
                out[t["title"]] = t
        return out

    return {"home": _block(0, half), "away": _block(half, n)}


def _parse_season_table(widget):
    """
    解析 All Season's Matches。可能有多个赛季行，每行：赛季名 + GS/GC 及 xG。
    footer 的 Scored/Conceded = Scored Factor / Conceded Factor。
    """
    rows = []
    for row in widget.locator("div.xgs-team-table-row").all():
        # 赛季行文本形如 "Season 2025/2026 25/26"，取第一个 span 即赛季名
        season = _txt(row.locator("strong.text-sm-small span").first)
        if not season:
            continue  # 空模板占位行（如 <div class="xgs-team-table-row"></div>）
        g = row.locator("div.xgs-team-goals")
        rows.append({
            "season": season,
            "gs": _parse_goals_block(g.nth(0)),   # 场均进球 + xG
            "gc": _parse_goals_block(g.nth(1)),   # 场均失球 + xG
        })
    return {
        "seasons": rows,
        "factors": _parse_widget_footer(widget),
    }


def _parse_result_table(widget):
    """
    解析 Tables Results：各口径（All Season/Recent/Home/H2H/Similar）平均进失球，
    底部 Scored/Conceded = 综合加权得分。
    """
    categories = {}
    for row in widget.locator("div.xgs-team-table-row").all():
        # 名称在 lead 里；注意数值的 strong 也带 text-sm-small，不能只按类名选
        name = _txt(row.locator(".xgs-team-table-row_lead strong"))
        marks = row.locator("mark strong")
        categories[name] = {
            "scored": _txt(marks.nth(0)),
            "conceded": _txt(marks.nth(1)),
        }
    return {
        "categories": categories,
        "weighted": _parse_widget_footer(widget),
    }


def _parse_conditions_table(widget):
    """
    解析 Team Form 的四个条件 + 底部修正后预估进失球。
    """
    conditions = {}
    for row in widget.locator("div.xgs-team-table-row").all():
        name = _txt(row.locator("strong.v-center"))
        conditions[name] = _txt(row.locator("mark strong"))
    return {
        "conditions": conditions,
        "adjusted": _parse_widget_footer(widget),
    }


def _parse_form_strip(el):
    """解析赛果条带（W/L/D 字母序列）。"""
    return [s for s in _list_texts(el.locator("li span")) if s]


def _parse_teams_impact(el):
    """解析 Teams Impact：两队占比。"""
    row = el.locator(".xgs-widget_row")
    pcts = _list_texts(row.locator(".xgs-mark strong"))   # [home%, away%]
    names = _list_texts(row.locator("div.v-center > strong"))  # [home, away]
    return {names[0]: pcts[0], names[1]: pcts[1]} if len(names) == 2 else {}


def get_xgscore_data(url=DEFAULT_URL):
    """
    用 Playwright 打开页面，展开 SHOW ALL，抓取全部区块。
    返回结构化字典（按 主队/客队 组织）。
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT)
            page.wait_for_timeout(5000)          # 等 Angular 水合
            _expand_show_all(page)

            teams = _parse_team_names(page)
            tables = _parse_game_table_blocks(page)
            season = [(_parse_season_table(x)) for x in
                      [page.locator("xgs-season-table").nth(i) for i in range(2)]]
            results = [_parse_result_table(page.locator("xgs-result-table").nth(i))
                       for i in range(2)]
            conditions = [_parse_conditions_table(
                page.locator("xgs-conditions-table").nth(i)) for i in range(2)]
            form_strips = [_parse_form_strip(page.locator("xgs-team-form").nth(i))
                           for i in range(2)]

            def _team_block(idx, side_title, side_key):
                block = {
                    "team": teams["home"] if idx == 0 else teams["away"],
                    "season_matches": season[idx],
                    "recent_matches": tables["home" if idx == 0 else "away"]
                                      .get("Recent Matches"),
                    "head_to_head": tables["home" if idx == 0 else "away"]
                                    .get("Head to Head"),
                    "similar_opponents": tables["home" if idx == 0 else "away"]
                                         .get("Similar Opponents"),
                    "tables_results": results[idx],
                    "team_form": {
                        "form": form_strips[idx],
                        **conditions[idx],
                    },
                }
                block[side_key] = tables["home" if idx == 0 else "away"].get(side_title)
                return block

            return {
                "url": url,
                "teams": teams,
                "home": _team_block(0, "Home Matches", "home_matches"),
                "away": _team_block(1, "Away Matches", "away_matches"),
                "teams_impact": _parse_teams_impact(page.locator("xgs-teams-impact")),
            }
        finally:
            browser.close()


def _fmt_goals(g):
    return f"{g['goals']} (xG {g['xg']})"


def print_report(data):
    """把抓取结果按区块打印出来（调试用）。"""
    teams = data["teams"]
    print(f"\n===== {teams['home']} vs {teams['away']} =====")

    for key, side_title in (("home", "Home Matches"), ("away", "Away Matches")):
        blk = data[key]
        print(f"\n########## {blk['team']} ##########")

        print(f"\n[All Season's Matches]")
        for s in blk["season_matches"]["seasons"]:
            print(f"  {s['season']}: GS {_fmt_goals(s['gs'])} | GC {_fmt_goals(s['gc'])}")
        f = blk["season_matches"]["factors"]
        print(f"  Factor: Scored {f['scored']} / Conceded {f['conceded']}")

        for sec in ("recent_matches", f"{side_title.split()[0].lower()}_matches",
                    "head_to_head", "similar_opponents"):
            t = blk[sec]
            if not t:
                continue
            print(f"\n[{t['title']}]")
            for r in t["rows"]:
                print(f"  {r['date']}  {r['opponent']:<14} [{r['side']}] "
                      f"进 {_fmt_goals(r['scored'])} | 失 {_fmt_goals(r['conceded'])}")
            a = t["average"]
            print(f"  平均: 进球 {a['scored']} / 失球 {a['conceded']}")

        print(f"\n[Tables Results]")
        for name, v in blk["tables_results"]["categories"].items():
            print(f"  {name:<20} 进球 {v['scored']} / 失球 {v['conceded']}")
        w = blk["tables_results"]["weighted"]
        print(f"  综合加权: 进球 {w['scored']} / 失球 {w['conceded']}")

        print(f"\n[Team Form]")
        print(f"  近期战绩: {' '.join(blk['team_form']['form'])}")
        for name, v in blk["team_form"]["conditions"].items():
            print(f"  {name:<18} {v}")
        adj = blk["team_form"]["adjusted"]
        print(f"  修正后预估进失球: 进球 {adj['scored']} / 失球 {adj['conceded']}")

    print(f"\n[Teams Impact]")
    for team, pct in data["teams_impact"].items():
        print(f"  {team}: {pct}")


def main(url=DEFAULT_URL):
    data = get_xgscore_data(url)
    print_report(data)
    return data


if __name__ == "__main__":
    main()
