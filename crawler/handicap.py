# -*- coding: utf-8 -*-
"""
抓取本场比赛各博彩公司的盘口变化历史（让球盘 + 大小球）。

- 数据源：okooo.com（需要有效的 OKOOO_COOKIE，否则可能返回 405）
- MATCH_ID / COOKIE 统一用上级目录 ai/config.py 的全局配置
- 本模块只负责"抓数据 + 渲染 Markdown"，不导出文件；
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
from config import OKOOO_COOKIE

# Windows 控制台默认 GBK，强制 UTF-8 输出避免中文乱码
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 盘口类型 → 采用的公司：(url_key, 中文名, 表头, (公司名, ID))
# 亚盘(让球盘)固定用澳门，大小球固定用澳门，两家公司各自负责一种盘口。
BET_TYPES = {
    "ah": ("让球盘", "澳门", ["时间", "更新时间", "主队赔率", "盘口", "客队赔率"], ('澳门', '84')),
    "overunder": ("大小球", "澳门", ["时间", "更新时间", "大球赔率", "盘口", "小球赔率"], ('澳门', '84')),
}

# URL 里的 oksid 参数（当前可用，若失效需从页面重新获取）
_OKSID = "fJewgMDQ0NTgxZGUxNTg4YTdjYTE1NzZmNTQwNGZlYTI5MzRiN2E3M2JmOA==vIMTj"

# ── 中文亚盘盘口 → 数字映射 ───────────────────────────────────────────────────
# 无前缀 / "让" 前缀和 "受" 前缀的符号含义由使用方自行约定。
_AH_BASE = {
    "平手": '0',
    "平手/半球": '-0.25',
    "半球": '-0.5',
    "半球/一球": '-0.75',
    "一球": '-1',
    "一球/球半": '-1.25',
    "球半": '-1.5',
    "球半/两球": '-1.75',
    "两球": '-2',
    "两球/两球半": '-2.25',
    "两球半": '-2.5',
    "两球半/三球": '-2.75',
    "三球": '-3',
    "三球/三球半": '-3.25',
    "三球半": '-3.5',
    "三球半/四球": '-3.75',
    "四球": '-4',
    "受平手/半球": '+0.25',
    "受半球": '+0.5',
    "受半球/一球": '+0.75',
    "受一球": '+1',
    "受一球/球半": '+1.25',
    "受球半": '+1.5',
    "受球半/两球": '+1.75',
    "受两球": '+2',
    "受两球/两球半": '+2.25',
    "受两球半": '+2.5',
    "受两球半/三球": '+2.75',
    "受三球": '+3',
    "受三球/三球半": '+3.25',
    "受三球半": '+3.5',
    "受三球半/四球": '+3.75',
    "受四球": '+4'
}



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


def parse_table(html):
    """解析页面中的变化历史表格，返回数据行列表（首列以数字开头）。"""
    soup = BeautifulSoup(html, "html.parser")
    table = max(soup.find_all("table"),
                key=lambda t: len(t.find_all("tr")), default=None)
    if not table:
        return []
    rows = []
    for tr in table.find_all("tr"):
        cols = [td.get_text(strip=True).replace("↑", "").replace("↓", "")
                for td in tr.find_all(["td", "th"])]
        if cols and cols[0] and cols[0][0].isdigit():
            rows.append(cols)
    return rows


def get_handicap(match_id=None, cookie=OKOOO_COOKIE):
    """
    抓取本场比赛的盘口变化历史（让球盘 + 大小球），直接渲染成 Markdown 文本。

    Args:
        match_id (str): 比赛 ID。
        cookie (str): 有效的 OKOOO_COOKIE。。

    Returns:
        str: Markdown 格式文本，形如：
            ### 盘口变化分析
            #### 让球盘（澳门）
            | 时间 | 更新时间 | 主队赔率 | 盘口 | 客队赔率 |
            | ...（全部变化记录）... |
            - **初始盘口**: ...
            - **当前盘口**: ...
            - **变化次数**: N 次
            - **趋势**: ...
            #### 大小球（澳门）
            （同上）

    Raises:
        RuntimeError: 页面结构变化或 Cookie 失效，导致无法抓取数据。
    """

    sections = []
    for url_key, (label, company_name, col_headers, (_name, company_id)) in BET_TYPES.items():
        url = (f"https://www.okooo.com/soccer/match/{match_id}/{url_key}/"
               f"change/{company_id}/?oksid={_OKSID}")
        try:
            html = fetch(url, match_id, cookie=cookie)
            rows = parse_table(html)
        except Exception:
            rows = []
        sections.append({"label": label, "company": company_name,
                         "columns": col_headers, "rows": rows})
    
    return format_handicap_report({"match_id": match_id, "sections": sections})

def format_handicap_report(data: dict) -> str:
    """
    本场比赛盘口信息
    输出：Markdown 字符串
    """
    lines = ["### 盘口变化分析", ""]

    for section in data["sections"]:
        label = section["label"]
        company = section["company"]
        columns = section["columns"]
        rows = section["rows"]

        lines.append(f"#### {label}（{company}）")
        lines.append("")

        if not rows:
            lines.append("_暂无数据_")
            lines.append("")
            continue

        # 完整盘口：全部变化记录（rows[0] 为最新一次，rows[-1] 为最早一次）
        lines.append("| " + " | ".join(columns) + " |")
        lines.append("| " + " | ".join(["---"] * len(columns)) + " |")
        for row in rows:
            # 让球盘的盘口列（第4列，index=3）用数字替换中文
            if label == "让球盘" and len(row) > 3:
                mapped = _AH_BASE.get(row[3], row[3])
                row = row[:3] + [mapped] + row[4:]
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")

        # 最新数据（第一行）
        latest = rows[0]
        # 最早数据（最后一行）
        earliest = rows[-1]

        # 根据盘口类型，提取关键字段
        if label == "让球盘":
            # columns: ["时间", "更新时间", "主队赔率", "盘口", "客队赔率"]
            initial_handicap = earliest[3] if len(earliest) > 3 else "N/A"
            current_handicap = latest[3] if len(latest) > 3 else "N/A"
            initial_mapped = _AH_BASE.get(initial_handicap, initial_handicap)
            current_mapped = _AH_BASE.get(current_handicap, current_handicap)

            lines.append(f"- **初始盘口**: {initial_mapped}")
            lines.append(f"- **当前盘口**: {current_mapped}")
            lines.append(f"- **变化次数**: {len(rows)} 次")

            # 简单趋势判断
            try:
                initial_val = float(initial_mapped)
                current_val = float(current_mapped)
                if current_val < initial_val:
                    trend = "盘口降低（主队支持度下降）"
                elif current_val > initial_val:
                    trend = "盘口升高（主队支持度上升）"
                else:
                    trend = "盘口稳定"
                lines.append(f"- **趋势**: {trend}")
            except (ValueError, TypeError):
                pass

        elif label == "大小球":
            # columns: ["时间", "更新时间", "大球赔率", "盘口", "小球赔率"]
            initial_total = earliest[3] if len(earliest) > 3 else "N/A"
            current_total = latest[3] if len(latest) > 3 else "N/A"

            lines.append(f"- **初始盘口**: {initial_total}")
            lines.append(f"- **当前盘口**: {current_total}")
            lines.append(f"- **变化次数**: {len(rows)} 次")

            # 简单趋势判断
            try:
                initial_val = float(initial_total)
                current_val = float(current_total)
                if current_val < initial_val:
                    trend = "总进球数下调"
                elif current_val > initial_val:
                    trend = "总进球数上调"
                else:
                    trend = "盘口稳定"
                lines.append(f"- **趋势**: {trend}")
            except (ValueError, TypeError):
                pass

        lines.append("")

    return "\n".join(lines)

