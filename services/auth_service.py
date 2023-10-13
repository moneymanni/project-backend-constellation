import bcrypt
from typing import Union

from data import AuthMessage

class AuthService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    # login
    def login(self, user: dict) -> Union[int, AuthMessage]:
        """사용자의 이메일과 비밀번호를 데이터베이스에 조회합니다.
        그리고 사용자의 정보가 존재하면 사용자 id를 반환합니다.
        만약 사용자의 정보가 존재하지 않고,
        사용자의 이메일과 비밀번호가 맞지 않으면 AuthMessage를 반환합니다.
        또한, 에러가 발생해도 AuthMessage를 반환합니다.

        :param user: 사용자의 이메일과 패스워드가 포함된 딕셔너리:
            {
                'email': str,   # 사용자의 이메일
                'password': str # 사용자의 비밀번호
            }
        :return: 사용자 id
        """
        try:
            user_info = self.user_dao.find_user_id_and_password_by_email(user['email'])
            authorized = user_info and bcrypt.checkpw(user['password'].encode('UTF-8'), user_info['hashed_password'].encode('UTF-8'))

            if user_info is None:
                return AuthMessage.FAIL_NOT_EXISTS
            if not authorized:
                return AuthMessage.FAIL_NOT_MATCH
        except Exception as e:
            return AuthMessage.ERROR

        return user_info['user_id']


    # logout
