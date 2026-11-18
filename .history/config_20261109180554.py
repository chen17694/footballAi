# -*- coding: utf-8 -*-
"""
比赛配置文件：每场比赛一个字典，放入 MATCHES 列表。
公共配置（OKOOO_RECENT_N、OKOOO_COOKIE）所有比赛共用。
"""

# ===== 公共配置 =====
SELECTION_COUNT: str = "0-2"  # 从所有比赛中精选的推荐场数
OKOOO_RECENT_N = 6
OKOOO_COOKIE = "LastUrl=; _ga=GA1.1.44804699.1730805190; _ga_B3LCXP8H9E=deleted; _c_WBKFRo=cUo3F5Rp9NBMRQ5Jr0cab0MffU1ZfxTEi0vsskgY; _ga_KDPR20Z4FF=GS2.1.s1768050455$o2$g0$t1768050455$j60$l1$h27564907; zq_companytype_odds=AuthoriteBooks; zq_companytype_overunder=TypicalOu; M_UserID=32588974; M_Ukey=85399cd13fbe10524f7bd4fa5acb3fc1; data_start_isShow=1; FirstURL=www.okooo.com/livecenter/football/; FirstOKURL=https%3A//www.okooo.com/soccer/; First_Source=www.okooo.com; IMUserID=32588974; IMUserName=%E8%8E%B1%E5%B0%94742570; historyShowThisMatch=1; _ga_7H2HVPJPLZ=GS2.1.s1793546384$o59$g0$t1793546384$j60$l1$h1277465565; _ga_B3LCXP8H9E=deleted; OkAutoUuid=5c76b747c098ccc0729c46d05c138eb8; OkMsIndex=6; OkTouchAutoUuid=5c76b747c098ccc0729c46d05c138eb8; OkTouchMsIndex=6; _ga_H8WNRJTRHH=GS2.1.s1793963629$o28$g1$t1793963712$j60$l0$h2143996911; M_UserName=%22%5Cu83b1%5Cu5c14742570%22; PHPSESSID=28454865144773da070ea076ea346581cffb5e75; OKSID=28454865144773da070ea076ea346581cffb5e75; Hm_lvt_213d524a1d07274f17dfa17b79db318f=1793758051,1793790103,1794012824,1794188738; HMACCOUNT=A236B6BD504505F5; LStatus=Y; LoginStr=%7B%22welcome%22%3A%22%u60A8%u597D%uFF0C%u6B22%u8FCE%u60A8%22%2C%22login%22%3A%22%u767B%u5F55%22%2C%22register%22%3A%22%u6CE8%u518C%22%2C%22TrustLoginArr%22%3A%7B%22alipay%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22tenpay%22%3A%7B%22LoginCn%22%3A%22%u8D22%u4ED8%u901A%22%7D%2C%22weibo%22%3A%7B%22LoginCn%22%3A%22%u65B0%u6D6A%u5FAE%u535A%22%7D%2C%22renren%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22baidu%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22snda%22%3A%7B%22LoginCn%22%3A%22%22%7D%7D%2C%22userlevel%22%3A%22%22%2C%22flog%22%3A%22hidden%22%2C%22UserInfo%22%3A%7B%22UserName%22%3A%22%u83B1%u5C14742570%22%2C%22UserID%22%3A32588974%2C%22AuthLevel%22%3A%22%22%2C%22UserAvatar%22%3A%22https%3A//imgv1.okoooimg.cn/Upload/user/032/58/89/74_avatar_middle.jpg%3Fdc%3D1837442401.3%22%7D%2C%22IsReal%22%3A%22N%22%2C%22PayMethod%22%3A%22okooo%22%2C%22projectStatusCount%22%3A0%2C%22loginSession%22%3A%22___GlobalSession%22%7D; acw_tc=707c9f7317941965767634832ec92d23bee79670eeb8f83f73fd33fa1e9f97; _ga_B3LCXP8H9E=GS2.1.s1794196578$o1840$g1$t1794196583$j55$l1$h2088538234; Hm_lpvt_213d524a1d07274f17dfa17b79db318f=1794196584"

# ===== 每场比赛配置 =====
MATCHES = [
    {
        "OKOOO_MATCH_ID":    "1331867",
        "PREVIEW_URL":       "https://xgscore.io/epl/sunderland-chelsea/preview",
        "XGSCORE_URL":       "https://xgscore.io/epl/sunderland-chelsea/xgscore",
        "SPORTSMOLE_URL":    "https://www.sportsmole.co.uk/football/chelsea/preview/sunderland-vs-chelsea-prediction-team-news-lineups_608574.html",
        "CLUBELO_HOME_ELO":  "1720",
        "CLUBELO_HOME_GOLO": "0.95",
        "CLUBELO_AWAY_ELO":  "1892",
        "CLUBELO_AWAY_GOLO": "1.68",
        "Information": """
1. 桑德兰周中欧联主场0比2不敌萨格勒布迪纳摩，紧接着又要征战联赛，主力球员休整时间不足。球队近两场正赛有5名球员连续首发，分别是罗宾·勒夫斯、奥马尔·阿尔德雷特、格拉尼特·扎卡、尼尔松·安古洛和克里斯·里格，体能消耗巨大。切尔西本赛季不用参加欧战，体能储备更为充裕，桑德兰在体能上处于明显劣势，本场抢分难度不小。
2. 桑德兰上轮英超客场1比3不敌保级对手考文垂，遭遇联赛两连败；随后欧联杯主场0比2负于萨格勒布迪纳摩，各项赛事已经三连败。英超9轮过后，桑德兰仅取得1胜2平6负，积5分排名垫底，有保级压力，本场比赛战意十足。球队上一次联赛取胜还是8月30日击败富勒姆，此后7轮取得2平5负，未尝胜绩；期间5场失利均至少丢掉2球，最近4轮仅打入1球，其中3场遭遇零封，主帅勒布里斯的帅位压力持续增加。
3. 桑德兰本赛季联赛9场战绩为1胜2平6负，目前排名联赛第20；9场进7球，是联赛进球数第2少的球队；9场失17球，是联赛失球数第3多的球队；在领先的情况下最终获胜的场次占总胜场的100%；在落后的情况下最终输球的场次占总负场的100%；本赛季联赛9场比赛得到3张红牌，是联赛得到红牌数最多的球队。
4. 桑德兰本场坐镇光明球场，但近期主场表现低迷：联赛主场刚刚遭遇失利，欧联杯主场又0比2不敌萨格勒布迪纳摩，主场氛围和信心受到影响。球队最近6个正式比赛主场取得2胜1平3负，联赛近3个主场更是1平2负，未尝胜绩，光明球场的传统主场优势暂时难以兑现。
5. 桑德兰中卫丹·巴拉德腿筋受伤缺阵，奥马尔·阿尔德雷特上轮吃到红牌本场停赛，两名主力中卫双双缺席，主帅勒布里斯不得不重新搭配中卫组合。罗曼·芒德尔也因伤无法登场，继续压缩后防轮换储备；中场迪亚拉、前锋蒙德尔同样伤缺。球队目前身处联赛垫底、各项赛事三连败，防线核心人员缺失，面对切尔西的冲击，防守容错空间变得很小。
6. 桑德兰上赛季两次面对切尔西均取得胜利，先在客场2比1取胜，随后回到主场又以2比1击败对手，两回合比赛都攻入2球。尽管桑德兰近期遭遇各项赛事三连败并排名英超垫底，但上赛季双杀切尔西的经历，或许能为球队本场比赛提供一定心理支持。桑德兰近5年面对切尔西主场胜率达到100%。
7. 切尔西上轮英超主场2比0击败曼联，最近4轮联赛赢下3场，积分排名升至第4位。阿隆索执教的球队近期防守表现有所改善，最近5场正式比赛仅丢4球，并完成2场零封。切尔西正逐步找回稳定节奏，攻防表现均有回升迹象。
8. 切尔西本赛季联赛9场进19球，是联赛进球数第3多的球队；佩德罗本赛季联赛9场比赛打入5球，目前排名联赛射手榜第3位；本赛季联赛9场比赛，在领先的情况下最终获胜的场次占总胜场的100%。
9. 切尔西确认若昂·佩德罗、里斯·詹姆斯、马克森斯·拉克鲁瓦、乔雷尔·哈托和杰米·吉滕斯无法出战。若昂·佩德罗遭遇腿筋伤势，是队内头号射手；詹姆斯接受膝盖手术后预计缺阵至明年1月；后防核心拉克鲁瓦、主力后卫哈托和边锋吉滕斯也分别因伤病缺席。中场铁闸莫伊塞斯·凯塞多和锋线轮换小将昆达目前出战成疑，切尔西的伤停覆盖锋线、防线和中场。
10. 切尔西门将埃米利亚诺·马丁内斯此前遭遇颌骨骨折并接受手术，本场将在赛前接受体能测试，以确定能否回归首发。近期表现出色的年轻门将迈克·彭德斯可能因此回到替补席。马丁内斯若通过测试，能够为切尔西防线带来更多经验和稳定性，但其术后身体状态与比赛节奏仍需观察。此外，中场老将亨德森此前遭遇病毒感染，目前也已经恢复训练，有望提升中场厚度。
11. 切尔西主帅阿隆索赛前谈及帕尔默落选英格兰国家队一事，他称并未和帕尔默专门聊起这件事，全队眼下重心放在周日的赛事上，同时肯定了帕尔默的赛场发挥。帕尔默本赛季英超出战9场，送出3球3助攻，和队友的配合、对战术的适应都在稳步进步，但这次落选或许会对他的自信心带来一些冲击。
""",
    }
]
