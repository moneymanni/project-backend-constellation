from flask import Blueprint, request, jsonify
import json

from forms import SignInForm
from data import response_from_message, ResponseText, AuthMessage, JwtMessage

def create_auth_endpoint(services, config):
    auth_view = Blueprint('auth_view', __name__)

    jwt_service = services.jwt_service
    auth_service = services.auth_service

    # login
    @auth_view.route('/sign-in', methods=['POST'])
    def auth_sign_in():
        """로그인 엔드포인트

        :request: 로그인하는 사용자의 정보가 담긴 json 객체
            {
                "email": str,       # 사용자의 이메일
                "password": str,    # 사용자의 비밀번호
            }

        :response: 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "accessToken": str,     # access 토큰
                "tokenExpiration": int, # 토큰 유효 기간
                "state": str,           # 상태
                "message": str,         # 결과 메시지
                "data": {               # 반환하는 데이터
                        userId: str     # 가입한 사용자 id
                    }
            }
        """
        form = SignInForm(meta={"csrf": False})
        if not form.validate():
            return json.dumps(form.errors), 400

        body = request.json
        user = {
            'email': body['email'],
            'password': body['password']
        }

        try:
            checked_user_id = auth_service.login(user)

            if isinstance(checked_user_id, AuthMessage):
                message = response_from_message(ResponseText.FAIL.value, checked_user_id.value)
                if checked_user_id == AuthMessage.FAIL_NOT_EXISTS:
                    return jsonify(message), 400
                elif checked_user_id == AuthMessage.FAIL_NOT_MATCH:
                    return jsonify(message), 401
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, AuthMessage.ERROR.value)), 500

        try:
            access_token = jwt_service.generate_access_token(checked_user_id)
            access_token_exp = config['JWT_EXP_DELTA_SECONDS']
        except:
            return jsonify(response_from_message(ResponseText.FAIL.value, JwtMessage.ERROR.value)), 500

        response = response_from_message(ResponseText.SUCCESS.value, AuthMessage.LOGIN.value, {'userId': checked_user_id})
        response['accessToken'], response['tokenExpiration'] = access_token, access_token_exp

        return jsonify(response), 200


    # logout
    @auth_view.route('/logout', methods=['POST'])
    def auth_logout():
        return None


    return auth_view