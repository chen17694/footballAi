from crawler.handicap import get_handicap
from config import OKOOO_RECENT_N, OKOOO_COOKIE, MATCHES, SELECTION_COUNT


def handicap_node():
    match = state["match_config"]

    handicap = get_handicap(match["OKOOO_MATCH_ID"], OKOOO_COOKIE)


    return {
        "handicap": handicap
    }
