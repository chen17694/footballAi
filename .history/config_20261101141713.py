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
OKOOO_COOKIE = "LastUrl=; _ga=GA1.1.44804699.1730805190; _ga_B3LCXP8H9E=deleted; _c_WBKFRo=cUo3F5Rp9NBMRQ5Jr0cab0MffU1ZfxTEi0vsskgY; _ga_KDPR20Z4FF=GS2.1.s1768050455$o2$g0$t1768050455$j60$l1$h27564907; zq_companytype_odds=AuthoriteBooks; zq_companytype_overunder=TypicalOu; M_UserID=32588974; M_Ukey=85399cd13fbe10524f7bd4fa5acb3fc1; data_start_isShow=1; FirstURL=www.okooo.com/livecenter/football/; FirstOKURL=https%3A//www.okooo.com/soccer/; First_Source=www.okooo.com; IMUserID=32588974; IMUserName=%E8%8E%B1%E5%B0%94742570; historyShowThisMatch=1; OkTouchAutoUuid=bce2ded58f29caf31cb7d1c297911525; OkTouchMsIndex=6; _ga_H8WNRJTRHH=GS2.1.s1792598779$o27$g1$t1792598798$j41$l0$h1716765268; M_UserName=%22%5Cu83b1%5Cu5c14742570%22; _ga_B3LCXP8H9E=deleted; _ga_7H2HVPJPLZ=GS2.1.s1793340142$o58$g1$t1793340176$j26$l1$h269290029; PHPSESSID=23bdcddc2230952eab3b1a00690c40ae9e2f788d; OKSID=23bdcddc2230952eab3b1a00690c40ae9e2f788d; Hm_lvt_213d524a1d07274f17dfa17b79db318f=1792803370,1792968352,1793073436,1793409260; HMACCOUNT=A236B6BD504505F5; pm=; acw_tc=76b20f6817934454029254308e058674a8eec29bca98af4150fef5b3d97f90; OkAutoUuid=0df26f614ab0d46230c693c96a83136e; OkMsIndex=2; LStatus=Y; LoginStr=%7B%22welcome%22%3A%22%u60A8%u597D%uFF0C%u6B22%u8FCE%u60A8%22%2C%22login%22%3A%22%u767B%u5F55%22%2C%22register%22%3A%22%u6CE8%u518C%22%2C%22TrustLoginArr%22%3A%7B%22alipay%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22tenpay%22%3A%7B%22LoginCn%22%3A%22%u8D22%u4ED8%u901A%22%7D%2C%22weibo%22%3A%7B%22LoginCn%22%3A%22%u65B0%u6D6A%u5FAE%u535A%22%7D%2C%22renren%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22baidu%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22snda%22%3A%7B%22LoginCn%22%3A%22%22%7D%7D%2C%22userlevel%22%3A%22%22%2C%22flog%22%3A%22hidden%22%2C%22UserInfo%22%3A%7B%22UserName%22%3A%22%u83B1%u5C14742570%22%2C%22UserID%22%3A32588974%2C%22AuthLevel%22%3A%22%22%2C%22UserAvatar%22%3A%22https%3A//imgv1.okoooimg.cn/Upload/user/032/58/89/74_avatar_middle.jpg%3Fdc%3D1837442401.3%22%7D%2C%22IsReal%22%3A%22N%22%2C%22PayMethod%22%3A%22okooo%22%2C%22projectStatusCount%22%3A0%2C%22loginSession%22%3A%22___GlobalSession%22%7D; _ga_B3LCXP8H9E=GS2.1.s1793443261$o1778$g1$t1793446572$j42$l1$h1872004109; Hm_lpvt_213d524a1d07274f17dfa17b79db318f=1793446572"
