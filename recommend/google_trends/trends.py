from pytrends.request import TrendReq

def recommend_pytrends(keyword: str) -> list:
    pytrends = TrendReq(hl='ko', tz=540)

    keyword_list = [keyword]

    # TODO: timeframe 날짜 변경
    pytrends.build_payload(keyword_list, cat=0, timeframe='2020-01-01 2022-08-30', geo='KR')
    data = pytrends.related_topics()

    return data