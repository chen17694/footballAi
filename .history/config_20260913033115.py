# -*- coding: utf-8 -*-
"""
全局 URL 配置：换比赛只改这一个文件。

被 main.py 和 xgscore / clubelo / sportsmole 三个子项目入口共同导入。
"""

# ===== xgscore：比赛预览页 + 比分预测页 =====
PREVIEW_URL = "https://xgscore.io/la-liga/malaga-la-coruna/preview"
XGSCORE_URL = "https://xgscore.io/la-liga/malaga-la-coruna/xgscore"

# ===== clubelo：主队 + 客队 =====
CLUBELO_HOME_URL = "https://clubelo.com/Malaga"
CLUBELO_AWAY_URL = "https://clubelo.com/Depor"

# ===== sportsmole：前瞻文章 =====
SPORTSMOLE_URL = ("https://www.sportsmole.co.uk/football/deportivo-la-coruna/preview/"
                  "malaga-vs-deportivo-prediction-team-news-lineups_603530.html")
OKOOO_MATCH_ID = "1335516"
OKOOO_RECENT_N = 6

# ===== AI 分析服务鉴权 =====
# 管理端登录后经 Node 转发（Node 持有此密钥）调用 /api/analyze。
# 生产环境务必改成随机长字符串，并与根目录 .env 的 AI_API_KEY 保持一致。
AI_API_KEY = "dev-ai-key-123"
OKOOO_COOKIE = "LastUrl=; _ga=GA1.1.44804699.1730805190; _ga_WHD99C0604=GS2.1.s1752898433$o1$g1$t1768050455$j60$l1$h27564907; zq_companytype_odds=AuthoriteBooks; zq_companytype_overunder=TypicalOu; M_UserID=32588974; M_Ukey=85399cd13fbe10524f7bd4fa5acb3fc1; data_start_isShow=1; _ga_7H2HVPJPLZ=GS2.1.s1784858347$o45$g1$t1784860172$j59$l1$h2052736857; _ga_B3LCXP8H9E=deleted; FirstURL=www.okooo.com/; FirstOKURL=https%3A//www.okooo.com/jingcai/; First_Source=www.okooo.com; _ga_H8WNRJTRHH=GS2.1.s1786143936$o24$g1$t1786143937$j59$l0$h2081753881; M_UserName=%22%5Cu83b1%5Cu5c14742570%22; IMUserID=32588974; IMUserName=%E8%8E%B1%E5%B0%94742570; HMACCOUNT=A236B6BD504505F5; PHPSESSID=c78cad9a568c491289e14a4000cfde8165658c91; OKSID=c78cad9a568c491289e14a4000cfde8165658c91; pm=; OkAutoUuid=203c76a0ddac7cfcb099bddc0087f97e; OkMsIndex=2; historyShowThisMatch=1; acw_tc=707c9f6e17874494073853839e5cb77639f0bb59e56655b1a12c016d8fd1f5; Hm_lpvt_213d524a1d07274f17dfa17b79db318f=1787449533; _ga_B3LCXP8H9E=GS2.1.s1787449407$o1335$g1$t1787449533$j59$l1$h917521189"
