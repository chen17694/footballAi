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
1. 维多利亚近12次对阵布拉干蒂诺4胜1平7负，球队整体实力略逊于对手。近两次交手布拉干蒂诺均零封并完胜维多利亚，不过回到自己主场维多利亚也曾两胜对手。维多利亚近5年面对布拉干蒂诺主场胜率达到100%，布拉干蒂诺近5年面对维多利亚客场输球率达到100%。布拉干蒂诺最近2次联赛对阵维多利亚均取得胜利，合计打入6球且保持零封，但此前两次客场挑战维多利亚全部告负。
2. 布拉干蒂诺在6个月内未能在客场取胜，无论是联赛还是南球杯，球队客场表现都很糟糕。上一次球队客场比赛取胜还是今年五月3比0战胜瓦斯科达伽马，球队客场已经三连败。布拉干蒂诺最近8个联赛客场取得4平4负，未尝胜绩，期间仅打入6球，另有2场未能破门。本赛季客场4胜5平8负，近10个客场不胜。
3. 维多利亚后卫布里特斯（15场2助）回归，他在上一场对阵弗鲁米嫩塞的比赛中因停赛被禁赛；左后卫拉蒙（38场2球）因伤缺席了最近九场比赛，今天回归，预计将从替补席首发。后卫卡穆坦加（14场）以及中场亚历杭德罗·阿尔马拉斯也入选了。但阵中两名从布拉干蒂诺租借而来的球员无法出战：中后卫卢安·坎迪多和前锋拉坎塔纳的租借合同均含条款，未经支付罚款不得对阵原属俱乐部。
4. 维多利亚阵容残缺：里切利、主力后卫纳坦·门德斯、后防租将法比亚诺和中场轮换杜杜均因伤无法出战。此外，中卫卢安·坎迪多和前锋纳乔·拉金塔纳受合同回避条款限制，本场不能对阵母队。多人缺席压缩了球队攻防两端的轮换空间，尤其后防受损严重。
5. 布拉干蒂诺方面，有膝盖问题的主力中场罗德里吉尼奥（28场4球1助）和正在从膝盖手术中恢复的前锋达维·戈麦斯（5场1球）不能参加今晚的比赛。球队的主力前锋费尔南多（35场7球3助）和伊格纳西奥·索萨（32场1球2助）回归，球队伤情有所好转。布拉干蒂诺的锋线绝对主力卢卡斯·巴博萨因累计黄牌停赛，本场无法出战，本赛季出战32场巴甲31次首发，贡献7球3助攻。此外，达维·戈梅斯、法布里西奥、后防主力何塞·赫尔塔多和中场主力罗德里吉尼奥也被列入缺阵名单。
6. 维多利亚近10场正赛多达7场比赛半场有得失球。维多利亚本赛季联赛34场比赛，在领先的情况下最终获胜的场次占总胜场的100%；本赛季近10个主场比赛，在领先的情况下最终主场赢球率达100%；近5场正赛连续失球，且场均丢球达1.8球；本赛季联赛34场进35球，是联赛进球数第2少的球队；在落后的情况下最终输球的场次占总负场的87%。
7. 维多利亚目前积分38分，排名联赛倒数第5，仅领先倒数第3的格雷米奥1分，仍有一定保级压力。最近状态持续低迷，5场联赛取得2平3负，未尝胜绩，上轮主场0比3不敌弗鲁米嫩塞。球队主场近期同样缺乏竞争力，近2个联赛主场1平1负未能取胜。维多利亚最近8轮联赛丢掉15球，场均失球达到1.88个，防守稳定性明显下滑；近2轮合计丢5球且连续被零封，进攻端同样缺乏输出。
8. 维多利亚在第33轮后与主帅雅伊尔·文图拉分道扬镳，球队当时连续4场不胜，仅领先降级区2分。新帅拉斐尔·拉塞尔达此前执教沙佩科恩斯，本场将迎来执教维多利亚的首秀。拉塞尔达长期在巴乙等低级别联赛执教，巴甲经验有限，且此前率领沙佩科恩斯在巴甲长期垫底，本赛季已提前降级。
9. 布拉干蒂诺本赛季联赛34场失39球，是联赛失球数第3少的球队；本赛季联赛34场比赛，在领先的情况下最终获胜的场次占总胜场的92%；近10场客场比赛多达6场平局；在落后的情况下最终输球的场次占总负场的76%；本赛季近10个客场比赛，在落后的情况下最终客场输球率达100%；本赛季联赛34场比赛，卡皮萨巴得到12张黄牌，是联赛获得黄牌最多的球员。
10. 布拉干蒂诺上轮联赛主场2比1击败桑托斯，取得联赛两连胜，近期状态有所回升。两场比赛合计打入5球、仅失1球，进攻端保持输出，防守稳定性也有所改善。布拉干蒂诺积47分排第8，还惦记着解放者杯资格的尾巴；近5场3胜1平1负，华莱士·扬连续进球，反击质量和前场反抢都在线。
11. 维多利亚擅长把比赛拖小：少控球、高密度中场、靠雷内跑位和定位球找机会；布拉干蒂诺则想用转换和反抢撕开口子。双方都不具备把比分拉开的条件，先失球的一方会非常难受——维多利亚本赛季落后后输球比例极高，布拉干蒂诺又偏偏客场不善打逆风。
12. 维多利亚目前34轮过后积38分，仅领先降级区1分，容错空间几乎归零。主场始终是变量：本赛季主场10胜2平5负，2024、2025两个赛季主场对布拉干蒂诺都是1比0拿下，保级时刻的主场气场是这套残阵唯一的底气。布拉干蒂诺防守端稳固，34轮只丢39球，联赛第三少，领先之后兑现胜率极高；问题在客场，攻坚效率一般，逆风球不会踢，领先也守不牢。
""",
    },
   {
        "OKOOO_MATCH_ID":    "1317041",
        "PREVIEW_URL":       "https://xgscore.io/brazil-serie-a/sao-paulo-fluminense/preview",
        "XGSCORE_URL":       "https://xgscore.io/brazil-serie-a/sao-paulo-fluminense/xgscore",
        "SPORTSMOLE_URL":    "https://www.sportsmole.co.uk/football/sao-paulo/preview/sao-paulo-vs-fluminense-prediction-team-news-lineups_609291.html",
        "CLUBELO_HOME_ELO":  "1715 ",
        "CLUBELO_HOME_GOLO": "0.99",
        "CLUBELO_AWAY_ELO":  "1769",
        "CLUBELO_AWAY_GOLO": "1.09",
        "Information": """

""",
    },
]
