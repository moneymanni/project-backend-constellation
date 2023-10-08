import bcrypt

class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao


    # create
    def create_new_user(self, user: dict) -> int:
        """사용자의 정보를 받아 사용자 테이블에 존재하는지 확인하고 등록합니다.
        그리고 등록된 사용자의 id를 반환합니다.
        만약 사용자가 등록되어 있다면 -1을 반환하고, 에러가 발생하면 None을 반환합니다.

        :param user: 사용자의 정보가 포함된 딕셔너리: 
            {
                'email': str,       # 사용자의 이메일
                'password': str,    # 사용자의 패스워드
                'profile': str      # 사용자의 프로필
            }
        :return: 등록된 사용자 id
        """
        try:
            user_id = self.user_dao.find_user_id_by_email(user['email'])
        except:
            return None
        finally:
            if user_id is None:
                return None
            elif user_id > 0:
                return -1

        user['password'] = bcrypt.hashpw(
            user['password'].encode('UTF-8'),
            bcrypt.gensalt()
        )
        try:
            new_user_id = self.user_dao.insert_user_info(user)
        except:
            return None

        return new_user_id if new_user_id is not None and new_user_id >= 0 else None


    # read
    def get_user(self, user_id: int) -> dict:
        """사용자 id로 정보를 조회합니다.
        만약 사용자 id가 존재하지 않거나 에러가 발생하면 None을 반환합니다.

        :param user_id: 조회할 사용자의 id
        :return: 사용자 정보가 포함된 딕셔너리
            {
                'user_id': int,
                'email': str,
                'profile': str,
                'created_at': str,
                'updated_at': str
            }
        """
        try:
            user = self.user_dao.get_user_info(user_id)
        except:
            return None

        return user if user is not None else None


    # update
    def update_user(self, user: dict) -> str:
        """사용자의 id와 프로필을 받아 사용자 정보를 수정합니다.
        그리고 수정된 날짜를 반환합니다.
        만약 에러가 발생하면 None을 반환합니다.

        :param user: 사용자의 정보가 포함된 딕셔너리:
            {
                'user_id': int, # 사용자 id
                'profile': str  # 사용자의 프로필
            }
        :return: 사용자 정보가 수정된 일자
        """
        try:
            is_updated = self.user_dao.update_user_info(user)
        except:
            return None
        finally:
            if is_updated is None or not is_updated:
                return None

        try:
            updated_user = self.user_dao.get_user_info(user['user_id'])
            print(updated_user)
        except:
            return None

        return updated_user['updated_at'] if updated_user else None


    # delete
    def delete_user(self, user_id: int) -> bool:
        """사용자 id로 사용자 정보를 데이터베이스에서 삭제합니다.
        그리고 삭제 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 None을 반환합니다.

        :param user_id: 사용자 id
        :return: 삭제 성공 여부 (True/False)
        """
        try:
            is_deleted = self.user_dao.delete_user_info(user_id)
        except:
            return None

        return True if is_deleted is not None and is_deleted else False
