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
        "OKOOO_MATCH_ID":    "1331854",
        "PREVIEW_URL":       "https://xgscore.io/epl/liverpool-arsenal/preview",
        "XGSCORE_URL":       "https://xgscore.io/epl/liverpool-arsenal/xgscore",
        "SPORTSMOLE_URL":    "https://www.sportsmole.co.uk/football/liverpool/preview/liverpool-vs-arsenal-prediction-team-news-lineups_608057.html",
        "CLUBELO_HOME_ELO":  "1943",
        "CLUBELO_HOME_GOLO": "1.55",
        "CLUBELO_AWAY_ELO":  "2040",
        "CLUBELO_AWAY_GOLO": "1",
        "Information": """
1. 利物浦确认弗林蓬、埃基蒂克、布拉德利以及莱奥尼本场无缘出战，几名球员分别遭遇大腿、跟腱与膝盖伤病困扰，埃基蒂克、布拉德利和莱奥尼本赛季至今还没有获得出场机会。弗林蓬和布拉德利一同缺席，让球队右后卫位置的备选空间大幅缩减，阿劳霍大概率继续客串该位置；埃基蒂克缺阵削弱锋线替补深度，莱奥尼伤停也给后防轮换安排带来阻碍。
2. 利物浦伤病迎来部分利好消息：索博斯洛伊与维克托·穆尼奥斯都已经回归训练，存在进入本场大名单的机会，但最终能否入选还没有定论。索博斯洛伊腿筋有伤，已经缺阵三场，主帅伊劳拉也提醒外界不要急于求成，他首发的概率不大；穆尼奥斯膝伤康复后同样迎来复出契机，需要赛前最终检查，就算上场大概率也是替补出战。维尔茨此前对阵布莱顿遭遇脚踝不适，不过他已经在联赛杯复出，本场确定可以上场。
3. 利物浦中场赫拉芬贝赫本场对阵阿森纳有望登场，目前他已经为利物浦出战149场各项赛事，此战有机会达成俱乐部生涯第150次出场的里程碑。这份特殊的荣誉感，或许会成为荷兰中场的额外动力，推动他在这场强强对话之中拿出更好的赛场发挥。
4. 利物浦周中在联赛杯历经点球大战淘汰切尔西，延续了近期不错的竞技状态。回到英超赛场，球队上轮主场2比0拿下布莱顿，斩获赛季主场联赛首胜，同时拿下联赛四连胜，积15分位列积分榜第4。近8场各项赛事红军拿下7场胜利，唯一败绩是客场不敌曼城。球队现阶段落后阿森纳、曼城6分，如果本场能够战胜阿森纳，双方分差就将缩短到3分。
5. 利物浦近5场正赛连续进球，且场均进球达3.0球；近10场正赛多达7场比赛半场有得失球；伊萨克本赛季联赛8场比赛打入6球，目前排名联赛射手榜第2位；本赛季联赛8场比赛，在领先的情况下最终获胜的场次占总胜场的75%；本赛季8场总失球数达到8球，其中主场失球数占总失球数62%；本赛季联赛8场比赛，在落后的情况下最终输球的场次占总负场的100%。
6. 阿森纳确认萨卡、萨利巴以及道曼本场无缘登场。边路核心萨卡大腿、股四头肌受伤，阿尔特塔透露他还需要数周休养；主力中卫萨利巴背伤缠身，12月之前难以回归；年轻边锋道曼在上轮联赛杯吃到红牌，开启三场国内禁赛，本场是禁赛首战。球队边锋储备进一步吃紧，萨利巴的长期缺阵也持续给中卫排兵布阵带来难题。
7. 阿森纳赛前阵容迎来不少好消息：周中联赛杯获得轮休的赖斯与卡拉菲奥里都恢复训练，客战利物浦有机会回归赛场，赖斯大概率重回首发，助力球队巩固中场控制力，卡拉菲奥里则能够充实后场轮换以及边路攻防；此前伤缺的主力边锋措利斯，现已参与合练，存在复出可能；马杜埃凯脚踝有伤缺席联赛杯，出战待定，教练组会根据赛前最后一练评估状态；因卡皮耶已经在联赛杯打满全场，本场确定可以登场。
8. 阿森纳本赛季英超前8轮交出7胜1负的亮眼战绩，拿到21分，和曼城积分持平，只因净胜球差距排在积分榜第二位。枪手近期联赛状态稳定，接连拿下诺丁汉森林、埃弗顿以及富勒姆，收获三连胜，这当中两场比赛实现零封。防守是阿森纳一大杀手锏，前8轮仅仅丢掉5球，场均失球低至0.625粒，是现阶段英超失球最少的队伍。
9. 阿森纳本赛季联赛8场失5球，是联赛失球数第1少的球队；本赛季联赛8场战绩为7胜0平1负，目前排名联赛第2，有争冠希望，本场比赛战意十足；本赛季联赛8场比赛，在领先的情况下最终获胜的场次占总胜场的71%；本赛季8场总失球数达到5球，其中客场失球数占总失球数60%；本赛季联赛8场比赛，半场失球占比达到总失球的60%；本赛季联赛8场比赛，在落后的情况下最终输球的场次占总负场的100%。
10. 阿森纳周中联赛杯第四轮面对英乙球队弗利特伍德镇，16岁小将道曼被红牌罚下，球队少一人作战，常规时间与对手1比1战平，最终在点球大战中告负，无缘晋级。此前阿森纳5场正式比赛取得4胜1平，整体表现稳定，此次被低级别球队淘汰，使连胜晋级的势头受到打击，球队士气和信心也受到一定影响。
11. 阿森纳近13次英超做客安菲尔德拿到5平8负，合计只收获5分，球队上一次在这座球场拿下联赛胜利，要追溯到2012年9月2比0取胜，距今已经长达约14年。阿尔特塔带队之后，阿森纳6次联赛客场对阵利物浦仅仅拿到3分。尽管枪手本赛季客场防守水准出众，不过利物浦如今主场豪取五连胜，安菲尔德热烈的主场氛围，加上主队擅长的高位压迫打法，会给阿森纳的客场征程带来不小压力。
12. 阿森纳在周中杯赛中先赛一天，轮换幅度也比利物浦更大，本场在体能以及备战层面可能占据一定优势。两队在周中都有英联杯任务，但阿森纳比利物浦先赛一天，也就是多了一天的休息时间，球员的恢复更为充分；而在阵容轮换幅度上，阿森纳只连场首发了2名主力，利物浦则有4人连续出战。一方休息更久、主力消耗更小，另一方休息时间较短、连续出战人数更多，两队的体能与备战状况形成对比。综合来看，客场造访的阿森纳在体能层面可能占据一定优势，这或将在比赛的跑动强度与下半场持续输出中体现出来。
""",
        "HANDICAP_TEAM": "阿森纳"
    }
]

OKOOO_COOKIE = "LastUrl=; _ga=GA1.1.44804699.1730805190; _ga_B3LCXP8H9E=deleted; _c_WBKFRo=cUo3F5Rp9NBMRQ5Jr0cab0MffU1ZfxTEi0vsskgY; _ga_KDPR20Z4FF=GS2.1.s1768050455$o2$g0$t1768050455$j60$l1$h27564907; zq_companytype_odds=AuthoriteBooks; zq_companytype_overunder=TypicalOu; M_UserID=32588974; M_Ukey=85399cd13fbe10524f7bd4fa5acb3fc1; data_start_isShow=1; FirstURL=www.okooo.com/livecenter/football/; FirstOKURL=https%3A//www.okooo.com/soccer/; First_Source=www.okooo.com; IMUserID=32588974; IMUserName=%E8%8E%B1%E5%B0%94742570; historyShowThisMatch=1; OkTouchAutoUuid=bce2ded58f29caf31cb7d1c297911525; OkTouchMsIndex=6; _ga_H8WNRJTRHH=GS2.1.s1792598779$o27$g1$t1792598798$j41$l0$h1716765268; M_UserName=%22%5Cu83b1%5Cu5c14742570%22; _ga_B3LCXP8H9E=deleted; _ga_7H2HVPJPLZ=GS2.1.s1793340142$o58$g1$t1793340176$j26$l1$h269290029; PHPSESSID=23bdcddc2230952eab3b1a00690c40ae9e2f788d; OKSID=23bdcddc2230952eab3b1a00690c40ae9e2f788d; Hm_lvt_213d524a1d07274f17dfa17b79db318f=1792803370,1792968352,1793073436,1793409260; HMACCOUNT=A236B6BD504505F5; pm=; acw_tc=76b20f6817934454029254308e058674a8eec29bca98af4150fef5b3d97f90; OkAutoUuid=0df26f614ab0d46230c693c96a83136e; OkMsIndex=2; LStatus=Y; LoginStr=%7B%22welcome%22%3A%22%u60A8%u597D%uFF0C%u6B22%u8FCE%u60A8%22%2C%22login%22%3A%22%u767B%u5F55%22%2C%22register%22%3A%22%u6CE8%u518C%22%2C%22TrustLoginArr%22%3A%7B%22alipay%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22tenpay%22%3A%7B%22LoginCn%22%3A%22%u8D22%u4ED8%u901A%22%7D%2C%22weibo%22%3A%7B%22LoginCn%22%3A%22%u65B0%u6D6A%u5FAE%u535A%22%7D%2C%22renren%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22baidu%22%3A%7B%22LoginCn%22%3A%22%22%7D%2C%22snda%22%3A%7B%22LoginCn%22%3A%22%22%7D%7D%2C%22userlevel%22%3A%22%22%2C%22flog%22%3A%22hidden%22%2C%22UserInfo%22%3A%7B%22UserName%22%3A%22%u83B1%u5C14742570%22%2C%22UserID%22%3A32588974%2C%22AuthLevel%22%3A%22%22%2C%22UserAvatar%22%3A%22https%3A//imgv1.okoooimg.cn/Upload/user/032/58/89/74_avatar_middle.jpg%3Fdc%3D1837442401.3%22%7D%2C%22IsReal%22%3A%22N%22%2C%22PayMethod%22%3A%22okooo%22%2C%22projectStatusCount%22%3A0%2C%22loginSession%22%3A%22___GlobalSession%22%7D; _ga_B3LCXP8H9E=GS2.1.s1793443261$o1778$g1$t1793446572$j42$l1$h1872004109; Hm_lpvt_213d524a1d07274f17dfa17b79db318f=1793446572"


model = ChatOpenAI(
    model_name="deepseek-v4.1-flash",
    temperature=0.3,
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

class FilterReport(BaseModel):
    xgscore_json: XgscoreReport = Field(description="XGSCORE报告的结构化JSON数据")
    handicap_json: HandicapReport = Field(description="盘口报告的结构化JSON数据")
    handicap_history_json: HandicapHistoryReport = Field(description="盘口历史报告的结构化JSON数据")
    article_json: ArticleReport = Field(description="比赛背景与情报分析的结构化JSON数据")
    matched_features: list[str] = Field(description="符合的特征列表")
    unmatched_features: list[str] = Field(description="不符合的特征列表")
    insufficient_data_features: list[str] = Field(description="数据不足的特征列表")

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
    print(information)
    if information and information.strip():
        article_data += f"\n\n#### match_information\n{information.strip()}"
    print(article_data)
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
    rprint(result)
    return {
        "raw_article": article_data,
        "article_json": result.model_dump()
    }

def filter_node(state: AgentState):
    match = state["match_config"]
    xgscore_data = state["xgscore_json"]
    handicap_data = state["handicap_json"]
    handicap_history_data = state["handicap_history_json"]
    article_data = state["article_json"]
    rules = Path("features.md").read_text(encoding="utf-8")
    structured_llm = llm.with_structured_output(FilterReport, method="function_calling")

    result = structured_llm.invoke([
        SystemMessage(
            content=f"""
            1. 以下是比赛特征筛选所需要的数据：
            球队数据综合评估（联赛）：{json.dumps(xgscore_data, ensure_ascii=False, indent=4)}
            盘口数据：{json.dumps(handicap_data, ensure_ascii=False, indent=4)}
            盘口历史数据：{json.dumps(handicap_history_data, ensure_ascii=False, indent=4)}
            比赛背景与情报分析：{json.dumps(article_data, ensure_ascii=False, indent=4)}
            \n
            2. 根据以下规则进行比赛特征筛选：
            {rules}
            """
        ),
        HumanMessage(content=f"对{match['OKOOO_MATCH_ID']}这场比赛进行特征筛选，输出符合的特征列表、未符合的特征列表、数据不足的特征列表。")
    ])

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
workflow.add_node("analysis_node", analysis_node)
workflow.add_edge(START, "xgscore_node")
workflow.add_edge("xgscore_node", "handicap_node")
workflow.add_edge("handicap_node", "handicap_history_node")
workflow.add_edge("handicap_history_node", "article_node")
workflow.add_edge("article_node", "analysis_node")
workflow.add_edge("analysis_node", END)

app = workflow.compile()


res = app.invoke({ "match_config": MATCHES[0], "raw_xgscore": "", "xgscore_json": None, "raw_handicap": "", "handicap_json": None, "raw_handicap_history": "", "handicap_history_json": None, "raw_article": "", "article_json": None, "analysis_result": None })

rprint(res["analysis_result"])
