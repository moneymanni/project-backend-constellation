from gensim.models import Word2Vec

from recommend import recommend_pytrends
from data import RecommendMessage

class RecommendService:
    def recommend_googletrends(self, keyword: str) -> list:
        """keyword를 google trends로 추천합니다.

        :param keyword: 추천할 단어
        :return: 추천된 단어를 포함한 리스트:
            [{
                'keyword': str, # 주요 단어
                'value': int    # 관계 정도
            }]
        """
        try:
            data = recommend_pytrends(keyword)

            # rising_data = data[keyword]['rising'].to_dict('records')
            top_data = data[keyword]['top'].to_dict('records')

            pytrends_topics_data = {'pytrends_topics_rising': {}, 'pytrends_topics_top': {}}
            # for rising in rising_data:
            #     rising_form = {'value': rising['value'], 'topic_type': rising['topic_type']}
            #     pytrends_topics_data['pytrends_topics_rising'][rising['topic_title']] = rising_form
            for top in top_data:
                top_form = {'value': str(top['value']), 'topic_type': top['topic_type']}
                pytrends_topics_data['pytrends_topics_top'][top['topic_title']] = top_form

            recommend_keywords = []

            for category, topics in pytrends_topics_data.items():
                for topic, details in topics.items():
                    recommend_keywords.append((topic, float(details['value'])))
        except Exception as e:
            return RecommendMessage.ERROR

        return recommend_keywords

    def recommend_w2v(self, keyword: str) -> list:
        """keyword를 Word2Vec로 추천합니다.

        :param keyword: 추천할 단어
        :return: 추천된 단어를 포함한 리스트:
            [{
                'keyword': str, # 주요 단어
                'value': int    # 관계 정도
            }]
        """
        loaded_model = Word2Vec.load('./recommend/w2v_model/w2v_crow.model')

        try:
            recommend_keywords = loaded_model.wv.most_similar(keyword, topn=25)
        except Exception as e:
            return RecommendMessage.ERROR

        return recommend_keywords
