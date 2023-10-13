from flask import jsonify

from data import response_from_message, ResponseText, IndexMessage

def create_endpoint(app, services):

    # health check endpoint
    @app.route('/ping', methods=['GET'])
    def ping():
        return jsonify(response_from_message(ResponseText.FAIL.value, IndexMessage.SUCCESS.value, 'pong')), 200
