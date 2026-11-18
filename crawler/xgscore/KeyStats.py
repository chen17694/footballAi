# -*- coding: utf-8 -*-
"""
xgscore.io 比赛预览页面的 Key Stats 抓取模块。

页面是 Angular 服务端渲染（SSR）的，Key Stats 的数值直接写在 HTML 里，
因此只需要 requests 拉取 + lxml 解析，不需要浏览器自动化。

Key Stats 的 DOM 结构（每个指标是一个 xgs-level-scale-bar-group）:
    <xgs-game-preview-stats>
      <h2>Key Stats</h2>
      <xgs-level-scale-bar-group>
        <div class="h-between">
          <mark class="xgs-mark"> 1.6 </mark>   <- 主队数值（左）
          <strong class="v-center"> Team rating </strong>  <- 指标名
          <mark class="xgs-mark"> 2.9 </mark>   <- 客队数值（右）
        </div>
        <xgs-level-scale-bar> <label> WORST TEAM </label>  <- 主队等级
        <xgs-level-scale-bar> <label> POOR TEAM </label>   <- 客队等级
"""

import requests
from lxml import html as lhtml

from ._config import PREVIEW_URL

# 浏览器 UA，避免被站点风控拦截
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

DEFAULT_URL = PREVIEW_URL


def _clean(text):
    """去掉空白、换行和 Angular 的 <!-- --> 注释残留。"""
    return " ".join(text.split()) if text else None


def fetch_page(url, headers=None, timeout=20):
    """拉取页面 HTML。返回原始文本，失败时抛出异常。"""
    resp = requests.get(url, headers=headers or DEFAULT_HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def parse_key_stats(html_text):
    """
    从页面 HTML 中解析 Key Stats。

    返回结构：
        [
            {
                "name": "Team rating",   # 指标名
                "home": "1.6",           # 主队数值（字符串，可能是 "5%" 这种）
                "away": "2.9",           # 客队数值
                "home_label": "WORST TEAM",  # 主队刻度等级
                "away_label": "POOR TEAM",   # 客队刻度等级
            },
            ...
        ]
    """
    doc = lhtml.fromstring(html_text)

    # 定位 Key Stats 区块；找不到说明页面结构变了或没拿到数据
    sections = doc.cssselect("xgs-game-preview-stats")
    if not sections:
        raise ValueError("未找到 xgs-game-preview-stats 区块，页面可能被风控或结构已变")

    stats = []
    for group in sections[0].cssselect("xgs-level-scale-bar-group"):
        strong = group.cssselect("strong.v-center")
        marks = group.cssselect("mark.xgs-mark")
        labels = group.cssselect("label.xgs-level-bar-segment_label")

        stats.append({
            "name": _clean(strong[0].text_content()) if strong else None,
            "home": _clean(marks[0].text_content()) if len(marks) > 0 else None,
            "away": _clean(marks[1].text_content()) if len(marks) > 1 else None,
            "home_label": _clean(labels[0].text_content()) if len(labels) > 0 else None,
            "away_label": _clean(labels[1].text_content()) if len(labels) > 1 else None,
        })
    return stats


def get_key_stats(url=DEFAULT_URL, headers=None, timeout=20):
    """拉取并解析 Key Stats，一步到位。"""
    return parse_key_stats(fetch_page(url, headers=headers, timeout=timeout))


if __name__ == "__main__":
    import json
    data = get_key_stats()
    print(json.dumps(data, ensure_ascii=False, indent=2))
