# -*- coding: utf-8 -*-
"""
比赛配置文件：每场比赛一个字典，放入 MATCHES 列表。
公共配置（OKOOO_RECENT_N、OKOOO_COOKIE）所有比赛共用。
"""

# ===== 公共配置 =====
SELECTION_COUNT: str = "1"  # 从所有比赛中精选的推荐场数
OKOOO_RECENT_N = 2
TAVILY_API_KEY = "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"  # Tavily 搜索 API key，替换为真实 key
OKOOO_COOKIE = "LastUrl=; _ga=GA1.1.44804699.1730805190; _ga_B3LCXP8H9E=deleted; _c_WBKFRo=cUo3F5Rp9NBMRQ5Jr0cab0MffU1ZfxTEi0vsskgY; _ga_KDPR20Z4FF=GS2.1.s1768050455$o2$g0$t1768050455$j60$l1$h27564907; zq_companytype_odds=AuthoriteBooks; zq_companytype_overunder=TypicalOu; M_UserID=32588974; M_Ukey=85399cd13fbe10524f7bd4fa5acb3fc1; data_start_isShow=1; FirstURL=www.okooo.com/livecenter/football/; FirstOKURL=https%3A//www.okooo.com/soccer/; First_Source=www.okooo.com; historyShowThisMatch=1; _ga_7H2HVPJPLZ=GS2.1.s1793546384$o59$g0$t1793546384$j60$l1$h1277465565; _ga_B3LCXP8H9E=deleted; OkTouchAutoUuid=5c76b747c098ccc0729c46d05c138eb8; OkTouchMsIndex=6; _ga_H8WNRJTRHH=GS2.1.s1793963629$o28$g1$t1793963712$j60$l0$h2143996911; M_UserName=%22%5Cu83b1%5Cu5c14742570%22; IMUserID=32588974; IMUserName=%E8%8E%B1%E5%B0%94742570; OkAutoUuid=66c8a1e3c39bc57553975515d6d64d5c; OkMsIndex=1; PHPSESSID=e55ffe10bbc34e44bb471f8dc36f1a1259cd42a2; OKSID=e55ffe10bbc34e44bb471f8dc36f1a1259cd42a2; Hm_lvt_213d524a1d07274f17dfa17b79db318f=1794475107,1794702405,1794886353,1794967787; HMACCOUNT=A236B6BD504505F5; acw_tc=707c9f6d17950394205395235efb16184e94366537589f47e11ea57465def9; LStatus=Y; LoginStr=%7B%22welcome%22%3A%22%u60A8%u597D%uFF0C%u6B22%u8FCE%u60A8%22%2C%22login%22%3A%22%u767B%u5F55%22%2C%22register%22%3A%22%u6CE8%u518C%22%2C%22TrustLoginArr%22%3A%7B%22alipay%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22tenpay%22%3A%7B%22LoginCn%22%3A%22%u8D22%u4ED8%u901A%22%7D%2C%22weibo%22%3A%7B%22LoginCn%22%3A%22%u65B0%u6D6A%u5FAE%u535A%22%7D%2C%22renren%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22baidu%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22snda%22%3A%7B%22LoginCn%22%3A%22%22%7D%7D%2C%22userlevel%22%3A%22%22%2C%22flog%22%3A%22hidden%22%2C%22UserInfo%22%3A%7B%22UserName%22%3A%22%u83B1%u5C14742570%22%2C%22UserID%22%3A32588974%2C%22AuthLevel%22%3A%22%22%2C%22UserAvatar%22%3A%22https%3A//imgv1.okoooimg.cn/Upload/user/032/58/89/74_avatar_middle.jpg%3Fdc%3D1837442401.3%22%7D%2C%22IsReal%22%3A%22N%22%2C%22PayMethod%22%3A%22okooo%22%2C%22projectStatusCount%22%3A0%2C%22loginSession%22%3A%22___GlobalSession%22%7D; _ga_B3LCXP8H9E=GS2.1.s1795039422$o1906$g1$t1795040796$j54$l1$h2075728589; Hm_lpvt_213d524a1d07274f17dfa17b79db318f=1795040797"

# ===== 每场比赛配置 =====
MATCHES = [
    {
        "OKOOO_MATCH_ID":    "1317047",
        "PREVIEW_URL":       "https://xgscore.io/brazil-serie-a/vitoria-bragantino/preview",
        "XGSCORE_URL":       "https://xgscore.io/brazil-serie-a/vitoria-bragantino/xgscore",
        "SPORTSMOLE_URL":    "https://www.sportsmole.co.uk/football/vitoria/preview/vitoria-vs-bragantino-prediction-team-news-lineups_609281.html",
        "CLUBELO_HOME_ELO":  "1652",
        "CLUBELO_HOME_GOLO": "1.11",
        "CLUBELO_AWAY_ELO":  "1700",
        "CLUBELO_AWAY_GOLO": "1.27",
        "Information": """

""",
    },
   {
        "OKOOO_MATCH_ID":    "1317039",
        "PREVIEW_URL":       "https://xgscore.io/brazil-serie-a/flamengo-atletico-pr/preview",
        "XGSCORE_URL":       "https://xgscore.io/brazil-serie-a/flamengo-atletico-pr/xgscore",
        "SPORTSMOLE_URL":    "https://www.sportsmole.co.uk/football/flamengo/preview/flamengo-vs-athletico-pr-prediction-team-news-lineups_609284.html",
        "CLUBELO_HOME_ELO":  "1884",
        "CLUBELO_HOME_GOLO": "1.17",
        "CLUBELO_AWAY_ELO":  "1714",
        "CLUBELO_AWAY_GOLO": "1.29",
        "Information": """
1. 弗拉门戈3场比赛连胜，状态极佳。本赛季联赛34场战绩为23胜7平4负，目前排名联赛第1，有争冠希望，本场比赛战意十足。球队本赛季联赛34场进71球，是联赛进球数第1多的球队；34场失29球，是联赛失球数第2少的球队。
2. 弗拉门戈本赛季联赛8个主场连续获胜，表现极佳。巴甲第34轮，弗拉门戈主场3比1击败格雷米奥，佩德罗梅开二度，利诺也取得进球。球队目前积76分，继续排名榜首，领先帕尔梅拉斯3分，联赛仅剩4轮。弗拉门戈近11轮取得10胜1平保持不败，取分效率极为出色，争冠形势依然占据主动。
3. 弗拉门戈佩德罗本赛季联赛34场比赛打入20球，目前排名联赛射手榜第2位。弗拉门戈本赛季联赛34场比赛，在领先的情况下最终输球的场次占总负场的50%。
4. 弗拉门戈近6次对阵巴拉纳竞技取得3胜2平1负，整体交锋占据优势。本赛季双方首次碰面，弗拉门戈客场1比1战平对手，保持不败。此番回到主场，弗拉门戈在近期状态和对赛信心方面均占据一定优势。
5. 国际比赛日结束后，弗拉门戈人员状况明显改善。达尼洛和帕奎塔均已恢复，本场预计从替补席待命；阿莱士·桑德罗近期随队训练，可以出任左路。德阿拉斯卡埃塔与巴雷拉已恢复合练，其中巴雷拉因此前代表乌拉圭打满90分钟，身体状态仍存疑，可能替补出场。普拉塔提前结束国家队集训后回归训练，预计同样从替补席开始。弗拉门戈目前没有确认因伤缺阵的核心球员。
6. 弗拉门戈主帅雅尔丁赛前表示，不会为了下一轮对阵争冠对手帕尔梅拉斯的直接对话进行轮换，本场计划派出主力阵容。不过，德阿拉斯卡埃塔、佩德罗、普尔加、莱奥·佩雷拉、阿莱士·桑德罗、布鲁诺·恩里克、路易斯·阿劳若和维唐均处于黄牌累积临界状态，再次吃牌将缺席下一轮争冠关键战。在“不轮换”与保护主力之间，弗拉门戈仍可能根据比赛进程调整阵容。
7. 巴拉纳竞技近10场正赛多达10场比赛半场有得失球。基韦罗斯本赛季联赛34场比赛打入21球，目前排名联赛射手榜第1位。巴拉纳竞技本赛季联赛34场比赛，在领先的情况下最终获胜的场次占总胜场的80%。
8. 巴拉纳竞技近5场正赛连续失球，且场均丢球达1.8球。近5年面对弗拉门戈客场输球率达到75%。本赛季联赛34场比赛，在落后的情况下最终输球的场次占总负场的80%。本赛季近10个客场比赛，在落后的情况下最终客场输球率达100%。
9. 巴拉纳竞技在巴甲第33轮客场0比2不敌格雷米奥，第34轮主场1比3遭瓦斯科达伽马逆转，近期遭遇两连败。球队目前处于积分榜中上游，仍保留争取解放者杯资格的理论可能，但客战马拉卡纳将面临较大考验。近10场比赛场均失球达到2.1个，防守端在高强度对抗下的稳定性不足。
10. 巴拉纳竞技前锋维韦罗斯因禁赛三场，本场执行第一场停赛，确认无法出战。作为球队联赛头号射手，他已攻入21球，缺席将直接削弱球队的禁区牵制和终结能力。中场/后卫丹塔斯同样因停赛缺席，影响后场轮换与边路防守。阿图尔·迪亚斯从国际比赛日归来后赶不上本场，巴拉纳竞技攻防两端的人员选择进一步收窄。
11. 巴拉纳竞技近期客场表现不佳，最近5个联赛客场取得1胜2平2负，胜率仅20%，上个客场对阵格雷米奥此前连续6个客场进球记录也终结。球队唯一一场胜利来自击败垫底的沙佩科恩斯，面对实力更强的对手时取分能力有限。本场客战领头羊弗拉门戈，巴拉纳竞技需要改善客场表现，才能争取带走积分。
""",
    },
]
