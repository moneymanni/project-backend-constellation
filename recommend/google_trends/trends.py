from pytrends.request import TrendReq

def recommend_pytrends(keyword: str) -> list:
    pytrends = TrendReq(hl='ko', tz=360)

    keyword_list = [keyword]

    # TODO: timeframe 날짜 변경
    pytrends.build_payload(keyword_list, cat=0, timeframe='today 5-y', geo='KR')
    data = pytrends.related_topics()

    return data