# -*- coding: utf-8 -*-
"""
爬取 Sports Mole 文章正文。

页面结构：
    <article>
      <h1 class="sm-article-title">标题</h1>
      <div> By 作者 | 日期 ... </div>
      <div class="sm-article-body">
        <p>段落</p>
        <h2>小标题</h2>
        <ul><li>列表项</li></ul>
      </div>
    </article>
"""
import re
import requests
from lxml import html as lhtml

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
}

# 正文里需要保留的标签
_CONTENT_TAGS = ("p", "h2", "h3", "h4")


def fetch_page(url, headers=None, timeout=20):
    """拉取文章页面 HTML。"""
    resp = requests.get(url, headers=headers or HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def parse_article(html_text):
    """
    从页面 HTML 解析文章标题、作者/日期、正文块。

    返回：
        {
            "title": "Preview: ...",
            "byline": "By Matt Law | 17 Aug 2026 ...",
            "blocks": [
                {"type": "p",    "text": "..."},
                {"type": "h2",   "text": "..."},
                {"type": "list", "items": ["...", "..."]},
                ...
            ],
        }
    """
    doc = lhtml.fromstring(html_text)
    art = doc.cssselect("article")
    if not art:
        raise ValueError("页面没有 article 元素，可能不是文章页或结构已变")
    art = art[0]

    # 标题
    h1 = doc.cssselect("h1.sm-article-title")
    title = " ".join(h1[0].text_content().split()) if h1 else None

    # 作者/日期（页面里 "By ... | ..." 开头的那行）
    byline = None
    for div in art.cssselect("div"):
        t = " ".join(div.text_content().split())
        if t.startswith("By "):
            byline = t
            break

    # 正文块（按文档顺序保留 p / 标题 / 列表）
    blocks = []
    body = doc.cssselect(".sm-article-body")
    if body:
        for e in body[0].iter():
            if e.tag in _CONTENT_TAGS:
                text = " ".join(e.text_content().split())
                if text:
                    blocks.append({"type": e.tag, "text": text})
            elif e.tag == "ul":
                items = [" ".join(li.text_content().split())
                         for li in e.cssselect("li")]
                items = [i for i in items if i]
                if items:
                    blocks.append({"type": "list", "items": items})

    return {"title": title, "byline": byline, "blocks": blocks}


def get_article(url, headers=None, timeout=20):
    """
    获取 Sports Mole 文章内容，返回 Markdown 格式文本。

    Args:
        url (str): 文章 URL。
        headers (dict, optional): 请求头。
        timeout (int, optional): 请求超时时间（秒）。

    Returns:
        str: Markdown 格式文本，形如：
            ### 比赛背景
            **标题**
            > 作者 | 日期
            段落
            #### 小标题
            - 列表项
    """
    return format_match_preview_report(parse_article(fetch_page(url, headers=headers, timeout=timeout)))

def format_match_preview_report(art):
    """
    本场比赛的背景
    输出：Markdown 字符串
    """
    lines = ["### 比赛背景", ""]
    if art["title"]:
        lines += [f"**{art['title']}**", ""]
    if art["byline"]:
        lines += [f"> {art['byline']}", ""]
    skip_next = False
    for b in art["blocks"]:
        # 跳过阵容行（紧跟 "possible starting lineup:" 标签后的下一段）
        if skip_next:
            skip_next = False
            continue
        # 比赛预测（We say: ...）—— 从这之后全部不要
        if b["type"] == "h2" and b["text"].startswith("We say:"):
            break
        # 球队近期赛果：W/L/D 列表 + 前置标签行（如 "... pre-season form:"）
        if b["type"] == "p" and _is_form_label(b["text"]):
            continue
        if (b["type"] == "list" and b["items"]
                and all(_is_form_result(i) for i in b["items"])):
            continue
        # 阵容预测：标签行 + 紧跟的阵容行
        if b["type"] == "p" and _is_lineup_label(b["text"]):
            skip_next = True
            continue
        if b["type"] == "h2":
            lines += ["", f"#### {b['text']}", ""]
        elif b["type"] == "list":
            lines += [f"- {i}" for i in b["items"]]
        else:
            lines.append(b["text"])
    return "\n".join(lines)

# 判断文本是否是近期战绩标签行（以 "form:" 结尾的行）
def _is_form_label(text):
    """是否是"... pre-season form:"这类近期赛果标签行。"""
    return re.search(r"\bform:\s*$", text) is not None

# 判断文本是否是首发阵容标签行（以 "possible starting lineup:" 结尾的行）
def _is_lineup_label(text):
    """是否是"... possible starting lineup:"阵容标签行。"""
    return re.search(r"\bpossible starting lineup:\s*$", text) is not None

# 判断文本是否是单字母比赛结果（W=胜、D=平、L=负）
def _is_form_result(text):
    """是否是单字母赛果（W/L/D）。"""
    return re.fullmatch(r"[WDL]", text.strip()) is not None
