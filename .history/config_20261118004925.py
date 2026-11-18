# -*- coding: utf-8 -*-
"""
比赛配置文件：每场比赛一个字典，放入 MATCHES 列表。
公共配置（OKOOO_RECENT_N、OKOOO_COOKIE）所有比赛共用。
"""

# ===== 公共配置 =====
SELECTION_COUNT: str = "1"  # 从所有比赛中精选的推荐场数
OKOOO_RECENT_N = 6
OKOOO_COOKIE = "LastUrl=; _ga=GA1.1.44804699.1730805190; _ga_B3LCXP8H9E=deleted; _c_WBKFRo=cUo3F5Rp9NBMRQ5Jr0cab0MffU1ZfxTEi0vsskgY; _ga_KDPR20Z4FF=GS2.1.s1768050455$o2$g0$t1768050455$j60$l1$h27564907; zq_companytype_odds=AuthoriteBooks; zq_companytype_overunder=TypicalOu; M_UserID=32588974; M_Ukey=85399cd13fbe10524f7bd4fa5acb3fc1; data_start_isShow=1; FirstURL=www.okooo.com/livecenter/football/; FirstOKURL=https%3A//www.okooo.com/soccer/; First_Source=www.okooo.com; historyShowThisMatch=1; _ga_7H2HVPJPLZ=GS2.1.s1793546384$o59$g0$t1793546384$j60$l1$h1277465565; _ga_B3LCXP8H9E=deleted; OkTouchAutoUuid=5c76b747c098ccc0729c46d05c138eb8; OkTouchMsIndex=6; _ga_H8WNRJTRHH=GS2.1.s1793963629$o28$g1$t1793963712$j60$l0$h2143996911; M_UserName=%22%5Cu83b1%5Cu5c14742570%22; PHPSESSID=60d8d046e4a06146b86816f374c532c03b24cd45; OKSID=60d8d046e4a06146b86816f374c532c03b24cd45; Hm_lvt_213d524a1d07274f17dfa17b79db318f=1794244784,1794306428,1794404240,1794475107; HMACCOUNT=A236B6BD504505F5; pm=; acw_tc=76b20f6817946558086317083ef004151456ff7c593892a1132826a1fe737d; IMUserID=32588974; IMUserName=%E8%8E%B1%E5%B0%94742570; OkAutoUuid=fdf89e34952e72cbef23dece312cc6aa; OkMsIndex=4; LStatus=Y; LoginStr=%7B%22welcome%22%3A%22%u60A8%u597D%uFF0C%u6B22%u8FCE%u60A8%22%2C%22login%22%3A%22%u767B%u5F55%22%2C%22register%22%3A%22%u6CE8%u518C%22%2C%22TrustLoginArr%22%3A%7B%22alipay%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22tenpay%22%3A%7B%22LoginCn%22%3A%22%u8D22%u4ED8%u901A%22%7D%2C%22weibo%22%3A%7B%22LoginCn%22%3A%22%u65B0%u6D6A%u5FAE%u535A%22%7D%2C%22renren%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22baidu%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22snda%22%3A%7B%22LoginCn%22%3A%22%22%7D%7D%2C%22userlevel%22%3A%22%22%2C%22flog%22%3A%22hidden%22%2C%22UserInfo%22%3A%7B%22UserName%22%3A%22%u83B1%u5C14742570%22%2C%22UserID%22%3A32588974%2C%22AuthLevel%22%3A%22%22%2C%22UserAvatar%22%3A%22https%3A//imgv1.okoooimg.cn/Upload/user/032/58/89/74_avatar_middle.jpg%3Fdc%3D1837442401.3%22%7D%2C%22IsReal%22%3A%22N%22%2C%22PayMethod%22%3A%22okooo%22%2C%22projectStatusCount%22%3A0%2C%22loginSession%22%3A%22___GlobalSession%22%7D; _ga_B3LCXP8H9E=GS2.1.s1794653661$o1872$g1$t1794656906$j40$l1$h239140238; Hm_lpvt_213d524a1d07274f17dfa17b79db318f=1794656907"

# ===== 每场比赛配置 =====
MATCHES = [
    {
        "OKOOO_MATCH_ID":    "1348700",
        "PREVIEW_URL":       "https://xgscore.io/nations-league/denmark-norway/preview",
        "XGSCORE_URL":       "",
        "SPORTSMOLE_URL":    "https://www.sportsmole.co.uk/football/switzerland/preview/switzerland-vs-scotland-prediction-team-news-lineups_609096.html",
        "CLUBELO_HOME_ELO":  "1967",
        "CLUBELO_HOME_GOLO": "无",
        "CLUBELO_AWAY_ELO":  "1724",
        "CLUBELO_AWAY_GOLO": "无",
        "Information": """

31. 本场比赛是国家队比赛（欧国联），苏格兰需要前往瑞士进行比赛。
32. 欧国联改制过渡年：容错率变了，但排位压力没有消失，从2028/29赛季起，欧国联将由A、B、C、D四级缩减为A、B、C三级，每个级别固定18支球队，D级取消。为了让各级别在过渡后恰好填满18个席位，欧足联对2026/27赛季的升降级规则做了针对性调整。以A级为例，直接降级的名额从此前每个小组末位一律降级的模式，收窄为“四个小组第四中排名最差的两支直接降入B级”；另外两支成绩较好的小组第四，与排名最低的两支小组第三一同进入A/B级附加赛，对手是B级的四个小组第二。这意味着A级球队的“底线”确实被抬高了：垫底不再必然意味着降级，仍有附加赛作为缓冲。但与此同时，小组第三与小组第四之间的区分被空前放大——排名靠前的第三可以直接留在A级，排名靠后的第三却要卷入附加赛的不确定性之中。容错率的提升，并未消解排位争夺的烈度，只是将压力从“避免垫底”重新分配到了“避免成为最差的那一个”。
""",
    }
]
