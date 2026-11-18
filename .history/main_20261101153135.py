from crawler.xgscore.build import build_report as get_xgscore
from crawler.handicap import get_handicap
from crawler.handicap_history import get_handicap_history
from crawler.sportsmole import get_article
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from rich import print as rprint
from typing import TypedDict, Annotated, Optional
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
        "OKOOO_MATCH_ID":    "1328557",
        "PREVIEW_URL":       "https://xgscore.io/league-1/lens-paris/preview",
        "XGSCORE_URL":       "https://xgscore.io/league-1/lens-paris/xgscore",
        "SPORTSMOLE_URL":    "https://www.sportsmole.co.uk/football/lens/preview/lens-vs-paris-fc-prediction-team-news-lineups_607391.html",
        "CLUBELO_HOME_ELO":  "1805",
        "CLUBELO_HOME_GOLO": "1.42",
        "CLUBELO_AWAY_ELO":  "1705",
        "CLUBELO_AWAY_GOLO": "1.2",
        "Intelligence": """
1. 朗斯周中欧冠刚远赴比利时客场挑战布鲁日，长途奔波加上双线作战消耗明显，体能储备处于下风。本场法甲面对以逸待劳的巴黎FC，朗斯在比赛后半段的跑动和对抗强度可能受到影响。巴黎FC没有欧战任务，上轮联赛是在6天多以前，主力球员的体能得到了充足恢复；朗斯虽然在3天前刚刚在比利时踢完一场欧冠，但只连场首发了门将里塞（11场）、后卫阿吉拉尔（10场2球1助）以及翼位斯库拉希（10场1助）3人。本场在体能以及备战层面，客场造访的巴黎FC可能占据一定优势，但并不明显。
2. 朗斯近期状态起伏明显，周中欧冠客场0比3不敌布鲁日，遭遇欧冠两连败。近6场各项赛事仅取得2胜1平3负，双线作战下体能与防线压力同步增加。虽然联赛层面刚完成两连胜，但欧冠连续丢球让球队士气受到一定影响。朗斯目前7轮联赛踢完拿到3胜1平3负，取得10个积分，排名第9位，不过最近两轮取得连胜，摆脱了此前4轮只拿1分的颓势。
3. 朗斯防守端问题不小，近10场正赛场场丢球，总计丢18球，场均失球达到1.8粒，防线稳定性持续不足。在欧冠客场0比3不敌布鲁日后，球队体能与防线信心都受到影响。
4. 朗斯本场伤停情况较为严重。主力边锋西马（7场2球1助）因大腿肌肉伤势，预计将缺席至11月底；后防线上，主力后卫加尼乌（8场1球）膝关节受伤同样缺阵至11月底，纳夫罗茨基（3场）十字韧带撕裂赛季报销，轮换后卫格拉蒂特/格雷迪特（3场）与查韦斯也因肌肉和腘绳肌伤势继续休战。此外，轮换前锋爱德华/奥德华（9场1球）和轮换后卫萨尼昂（4场）同样因伤无缘出战。朗斯官方社媒公布的参赛名单较上场欧冠又新增2人缺席，包括替补未出场的年轻后卫苏莱曼-萨尼昂（4场）以及踢了半个多小时的轮换中锋奥德华（9场1球）；此外，进攻核心西马（7场2球1助）以及三大中卫加尼乌（8场1球）、纳夫罗茨基（3场）以及格雷迪特（3场）也都继续缺席。多条防线主力与轮换球员同时缺阵，让朗斯后防深度受到明显影响，本场防守端压力不小。
5. 巴黎FC本赛季表现抢眼，前7轮联赛取得4胜2平1负，暂居高位，整体状态明显优于对手。上轮法甲主场4比3击败雷恩，这场胜利也是球队46年来首次击败雷恩，士气明显提升；前7轮取得4胜2平1负，目前高居联赛第3位。巴黎FC是本赛季法甲最大黑马，迄今7轮获得4胜2平1负，唯一败绩是上上轮客场0比1不敌洛里昂。不过球队客场表现相对一般，本赛季3个联赛客场仅取得1胜1平1负，客场拿分效率并不算突出。
6. 巴黎FC近5次联赛面对朗斯仅取得1平4负，交锋记录完全处于下风。上赛季联赛主客场两度交手，巴黎FC均以1比2和0比5落败，被朗斯“双杀”。本场再遇老对手，巴黎FC在心理层面难免承受压力。双方近期10场各项赛事交手中，朗斯取得5胜4平1负，占据绝对优势；其中最近4次联赛交手，朗斯全部拿下，上季球队主场2比1拿下，客场5比0大胜。
7. 巴黎FC本场也有伤停隐患。替补前锋乔纳森·伊科内因大腿伤势继续缺席；主力中卫萨米尔·谢尔吉（5场1球）和主力边后卫哈马里·特劳雷（6场）上轮联赛后出现伤情，虽然两人已参与球队合练、本周都能正常参训，但本场出战仍存疑，最终是否出场还需要做出决定。中场樊尚·马尔凯蒂（2场1球）已经恢复完整训练，等于确定缺席的只有替补前锋伊科内（2场）以及本季还没出过场的桑吉两人。巴黎FC主帅罗塞尼尔赛前介绍球队阵容情况，整体而言还是比较齐整的。
""",
        "HANDICAP_TEAM": "朗斯"
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

class handicap_history_report(BaseModel):
    match_time:str=Field(description="比赛时间，如'2026-10-27'")
    handicap_history: list[dict] = Field(description="盘口历史数据，每行包含日期、赛事、主队、比分、客队 、让球方盘口、结果")
    # 合计：赢盘 + 走盘×0.5 = 2.5 场 ，输盘 3 场
    

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
    
    rprint("【盘口报告原始文本】")
    rprint(handicap_data)
    structured_llm = llm.with_structured_output(HandicapReport, method="function_calling")
    rprint("【盘口报告结构化 JSON】")
    result = structured_llm.invoke([
        SystemMessage(
            content="你是一个足球数据提取器。请把输入的盘口报告转换为标准的 JSON 格式数据。"
        ),
        HumanMessage(content=handicap_data)
    ])
    rprint(result)
    return {
        "raw_handicap": handicap_data,
        "handicap_json": result.model_dump()
    }

def handicap_history_node(state: AgentState):
    match = state["match_config"]
    handicap_history_data = get_handicap_history(match["OKOOO_MATCH_ID"], OKOOO_COOKIE)
    
    rprint("【盘口历史报告原始文本】")
    rprint(handicap_history_data)
    structured_llm = llm.with_structured_output(handicap_history_report, method="function_calling")
    rprint("【盘口历史报告结构化 JSON】")
    result = structured_llm.invoke([
        SystemMessage(
            content="你是一个足球数据提取器。请把输入的盘口历史报告转换为标准的 JSON 格式数据。"
        ),
        HumanMessage(content=handicap_history_data)
    ])
    rprint(result)
    return {
        "raw_handicap_history": handicap_history_data,
        "handicap_history_json": result.model_dump()
    }

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
workflow.add_node("handicap_history_node", handicap_history_node)
workflow.add_node("analysis_node", analysis_node)
workflow.add_edge(START, "xgscore_node")
workflow.add_edge("xgscore_node", "handicap_node")
workflow.add_edge("handicap_node", "handicap_history_node")
workflow.add_edge("handicap_history_node", "analysis_node")
workflow.add_edge("analysis_node", END)

app = workflow.compile()


res = app.invoke({ "match_config": MATCHES[0], "raw_xgscore": "", "xgscore_json": None, "raw_handicap": "", "handicap_json": None, "analysis_result": None })

rprint("【第一步产出的 JSON 数据】")
rprint(res["xgscore_json"])

rprint("\n【第二步产出的分析报告】") 
rprint(res["analysis_result"])
