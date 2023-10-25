import numpy as np

from gensim.models import Word2Vec

from recommend import recommend_pytrends
from data import RecommendMessage

class RecommendService:
    def __init__(self, page_dao):
        self.page_dao = page_dao


    def recommend_googletrends(self, keyword: str, page_id: int) -> list:
        """keyword를 google trends로 추천합니다.

        :param keyword: 추천할 단어, page_id: 추천할 id
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

            note_id = self.page_dao.find_note_id_by_page_id(page_id)
            page_list = self.page_dao.find_page_id_and_keyword_by_note_id(note_id)


            # 중복되는 키워드는 삭제한다.
            page_keywords_set = set([page['keyword'] for page in page_list])
            recommend_keywords = [(topic, value) for topic, value in recommend_keywords if topic not in page_keywords_set]

            # 5개의 토픽만 남기고 나머지는 삭제한다.
            topics, values = zip(*recommend_keywords)
            probabilities = np.array(values) / sum(values)
            selected_indices = np.random.choice(len(topics), size=min(5, len(topics)), replace=False, p=probabilities)
        except Exception as e:
            return RecommendMessage.ERROR

        return [recommend_keywords[index] for index in selected_indices]

    def recommend_w2v(self, keyword: str, page_id: int) -> list:
        """keyword를 Word2Vec로 추천합니다.

        :param keyword: 추천할 단어, page_id: 추천할 id
        :return: 추천된 단어를 포함한 리스트:
            [{
                'keyword': str, # 주요 단어
                'value': int    # 관계 정도
            }]
        """
        loaded_model = Word2Vec.load('./recommend/w2v_model/w2v_sg.model')

        try:
            recommend_keywords = loaded_model.wv.most_similar(keyword, topn=50)

            note_id = self.page_dao.find_note_id_by_page_id(page_id)
            page_list = self.page_dao.find_page_id_and_keyword_by_note_id(note_id)

            # 중복되는 키워드는 삭제한다.
            page_keywords_set = set([page['keyword'] for page in page_list])
            recommend_keywords = [(topic, value) for topic, value in recommend_keywords if topic not in page_keywords_set]

            # 5개의 키워드만 남기고 나머지는 삭제한다.
            topics, values = zip(*recommend_keywords)
            probabilities = np.array(values) / sum(values)
            selected_indices = np.random.choice(len(topics), size=min(5, len(topics)), replace=False, p=probabilities)

        except Exception as e:
            return RecommendMessage.ERROR

        return [recommend_keywords[index] for index in selected_indices]
