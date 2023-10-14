from flask import Blueprint, request, jsonify

from data import response_from_message, ResponseText, RecommendMessage

def create_recommend_endpoint(services):
    recommend_view = Blueprint('recommend_view', __name__)

    jwt_service = services.jwt_service
    recommend_service = services.recommend_service

    @recommend_view.route('/trend', methods=['GET'])
    def recommend_trend():
        keyword = request.args.get('keyword')

        try:
            recommend = recommend_service.recommend_googletrends(keyword)

            if isinstance(recommend, RecommendMessage):
                message = response_from_message(ResponseText.FAIL.value, recommend.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, RecommendMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, RecommendMessage.GET.value, {
            'recommend': [{
                'keyword': word[0],
                'similarity': word[1]
            } for word in recommend]
        })), 200

    @recommend_view.route('/association', methods=['GET'])
    def recommend_association():
        keyword = request.args.get('keyword')

        try:
            recommend = recommend_service.recommend_w2v(keyword)

            if isinstance(recommend, RecommendMessage):
                message = response_from_message(ResponseText.FAIL.value, recommend.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, RecommendMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, RecommendMessage.GET.value, {
            'recommend': [{
                'keyword': word[0],
                'similarity': word[1]
            } for word in recommend]
        })), 200

    return recommend_view
