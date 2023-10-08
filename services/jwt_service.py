from flask import request, Response, g
from functools import wraps
from datetime import datetime, timedelta
import jwt
import json

from data import response_from_message, ResponseText, JwtMessage, UserMessage

class JWTService:
    def __init__(self, user_dao, config):
        self.user_dao = user_dao
        self.config = config


    # TODO: 이후 refresh-token도 추가할 것
    # 로그인 인증 데코레이터
    def login_required(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            access_token = request.headers.get('accessToken')

            if access_token is not None:
                try:
                    payload = jwt.decode(access_token, self.config['JWT_SECRET_KEY'], 'HS256')
                except jwt.InvalidTokenError:
                    payload = None

                if payload is None:
                    return Response(json.dumps(response_from_message(ResponseText.FAIL.value, JwtMessage.ERROR.value)), status=401)

                try:
                    if not self.user_dao.get_user_info(payload['user_id']):
                        return Response(json.dumps(response_from_message(ResponseText.FAIL.value, UserMessage.FAIL_NOT_EMAIL.value)), status=401)
                except:
                    return Response(json.dumps(response_from_message(ResponseText.FAIL.value, JwtMessage.ERROR.value)), status=500)

                user_id = payload['user_id']
                g.user_id = user_id
            else:
                return Response(json.dumps(response_from_message(ResponseText.FAIL.value, JwtMessage.FAIL_NOT_EXISTS.value)), status=401)

            return f(*args, **kwargs)
        return decorated_function


    # access token 발급
    def generate_access_token(self, user_id: int):
        """ access token 생성

        :param user_id: 사용자 id
        :return: 사용자 id와 유효기간이 포함된 access token
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=self.config['JWT_EXP_DELTA_SECONDS'])
        }
        token = jwt.encode(payload, self.config['JWT_SECRET_KEY'], 'HS256')

        return token
