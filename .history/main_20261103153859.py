from crawler.xgscore.build import build_report as get_xgscore
from crawler.handicap import get_handicap
from crawler.handicap_history import get_handicap_history
from crawler.sportsmole import get_article
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from rich import print as rprint
from typing import TypedDict, Annotated, Optional, Union
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
import operator
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
import json



SELECTION_COUNT = 3

MATCHES = [
    {
        "OKOOO_MATCH_ID":    "1328150",
        "PREVIEW_URL":       "https://xgscore.io/serie-a/atalanta-parma/preview",
        "XGSCORE_URL":       "https://xgscore.io/serie-a/atalanta-parma/xgscore",
        "SPORTSMOLE_URL":    "https://www.sportsmole.co.uk/football/atalanta-bc/preview/atalanta-vs-parma-prediction-team-news-lineups_608153.html",
        "CLUBELO_HOME_ELO":  "1796",
        "CLUBELO_HOME_GOLO": "1.41",
        "CLUBELO_AWAY_ELO":  "1631",
        "CLUBELO_AWAY_GOLO": "1.03",
        "Information": """
1. 意甲第10轮收官战在贝加莫打响，亚特兰大坐镇新百伦竞技场迎战帕尔马。一边是9轮仅积11分、防线濒临“无人可用”的主队，另一边是9轮5分、进球数联赛垫底的客队。两支赛季初各有抱负的球队，在第十轮就被迫提前面对一个共同的追问：谁先把自己从泥潭里拔出来？
2. 亚特兰大打完本场联赛之后仅有三天休整时间，就要出战欧协联，一周之内迎来双线作战，球队的体能储备并不占优。此役面对排名靠后的帕尔马，在赛程紧凑、欧战任务迫近的背景下，亚特兰大有可能对阵容做出较大轮换，以此减少主力球员的消耗，规避伤病风险。
3. 亚特兰大本赛季8场总进球数达到14球，其中主场进球数占总进球数78%。亚特兰大近10场正赛多达7场比赛半场有得失球。亚特兰大本赛季近10个客场比赛，在落后的情况下最终客场输球率达80%。
4. 亚特兰大近期状态有所下滑，近4场正式比赛取得2平2负，始终未能取胜。上轮联赛客场对阵佛罗伦萨，球队2比2与对手握手言和，未能全取三分。不过，球队本赛季主场表现较为稳健，5个联赛主场拿下3胜1平1负，胜率达到60%。相比之下，帕尔马本赛季状态持续低迷，前9轮联赛仅取得1胜2平6负，4个联赛客场更是全部告负。结合双方过往交锋情况，亚特兰大此役坐镇主场仍具备一定优势，有望借助主场之利争取胜利，终结近期不胜的局面。
5. 亚特兰大正深陷严重的伤病危机，多名主力进攻球员无法登场。前锋拉斯帕多里、斯卡马卡均遭遇大腿伤势，预计休战至11月中旬；中场大将凯西小腿受伤，同样要等到11月中旬回归；加埃塔诺本场能否出战还没有定论。后防方面，科拉希纳茨、贝拉诺瓦、科苏努、克里斯滕森继续伤停，希恩腘绳肌受伤大概率缺席。大量主力伤缺或者出战存疑，球队阵容深度大打折扣，本场要承受巨大的人员压力。
6. 亚特兰大本赛季的困境不止于积分。萨里接手后试图将球队从加斯佩里尼时代的高强度人盯人体系，转向更强调站位与控球的4-2-3-1，但这一改造的代价直接落在了防线身前。球队9轮丢17球，是意甲失球第四多的队伍，而进攻端打进16球，净胜球为负一。攻守之间的失衡，在近期比赛中被反复放大：对AC米兰两球落后的追分、与弗罗西诺内的4比4、对佛罗伦萨的2比2，场面不缺进球，缺的是控制。
7. 更棘手的是，亚特兰大主教练萨里手中可用的中后卫已经所剩无几。希恩、科索努、科拉希纳茨先后进入伤病名单，克里斯滕森又在上一轮开场四分钟即因肌肉不适被换下。仓促入替的斯卡尔维尼刚刚结束十六天的伤停，便打满全场；与他搭档的奥布里奇，原本是U23梯队的第四中卫选择。萨里赛前坦言，伤病让球队的处境“变得复杂”。面对帕尔马，亚特兰大的中前场框架尚算完整，克尔斯托维奇已有6球入账，但防线已经没有再伤一个人的余地。
8. 帕尔马近5次联赛和亚特兰大交手，只拿到1胜1平3负，往绩处于下风。这几场对决里帕尔马合计打进7球，面对亚特兰大的防守很难稳定制造威胁；后防一共丢了15球，防守压力巨大。从赛果和攻防数据来看，帕尔马在交锋当中被对手全面压制。从历史交锋看，亚特兰大近10次面对帕尔马赢下7场，近6次主场对阵帕尔马5胜且全部零封。
9. 帕尔马本赛季攻防表现都不尽如人意。进攻端前9轮联赛只打进5球，场均进球不到1球，多达5场比赛交白卷，持续创造威胁的能力严重不足。防守端同样隐患重重，9轮仅有1场零封，合计丢15球，场均失球1.67粒。球队既缺少稳定得分点，防线也很难稳住，整体竞争力大打折扣。帕尔马本赛季9场总失球数达到15球，其中客场失球数占总失球数60%。帕尔马本赛季近10个客场比赛，在落后的情况下最终客场输球率达100%。
10. 帕尔马本赛季状态持续低迷，联赛前9轮仅取得1胜2平6负，整体表现难言理想。上轮球队坐镇主场迎战乌迪内斯，最终0比0握手言和，未能借助主场之利全取三分。算上这场平局，帕尔马近4轮联赛仅收获1平3负，期间始终未能取胜。
11. 帕尔马目前仅有前锋埃尔菲格因伤缺阵，他预计将休战至11月中旬。本赛季，这名高中锋在联赛中出场5次，送出1次助攻，他的缺席无疑会对球队的进攻端造成一定影响。此外，主力中场伯纳贝在上轮联赛第74分钟因肌肉不适被换下，本场能否出战仍存疑。后卫巴伦蒂因伤，本场比赛同样出战成疑。
12. 帕尔马的处境在数据上更为刺眼。9轮5球，场均射正2.8次，两项均排意甲末位；客场四战全败，一球未进。帕尔马主教练吉拉迪诺九月底接手球队后，仍未在联赛中打开胜利账户，他此前在比萨的执教同样以长期不胜告终。
13. 亚特兰大主教练萨里在赛前发布会上给出了一个容易被忽略的判断：帕尔马的排名“只是因为他们把创造出来的机会转化成进球的比例太低”，而这支球队在5-3-2低位防守中的结构并不差，反击足以让对手“措手不及”。问题的核心不在态度，而在终结能力。今夏帕尔马通过出售铃木彩艳、奇尔卡蒂、佩莱格里诺等人回收约7700万欧元，净收入超过4700万，阵容失血与进攻端的低效之间存在一条清晰的因果链。吉拉迪诺能做的调整有限，卡维利亚的复出或许能改善中场向前的输送，但锋线把握机会的能力，不是一两场训练能够修复的。
14. 从历史交锋看，亚特兰大近10次面对帕尔马赢下7场，近6次主场对阵帕尔马5胜且全部零封。但眼下这支亚特兰大已经连续四轮不胜，主场是萨里止住下滑最现实的依托。帕尔马则需要在客场取得进球，才有资格谈论拿分，而他们恰恰是意甲当下最不具备“在客场进球”条件的球队。
15. 这场比赛大概率不会重现亚特兰大此前那种大开大合的节奏。亚特兰大主教练萨里需要的是三分，哪怕过程收着踢；帕尔马主教练吉拉迪诺需要的是结构不散，哪怕场面被动。真正值得关注的变量只有一个：亚特兰大那条临时拼凑的防线，会不会给意甲最钝的锋线送去一次本不该属于他们的机会？如果会，这场比赛的剧本就会比积分榜显示的更加复杂。
""",
        "HANDICAP_TEAM": "亚特兰大"
    },
]

OKOOO_COOKIE = "LastUrl=; _ga=GA1.1.44804699.1730805190; _ga_B3LCXP8H9E=deleted; _c_WBKFRo=cUo3F5Rp9NBMRQ5Jr0cab0MffU1ZfxTEi0vsskgY; _ga_KDPR20Z4FF=GS2.1.s1768050455$o2$g0$t1768050455$j60$l1$h27564907; zq_companytype_odds=AuthoriteBooks; zq_companytype_overunder=TypicalOu; M_UserID=32588974; M_Ukey=85399cd13fbe10524f7bd4fa5acb3fc1; data_start_isShow=1; FirstURL=www.okooo.com/livecenter/football/; FirstOKURL=https%3A//www.okooo.com/soccer/; First_Source=www.okooo.com; IMUserID=32588974; IMUserName=%E8%8E%B1%E5%B0%94742570; historyShowThisMatch=1; OkTouchAutoUuid=bce2ded58f29caf31cb7d1c297911525; OkTouchMsIndex=6; _ga_H8WNRJTRHH=GS2.1.s1792598779$o27$g1$t1792598798$j41$l0$h1716765268; M_UserName=%22%5Cu83b1%5Cu5c14742570%22; _ga_B3LCXP8H9E=deleted; _ga_7H2HVPJPLZ=GS2.1.s1793340142$o58$g1$t1793340176$j26$l1$h269290029; PHPSESSID=23bdcddc2230952eab3b1a00690c40ae9e2f788d; OKSID=23bdcddc2230952eab3b1a00690c40ae9e2f788d; Hm_lvt_213d524a1d07274f17dfa17b79db318f=1792803370,1792968352,1793073436,1793409260; HMACCOUNT=A236B6BD504505F5; pm=; acw_tc=76b20f6817934454029254308e058674a8eec29bca98af4150fef5b3d97f90; OkAutoUuid=0df26f614ab0d46230c693c96a83136e; OkMsIndex=2; LStatus=Y; LoginStr=%7B%22welcome%22%3A%22%u60A8%u597D%uFF0C%u6B22%u8FCE%u60A8%22%2C%22login%22%3A%22%u767B%u5F55%22%2C%22register%22%3A%22%u6CE8%u518C%22%2C%22TrustLoginArr%22%3A%7B%22alipay%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22tenpay%22%3A%7B%22LoginCn%22%3A%22%u8D22%u4ED8%u901A%22%7D%2C%22weibo%22%3A%7B%22LoginCn%22%3A%22%u65B0%u6D6A%u5FAE%u535A%22%7D%2C%22renren%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22baidu%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22snda%22%3A%7B%22LoginCn%22%3A%22%22%7D%7D%2C%22userlevel%22%3A%22%22%2C%22flog%22%3A%22hidden%22%2C%22UserInfo%22%3A%7B%22UserName%22%3A%22%u83B1%u5C14742570%22%2C%22UserID%22%3A32588974%2C%22AuthLevel%22%3A%22%22%2C%22UserAvatar%22%3A%22https%3A//imgv1.okoooimg.cn/Upload/user/032/58/89/74_avatar_middle.jpg%3Fdc%3D1837442401.3%22%7D%2C%22IsReal%22%3A%22N%22%2C%22PayMethod%22%3A%22okooo%22%2C%22projectStatusCount%22%3A0%2C%22loginSession%22%3A%22___GlobalSession%22%7D; _ga_B3LCXP8H9E=GS2.1.s1793443261$o1778$g1$t1793446572$j42$l1$h1872004109; Hm_lpvt_213d524a1d07274f17dfa17b79db318f=1793446572"


model = ChatOpenAI(
    model_name="claude-fable-5-1",
    temperature=0.4,
    api_key='sk-yFOTmuKp5mZee1kP6ZrS3FiCZqy63wvckE0fiAq0JLgu4fuZ',
    base_url='https://globalai.vip/v1',
    timeout=240
)


class AgentState(TypedDict):
    match_config: dict
    raw_xgscore: str
    xgscore_json: Optional[str]
    raw_handicap: Optional[str]
    handicap_json: Optional[str]
    raw_handicap_history: Optional[str]
    raw_article: Optional[str]
    article_json: Optional[str]
    handicap_history_json: Optional[str]
    features:str
    analysis_result: Optional[str]

class XgscoreReport(BaseModel):
    #一、比赛时间与来源
    match_time:str=Field(description="一、报告头部'比赛时间'，如'2026-10-27'")
    source_url:str=Field(description="一、报告头部'来源'后的URL")

    #二、关键指标对比 (Key Stats)
    home_team_rating:float=Field(description="二、关键指标对比表，主队'球队评级'行数值，如5.4")
    away_team_rating:float=Field(description="二、关键指标对比表，客队'球队评级'行数值，如7.6")
    home_recent_form:float=Field(description="二、关键指标对比表，主队'近期状态'行数值，如6.7")
    away_recent_form:float=Field(description="二、关键指标对比表，客队'近期状态'行数值，如6.5")
    home_xg_luck:str=Field(description="二、关键指标对比表，主队'xG运气指数'行数值，如'+2%'")
    away_xg_luck:str=Field(description="二、关键指标对比表，客队'xG运气指数'行数值，如'-3%'")
    home_xg_predict:str=Field(description="二、关键指标对比表，主队'xG可预测性'行数值，如'74%'")
    away_xg_predict:str=Field(description="二、关键指标对比表，客队'xG可预测性'行数值，如'71%'")

    #三、All matches（胜平负+评分）
    home_all_matches:list[dict]=Field(description="三、All matches下主队小节表格每行，[{opponent,score,result,rating}]")
    away_all_matches:list[dict]=Field(description="三、All matches下客队小节表格每行，[{opponent,score,result,rating}]")

    #四、Home/Away matches（主客队本场地近期胜平负，场次可能不足，允许为空）
    home_home_matches:list[dict]=Field(default_factory=list, description="四、Home/Away下'主队（主场）'小节表格每行，[{opponent,score,result,rating}]")
    away_away_matches:list[dict]=Field(default_factory=list, description="四、Home/Away下'客队（客场）'小节表格每行，[{opponent,score,result,rating}]")

    #五、HEAD TO HEAD 简表
    h2h_home_view:list[dict]=Field(description="五、HEAD TO HEAD简表主队行，[{score,result,rating}]，如比分'0-6, 1-5...'战绩'1胜0平3负'评分'0.2, 1...'拆成多行")
    h2h_away_view:list[dict]=Field(description="五、HEAD TO HEAD简表客队行，[{score,result,rating}]，如比分'6-0, 5-1...'战绩'3胜0平1负'评分'9.8, 9...'拆成多行")

    #六、The Season's Matches
    home_seasons:list[dict]=Field(description="六、The Season's Matches下主队各赛季数据，[{season,gs,gc,xg_scored,xg_conceded}]，每赛季一行")
    home_scored_factor:float=Field(description="六、主队'球队综合预期（多赛季）'下'综合预期进球能力（Scored Factor）'，如1.3")
    home_conceded_factor:float=Field(description="六、主队'球队综合预期（多赛季）'下'综合预期失球风险（Conceded Factor）'，如1.5")
    away_seasons:list[dict]=Field(description="六、The Season's Matches下客队各赛季数据，[{season,gs,gc,xg_scored,xg_conceded}]，每赛季一行")
    away_scored_factor:float=Field(description="六、客队'球队综合预期（多赛季）'下'综合预期进球能力（Scored Factor）'，如1.8")
    away_conceded_factor:float=Field(description="六、客队'球队综合预期（多赛季）'下'综合预期失球风险（Conceded Factor）'，如1.1")

    #七、Recent Matches
    home_recent_gs:float=Field(description="七、Recent Matches下主队'近期每场平均进球（GS）'，如1.5")
    home_recent_gc:float=Field(description="七、Recent Matches下主队'近期每场平均失球（GC）'，如1.2")
    home_recent_matches:list[dict]=Field(description="七、Recent Matches下主队'具体场次数据'每行，[{opponent,date,goals_scored,goals_conceded,xg_scored,xg_conceded}]")
    away_recent_gs:float=Field(description="七、Recent Matches下客队'近期每场平均进球（GS）'，如2.0")
    away_recent_gc:float=Field(description="七、Recent Matches下客队'近期每场平均失球（GC）'，如1.2")
    away_recent_matches:list[dict]=Field(description="七、Recent Matches下客队'具体场次数据'每行，[{opponent,date,goals_scored,goals_conceded,xg_scored,xg_conceded}]")

    #八、Home Matches/Away Matches（详细xG）
    home_home_detail:list[dict]=Field(description="八、Home Matches下主队逐场xG表每行，[{date,opponent,score,xg_scored,xg_conceded}]")
    home_home_avg_gs:float=Field(description="八、Home Matches末'主场均场得分/失分'前一个数，如1.3")
    home_home_avg_gc:float=Field(description="八、Home Matches末'主场均场得分/失分'后一个数，如1.8")
    away_away_detail:list[dict]=Field(description="八、Away Matches下客队逐场xG表每行，[{date,opponent,score,xg_scored,xg_conceded}]")
    away_away_avg_gs:float=Field(description="八、Away Matches末'客场均场得分/失分'前一个数，如1.8")
    away_away_avg_gc:float=Field(description="八、Away Matches末'客场均场得分/失分'后一个数，如1.3")

    #九、Head to Head（详细xG）
    h2h_home_detail:list[dict]=Field(description="九、主队视角H2H逐场xG表每行，[{date,opponent,score,xg_scored,xg_conceded}]")
    h2h_home_avg_gs:float=Field(description="九、主队视角H2H'场均表现'前一个数，如1.0")
    h2h_home_avg_gc:float=Field(description="九、主队视角H2H'场均表现'后一个数，如2.6")
    h2h_away_detail:list[dict]=Field(description="九、客队视角H2H逐场xG表每行，[{date,opponent,score,xg_scored,xg_conceded}]")
    h2h_away_avg_gs:float=Field(description="九、客队视角H2H'场均表现'前一个数，如2.6")
    h2h_away_avg_gc:float=Field(description="九、客队视角H2H'场均表现'后一个数，如1.0")

    #十、Similar Opponents
    home_similar:list[dict]=Field(description="十、Similar Opponents下主队逐场xG，[{date,opponent,score,xg_scored,xg_conceded}]，*平均每场行除外")
    home_similar_avg_gs:float=Field(description="十、Similar Opponents下主队'*平均每场'前一个数，如1.0")
    home_similar_avg_gc:float=Field(description="十、Similar Opponents下主队'*平均每场'后一个数，如1.8")
    away_similar:list[dict]=Field(description="十、Similar Opponents下客队逐场xG，[{date,opponent,score,xg_scored,xg_conceded}]，*平均每场行除外")
    away_similar_avg_gs:float=Field(description="十、Similar Opponents下客队'*平均每场'前一个数，如1.9")
    away_similar_avg_gc:float=Field(description="十、Similar Opponents下客队'*平均每场'后一个数，如1.5")

    #十一、Tables Results
    home_table_all_season_gs:float=Field(description="十一、主队'所有赛季比赛（All Season's Matches）'行的进失球前一个数，如1.3")
    home_table_all_season_gc:float=Field(description="十一、主队'所有赛季比赛（All Season's Matches）'行后一个数，如1.5")
    home_table_recent_gs:float=Field(description="十一、主队'近期比赛（Recent Matches）'行前一个数，如1.5")
    home_table_recent_gc:float=Field(description="十一、主队'近期比赛（Recent Matches）'行后一个数，如1.2")
    home_table_home_gs:float=Field(description="十一、主队'主场比赛（Home Matches）'行前一个数，如1.3")
    home_table_home_gc:float=Field(description="十一、主队'主场比赛（Home Matches）'行后一个数，如1.8")
    home_table_h2h_gs:float=Field(description="十一、主队'历史交锋（Head to Head）'行前一个数，如1.0")
    home_table_h2h_gc:float=Field(description="十一、主队'历史交锋（Head to Head）'行后一个数，如2.6")
    home_table_similar_gs:float=Field(description="十一、主队'相似对手（Similar Opponents）'行前一个数，如1.0")
    home_table_similar_gc:float=Field(description="十一、主队'相似对手（Similar Opponents）'行后一个数，如1.8")
    home_table_weighted_gs:float=Field(description="十一、主队'综合加权得分'行前一个数，如1.22")
    home_table_weighted_gc:float=Field(description="十一、主队'综合加权得分'行后一个数，如1.81")
    away_table_all_season_gs:float=Field(description="十一、客队'本赛季比赛（The Season's Matches）'行前一个数，如1.8")
    away_table_all_season_gc:float=Field(description="十一、客队'本赛季比赛（The Season's Matches）'行后一个数，如1.1")
    away_table_recent_gs:float=Field(description="十一、客队'近期比赛（Recent Matches）'行前一个数，如2.0")
    away_table_recent_gc:float=Field(description="十一、客队'近期比赛（Recent Matches）'行后一个数，如1.2")
    away_table_away_gs:float=Field(description="十一、客队'客场比赛（Away Matches）'行前一个数，如1.8")
    away_table_away_gc:float=Field(description="十一、客队'客场比赛（Away Matches）'行后一个数，如1.3")
    away_table_h2h_gs:float=Field(description="十一、客队'历史交锋（Head to Head）'行前一个数，如2.6")
    away_table_h2h_gc:float=Field(description="十一、客队'历史交锋（Head to Head）'行后一个数，如1.0")
    away_table_similar_gs:float=Field(description="十一、客队'相似对手（Similar Opponents）'行前一个数，如1.9")
    away_table_similar_gc:float=Field(description="十一、客队'相似对手（Similar Opponents）'行后一个数，如1.5")
    away_table_weighted_gs:float=Field(description="十一、客队'综合加权得分'行前一个数，如1.98")
    away_table_weighted_gc:float=Field(description="十一、客队'综合加权得分'行后一个数，如1.27")

    #十二、Team Form
    home_attack_condition:str=Field(description="十二、主队'Attack condition'行，如'+0%'")
    home_defence_condition:str=Field(description="十二、主队'Defence condition'行，如'+0%'")
    home_overall_form:str=Field(description="十二、主队'Overall form'行，如'+5%'")
    home_motivation:str=Field(description="十二、主队'Motivation'行，如'+0%'")
    home_adjusted_gs:float=Field(description="十二、主队'修正后预估进失球'前一个数，如1.28")
    home_adjusted_gc:float=Field(description="十二、主队'修正后预估进失球'后一个数，如1.72")
    away_attack_condition:str=Field(description="十二、客队'Attack condition'行，如'-5%'")
    away_defence_condition:str=Field(description="十二、客队'Defence condition'行，如'-5%'")
    away_overall_form:str=Field(description="十二、客队'Overall form'行，如'+0%'")
    away_motivation:str=Field(description="十二、客队'Motivation'行，如'+5%'")
    away_adjusted_gs:float=Field(description="十二、客队'修正后预估进失球'前一个数，如1.97")
    away_adjusted_gc:float=Field(description="十二、客队'修正后预估进失球'后一个数，如1.28")

    #十三、Teams Impact
    home_impact:int=Field(description="十三、Teams Impact下主队数值，如30")
    away_impact:int=Field(description="十三、Teams Impact下客队数值，如70")

    #十四、球队 Elo/Golo
    home_elo:float=Field(description="十四、球队Elo/Golo表主队Elo列，如1700")
    home_golo:float=Field(description="十四、球队Elo/Golo表主队Golo列，如1.13")
    away_elo:float=Field(description="十四、球队Elo/Golo表客队Elo列，如1819")
    away_golo:float=Field(description="十四、球队Elo/Golo表客队Golo列，如1.34")

class HandicapReport(BaseModel):
    match_time:str=Field(description="比赛时间，如'2026-10-27'")
    handicap: str = Field(description="让球盘口，如'主-0.5'")
    over_under: str = Field(description="进球盘口，如'大2.5'")
    home_odds: float = Field(description="让球盘口，主队水位，如1.85")
    away_odds: float = Field(description="让球盘口，客队水位，如2.10")
    over_under_odds: float = Field(description="进球盘口，大球水位，如1.95")
    under_under_odds: float = Field(description="进球盘口，小球水位，如1.85")

class HandicapHistoryReport(BaseModel):
    match_time:str=Field(description="比赛时间，如'2026-10-27'")
    handicap_history: list[dict] = Field(description="本场比赛的让球方近六场比赛盘口历史数据，每行包含日期、赛事、主队、比分、客队 、让球方盘口、结果")
    total_wins: int = Field(description="赢盘场次，加1分")
    total_draws: Union[int, float] = Field(description="走盘场次，加0.5分")
    total_losses: int = Field(description="输盘场次，加0分")
    total: Union[int, float] = Field(description="合计，如赢盘2场：2分，走盘1场：0.5分，输盘3场：0分，总计2.5分")

class ArticleReport(BaseModel):
    opening_paragraph: str = Field(description="导语（开篇引子）")
    match_preview: str = Field(description="比赛前瞻")
    team_news: str = Field(description="球队新闻")
    match_information: str = Field(description="比赛情报")


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
    api_key='sk-yFOTmuKp5mZee1kP6ZrS3FiCZqy63wvckE0fiAq0JLgu4fuZ',
    base_url='https://globalai.vip/v1'
)


def xgscore_node(state: AgentState):
    match = state["match_config"]
    elo_golo = {
        "home_elo":  match["CLUBELO_HOME_ELO"],
        "away_elo":  match["CLUBELO_AWAY_ELO"],
        "home_golo": match["CLUBELO_HOME_GOLO"],
        "away_golo": match["CLUBELO_AWAY_GOLO"],
    }

    xgscore_text = get_xgscore(
        preview_url=match["PREVIEW_URL"],
        xgscore_url=match["XGSCORE_URL"],
        elo_golo=elo_golo,
    )


    structured_llm = llm.with_structured_output(XgscoreReport, method="function_calling")


    result = structured_llm.invoke([
        SystemMessage(
            content="你是一个足球数据提取器。请把输入的XGSCORE报告转换为标准的 JSON 格式数据。"
        ),
        HumanMessage(content=xgscore_text)
    ])

    return {
        "raw_xgscore": xgscore_text,
        "xgscore_json": result.model_dump()
    }

def handicap_node(state: AgentState):
    match = state["match_config"]
    handicap_data = get_handicap(match["OKOOO_MATCH_ID"], OKOOO_COOKIE)
    
    structured_llm = llm.with_structured_output(HandicapReport, method="function_calling")
   
    result = structured_llm.invoke([
        SystemMessage(
            content="你是一个足球数据提取器。请把输入的盘口报告转换为标准的 JSON 格式数据。"
        ),
        HumanMessage(content=handicap_data)
    ])
    return {
        "raw_handicap": handicap_data,
        "handicap_json": result.model_dump()
    }

def handicap_history_node(state: AgentState):
    match = state["match_config"]
    handicap_history_data = get_handicap_history(match["OKOOO_MATCH_ID"], 6, OKOOO_COOKIE)
    rules = Path("handicap.md").read_text(encoding="utf-8")
    structured_llm = llm.with_structured_output(HandicapHistoryReport, method="function_calling")
    result = structured_llm.invoke([
        SystemMessage(
            content=f"""
    你是一个足球数据提取器。请把输入的盘口历史报告转换为标准的 JSON 格式数据。
    盘口让球规则：
    {rules}
    """
        ),
        HumanMessage(content=handicap_history_data)
    ])
    return {
        "raw_handicap_history": handicap_history_data,
        "handicap_history_json": result.model_dump()
    }

def article_node(state: AgentState):
    match = state["match_config"]
    article_data = get_article(match["SPORTSMOLE_URL"])
    information = match.get("Information", "")
    if information and information.strip():
        article_data += f"\n\n#### match_information\n{information.strip()}"
    structured_llm = llm.with_structured_output(ArticleReport, method="function_calling")
    result = structured_llm.invoke([
        SystemMessage(
            content="""
        你是一个足球数据提取器。请把输入的文章内容转换为标准的 JSON 格式数据，格式如下：
        ```json
        opening_paragraph: 导语（开篇引子）
        match_preview: 比赛前瞻
        team_news: 球队新闻
        match_information: 比赛情报
        ```
        """
        ),
        HumanMessage(content=article_data)
    ])
    return {
        "raw_article": article_data,
        "article_json": result.model_dump()
    }

def filter_node(state: AgentState):
    features_rules = Path("features.md").read_text(encoding="utf-8")
    handicap_rules = Path("handicap.md").read_text(encoding="utf-8")

    result = llm.invoke([
        SystemMessage(
            content=f"""
            "你是一位专业的足球数据分析师。\n"
        "我会给你提供本场比赛的全部数据，以及一份特征筛选规则文档。\n"
        "请对照规则文档，逐一判断本场比赛是否符合每种特征的所有必要条件。\n\n"
        "判断规则：\n"
        "1. 每种特征的最后一条必要条件必须强制执行，不论前面条件如何。\n"
        "2. 最后一条的作用是：用必要条件一与必要条件二的综合评估，决定是否修正某些不满足的条件，或推翻某些已满足的条件。\n"
        "3. 经过最后一条修正后，所有条件全部满足（含修正结果），总结论为'符合'；否则为'不符合'。\n"
        "4. 关键数据缺失无法判断时，总结论为'数据不足'。\n\n"
        "输出格式要求：\n"
        "比赛双方 + 让球方\n"
        "对每种特征，按以下格式输出：\n\n"
        "## [特征名称]\n"
        "**总结论**：符合 / 不符合 / 数据不足\n"
        "（仅当总结论为'符合'时，紧接着输出）**观点**：根据该特征的含义，给出具体的投注建议，包括盘口推荐和比分预测。\n\n"
        "逐条列出每个必要条件：\n"
        "**必要条件X**：满足 / 不满足 / 数据不足\n"
        "> 理由：引用数据中的具体数值或事实，说明为什么满足或不满足。\n"
        "> 例如：让球方（阿森纳）近5场战绩为4胜1平，满足≥3场获胜的条件。\n\n"
        "最后输出汇总：\n"
        "## 汇总结论\n"
        "- 符合的特征：列出名称 + 一句话关键理由 + 观点（盘口建议和比分预测）\n"
        "- 不符合的特征：列出名称，并用一句话说明最关键的不满足原因\n"
        "- 数据不足的特征：列出名称，并说明缺少哪项数据\n"
            """
        ),
        HumanMessage(content=f"""
        "## 特征筛选规则\n{features_rules}\n\n"
        "## 盘口规则\n{handicap_rules}\n\n"
        "## 盘口数据\n{state['handicap_json']}\n\n"
        "## 盘口历史\n{state['handicap_history_json']}\n\n"
        "## 比赛背景\n{state['article_json']}\n\n"
        "## xGscore报告\n{state['xgscore_json']}\n\n"
        "请逐一判断本场比赛符合哪些特征、不符合哪些特征，并给出每条必要条件的判断理由。"
        "注：xGscore 报告中除球队 Elo 与 Golo 覆盖全部赛事外，其余数据均为联赛数据。"
""")
    ])

    rprint('++++++++++++++++++++++++++++++++++++++++++')
    rprint(result.content)

    return {
        "features": result.content
    }

def save_node(state: AgentState):
    """在 analysis_node 之前保存两份 markdown 文件到 output 目录。"""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    match_id = state["match_config"]["OKOOO_MATCH_ID"]

    report_lines = []
    report_lines.append(f"# 比赛数据报告 - {match_id}\n")

    report_lines.append("## XGScore 数据\n")
    report_lines.append(f"```json\n{json.dumps(state['xgscore_json'], ensure_ascii=False, indent=4)}\n```\n")

    report_lines.append("## 盘口数据\n")
    report_lines.append(f"```json\n{json.dumps(state['handicap_json'], ensure_ascii=False, indent=4)}\n```\n")

    report_lines.append("## 让球历史盘路\n")
    report_lines.append(f"{state['raw_handicap_history']}\n")

    report_lines.append("## 比赛情报\n")
    report_lines.append(f"```json\n{json.dumps(state['article_json'], ensure_ascii=False, indent=4)}\n```\n")

    (output_dir / f"{match_id}_report.md").write_text("".join(report_lines), encoding="utf-8")

    filters = state['features']
    
    (output_dir / f"{match_id}_features.md").write_text("".join(filters), encoding="utf-8")

    return {}

def analysis_node(state: AgentState) -> AgentState:
    xgscore_data = state["xgscore_json"]
    handicap_data = state["handicap_json"]
    
    response = llm.invoke([
        SystemMessage(content="你是一个资深的足球赛事分析师。"),
        HumanMessage(content=f"""
    请根据以下结构化的比赛数据 JSON，对比赛走势和胜负进行专业分析：
        ```json
        {json.dumps(xgscore_data, ensure_ascii=False, indent=4)}
        ```
        以及以下盘口数据：
        ```json
        {json.dumps(handicap_data, ensure_ascii=False, indent=4)}
        ```
     """)
    ])

    return {"analysis_result": response.content}


workflow = StateGraph(AgentState)
workflow.add_node("xgscore_node", xgscore_node)
workflow.add_node("handicap_node", handicap_node)
workflow.add_node("article_node", article_node)
workflow.add_node("handicap_history_node", handicap_history_node)
workflow.add_node("filter_node", filter_node)
workflow.add_node("save_node", save_node)
workflow.add_node("analysis_node", analysis_node)
workflow.add_edge(START, "xgscore_node")
workflow.add_edge("xgscore_node", "handicap_node")
workflow.add_edge("handicap_node", "handicap_history_node")
workflow.add_edge("handicap_history_node", "article_node")
workflow.add_edge("article_node", "filter_node")
workflow.add_edge("filter_node", "save_node")
workflow.add_edge("save_node", "analysis_node")
workflow.add_edge("analysis_node", END)

app = workflow.compile()


res = app.invoke({ "match_config": MATCHES[0], "raw_xgscore": "", "xgscore_json": None, "raw_handicap": "", "handicap_json": None, "raw_handicap_history": "", "handicap_history_json": None, "raw_article": "", "article_json": None, "features": None, "analysis_result": None })

# rprint(res["analysis_result"])
