import bcrypt

class AuthService:
    def __init__(self, user_dao):
        self.user_dao = user_dao


    # login
    def login(self, user: dict) -> int:
        """사용자의 이메일과 비밀번호를 데이터베이스에 조회합니다.
        그리고 사용자의 정보가 존재하면 사용자 id를 반환합니다.
        만약 사용자의 정보가 존재하지 않으면 -1을 반환하고,
        사용자의 이메일과 비밀번호가 맞지 않으면 -2를 반환합니다.
        또한, 에러가 발생하면 None을 반환합니다.

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
        except:
            return None
        finally:
            if user_info is None:
                user_info = self.user_dao.find_user_id_by_email(user['email'])
                return -1 if user_info == -1 else None
            elif not authorized:
                return -2

        return user_info['user_id']


    # logout
