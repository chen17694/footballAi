# -*- coding: utf-8 -*-
"""
xgscore 子项目入口：构建 12 节 Markdown 报告。

    - KeyStats.get_key_stats     → 一（关键指标）
    - Last5Matches.get_last5     → 二~四（All matches / Home-Away / Head to Head）
    - xgscore.get_xgscore_data   → 五~十二（Season/Recent/.../Team Form/Teams Impact）
    - Report.render_report       → 纯渲染层，把以上数据渲染成 12 节 Markdown
"""

import sys

from ._config import PREVIEW_URL, XGSCORE_URL

# Windows 控制台默认 GBK，强制 UTF-8 输出避免中文乱码
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def build_report(preview_url=PREVIEW_URL, xgscore_url=XGSCORE_URL, elo_golo=None):
    """引用三个模块拿数据，交给 Report 渲染成完整 Markdown，返回字符串。"""
    from .KeyStats import get_key_stats
    from .Last5Matches import get_last5
    from .xgscore import get_xgscore_data
    from .Report import render_report

    stats = get_key_stats(preview_url)
    last5 = get_last5(preview_url)
    print("正在抓取 /xgscore 页（Playwright）...")
    xgscore_data = get_xgscore_data(xgscore_url)
    return render_report(stats, last5, xgscore_data, elo_golo=elo_golo, url=preview_url)


if __name__ == "__main__":
    report = build_report()
    first = report.splitlines()[0] if report else ""
    print(f"报告已生成（{len(report)} 字符），标题：{first}")
